from zope.interface import implementer
from marshmallow import Schema
from .__interface__ import IJSONSchema

@implementer(IJSONSchema)
class BaseSchema(Schema):
    def set_schema_by_method(self, method):
        # Default implementation
        pass