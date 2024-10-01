from pyramid.view import view_config, view_defaults
from ..models.health_record import HealthRecord
from ..orms.health_record import HealthRecordORM
from pyramid.httpexceptions import HTTPBadRequest
from datetime import datetime
import logging

log = logging.getLogger(__name__)

@view_defaults(route_name='health_record')
class HealthRecordViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        children_id = int(self.request.matchdict['children_id'])
        health_records_orm = self.request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.children_id == children_id).all()
        health_records = [HealthRecord.from_orm(record).to_dict() for record in health_records_orm]
        
        return {
            'data': health_records,
            'total': len(health_records)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        log.debug("Entering health_record_add view")
        log.debug(f"Request method: {self.request.method}")
        log.debug(f"Route name: {self.request.matched_route.name}")
        log.debug(f"Renderer: {getattr(self.request.matched_route, 'renderer', 'Not set')}")
        try:
            children_id = int(self.request.matchdict['children_id'])
            data = self.request.json_body
            new_record = HealthRecordORM(
                children_id=children_id,
                record_date=datetime.strptime(data['record_date'], '%Y-%m-%d').date(),
                record_immunization=data['record_immunization'],
                record_vaccinated_by=data['record_vaccinated_by']
            )
            self.request.dbsession.add(new_record)
            self.request.dbsession.flush()
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

@view_defaults(route_name='health_record_detail')
class HealthRecordDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        record_id = int(self.request.matchdict['record_id'])
        record_orm = self.request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
        if record_orm is None:
            return HTTPBadRequest(detail='Health record not found')
        record = HealthRecord.from_orm(record_orm)
        return record.to_dict()

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            record_id = int(self.request.matchdict['record_id'])
            data = self.request.json_body
            record_orm = self.request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
            if record_orm is None:
                return HTTPBadRequest(detail='Health record not found')
            
            record_orm.record_date = datetime.strptime(data['record_date'], '%Y-%m-%d').date()
            record_orm.record_immunization = data['record_immunization']
            record_orm.record_vaccinated_by = data['record_vaccinated_by']
            
            self.request.dbsession.flush()
            return {'message': 'Health record updated successfully'}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        record_id = int(self.request.matchdict['record_id'])
        record_orm = self.request.dbsession.query(HealthRecordORM).filter(HealthRecordORM.record_id == record_id).first()
        if record_orm is None:
            return HTTPBadRequest(detail='Health record not found')
        self.request.dbsession.delete(record_orm)
        return {'message': 'Health record deleted successfully'}