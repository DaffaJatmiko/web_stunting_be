from ..orms.health_record import HealthRecordORM

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