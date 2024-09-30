from .jv import json_validator_tween_factory
from .cors import cors_tween_factory
from ..schema import (
    ChildSchema,
    HealthRecordSchema,
    MeasurementSchema,
    IJSONSchema
)

def includeme(config):
    # Include middleware JSON Validator
    config.add_tween('web_stunting_be.middleware.jv.json_validator_tween_factory')
    
    # Register schemas
    config.registry.registerUtility(ChildSchema(), IJSONSchema, name='child_schema')
    config.registry.registerUtility(HealthRecordSchema(), IJSONSchema, name='health_record_schema')
    config.registry.registerUtility(MeasurementSchema(), IJSONSchema, name='measurement_schema')

    # Include CORS
    config.add_tween('web_stunting_be.middleware.cors.cors_tween_factory')