from ..orms.anthropometric_measurement import MeasurementORM

class Measurement:
    def __init__(self, measurement_id, children_id, measurement_date, measurement_weight, 
                 measurement_height, measurement_head_circumference, measurement_abdominal_circumference, 
                 measurement_leg_circumference, measurement_arm_circumference):
        self.measurement_id = measurement_id
        self.children_id = children_id
        self.measurement_date = measurement_date
        self.measurement_weight = measurement_weight
        self.measurement_height = measurement_height
        self.measurement_head_circumference = measurement_head_circumference
        self.measurement_abdominal_circumference = measurement_abdominal_circumference
        self.measurement_leg_circumference = measurement_leg_circumference
        self.measurement_arm_circumference = measurement_arm_circumference

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            measurement_id=orm_obj.measurement_id,
            children_id=orm_obj.children_id,
            measurement_date=orm_obj.measurement_date,
            measurement_weight=orm_obj.measurement_weight,
            measurement_height=orm_obj.measurement_height,
            measurement_head_circumference=orm_obj.measurement_head_circumference,
            measurement_abdominal_circumference=orm_obj.measurement_abdominal_circumference,
            measurement_leg_circumference=orm_obj.measurement_leg_circumference,
            measurement_arm_circumference=orm_obj.measurement_arm_circumference
        )

    def to_dict(self):
        return {
            'measurement_id': self.measurement_id,
            'children_id': self.children_id,
            'measurement_date': str(self.measurement_date),
            'measurement_weight': self.measurement_weight,
            'measurement_height': self.measurement_height,
            'measurement_head_circumference': self.measurement_head_circumference,
            'measurement_abdominal_circumference': self.measurement_abdominal_circumference,
            'measurement_leg_circumference': self.measurement_leg_circumference,
            'measurement_arm_circumference': self.measurement_arm_circumference
        }