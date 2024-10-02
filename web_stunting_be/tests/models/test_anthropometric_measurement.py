import unittest
from unittest.mock import Mock, patch
from web_stunting_be.models.anthropometric_measurement import Measurement
from web_stunting_be.models.health_record import HealthRecord
from web_stunting_be.orms.health_record import HealthRecordORM
from datetime import date

class TestMeasurementModel(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()

    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_get_all_by_child(self, MockMeasurementORM):
        mock_measurements = [Mock(), Mock()]
        self.mock_session.query.return_value.filter.return_value.all.return_value = mock_measurements

        measurements = Measurement.get_all_by_child(self.mock_session, 1)

        self.assertEqual(len(measurements), 2)
        self.assertIsInstance(measurements[0], Measurement)
        self.assertIsInstance(measurements[1], Measurement)

    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_get_by_id(self, MockMeasurementORM):
        mock_measurement = Mock()
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_measurement

        measurement = Measurement.get_by_id(self.mock_session, 1)

        self.assertIsInstance(measurement, Measurement)
        self.mock_session.query.assert_called_once_with(MockMeasurementORM)

    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_get_by_id_not_found(self, MockMeasurementORM):
        self.mock_session.query.return_value.filter.return_value.first.return_value = None

        measurement = Measurement.get_by_id(self.mock_session, 1)

        self.assertIsNone(measurement)

    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_create_measurement(self, MockMeasurementORM):
        data = {
            'children_id': 1,
            'measurement_date': '2023-01-01',
            'measurement_weight': 10.5,
            'measurement_height': 80.0,
            'measurement_head_circumference': 40.0,
            'measurement_abdominal_circumference': 50.0,
            'measurement_leg_circumference': 30.0,
            'measurement_arm_circumference': 20.0
        }
        
        new_measurement = Measurement.create(self.mock_session, data)
        
        self.assertIsInstance(new_measurement, Measurement)
        self.mock_session.add.assert_called_once()
        self.mock_session.flush.assert_called_once()


    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_update_measurement(self, MockMeasurementORM):
        mock_measurement = Mock()
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_measurement
        
        data = {
            'measurement_weight': 11.0,
            'measurement_height': 82.0
        }
        
        updated_measurement = Measurement.update(self.mock_session, 1, data)
        
        self.assertIsInstance(updated_measurement, Measurement)
        self.mock_session.flush.assert_called_once()
        
        for key, value in data.items():
            self.assertEqual(getattr(updated_measurement, key), value)
        
        # Verify that the mock_measurement was updated
        for key, value in data.items():
            self.assertEqual(getattr(mock_measurement, key), value)

    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_delete_measurement(self, MockMeasurementORM):
        mock_measurement = Mock()
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_measurement

        result = Measurement.delete(self.mock_session, 1)

        self.assertTrue(result)
        self.mock_session.delete.assert_called_once_with(mock_measurement)

    @patch('web_stunting_be.models.anthropometric_measurement.MeasurementORM')
    def test_delete_measurement_not_found(self, MockMeasurementORM):
        self.mock_session.query.return_value.filter.return_value.first.return_value = None

        result = Measurement.delete(self.mock_session, 1)

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()