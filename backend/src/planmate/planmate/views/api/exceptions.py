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


def view(exception, request):
  (error_code, message) = _get_http_exception(exception, request)

  response = Response(json={'message':message})
  response.status = error_code

  return response

