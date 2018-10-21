"""
Custom errors
"""


class RestException(Exception):
    """ Base Rest API exception """
    def __init__(self, error_message=None, log_message=None):
        Exception.__init__(self)
        if error_message:
            self.error_message = error_message
        self.log_message = log_message
        self.payload = None

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['error_message'] = self.error_message
        return rv


class BadRequestException(RestException):
    status_code = 400
    error_message = 'bad_request'


class ServerErrorException(RestException):
    status_code = 500
    error_message = 'server_error'


class PageNotFound(RestException):
    status_code = 404
    error_message = 'page_not_found'


class ObjectNotFoundException(RestException):
    status_code = 404
    error_message = 'object_not_found'
