from twilio.twiml.messaging_response import MessagingResponse

MORE_INFO_LINK = "land.codeforanchorage.org"
SUFFIX = f"More info: {MORE_INFO_LINK}"

def twilio_response(resp):
    '''Convert string to twilio xml response'''
    resp = f'{str(resp)}\n{SUFFIX}'
    twil_resp = MessagingResponse()
    twil_resp.message(resp)
    return str(twil_resp)
