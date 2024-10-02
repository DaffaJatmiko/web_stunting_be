import unittest
from unittest.mock import Mock, patch
from web_stunting_be.models.health_record import HealthRecord
from web_stunting_be.orms.health_record import HealthRecordORM
from datetime import date

class TestHealthRecordModel(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()

    @patch('web_stunting_be.models.health_record.HealthRecordORM')
    def test_get_all_by_child(self, MockHealthRecordORM):
        mock_records = [Mock(
            record_id=1,
            children_id=1,
            record_date=date(2023, 1, 1),
            record_immunization='Test Immunization',
            record_vaccinated_by='Test Doctor'
        ), Mock(
            record_id=2,
            children_id=1,
            record_date=date(2023, 2, 1),
            record_immunization='Test Immunization 2',
            record_vaccinated_by='Test Doctor 2'
        )]
        self.mock_session.query.return_value.filter.return_value.all.return_value = mock_records

        records = HealthRecord.get_all_by_child(self.mock_session, 1)

        self.assertEqual(len(records), 2)
        self.assertIsInstance(records[0], HealthRecord)
        self.assertIsInstance(records[1], HealthRecord)
        self.mock_session.query.assert_called_once_with(MockHealthRecordORM)
        self.mock_session.query.return_value.filter.assert_called_once_with(MockHealthRecordORM.children_id == 1)

    @patch('web_stunting_be.models.health_record.HealthRecordORM')
    def test_get_by_id(self, MockHealthRecordORM):
        mock_record = Mock(
            record_id=1,
            children_id=1,
            record_date=date(2023, 1, 1),
            record_immunization='Test Immunization',
            record_vaccinated_by='Test Doctor'
        )
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_record

        record = HealthRecord.get_by_id(self.mock_session, 1)

        self.assertIsInstance(record, HealthRecord)
        self.assertEqual(record.record_id, 1)
        self.assertEqual(record.children_id, 1)
        self.assertEqual(record.record_date, date(2023, 1, 1))
        self.assertEqual(record.record_immunization, 'Test Immunization')
        self.assertEqual(record.record_vaccinated_by, 'Test Doctor')
        self.mock_session.query.assert_called_once_with(MockHealthRecordORM)
        self.mock_session.query.return_value.filter.assert_called_once_with(MockHealthRecordORM.record_id == 1)

    @patch('web_stunting_be.models.health_record.HealthRecordORM')
    def test_get_by_id_not_found(self, MockHealthRecordORM):
        self.mock_session.query.return_value.filter.return_value.first.return_value = None

        record = HealthRecord.get_by_id(self.mock_session, 1)

        self.assertIsNone(record)
        self.mock_session.query.assert_called_once_with(MockHealthRecordORM)
        self.mock_session.query.return_value.filter.assert_called_once_with(MockHealthRecordORM.record_id == 1)

    @patch('web_stunting_be.models.health_record.HealthRecordORM')
    def test_create_health_record(self, MockHealthRecordORM):
        data = {
            'children_id': 1,
            'record_date': '2023-01-01',
            'record_immunization': 'Test Immunization',
            'record_vaccinated_by': 'Test Doctor'
        }
        
        new_record = HealthRecord.create(self.mock_session, data)
        
        self.assertIsInstance(new_record, HealthRecord)
        self.mock_session.add.assert_called_once()
        self.mock_session.flush.assert_called_once()

    @patch('web_stunting_be.models.health_record.HealthRecordORM')
    def test_update_health_record(self, MockHealthRecordORM):
        mock_record = Mock()
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_record

        data = {
            'record_immunization': 'Updated Immunization',
            'record_vaccinated_by': 'Updated Doctor'
        }

        updated_record = HealthRecord.update(self.mock_session, 1, data)

        self.assertIsInstance(updated_record, HealthRecord)
        self.mock_session.flush.assert_called_once()
        for key, value in data.items():
            self.assertEqual(getattr(updated_record, key), value)

if __name__ == '__main__':
    unittest.main()