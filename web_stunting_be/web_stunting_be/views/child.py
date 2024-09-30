from pyramid.view import view_config, view_defaults
from ..models.child import Child
from ..orms.child import ChildORM
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from datetime import datetime

@view_defaults(route_name='child')
class ChildViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        children_orm = self.request.dbsession.query(ChildORM).all()
        children = [Child.from_orm(child) for child in children_orm]
        return {'children': [child.to_dict() for child in children]}

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            data = self.request.json_body
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
            self.request.dbsession.add(new_child)
            self.request.dbsession.flush()
            return {'message': 'Child added successfully', 'children_id': new_child.children_id}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

@view_defaults(route_name='child_detail')
class ChildDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        children_id = int(self.request.matchdict['id'])
        child_orm = self.request.dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
        if child_orm is None:
            return HTTPNotFound(detail='Child not found')
        child = Child.from_orm(child_orm)
        return child.to_dict()

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            children_id = int(self.request.matchdict['id'])
            child_orm = self.request.dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
            if child_orm is None:
                return HTTPNotFound(detail='Child not found')

            data = self.request.json_body
            child_orm.children_name = data.get('children_name', child_orm.children_name)
            child_orm.children_birth_date = datetime.strptime(data['children_birth_date'], '%Y-%m-%d').date() if 'children_birth_date' in data else child_orm.children_birth_date
            child_orm.children_address = data.get('children_address', child_orm.children_address)
            child_orm.children_parent = data.get('children_parent', child_orm.children_parent)
            child_orm.children_parent_phone = data.get('children_parent_phone', child_orm.children_parent_phone)
            child_orm.children_allergy = data.get('children_allergy', child_orm.children_allergy)
            child_orm.children_blood_type = data.get('children_blood_type', child_orm.children_blood_type)
            child_orm.children_weight = data.get('children_weight', child_orm.children_weight)
            child_orm.children_height = data.get('children_height', child_orm.children_height)

            self.request.dbsession.flush()
            return {'message': 'Child updated successfully', 'children_id': child_orm.children_id}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        children_id = int(self.request.matchdict['id'])
        child_orm = self.request.dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
        if child_orm is None:
            return HTTPNotFound(detail='Child not found')
        
        self.request.dbsession.delete(child_orm)
        return {'message': 'Child deleted successfully', 'children_id': children_id}