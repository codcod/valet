"""create schema

Revision ID: ec5ddda825ce
Revises: 
Create Date: 2023-01-22 15:43:12.663404

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime as dt

# revision identifiers, used by Alembic.
revision = 'ec5ddda825ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('surname', sa.String(64), nullable=False),
        sqlite_autoincrement=True
    )
    op.create_table(
        'spots',
        sa.Column('spot_id', sa.Integer, primary_key=True),
        sa.Column('number', sa.String(64), unique=True),
        sqlite_autoincrement=True
    )
    op.create_table(
        'statuses',
        sa.Column('status_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64)),
        sqlite_autoincrement=True
    )
    op.create_table(
        'assignments',
        sa.Column('assignment_id', sa.Integer, primary_key=True),
        sa.Column('parking_day', sa.DateTime, index=True, default=dt.utcnow),
        
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('spot_id', sa.Integer, sa.ForeignKey('spots.spot_id')),
    )
    op.create_table(
        'workflow',
        sa.Column('workflow_id', sa.Integer, primary_key=True),
        sa.Column('timestamp', sa.DateTime, index=True, default=dt.utcnow),
        sa.Column('parking_day', sa.DateTime, default=dt.utcnow),
        
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('statuses.status_id')),
    )


def downgrade() -> None:
    op.drop_table('assignments')
    op.drop_table('workflow')
    op.drop_table('users')
    op.drop_table('spots')
    op.drop_table('statuses')
