from pyramid.view import view_config, view_defaults
from ..models.anthropometric_measurement import Measurement
from ..orms.anthropometric_measurement import MeasurementORM
from pyramid.httpexceptions import HTTPBadRequest
from datetime import datetime

@view_defaults(route_name='measurement')
class MeasurementViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        children_id = int(self.request.matchdict['children_id'])
        measurements_orm = self.request.dbsession.query(MeasurementORM).filter(MeasurementORM.children_id == children_id).all()
        measurements = [Measurement.from_orm(measurement).to_dict() for measurement in measurements_orm]
        
        return {
            'data': measurements,
            'total': len(measurements)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            children_id = int(self.request.matchdict['children_id'])
            data = self.request.json_body
            new_measurement = MeasurementORM(
                children_id=children_id,
                measurement_date=datetime.strptime(data['measurement_date'], '%Y-%m-%d').date(),
                measurement_weight=float(data['measurement_weight']),
                measurement_height=float(data['measurement_height']),
                measurement_head_circumference=float(data.get('measurement_head_circumference', 0)),
                measurement_abdominal_circumference=float(data.get('measurement_abdominal_circumference', 0)),
                measurement_leg_circumference=float(data.get('measurement_leg_circumference', 0)),
                measurement_arm_circumference=float(data.get('measurement_arm_circumference', 0))
            )
            self.request.dbsession.add(new_measurement)
            self.request.dbsession.flush()
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
        measurement_orm = self.request.dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
        if measurement_orm is None:
            return HTTPBadRequest(detail='Measurement not found')
        measurement = Measurement.from_orm(measurement_orm)
        return measurement.to_dict()

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            measurement_id = int(self.request.matchdict['measurement_id'])
            data = self.request.json_body
            measurement_orm = self.request.dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
            if measurement_orm is None:
                return HTTPBadRequest(detail='Measurement not found')
            
            measurement_orm.measurement_date = datetime.strptime(data['measurement_date'], '%Y-%m-%d').date()
            measurement_orm.measurement_weight = float(data['measurement_weight'])
            measurement_orm.measurement_height = float(data['measurement_height'])
            measurement_orm.measurement_head_circumference = float(data.get('measurement_head_circumference', measurement_orm.measurement_head_circumference))
            measurement_orm.measurement_abdominal_circumference = float(data.get('measurement_abdominal_circumference', measurement_orm.measurement_abdominal_circumference))
            measurement_orm.measurement_leg_circumference = float(data.get('measurement_leg_circumference', measurement_orm.measurement_leg_circumference))
            measurement_orm.measurement_arm_circumference = float(data.get('measurement_arm_circumference', measurement_orm.measurement_arm_circumference))
            
            self.request.dbsession.flush()
            return {'message': 'Measurement updated successfully'}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        measurement_id = int(self.request.matchdict['measurement_id'])
        measurement_orm = self.request.dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
        if measurement_orm is None:
            return HTTPBadRequest(detail='Measurement not found')
        self.request.dbsession.delete(measurement_orm)
        return {'message': 'Measurement deleted successfully'}