from pyramid.view import view_config
from ..models.health_record import HealthRecord
from ..orms.health_record import HealthRecordORM
from pyramid.httpexceptions import HTTPBadRequest
from datetime import datetime
import logging
log = logging.getLogger(__name__)


@view_config(route_name='health_record_list', renderer='json', request_method='GET')
def health_record_list(request):
    children_id = int(request.matchdict['children_id'])
    health_records_orm = request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.children_id == children_id).all()
    health_records = [HealthRecord.from_orm(record) for record in health_records_orm]
    return {'health_records': [record.to_dict() for record in health_records]}

@view_config(route_name='health_record_detail', renderer='json', request_method='GET')
def health_record_detail(request):
    record_id = int(request.matchdict['record_id'])
    record_orm = request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
    if record_orm is None:
        return HTTPBadRequest(detail='Health record not found')
    record = HealthRecord.from_orm(record_orm)
    return record.to_dict()


@view_config(route_name='health_record_add', renderer='json', request_method='POST')
def health_record_add(request):
    log.debug("Entering health_record_add view")
    log.debug(f"Request method: {request.method}")
    log.debug(f"Route name: {request.matched_route.name}")
    log.debug(f"Renderer: {getattr(request.matched_route, 'renderer', 'Not set')}")
    try:
        children_id = int(request.matchdict['children_id'])
        data = request.json_body
        new_record = HealthRecordORM(
            children_id=children_id,
            record_date=datetime.strptime(data['record_date'], '%Y-%m-%d').date(),
            record_immunization=data['record_immunization'],
            record_vaccinated_by=data['record_vaccinated_by']
        )
        request.dbsession.add(new_record)
        request.dbsession.flush()
        return {'message': 'Health record added successfully', 'record_id': new_record.record_id}
    except KeyError as e:
        log.error(f"KeyError in health_record_add: {str(e)}")
        return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
    except ValueError as e:
        log.error(f"ValueError in health_record_add: {str(e)}")
        return HTTPBadRequest(detail=f'Invalid value: {str(e)}')
    except Exception as e:
        log.error(f"Unexpected error in health_record_add: {str(e)}")
        return HTTPBadRequest(detail=f'An unexpected error occurred: {str(e)}')

@view_config(route_name='health_record_update', renderer='json', request_method='PUT')
def health_record_update(request):
    try:
        record_id = int(request.matchdict['record_id'])
        data = request.json_body
        record_orm = request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
        if record_orm is None:
            return HTTPBadRequest(detail='Health record not found')
        
        record_orm.record_date = datetime.strptime(data['record_date'], '%Y-%m-%d').date()
        record_orm.record_immunization = data['record_immunization']
        record_orm.record_vaccinated_by = data['record_vaccinated_by']
        
        request.dbsession.flush()
        return {'message': 'Health record updated successfully'}
    except KeyError as e:
        return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
    except ValueError as e:
        return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

@view_config(route_name='health_record_delete', renderer='json', request_method='DELETE')
def health_record_delete(request):
    record_id = int(request.matchdict['record_id'])
    record_orm = request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
    if record_orm is None:
        return HTTPBadRequest(detail='Health record not found')
    request.dbsession.delete(record_orm)
    return {'message': 'Health record deleted successfully'}