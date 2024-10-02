import unittest
from unittest.mock import Mock, patch, PropertyMock, call, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from web_stunting_be.models.child import Child
from web_stunting_be.orms.child import ChildORM
from datetime import date

class TestChildModel(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()

    @patch('web_stunting_be.models.child.ChildORM')
    @patch('web_stunting_be.models.child.joinedload')
    @patch('web_stunting_be.models.child.Measurement')
    @patch('web_stunting_be.models.child.HealthRecord')
    def test_get_all(self, MockHealthRecord, MockMeasurement, mock_joinedload, MockChildORM):
        mock_child = MagicMock()
        mock_child.children_id = 1
        mock_child.children_name = 'Test Child'
        mock_child.children_birth_date = date(2020, 1, 1)
        mock_child.children_address = 'Test Address'
        mock_child.children_parent = 'Test Parent'
        mock_child.children_parent_phone = '1234567890'
        mock_child.children_allergy = None
        mock_child.children_blood_type = 'A'
        mock_child.children_weight = 10.5
        mock_child.children_height = 80.0
        mock_child.measurements = []
        mock_child.health_records = []

        self.mock_session.query.return_value.options.return_value.all.return_value = [mock_child]
        
        MockMeasurement.from_orm.return_value = Mock()
        MockHealthRecord.from_orm.return_value = Mock()

        children = Child.get_all(self.mock_session)
        
        self.assertEqual(len(children), 1)
        self.assertIsInstance(children[0], Child)
        self.mock_session.query.assert_called_once_with(MockChildORM)
        self.mock_session.query.return_value.options.assert_called_once()
        mock_joinedload.assert_any_call(MockChildORM.measurements)
        mock_joinedload.assert_any_call(MockChildORM.health_records)

    @patch('web_stunting_be.models.child.ChildORM')
    @patch('web_stunting_be.models.child.joinedload')
    @patch('web_stunting_be.models.child.Measurement')
    @patch('web_stunting_be.models.child.HealthRecord')
    def test_get_by_id(self, MockHealthRecord, MockMeasurement, mock_joinedload, MockChildORM):
        mock_child = MagicMock()
        mock_child.children_id = 1
        mock_child.children_name = 'Test Child'
        mock_child.children_birth_date = date(2020, 1, 1)
        mock_child.children_address = 'Test Address'
        mock_child.children_parent = 'Test Parent'
        mock_child.children_parent_phone = '1234567890'
        mock_child.children_allergy = None
        mock_child.children_blood_type = 'A'
        mock_child.children_weight = 10.5
        mock_child.children_height = 80.0
        mock_child.measurements = []
        mock_child.health_records = []

        self.mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = mock_child
        
        MockMeasurement.from_orm.return_value = Mock()
        MockHealthRecord.from_orm.return_value = Mock()

        child = Child.get_by_id(self.mock_session, 1)
        
        self.assertIsInstance(child, Child)
        self.mock_session.query.assert_called_once_with(MockChildORM)
        self.mock_session.query.return_value.options.assert_called_once()
        mock_joinedload.assert_any_call(MockChildORM.measurements)
        mock_joinedload.assert_any_call(MockChildORM.health_records)
        self.mock_session.query.return_value.options.return_value.filter.assert_called_once_with(MockChildORM.children_id == 1)

    @patch('web_stunting_be.models.child.ChildORM')
    @patch('web_stunting_be.models.child.joinedload')
    def test_get_by_id_not_found(self, mock_joinedload, MockChildORM):
        self.mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = None
        
        child = Child.get_by_id(self.mock_session, 1)
        
        self.assertIsNone(child)
        self.mock_session.query.assert_called_once_with(MockChildORM)
        self.mock_session.query.return_value.options.assert_called_once()
        mock_joinedload.assert_any_call(MockChildORM.measurements)
        mock_joinedload.assert_any_call(MockChildORM.health_records)
        self.mock_session.query.return_value.options.return_value.filter.assert_called_once_with(MockChildORM.children_id == 1)

    @patch('web_stunting_be.models.child.ChildORM')
    def test_get_all_database_error(self, MockChildORM):
        MockChildORM.query.side_effect = SQLAlchemyError("Database error")
        
        with self.assertRaises(SQLAlchemyError):
            Child.get_all(self.mock_session)


    @patch('web_stunting_be.models.child.ChildORM')
    @patch('web_stunting_be.models.child.Measurement')
    @patch('web_stunting_be.models.child.HealthRecord')
    def test_update(self, MockHealthRecord, MockMeasurement, MockChildORM):
        # Create a mock child ORM object
        mock_child_orm = Mock()
        mock_child_orm.children_id = 1
        mock_child_orm.measurements = []
        mock_child_orm.health_records = []

        # Set up the attributes that will be updated
        mock_child_orm.children_name = 'Old Name'
        mock_child_orm.children_birth_date = date(2000, 1, 1)
        mock_child_orm.children_address = 'Old Address'
        mock_child_orm.children_parent = 'Old Parent'
        mock_child_orm.children_parent_phone = '0000000000'
        mock_child_orm.children_allergy = None
        mock_child_orm.children_blood_type = None
        mock_child_orm.children_weight = None
        mock_child_orm.children_height = None

        # Set up the query mock to return our mock child ORM
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_child_orm

        # Data to update
        data = {
            'children_name': 'Updated Child',
            'children_birth_date': '2023-01-01',
            'children_address': 'Updated Address',
            'children_parent': 'Updated Parent',
            'children_parent_phone': '1112223333',
        }

        # Call the update method
        updated_child = Child.update(self.mock_session, 1, data)

        self.assertIsInstance(updated_child, Child)
        self.assertEqual(updated_child.children_name, 'Updated Child')
        self.assertEqual(updated_child.children_birth_date, date(2023, 1, 1))
        self.assertEqual(updated_child.children_address, 'Updated Address')
        self.assertEqual(updated_child.children_parent, 'Updated Parent')
        self.assertEqual(updated_child.children_parent_phone, '1112223333')
        
        self.mock_session.flush.assert_called_once()

    
    @patch('web_stunting_be.models.child.ChildORM')
    def test_create(self, MockChildORM):
        data = {
            'children_name': 'New Child',
            'children_birth_date': '2023-01-01',
            'children_address': 'New Address',
            'children_parent': 'New Parent',
            'children_parent_phone': '0987654321',
        }
        
        new_child = Child.create(self.mock_session, data)
        
        self.assertIsInstance(new_child, Child)
        self.mock_session.add.assert_called_once()
        self.mock_session.flush.assert_called_once()

    def test_create_invalid_data(self):
        data = {
            'children_name': 'New Child',
            'children_address': 'New Address',
            'children_parent': 'New Parent',
            'children_parent_phone': '0987654321',
            # Missing children_birth_date
        }
        
        with self.assertRaises(KeyError):
            Child.create(self.mock_session, data)

    @patch('web_stunting_be.models.child.ChildORM')
    @patch('web_stunting_be.models.child.MeasurementORM')
    @patch('web_stunting_be.models.child.HealthRecordORM')
    def test_delete(self, MockHealthRecordORM, MockMeasurementORM, MockChildORM):
        mock_child = Mock()
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_child

        result = Child.delete(self.mock_session, 1)

        self.assertTrue(result)
        self.mock_session.query.assert_has_calls([
            call(MockChildORM),
            call(MockMeasurementORM),
            call(MockHealthRecordORM)
        ], any_order=True)

        self.mock_session.query.return_value.filter.assert_has_calls([
            call(MockChildORM.children_id == 1),
            call(MockMeasurementORM.children_id == 1),
            call(MockHealthRecordORM.children_id == 1)
        ], any_order=True)

    @patch('web_stunting_be.models.child.ChildORM')
    def test_delete_not_found(self, MockChildORM):
        self.mock_session.query.return_value.filter.return_value.first.return_value = None

        result = Child.delete(self.mock_session, 1)

        self.assertFalse(result)
        self.mock_session.query.assert_called_once_with(MockChildORM)
        self.mock_session.query.return_value.filter.assert_called_once_with(MockChildORM.children_id == 1)

if __name__ == '__main__':
    unittest.main()