from marshmallow import Schema, fields
from .base import BaseSchema

class ChildSchema(BaseSchema):
    children_id = fields.Integer(dump_only=True)
    children_name = fields.String(required=True)
    children_birth_date = fields.Date(required=True)
    children_address = fields.String(required=True)
    children_parent = fields.String(required=True)
    children_parent_phone = fields.String(required=True)
    children_allergy = fields.String()
    children_blood_type = fields.String()
    children_weight = fields.Float()
    children_height = fields.Float()

    def set_schema_by_method(self, method):
        # Implement logic here if needed
        pass