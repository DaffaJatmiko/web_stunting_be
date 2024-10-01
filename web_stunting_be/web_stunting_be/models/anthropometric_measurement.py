from ..orms.anthropometric_measurement import MeasurementORM
from sqlalchemy.orm import Session
from datetime import datetime

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

    @classmethod
    def get_all_by_child(cls, dbsession: Session, children_id: int):
        measurements_orm = dbsession.query(MeasurementORM).filter(MeasurementORM.children_id == children_id).all()
        return [cls.from_orm(measurement) for measurement in measurements_orm]

    @classmethod
    def get_by_id(cls, dbsession: Session, measurement_id: int):
        measurement_orm = dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
        return cls.from_orm(measurement_orm) if measurement_orm else None

    @classmethod
    def create(cls, dbsession: Session, data: dict):
        new_measurement = MeasurementORM(
            children_id=data['children_id'],
            measurement_date=datetime.strptime(data['measurement_date'], '%Y-%m-%d').date(),
            measurement_weight=float(data['measurement_weight']),
            measurement_height=float(data['measurement_height']),
            measurement_head_circumference=float(data.get('measurement_head_circumference', 0)),
            measurement_abdominal_circumference=float(data.get('measurement_abdominal_circumference', 0)),
            measurement_leg_circumference=float(data.get('measurement_leg_circumference', 0)),
            measurement_arm_circumference=float(data.get('measurement_arm_circumference', 0))
        )
        dbsession.add(new_measurement)
        dbsession.flush()
        return cls.from_orm(new_measurement)

    @classmethod
    def update(cls, dbsession: Session, measurement_id: int, data: dict):
        measurement_orm = dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
        if measurement_orm:
            for key, value in data.items():
                if key == 'measurement_date':
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                elif key in ['measurement_weight', 'measurement_height', 'measurement_head_circumference',
                             'measurement_abdominal_circumference', 'measurement_leg_circumference',
                             'measurement_arm_circumference']:
                    value = float(value)
                setattr(measurement_orm, key, value)
            dbsession.flush()
            return cls.from_orm(measurement_orm)
        return None

    @classmethod
    def delete(cls, dbsession: Session, measurement_id: int):
        measurement_orm = dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
        if measurement_orm:
            dbsession.delete(measurement_orm)
            return True
        return False