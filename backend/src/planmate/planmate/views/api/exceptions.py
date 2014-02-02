from pyramid.response import Response
from pyramid import httpexceptions
from pyramid.httpexceptions import HTTPBadRequest,HTTPNotFound,HTTPNotImplemented
from google.appengine.api.datastore_errors import *

import copy


datastore_exceptions = [
  (BadValueError, 400, 'Sent data were invalid.')
  ]

def _get_datastore_exception(exception):
  for cls, code, message in datastore_exceptions:
    if exception.__class__ is cls:
      if exception.args and exception.args[0]:
        message = exception.args[0]
      return (code, message)


status_map = copy.copy(httpexceptions.status_map)
status_map[400] = HTTPBadRequest

def _get_http_exception(exception, request):
  print('Exception', exception, status_map[400])
  if exception.__class__ == HTTPNotFound and exception.args[0] == request.path_info:
    return (404, 'URL %s is not found.' % request.path_info)

  for code in status_map:
    cls = status_map[code]
    if exception.__class__ is cls:
      if exception.args and exception.args[0]:
        message = exception.args[0]
      else:
        message = cls.explanation

      return (code, message)

  #return (HTTPNotImplemented.code, HTTPNotImplemented.explanation)


def view(exception, request):
  result = _get_http_exception(exception, request)

  if not result:
    result =  _get_datastore_exception(exception)
    if not result:
      result = (HTTPNotImplemented.code, HTTPNotImplemented.explanation)

  (error_code, message) = result

  response = Response(json={'message':message})
  response.status = error_code

  return response

