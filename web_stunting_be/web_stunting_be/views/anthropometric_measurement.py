from pyramid.view import view_config, view_defaults
from ..models.anthropometric_measurement import Measurement
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

@view_defaults(route_name='measurement')
class MeasurementViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        children_id = int(self.request.matchdict['children_id'])
        measurements = Measurement.get_all_by_child(self.request.dbsession, children_id)
        return {
            'data': [measurement.to_dict() for measurement in measurements],
            'total': len(measurements)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            children_id = int(self.request.matchdict['children_id'])
            data = self.request.json_body
            data['children_id'] = children_id
            new_measurement = Measurement.create(self.request.dbsession, data)
            return {'message': 'Measurement added successfully', 'measurement_id': new_measurement.measurement_id}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

@view_defaults(route_name='measurement_detail')
class MeasurementDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        measurement_id = int(self.request.matchdict['measurement_id'])
        measurement = Measurement.get_by_id(self.request.dbsession, measurement_id)
        if measurement is None:
            return HTTPNotFound(detail='Measurement not found')
        return measurement.to_dict()

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            measurement_id = int(self.request.matchdict['measurement_id'])
            data = self.request.json_body
            updated_measurement = Measurement.update(self.request.dbsession, measurement_id, data)
            if updated_measurement is None:
                return HTTPNotFound(detail='Measurement not found')
            return {'message': 'Measurement updated successfully'}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        measurement_id = int(self.request.matchdict['measurement_id'])
        if Measurement.delete(self.request.dbsession, measurement_id):
            return {'message': 'Measurement deleted successfully'}
        return HTTPNotFound(detail='Measurement not found')