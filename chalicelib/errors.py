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
