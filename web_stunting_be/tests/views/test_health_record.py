import unittest
from unittest.mock import Mock, patch
from pyramid import testing

from web_stunting_be.views.health_record import HealthRecordViews, HealthRecordDetailViews

class TestHealthRecordViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.dbsession = Mock()
        self.request.matchdict = {'children_id': '1'}

    def tearDown(self):
        testing.tearDown()

    @patch('web_stunting_be.models.health_record.HealthRecord.get_all_by_child')
    def test_list(self, mock_get_all):
        mock_get_all.return_value = [Mock(to_dict=lambda: {'id': 1})]
        view = HealthRecordViews(self.request)
        response = view.list()
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['total'], 1)

    @patch('web_stunting_be.models.health_record.HealthRecord.create')
    def test_add(self, mock_create):
        mock_create.return_value = Mock(record_id=1)
        self.request.json_body = {'date': '2023-01-01'}
        view = HealthRecordViews(self.request)
        response = view.add()
        self.assertEqual(response['record_id'], 1)

class TestHealthRecordDetailViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.dbsession = Mock()
        self.request.matchdict = {'record_id': '1'}

    def tearDown(self):
        testing.tearDown()

    @patch('web_stunting_be.models.health_record.HealthRecord.get_by_id')
    def test_detail(self, mock_get_by_id):
        mock_get_by_id.return_value = Mock(to_dict=lambda: {'id': 1})
        view = HealthRecordDetailViews(self.request)
        response = view.detail()
        self.assertEqual(response['id'], 1)

    @patch('web_stunting_be.models.health_record.HealthRecord.update')
    def test_update(self, mock_update):
        mock_update.return_value = Mock(record_id=1)
        self.request.json_body = {'date': '2023-01-02'}
        view = HealthRecordDetailViews(self.request)
        response = view.update()
        self.assertEqual(response['message'], 'Health record updated successfully')

    @patch('web_stunting_be.models.health_record.HealthRecord.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = True
        view = HealthRecordDetailViews(self.request)
        response = view.delete()
        self.assertEqual(response['message'], 'Health record deleted successfully')

if __name__ == '__main__':
    unittest.main()