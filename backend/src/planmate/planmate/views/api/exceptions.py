from pyramid.httpexceptions import HTTPNotFound,HTTPNotImplemented
from pyramid.response import Response

from planmate.lib.exceptions import get_datastore_exception,get_http_exception,get_app_exception


def view(exception, request):
  result = None

  if exception.__class__ == HTTPNotFound and exception.args[0] == request.path_info:
    result = (404, 'URL %s is not found.' % request.path_info)

  if not result:
    result = get_app_exception(exception)

  if not result:
    result = get_http_exception(exception, request)

  if not result:
    result =  get_datastore_exception(exception)

  if not result:
    result = (HTTPNotImplemented.code, HTTPNotImplemented.explanation)

  (error_code, message) = result

  response = Response(json={'message':message})
  response.status = error_code

  return response

