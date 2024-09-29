from pyramid.events import NewRequest
from pyramid.httpexceptions import HTTPBadRequest
import json

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        })
    event.request.add_response_callback(cors_headers)

def json_validator(event):
    request = event.request
    if request.method in ('POST', 'PUT') and request.content_type == 'application/json':
        try:
            json.loads(request.body)
        except json.JSONDecodeError:
            raise HTTPBadRequest('Invalid JSON')

def includeme(config):
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    config.add_subscriber(json_validator, NewRequest)