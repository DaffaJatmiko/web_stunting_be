from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base

class MeasurementORM(Base):
    __tablename__ = 'measurements'
    measurement_id = Column(Integer, primary_key=True)
    children_id = Column(Integer, ForeignKey('children.children_id'), nullable=False)
    measurement_date = Column(Date, nullable=False)
    measurement_weight = Column(Float, nullable=False)
    measurement_height = Column(Float, nullable=False)
    measurement_head_circumference = Column(Float)
    measurement_abdominal_circumference = Column(Float)
    measurement_leg_circumference = Column(Float)
    measurement_arm_circumference = Column(Float)
    
    child = relationship("ChildORM", back_populates="measurements")