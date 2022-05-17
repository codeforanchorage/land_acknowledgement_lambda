'''
Classes to handle responses based on the type of location returned from the geocoder.
In general we are hoping for place and postal code locations. Larger areas like states
and countries don't make sense and the classes should respond appropriately.
'''
import abc

from chalicelib.native_land import native_land_from_point
from chalicelib.geocode import geolocate, LocationNotFound

MORE_INFO_LINK = "land.codeforanchorage.org"
SUFFIX = f"More info: {MORE_INFO_LINK}"


class GenericResponse():
    def __init__(self, query, location):
        self.location = location
        self.query = query

    def land_string(self, lands):
        '''Converts lists of lands into string sent to user'''
        names = [land['Name'] for land in lands]
        if len(lands) == 1:
            land_string = names[0]
        elif len(lands) == 2:
            land_string = ' and '.join(names)
        else:
            all_but_last = ', '.join(names[:-1])
            land_string = f'{all_but_last}, and {names[-1]}'

        return land_string

    def __str__(self):
        return f"Sorry, I don't have information about {self.query}."


class TooBigResponse(GenericResponse):
    '''Respond to places like countries and states.'''
    def __str__(self):
        place_type = self.location['place_type'][0]
        place_name = self.location['text']
        return (
            f"A {place_type} like {place_name} is a little too big for this service. "
            f"Try sending a city and state."
        )


class PoiResponse(GenericResponse):
    '''Response for points of interest.'''
    def __str__(self):
        place_name = self.query
        return (
            f"I don't know how to find information about {place_name}. "
            f"Try sending a city and state."
        )


class LocationResponse(GenericResponse):
    '''Base class for repsonses that hit the geocoder.'''

    def __init__(self, query, location):
        super().__init__(query, location)
        self.lands = native_land_from_point(*self.location['center'])

    @abc.abstractmethod
    def response_from_area(self, lands_string, context):
        """Create a response string appropritate to the type"""
        return

    def __str__(self):
        if not self.lands:
            return super().__str__()
        context = {item['id'].partition('.')[0]: item['text'] for item in self.location['context']}
        land_string = self.land_string(self.lands)
        return self.response_from_area(land_string, context)


class PostalCodeResponse(LocationResponse):
    '''Response for zip codes.'''
    def response_from_area(self, land_string, context):
        area = self.location['text']
        return f"In the area of {area} you are on {land_string} land."


class PlaceResponse(LocationResponse):
    '''Response for cities and towns.'''
    def response_from_area(self, land_string, context):
        place = self.location['text']
        if 'region' in context:
            place = ', '.join([place, context.get('region')])
        return f"In {place} you are on {land_string} land."


class AddressResponse(LocationResponse):
    '''Response for addresses'''
    def response_from_area(self, land_string, context):
        street = self.location['text']
        if 'place' in context:
            street = ', '.join([street, context.get('place'), context.get('region')])
        return f"On {street} you are on {land_string} land."


type_dispatch = {
    'country': TooBigResponse,
    'region': TooBigResponse,
    'postcode': PostalCodeResponse,
    'district': TooBigResponse,
    'place': PlaceResponse,
    'locality': PlaceResponse,
    'neighborhood': PlaceResponse,  # these might be too vauge to handle
    'address': AddressResponse,
    'poi': PoiResponse
}


def process_body(body):
    greetings = {'hello', 'hi', 'help'}

    if not body or body.lower() in greetings:
        return "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"
    elif len(body) < 3:
        return "Hmm, that seems a little vague. Try sending a city and state such as 'Anchorage, AK'"
    else:
        try:
            location = geolocate(body)
            place_type = location['place_type'][0]            
            response_class = type_dispatch.get(place_type, GenericResponse)
            return response_class(body, location)
        except LocationNotFound:
            return f"I could not find the location: {body}"
        except Exception:
            return "Sorry, I having some technical trouble right now."
