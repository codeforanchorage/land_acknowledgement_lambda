from urllib.parse import parse_qs

import structlog
from chalice import CORSConfig
from chalice.app import BadRequestError, Chalice, Response

from chalicelib.errors import (LocationNotFound, MissingLocationError,
                               ShortLocationError)
from chalicelib.geocode import geolocate
from chalicelib.responses import response_type_from_place_type
from chalicelib.twilio import twilio_response

logger = structlog.get_logger()

app = Chalice(app_name='ak_land_aws')


def get_request_body(current_request):
    raw_body = current_request.raw_body
    if not raw_body:
        raise BadRequestError("Requests must post a 'Body' paramter")
    str_body = raw_body.decode('utf-8')
    str_body = parse_qs(str_body)
    body = str_body.get('Body', [])
    if len(body):
        return body[0].strip()
    return ''

def process_body(body):
    log = logger.bind(body=body)

    greetings = {'hello', 'hi', 'help'}

    if not body or body.lower() in greetings:
        log.info('no_location')
        raise MissingLocationError
    elif len(body) < 3:
        log.info('no_location')
        raise ShortLocationError
    else:
        location = geolocate(body)
        place_type = location['place_type'][0]

        response_class = response_type_from_place_type(place_type)
        ret_object = response_class(body, location)
        log = logger.bind(**ret_object.to_dict())
        log.info('success')
        return ret_object

@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index_post():
    '''
    This is the route Twilio should access, e.g. from texting or from the
    Facebook Messenger bot.

    The user input should be in a www-form-encoded `body`.
    It will respond with TwilML xml output.
    '''
    body = get_request_body(app.current_request)

    try:
        ret_object = process_body(body)
    except (MissingLocationError, LocationNotFound) as e:
        ret_object = str(e)

    return Response(body=twilio_response(ret_object),
                    status_code=200,
                    headers={'Content-Type': 'application/xml'})


@app.route('/', methods=['GET'])
def index_empty_get():
    ret_text = "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"
    return Response(body=ret_text,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})


CORS_CONFIG = CORSConfig(
    allow_origin='https://land.codeforanchorage.org',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)


@app.route('/{body}', cors=CORS_CONFIG, methods=['GET'])
def index_get(body):
    '''
    Non-Twilio users can access this route with a GET request
    and will receive a string response.

    This for instance is what the land.codeforanchorage.org website
    uses to get the response.
    '''
    try:
        ret_object = process_body(body)
    except (MissingLocationError, LocationNotFound) as e:
        ret_object = str(e)

    return Response(body=str(ret_object),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})
