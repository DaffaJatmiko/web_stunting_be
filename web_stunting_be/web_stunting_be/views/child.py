from pyramid.view import view_config
from ..models.child import Child
from ..orms.child import ChildORM
from pyramid.httpexceptions import HTTPBadRequest
from datetime import datetime

@view_config(route_name='child_list', renderer='json', request_method='GET')
def child_list(request):
    children_orm = request.dbsession.query(ChildORM).all()
    children = [Child.from_orm(child) for child in children_orm]
    return {'children': [child.to_dict() for child in children]}

@view_config(route_name='child_detail', renderer='json', request_method='GET')
def child_detail(request):
    children_id = int(request.matchdict['id'])
    child_orm = request.dbsession.query(ChildORM).filter(ChildORM.children_id == children_id).first()
    if child_orm is None:
        return HTTPBadRequest(detail='Child not found')
    child = Child.from_orm(child_orm)
    return child.to_dict()

@view_config(route_name='child_add', renderer='json', request_method='POST')
def child_add(request):
    try:
        data = request.json_body
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
        request.dbsession.add(new_child)
        request.dbsession.flush()
        return {'message': 'Child added successfully', 'children_id': new_child.children_id}
    except KeyError as e:
        return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
    except ValueError as e:
        return HTTPBadRequest(detail=f'Invalid value: {str(e)}')