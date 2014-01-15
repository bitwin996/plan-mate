from pyramid.events import subscriber, NewResponse

@subscriber(NewResponse)
def add_cors_header(event):
    event.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:9000'
    event.response.headers['Access-Control-Allow-Credentials'] = 'true'
