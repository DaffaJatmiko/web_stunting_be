from ..orms.health_record import HealthRecordORM
from sqlalchemy.orm import Session
from datetime import datetime

class HealthRecord:
    def __init__(self, record_id, children_id, record_date, record_immunization, record_vaccinated_by):
        self.record_id = record_id
        self.children_id = children_id
        self.record_date = record_date
        self.record_immunization = record_immunization
        self.record_vaccinated_by = record_vaccinated_by

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            record_id=orm_obj.record_id,
            children_id=orm_obj.children_id,
            record_date=orm_obj.record_date,
            record_immunization=orm_obj.record_immunization,
            record_vaccinated_by=orm_obj.record_vaccinated_by
        )

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'children_id': self.children_id,
            'record_date': str(self.record_date),
            'record_immunization': self.record_immunization,
            'record_vaccinated_by': self.record_vaccinated_by
        }

    @classmethod
    def get_all_by_child(cls, dbsession: Session, children_id: int):
        records_orm = dbsession.query(HealthRecordORM).filter(HealthRecordORM.children_id == children_id).all()
        return [cls.from_orm(record) for record in records_orm]

    @classmethod
    def get_by_id(cls, dbsession: Session, record_id: int):
        record_orm = dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
        return cls.from_orm(record_orm) if record_orm else None

    @classmethod
    def create(cls, dbsession: Session, data: dict):
        new_record = HealthRecordORM(
            children_id=data['children_id'],
            record_date=datetime.strptime(data['record_date'], '%Y-%m-%d').date(),
            record_immunization=data['record_immunization'],
            record_vaccinated_by=data['record_vaccinated_by']
        )
        dbsession.add(new_record)
        dbsession.flush()
        return cls.from_orm(new_record)

    @classmethod
    def update(cls, dbsession: Session, record_id: int, data: dict):
        record_orm = dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
        if record_orm:
            for key, value in data.items():
                if key == 'record_date':
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(record_orm, key, value)
            dbsession.flush()
            return cls.from_orm(record_orm)
        return None

    @classmethod
    def delete(cls, dbsession: Session, record_id: int):
        record_orm = dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
        if record_orm:
            dbsession.delete(record_orm)
            return True
        return False