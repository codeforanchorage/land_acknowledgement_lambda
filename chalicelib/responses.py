'''
Classes to handle responses based on the type of location returned from the geocoder.
In general we are hoping for place and postal code locations. Larger areas like states
and countries don't make sense and the classes should respond appropriately.
'''
import abc
import html
from typing import Type

import structlog

from chalicelib.native_land import native_land_from_point

structlog.configure(processors=[structlog.processors.JSONRenderer()])


class GenericResponse():
    def __init__(self, query: str, location: dict):
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
            "Try sending a city and state."
        )


class PoiResponse(GenericResponse):
    '''Response for points of interest.'''

    def __str__(self):
        return (
            f"I don't know how to find information about {self.query}. "
            "Try sending a city and state."
        )


class LocationResponse(GenericResponse):
    '''Base class for repsonses that hit the geocoder.'''

    def __init__(self, query: str, location: dict):
        super().__init__(query, location)
        lands = native_land_from_point(*self.location['center'])
        self.land_names = [land['Name'] for land in lands]

    @property
    def land_string(self) -> str:
        '''Converts lists of lands into string sent to user'''
        if len(self.land_names) == 1:
            return self.land_names[0]
        elif len(self.land_names) == 2:
            return " and ".join(self.land_names)
        else:
            all_but_last = ', '.join(self.land_names[:-1])
            return f'{all_but_last}, and {self.land_names[-1]}'

    @abc.abstractmethod
    def response_from_area(self, context):
        """Create a response string appropriate to the type"""
        pass

    def __str__(self):
        if not self.land_names:
            return super().__str__()
        context = {item['id'].partition('.')[0]: item['text'] for item in self.location['context']}
        return self.response_from_area(context)


class PostalCodeResponse(LocationResponse):
    '''Response for zip codes.'''

    def response_from_area(self, context):
        area = self.location['text']
        return f"In the area of {area} you are on {self.land_string} land."


class PlaceResponse(LocationResponse):
    '''Response for cities and towns.'''

    def response_from_area(self, context):
        place = self.location['text']
        if 'region' in context:
            place = ', '.join([place, context['region']])
        return html.unescape(f"In {place} you are on {self.land_string} land.")


class AddressResponse(LocationResponse):
    '''Response for addresses'''

    def response_from_area(self, context):
        street = self.location['text']
        if 'place' in context:
            street = ', '.join([street, context['place'], context.get('region')])
        return f"On {street} you are on {self.land_string} land."


def response_type_from_place_type(place_type: str) -> Type[GenericResponse]:
    m = {
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
    return m.get(place_type, GenericResponse)
