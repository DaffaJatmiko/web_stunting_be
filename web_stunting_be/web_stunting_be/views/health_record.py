from pyramid.view import view_config, view_defaults
from ..models.health_record import HealthRecord
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
import logging

log = logging.getLogger(__name__)

@view_defaults(route_name='health_record')
class HealthRecordViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        children_id = int(self.request.matchdict['children_id'])
        health_records = HealthRecord.get_all_by_child(self.request.dbsession, children_id)
        return {
            'data': [record.to_dict() for record in health_records],
            'total': len(health_records)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        log.debug("Entering health_record_add view")
        try:
            children_id = int(self.request.matchdict['children_id'])
            data = self.request.json_body
            data['children_id'] = children_id
            new_record = HealthRecord.create(self.request.dbsession, data)
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
        record = HealthRecord.get_by_id(self.request.dbsession, record_id)
        if record is None:
            return HTTPNotFound(detail='Health record not found')
        return record.to_dict()

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            record_id = int(self.request.matchdict['record_id'])
            data = self.request.json_body
            updated_record = HealthRecord.update(self.request.dbsession, record_id, data)
            if updated_record is None:
                return HTTPNotFound(detail='Health record not found')
            return {'message': 'Health record updated successfully'}
        except KeyError as e:
            return HTTPBadRequest(detail=f'Missing required field: {str(e)}')
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        record_id = int(self.request.matchdict['record_id'])
        if HealthRecord.delete(self.request.dbsession, record_id):
            return {'message': 'Health record deleted successfully'}
        return HTTPNotFound(detail='Health record not found')