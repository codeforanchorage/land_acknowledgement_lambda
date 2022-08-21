class ConfigurationError(Exception):
    pass


class APIError(Exception):
    pass


class LocationNotFound(Exception):
     def __init__(self, location=None):
        if location is None:
            message = "I couldn't find this location"
        else: 
            message = f"I couldn't find the location: {location}"

        super().__init__(message)


class MissingLocationError(Exception):
    def __init__(self):
        message = "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"
        super().__init__(message)

class ShortLocationError(Exception):
    def __init__(self):
        message = "Hmm, that seems a little vague. Try sending a city and state such as 'Anchorage, AK'"
        super().__init__(message)