"""seed sample data

Revision ID: d26fafd3a01b
Revises: ec5ddda825ce
Create Date: 2023-01-22 15:43:34.071949

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime as dt


# revision identifiers, used by Alembic.
revision = 'd26fafd3a01b'
down_revision = 'ec5ddda825ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("insert into users (name, surname) values ('Jan1', 'Kowalski')")
    op.execute("insert into users (name, surname) values ('Jan2', 'Kowalski')")
    op.execute("insert into users (name, surname) values ('Jan3', 'Kowalski')")
    op.execute("insert into users (name, surname) values ('Jan4', 'Kowalski')")
    op.execute("insert into users (name, surname, slack_id) values ('Nikos', 'Ka', 'U040RMTUD8E')")

    op.execute("insert into spots (number) values ('53')")
    op.execute("insert into spots (number) values ('54')")
    op.execute("insert into spots (number) values ('55')")
    op.execute("insert into spots (number) values ('56')")
    op.execute("insert into spots (number) values ('57')")
    op.execute("insert into spots (number) values ('58')")

    op.execute("insert into statuses (status_id, name) values (100, 'requested')")
    op.execute("insert into statuses (status_id, name) values (201, 'lottery')")
    op.execute("insert into statuses (status_id, name) values (210, 'cancelled')")
    op.execute("insert into statuses (status_id, name) values (301, 'won')")
    op.execute("insert into statuses (status_id, name) values (310, 'lost')")
    op.execute("insert into statuses (status_id, name) values (401, 'used')")
    op.execute("insert into statuses (status_id, name) values (402, 'unconfirmed')")
    op.execute("insert into statuses (status_id, name) values (405, 'unused')")
    op.execute("insert into statuses (status_id, name) values (410, 'resigned')")

    # temporary table to create inserts
    workflow_table = sa.sql.table(
        'workflow',
        sa.Column('workflow_id', sa.Integer, autoincrement=True),
        sa.Column('timestamp', sa.DateTime, index=True, default=dt.utcnow),
        sa.Column('parking_day', sa.Date),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('statuses.status_id')),
    )
    
    d1 = dt(2023, 1, 1).date()
    d2 = dt(2023, 1, 2).date()
    op.bulk_insert(workflow_table,
        [
            # 2023-01-01 has complete 'workflow' for all requestors
            {'timestamp': dt(2022, 12, 1, 10,  1, 0), 'parking_day': d1, 'user_id': 1, 'status_id': 100},
            {'timestamp': dt(2022, 12, 1, 10,  2, 0), 'parking_day': d1, 'user_id': 2, 'status_id': 100},
            {'timestamp': dt(2022, 12, 1, 10,  3, 0), 'parking_day': d1, 'user_id': 3, 'status_id': 100},
            {'timestamp': dt(2022, 12, 1, 10,  4, 0), 'parking_day': d1, 'user_id': 4, 'status_id': 100},
            {'timestamp': dt(2022, 12, 1, 10,  5, 0), 'parking_day': d1, 'user_id': 4, 'status_id': 210},
            {'timestamp': dt(2022, 12, 1, 10, 10, 1), 'parking_day': d1, 'user_id': 1, 'status_id': 201},
            {'timestamp': dt(2022, 12, 1, 10, 10, 1), 'parking_day': d1, 'user_id': 2, 'status_id': 201},
            {'timestamp': dt(2022, 12, 1, 10, 10, 1), 'parking_day': d1, 'user_id': 3, 'status_id': 201},
            {'timestamp': dt(2022, 12, 1, 10, 10, 1), 'parking_day': d1, 'user_id': 1, 'status_id': 301},
            {'timestamp': dt(2022, 12, 1, 10, 10, 2), 'parking_day': d1, 'user_id': 2, 'status_id': 301},
            {'timestamp': dt(2022, 12, 1, 10, 10, 2), 'parking_day': d1, 'user_id': 3, 'status_id': 310},
            {'timestamp': dt(2022, 12, 1, 10, 11, 1), 'parking_day': d1, 'user_id': 1, 'status_id': 401},
            {'timestamp': dt(2022, 12, 1, 10, 12, 1), 'parking_day': d1, 'user_id': 2, 'status_id': 410},
            
            # 2023-01-02 has only 3 requestors waiting for the lottery and 1 who cancelled
            {'timestamp': dt(2022, 12, 2, 11, 1, 0), 'parking_day': d2, 'user_id': 1, 'status_id': 100},
            {'timestamp': dt(2022, 12, 2, 11, 2, 0), 'parking_day': d2, 'user_id': 2, 'status_id': 100},
            {'timestamp': dt(2022, 12, 2, 11, 3, 0), 'parking_day': d2, 'user_id': 4, 'status_id': 100},
            {'timestamp': dt(2022, 12, 2, 11, 4, 0), 'parking_day': d2, 'user_id': 3, 'status_id': 100},
            {'timestamp': dt(2022, 12, 2, 11, 5, 0), 'parking_day': d2, 'user_id': 3, 'status_id': 210},

        ]

    )


def downgrade() -> None:
    op.execute('delete from assignments')
    op.execute('delete from workflow')
    op.execute('delete from users')
    op.execute('delete from spots')
