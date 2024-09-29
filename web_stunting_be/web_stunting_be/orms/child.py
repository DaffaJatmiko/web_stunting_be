from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from .meta import Base

class ChildORM(Base):
    __tablename__ = 'children'
    children_id = Column(Integer, primary_key=True)
    children_name = Column(String(100), nullable=False)
    children_birth_date = Column(Date, nullable=False)
    children_address = Column(String(255), nullable=False)
    children_parent = Column(String(100), nullable=False)
    children_parent_phone = Column(String(20), nullable=False)
    children_allergy = Column(String(255))
    children_blood_type = Column(String(5))
    children_weight = Column(Float)
    children_height = Column(Float)
    
    health_records = relationship("HealthRecordORM", back_populates="child")
    measurements = relationship("MeasurementORM", back_populates="child")