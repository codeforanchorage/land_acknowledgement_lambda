from urllib.parse import parse_qs

from chalice.app import Chalice, BadRequestError, Response

from chalicelib.twilio import twilio_response
from chalicelib.responses import process_body


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



@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index_post():
    body = get_request_body(app.current_request)
    ret_text = process_body(body)
    return Response(body=twilio_response(ret_text),
                    status_code=200,
                    headers={'Content-Type': 'application/xml'})

@app.route('/', methods=['GET'])
def index_empty_get():
    return "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"

@app.route('/{body}', methods=['GET'])
def index_get(body):
    ret_text = process_body(body)
    return Response(body=str(ret_text),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})
