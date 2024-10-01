from pyramid.view import view_config, view_defaults
from ..models.child import Child
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

@view_defaults(route_name='child')
class ChildViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        children = Child.get_all(self.request.dbsession)
        return {
            'data': [child.to_dict() for child in children],
            'total': len(children)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            data = self.request.json_body
            new_child = Child.create(self.request.dbsession, data)
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
        child = Child.get_by_id(self.request.dbsession, children_id)
        if child is None:
            return HTTPNotFound(detail='Child not found')
        return child.to_dict()

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            children_id = int(self.request.matchdict['id'])
            data = self.request.json_body
            updated_child = Child.update(self.request.dbsession, children_id, data)
            if updated_child is None:
                return HTTPNotFound(detail='Child not found')
            return {'message': 'Child updated successfully', 'children_id': updated_child.children_id}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        children_id = int(self.request.matchdict['id'])
        if Child.delete(self.request.dbsession, children_id):
            return {'message': 'Child deleted successfully', 'children_id': children_id}
        return HTTPNotFound(detail='Child not found')