from pyramid.response import Response
from pyramid.httpexceptions import status_map,HTTPNotFound,HTTPNotImplemented
from google.appengine.ext.ndb.model import InvalidPropertyError


def _get_http_exception(exception, request):
  if isinstance(exception, HTTPNotFound) and exception.args[0] == request.path_info:
    return (404, 'URL %s is not found.' % request.path_info)

  for code in status_map:
    cls = status_map[code]
    if isinstance(exception, cls):
      if exception.args and exception.args[0]:
        message = exception.args[0]
      else:
        message = cls.explanation

      return (code, message)

  return (HTTPNotImplemented.code, HTTPNotImplemented.explanation)


"""
def _get_exception(exception, request):
  error_code = 500
  message = 'Server error.'

  # http exceptions
  if isinstance(exception, HTTPUnauthorized):
    error_code = 401
    message = 'Please login to continue.'

  elif isinstance(exception, HTTPForbidden):
    error_code = 403
    message = 'Accessing to this URL is forbidden.'

  elif isinstance(exception, HTTPNotFound):
    error_code = 404
    message = 'Content is not found.'

  elif isinstance(exception, HTTPUnauthorized):
    error_code = 405
    message = 'The action is not allowed at this URL.'

  elif isinstance(exception, HTTPConflict):
    error_code = 409
    message = 'The data you sent conflicted with another.'


  # ndb exceptions
  elif isinstance(exception, InvalidPropertyError):
    error_code = 409
    message = 'Some invalid parameters are posted.'

  return (error_code, message)
"""


def view(exception, request):
  (error_code, message) = _get_http_exception(exception, request)

  #if isinstance(exception, HTTPNotFound) and exception.args[0] == request.path_info:
  #  message = "PATH '%s' is not found." % request.path_info

  #elif exception.args and exception.args[0]:
  #  message = exception.args[0]

  response = Response(json={'message':message})
  response.status = error_code

  return response

