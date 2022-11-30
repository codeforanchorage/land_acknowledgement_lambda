from urllib.parse import parse_qs

import structlog
from chalice import CORSConfig
from chalice.app import BadRequestError, Chalice, Response

from chalicelib.errors import LocationNotFound
from chalicelib.geocode import geolocate
from chalicelib.responses import response_type_from_place_type
from chalicelib.twilio import twilio_response

logger = structlog.get_logger()

app = Chalice(app_name='ak_land_aws')

HELLO_RESPONSE = "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"


def get_query(raw_body: bytes) -> str:
    if not raw_body:
        raise BadRequestError("Requests must post a 'Body' paramter")
    str_body = raw_body.decode('utf-8')
    str_body = parse_qs(str_body)
    body = str_body.get('Body', [])
    if len(body):
        return body[0].strip()
    return ''


def process_query(query: str) -> str:
    log = logger.bind(body=query)

    greetings = {'hello', 'hi', 'help'}
    if not query or query.lower() in greetings:
        log.info('no_location')
        return HELLO_RESPONSE
    elif len(query) < 3:
        log.info('short_query')
        return "Hmm, that seems a little vague. Try sending a city and state such as 'Anchorage, AK'"
    else:
        try:
            location = geolocate(query)
        except LocationNotFound as e:
            log.info('location_not_found')
            return str(e)
        place_type = location['place_type'][0]

        response_class = response_type_from_place_type(place_type)
        ret_object = response_class(query, location)
        log = logger.bind(**ret_object.to_dict())
        log.info('success')
        return str(ret_object)


@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index_post():
    '''
    This is the route Twilio should access, e.g. from texting or from the
    Facebook Messenger bot.

    The user input should be in a www-form-encoded `body`.
    It will respond with TwilML xml output.
    '''
    query = get_query(app.current_request.raw_body)
    resp_text = process_query(query)
    return Response(body=twilio_response(resp_text),
                    status_code=200,
                    headers={'Content-Type': 'application/xml'})


@app.route('/', methods=['GET'])
def index_empty_get():
    return Response(body=HELLO_RESPONSE,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})


CORS_CONFIG = CORSConfig(
    allow_origin='https://land.codeforanchorage.org',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)


@app.route('/{query}', cors=CORS_CONFIG, methods=['GET'])
def index_get(query: str):
    '''
    Non-Twilio users can access this route with a GET request
    and will receive a string response.

    This for instance is what the land.codeforanchorage.org website
    uses to get the response.
    '''
    resp_text = process_query(query)
    return Response(body=resp_text,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})
