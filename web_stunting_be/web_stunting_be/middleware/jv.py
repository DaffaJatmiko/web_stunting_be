from pyramid.httpexceptions import HTTPBadRequest
from marshmallow import ValidationError
from ..schema import IJSONSchema

def json_validator_tween_factory(handler, registry):
    def json_validator_tween(request):
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                first_path = request.path.split('/')[1]
                schema_name = f"{first_path}_schema"
                schema = registry.queryUtility(IJSONSchema, name=schema_name)
                if schema:
                    schema.set_schema_by_method(request.method)
                    schema.load(request.json_body)
            except ValidationError as e:
                raise HTTPBadRequest(json={'errors': e.messages})
        return handler(request)
    return json_validator_tween