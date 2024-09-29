from ..orms.health_worker import HealthWorkerORM

class HealthWorker:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.name,
            username=orm_obj.username,
            password=orm_obj.password
        )

    def to_orm(self):
        return HealthWorkerORM(
            name=self.name,
            username=self.username,
            password=self.password
        )