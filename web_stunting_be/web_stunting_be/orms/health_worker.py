from sqlalchemy import Column, Integer, String
from .meta import Base

class HealthWorkerORM(Base):
    __tablename__ = 'health_workers'
    worker_id = Column(Integer, primary_key=True)
    worker_name = Column(String(100), nullable=False)