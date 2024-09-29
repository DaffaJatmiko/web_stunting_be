from pyramid.view import view_config
from ..models.anthropometric_measurement import Measurement
from ..orms.anthropometric_measurement import MeasurementORM
from pyramid.httpexceptions import HTTPBadRequest
from datetime import datetime

@view_config(route_name='measurement_list', renderer='json', request_method='GET')
def measurement_list(request):
    children_id = int(request.matchdict['children_id'])
    measurements_orm = request.dbsession.query(MeasurementORM).filter(MeasurementORM.children_id == children_id).all()
    measurements = [Measurement.from_orm(measurement) for measurement in measurements_orm]
    return {'measurements': [measurement.to_dict() for measurement in measurements]}

@view_config(route_name='measurement_detail', renderer='json', request_method='GET')
def measurement_detail(request):
    measurement_id = int(request.matchdict['measurement_id'])
    measurement_orm = request.dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
    if measurement_orm is None:
        return HTTPBadRequest(detail='Measurement not found')
    measurement = Measurement.from_orm(measurement_orm)
    return measurement.to_dict()

@view_config(route_name='measurement_add', renderer='json', request_method='POST')
def measurement_add(request):
    try:
        children_id = int(request.matchdict['children_id'])
        data = request.json_body
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
        request.dbsession.add(new_measurement)
        request.dbsession.flush()
        return {'message': 'Measurement added successfully', 'measurement_id': new_measurement.measurement_id}
    except KeyError as e:
        return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
    except ValueError as e:
        return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

@view_config(route_name='measurement_update', renderer='json', request_method='PUT')
def measurement_update(request):
    try:
        measurement_id = int(request.matchdict['measurement_id'])
        data = request.json_body
        measurement_orm = request.dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
        if measurement_orm is None:
            return HTTPBadRequest(detail='Measurement not found')
        
        measurement_orm.measurement_date = datetime.strptime(data['measurement_date'], '%Y-%m-%d').date()
        measurement_orm.measurement_weight = float(data['measurement_weight'])
        measurement_orm.measurement_height = float(data['measurement_height'])
        measurement_orm.measurement_head_circumference = float(data.get('measurement_head_circumference', measurement_orm.measurement_head_circumference))
        measurement_orm.measurement_abdominal_circumference = float(data.get('measurement_abdominal_circumference', measurement_orm.measurement_abdominal_circumference))
        measurement_orm.measurement_leg_circumference = float(data.get('measurement_leg_circumference', measurement_orm.measurement_leg_circumference))
        measurement_orm.measurement_arm_circumference = float(data.get('measurement_arm_circumference', measurement_orm.measurement_arm_circumference))
        
        request.dbsession.flush()
        return {'message': 'Measurement updated successfully'}
    except KeyError as e:
        return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
    except ValueError as e:
        return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

@view_config(route_name='measurement_delete', renderer='json', request_method='DELETE')
def measurement_delete(request):
    measurement_id = int(request.matchdict['measurement_id'])
    measurement_orm = request.dbsession.query(MeasurementORM).filter(MeasurementORM.measurement_id == measurement_id).first()
    if measurement_orm is None:
        return HTTPBadRequest(detail='Measurement not found')
    request.dbsession.delete(measurement_orm)
    return {'message': 'Measurement deleted successfully'}