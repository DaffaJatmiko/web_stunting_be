from ..orms.child import ChildORM

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