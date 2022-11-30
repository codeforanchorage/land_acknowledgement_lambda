'''
Classes to handle responses based on the type of location returned from the geocoder.
In general we are hoping for place and postal code locations. Larger areas like states
and countries don't make sense and the classes should respond appropriately.
'''
import abc
import html

import structlog

from chalicelib.native_land import native_land_from_point

structlog.configure(processors=[structlog.processors.JSONRenderer()])

MORE_INFO_LINK = "land.codeforanchorage.org"
SUFFIX = f"More info: {MORE_INFO_LINK}"


class GenericResponse():
    def __init__(self, query, location):
        self.location = location
        self.query = query

    def to_dict(self):
        return self.__dict__

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
        lands = native_land_from_point(*self.location['center'])
        self.land_names = [land['Name'] for land in lands]

    def land_string(self):
        '''Converts lists of lands into string sent to user'''
        if len(self.land_names) == 1:
            land_string = self.land_names[0]
        elif len(self.land_names) == 2:
            land_string = " and ".join(self.land_names)
        else:
            all_but_last = ', '.join(self.land_names[:-1])
            land_string = f'{all_but_last}, and {self.land_names[-1]}'
        return land_string

    @abc.abstractmethod
    def response_from_area(self, lands_string, context):
        """Create a response string appropritate to the type"""
        pass

    def __str__(self):
        if not self.land_names:
            return super().__str__()
        context = {item['id'].partition('.')[0]: item['text'] for item in self.location['context']}
        land_string = self.land_string()
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
        return html.unescape(f"In {place} you are on {land_string} land.")


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
