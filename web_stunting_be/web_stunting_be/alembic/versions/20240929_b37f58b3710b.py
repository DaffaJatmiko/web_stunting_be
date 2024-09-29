"""Add dummy data

Revision ID: b37f58b3710b
Revises: cea6831e60bf
Create Date: 2024-09-29 23:07:03.565782

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import date


# revision identifiers, used by Alembic.
revision = 'b37f58b3710b'
down_revision = 'cea6831e60bf'
branch_labels = None
depends_on = None


def upgrade():
    # Add dummy health workers
    health_workers = table('health_workers',
        column('worker_id', sa.Integer),
        column('worker_name', sa.String)
    )
    op.bulk_insert(health_workers,
        [
            {'worker_name': 'Dr. John Doe'},
            {'worker_name': 'Nurse Jane Smith'},
            {'worker_name': 'Dr. Alice Johnson'},
            {'worker_name': 'Nurse Bob Brown'},
            {'worker_name': 'Dr. Carol White'}
        ]
    )

    # Add dummy children
    children = table('children',
        column('children_id', sa.Integer),
        column('children_name', sa.String),
        column('children_birth_date', sa.Date),
        column('children_address', sa.String),
        column('children_parent', sa.String),
        column('children_parent_phone', sa.String),
        column('children_allergy', sa.String),
        column('children_blood_type', sa.String),
        column('children_weight', sa.Float),
        column('children_height', sa.Float)
    )
    op.bulk_insert(children,
        [
            {'children_name': 'Emma Thompson', 'children_birth_date': date(2020, 5, 15), 'children_address': '123 Main St', 'children_parent': 'Sarah Thompson', 'children_parent_phone': '123-456-7890', 'children_allergy': 'None', 'children_blood_type': 'A+', 'children_weight': 12.5, 'children_height': 80.0},
            {'children_name': 'Liam Parker', 'children_birth_date': date(2019, 8, 22), 'children_address': '456 Elm St', 'children_parent': 'Michael Parker', 'children_parent_phone': '234-567-8901', 'children_allergy': 'Peanuts', 'children_blood_type': 'B-', 'children_weight': 15.0, 'children_height': 90.0},
            {'children_name': 'Olivia Davis', 'children_birth_date': date(2021, 2, 10), 'children_address': '789 Oak St', 'children_parent': 'Emily Davis', 'children_parent_phone': '345-678-9012', 'children_allergy': 'Lactose', 'children_blood_type': 'O+', 'children_weight': 10.0, 'children_height': 75.0},
            {'children_name': 'Noah Wilson', 'children_birth_date': date(2020, 11, 5), 'children_address': '101 Pine St', 'children_parent': 'Jennifer Wilson', 'children_parent_phone': '456-789-0123', 'children_allergy': 'None', 'children_blood_type': 'AB+', 'children_weight': 13.0, 'children_height': 85.0},
            {'children_name': 'Ava Martinez', 'children_birth_date': date(2019, 6, 30), 'children_address': '202 Cedar St', 'children_parent': 'David Martinez', 'children_parent_phone': '567-890-1234', 'children_allergy': 'Eggs', 'children_blood_type': 'A-', 'children_weight': 16.0, 'children_height': 95.0}
        ]
    )

    # Add dummy health records
    health_records = table('health_records',
        column('record_id', sa.Integer),
        column('children_id', sa.Integer),
        column('record_date', sa.Date),
        column('record_immunization', sa.String),
        column('record_vaccinated_by', sa.String)
    )
    op.bulk_insert(health_records,
        [
            {'children_id': 1, 'record_date': date(2023, 1, 15), 'record_immunization': 'MMR', 'record_vaccinated_by': 'Dr. John Doe'},
            {'children_id': 2, 'record_date': date(2023, 2, 20), 'record_immunization': 'DTP', 'record_vaccinated_by': 'Nurse Jane Smith'},
            {'children_id': 3, 'record_date': date(2023, 3, 25), 'record_immunization': 'Polio', 'record_vaccinated_by': 'Dr. Alice Johnson'},
            {'children_id': 4, 'record_date': date(2023, 4, 30), 'record_immunization': 'Hepatitis B', 'record_vaccinated_by': 'Nurse Bob Brown'},
            {'children_id': 5, 'record_date': date(2023, 5, 5), 'record_immunization': 'BCG', 'record_vaccinated_by': 'Dr. Carol White'}
        ]
    )

    # Add dummy measurements
    measurements = table('measurements',
        column('measurement_id', sa.Integer),
        column('children_id', sa.Integer),
        column('measurement_date', sa.Date),
        column('measurement_weight', sa.Float),
        column('measurement_height', sa.Float),
        column('measurement_head_circumference', sa.Float),
        column('measurement_abdominal_circumference', sa.Float),
        column('measurement_leg_circumference', sa.Float),
        column('measurement_arm_circumference', sa.Float)
    )
    op.bulk_insert(measurements,
        [
            {'children_id': 1, 'measurement_date': date(2023, 6, 1), 'measurement_weight': 13.0, 'measurement_height': 82.0, 'measurement_head_circumference': 45.0, 'measurement_abdominal_circumference': 50.0, 'measurement_leg_circumference': 25.0, 'measurement_arm_circumference': 15.0},
            {'children_id': 2, 'measurement_date': date(2023, 6, 15), 'measurement_weight': 15.5, 'measurement_height': 92.0, 'measurement_head_circumference': 47.0, 'measurement_abdominal_circumference': 52.0, 'measurement_leg_circumference': 27.0, 'measurement_arm_circumference': 16.0},
            {'children_id': 3, 'measurement_date': date(2023, 6, 30), 'measurement_weight': 10.5, 'measurement_height': 77.0, 'measurement_head_circumference': 43.0, 'measurement_abdominal_circumference': 48.0, 'measurement_leg_circumference': 23.0, 'measurement_arm_circumference': 14.0},
            {'children_id': 4, 'measurement_date': date(2023, 7, 15), 'measurement_weight': 13.5, 'measurement_height': 87.0, 'measurement_head_circumference': 46.0, 'measurement_abdominal_circumference': 51.0, 'measurement_leg_circumference': 26.0, 'measurement_arm_circumference': 15.5},
            {'children_id': 5, 'measurement_date': date(2023, 7, 30), 'measurement_weight': 16.5, 'measurement_height': 97.0, 'measurement_head_circumference': 48.0, 'measurement_abdominal_circumference': 53.0, 'measurement_leg_circumference': 28.0, 'measurement_arm_circumference': 16.5}
        ]
    )

def downgrade():
    op.execute("DELETE FROM measurements")
    op.execute("DELETE FROM health_records")
    op.execute("DELETE FROM children")
    op.execute("DELETE FROM health_workers")
