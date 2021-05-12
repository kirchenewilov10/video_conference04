class WebRTCException(Exception):
    """Base exception class for distinguishing our own exception classes."""
    pass


class Http302(WebRTCException):
    """Exception used to redirect at the middleware level.

    This error class which can be raised from within a handler to cause
    an early bailout and redirect at the middleware level.
    """
    status_code = 302

    def __init__(self, location, message=None):
        self.location = location
        self.message = message


class BadRequest(WebRTCException):
    """Generic error to replace all "BadRequest"-type API errors."""
    status_code = 400

class NotAuthorized(WebRTCException):
    """User tries to access a resource without sufficient permissions.
    Raised whenever a user attempts to access a resource which they do not
    have permission-based access to
    """
    status_code = 401

class NotAuthenticated(WebRTCException):
    """Raised when a user is trying to make requests and they are not logged in.
    """
    status_code = 403

class NotFound(WebRTCException):
    """Generic error to replace all "Not Found"-type API errors."""
    status_code = 404


class InternelServerError(WebRTCException):
    """Generic error to replace all "Internel Server Error"-type Server errors."""
    status_code = 500