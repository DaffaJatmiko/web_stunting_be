from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base

class HealthRecordORM(Base):
    __tablename__ = 'health_records'
    record_id = Column(Integer, primary_key=True)
    children_id = Column(Integer, ForeignKey('children.children_id'), nullable=False)
    record_date = Column(Date, nullable=False)
    record_immunization = Column(String(100))
    record_vaccinated_by = Column(String(100))
    
    child = relationship("ChildORM", back_populates="health_records")