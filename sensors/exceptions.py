""" Module to hold all exceptions related to thermocouple admin """

class ThermocoupleError(Exception):
    """ Base class for exceptions raised when the thermocouple throws an error """
    pass

class OpenThermocoupleError(ThermocoupleError):
    """ Raised if the thermocouple is flagging an open circuit error """
    pass