from ..orms.child import ChildORM
from sqlalchemy.orm import Session
from datetime import datetime

class Child:
    def __init__(self, children_id, children_name, children_birth_date, children_address, 
                 children_parent, children_parent_phone, children_allergy, 
                 children_blood_type, children_weight, children_height):
        self.children_id = children_id
        self.children_name = children_name
        self.children_birth_date = children_birth_date
        self.children_address = children_address
        self.children_parent = children_parent
        self.children_parent_phone = children_parent_phone
        self.children_allergy = children_allergy
        self.children_blood_type = children_blood_type
        self.children_weight = children_weight
        self.children_height = children_height

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            children_id=orm_obj.children_id,
            children_name=orm_obj.children_name,
            children_birth_date=orm_obj.children_birth_date,
            children_address=orm_obj.children_address,
            children_parent=orm_obj.children_parent,
            children_parent_phone=orm_obj.children_parent_phone,
            children_allergy=orm_obj.children_allergy,
            children_blood_type=orm_obj.children_blood_type,
            children_weight=orm_obj.children_weight,
            children_height=orm_obj.children_height
        )

    def to_dict(self):
        return {
            'children_id': self.children_id,
            'children_name': self.children_name,
            'children_birth_date': str(self.children_birth_date),
            'children_address': self.children_address,
            'children_parent': self.children_parent,
            'children_parent_phone': self.children_parent_phone,
            'children_allergy': self.children_allergy,
            'children_blood_type': self.children_blood_type,
            'children_weight': self.children_weight,
            'children_height': self.children_height
        }

    @classmethod
    def get_all(cls, dbsession: Session):
        children_orm = dbsession.query(ChildORM).all()
        return [cls.from_orm(child) for child in children_orm]

    @classmethod
    def get_by_id(cls, dbsession: Session, children_id: int):
        child_orm = dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
        return cls.from_orm(child_orm) if child_orm else None

    @classmethod
    def create(cls, dbsession: Session, data: dict):
        new_child = ChildORM(
            children_name=data['children_name'],
            children_birth_date=datetime.strptime(data['children_birth_date'], '%Y-%m-%d').date(),
            children_address=data['children_address'],
            children_parent=data['children_parent'],
            children_parent_phone=data['children_parent_phone'],
            children_allergy=data.get('children_allergy'),
            children_blood_type=data.get('children_blood_type'),
            children_weight=data.get('children_weight'),
            children_height=data.get('children_height')
        )
        dbsession.add(new_child)
        dbsession.flush()
        return cls.from_orm(new_child)

    @classmethod
    def update(cls, dbsession: Session, children_id: int, data: dict):
        child_orm = dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
        if child_orm:
            for key, value in data.items():
                if key == 'children_birth_date':
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(child_orm, key, value)
            dbsession.flush()
            return cls.from_orm(child_orm)
        return None

    @classmethod
    def delete(cls, dbsession: Session, children_id: int):
        child_orm = dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
        if child_orm:
            dbsession.delete(child_orm)
            return True
        return False