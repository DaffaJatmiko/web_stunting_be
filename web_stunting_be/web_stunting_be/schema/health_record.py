from marshmallow import Schema, fields
from .base import BaseSchema



class HealthRecordSchema(BaseSchema):
    record_id = fields.Integer(dump_only=True)
    children_id = fields.Integer(required=True)
    record_date = fields.Date(required=True)
    record_immunization = fields.String()
    record_vaccinated_by = fields.String()

    
    def set_schema_by_method(self, method):
        # Implement logic here if needed
        pass