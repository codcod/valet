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

    op.execute('insert into spots(number) values ("53")')
    op.execute('insert into spots(number) values ("54")')
    op.execute('insert into spots(number) values ("55")')
    op.execute('insert into spots(number) values ("56")')
    op.execute('insert into spots(number) values ("57")')
    op.execute('insert into spots(number) values ("58")')

    op.execute('insert into statuses(tag, descr) values ("RE", "requested")')
    op.execute('insert into statuses(tag, descr) values ("CA", "cancelled")')
    op.execute('insert into statuses(tag, descr) values ("AS", "assigned")')
    op.execute('insert into statuses(tag, descr) values ("RS", "resigned")')
    op.execute('insert into statuses(tag, descr) values ("LO", "lost")')
    op.execute('insert into statuses(tag, descr) values ("AR", "assigned after resignation")')

    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (1, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (2, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (3, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (4, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (5, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (6, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (7, null, 1, "2023-01-01")')
    op.execute('insert into assignments (user_id, spot_id, status_id, parking_day) values (8, null, 1, "2023-01-01")')


def downgrade() -> None:
    op.execute('delete from users')
    op.execute('delete from spots')
    op.execute('delete from assignments')
