from .default import home
from .child import ChildViews, ChildDetailViews
from .health_record import HealthRecordViews, HealthRecordDetailViews
from .anthropometric_measurement import MeasurementViews, MeasurementDetailViews

__all__ = [
    'home',
    'ChildViews',
    'ChildDetailViews',
    'HealthRecordViews',
    'HealthRecordDetailViews',
    'MeasurementViews',
    'MeasurementDetailViews'
]