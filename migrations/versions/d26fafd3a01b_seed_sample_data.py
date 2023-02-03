"""seed sample data

Revision ID: d26fafd3a01b
Revises: ec5ddda825ce
Create Date: 2023-01-22 15:43:34.071949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd26fafd3a01b'
down_revision = 'ec5ddda825ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('insert into users(name, surname) values("Jan1", "Kowalski")')
    op.execute('insert into users(name, surname) values("Jan2", "Kowalski")')
    op.execute('insert into users(name, surname) values("Jan3", "Kowalski")')
    op.execute('insert into users(name, surname) values("Jan4", "Kowalski")')

    op.execute('insert into spots(number) values ("53")')
    op.execute('insert into spots(number) values ("54")')
    op.execute('insert into spots(number) values ("55")')
    op.execute('insert into spots(number) values ("56")')
    op.execute('insert into spots(number) values ("57")')
    op.execute('insert into spots(number) values ("58")')

    op.execute('insert into statuses(status_id, name) values (100, "requested")')
    op.execute('insert into statuses(status_id, name) values (201, "lottery")')
    op.execute('insert into statuses(status_id, name) values (210, "cancelled")')
    op.execute('insert into statuses(status_id, name) values (301, "won")')
    op.execute('insert into statuses(status_id, name) values (310, "lost")')
    op.execute('insert into statuses(status_id, name) values (401, "used")')
    op.execute('insert into statuses(status_id, name) values (402, "unconfirmed")')
    op.execute('insert into statuses(status_id, name) values (405, "unused")')
    op.execute('insert into statuses(status_id, name) values (410, "resigned")')

    # 2023-01-01 has complete 'workflow' for all requestors
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:01:00", "2023-01-01", 1, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:02:00", "2023-01-01", 2, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:03:00", "2023-01-01", 3, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:04:00", "2023-01-01", 4, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:05:00", "2023-01-01", 4, 210)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:10:01", "2023-01-01", 1, 201)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:10:01", "2023-01-01", 2, 201)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:10:01", "2023-01-01", 3, 201)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:10:02", "2023-01-01", 1, 301)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:10:02", "2023-01-01", 2, 301)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:10:02", "2023-01-01", 3, 310)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:11:01", "2023-01-01", 1, 401)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-01 10:12:01", "2023-01-01", 2, 410)')

    # 2023-01-02 has only 3 requestors waiting for the lottery and 1 who cancelled
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-02 11:01:00", "2023-01-02", 1, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-02 11:02:00", "2023-01-02", 2, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-02 11:03:00", "2023-01-02", 4, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-02 11:04:00", "2023-01-02", 3, 100)')
    op.execute('insert into workflow (timestamp, parking_day, user_id, status_id) values ("2022-12-02 11:05:00", "2023-01-02", 3, 210)')
    
    op.execute('insert into assignments (parking_day, user_id, spot_id) values ("2023-01-01", 1, 1)')


def downgrade() -> None:
    op.execute('delete from users')
    op.execute('delete from spots')
    op.execute('delete from assignments')
