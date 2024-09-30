from marshmallow import Schema, fields
from .base import BaseSchema

class MeasurementSchema(BaseSchema):
    measurement_id = fields.Integer(dump_only=True)
    children_id = fields.Integer(required=True)
    measurement_date = fields.Date(required=True)
    measurement_weight = fields.Float(required=True)
    measurement_height = fields.Float(required=True)
    measurement_head_circumference = fields.Float()
    measurement_abdominal_circumference = fields.Float()
    measurement_leg_circumference = fields.Float()
    measurement_arm_circumference = fields.Float()

    
    def set_schema_by_method(self, method):
        # Implement logic here if needed
        pass
