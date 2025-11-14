"""add_alert_trigger_fields

Revision ID: 4161c4cf01ff
Revises: 5a301775c55d
Create Date: 2025-11-08 17:45:35.241763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '4161c4cf01ff'
down_revision: Union[str, Sequence[str], None] = '5a301775c55d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add new fields for alert trigger functionality."""
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('alerts')]

    # Add columns only if not present
    if 'type' not in columns:
        op.add_column('alerts', sa.Column('type', sa.String(), nullable=True))
    if 'severity' not in columns:
        op.add_column('alerts', sa.Column('severity', sa.String(), nullable=True))
    if 'source' not in columns:
        op.add_column('alerts', sa.Column('source', sa.String(), nullable=True))
    if 'notes' not in columns:
        op.add_column('alerts', sa.Column('notes', sa.Text(), nullable=True))
    if 'lat' not in columns:
        op.add_column('alerts', sa.Column('lat', sa.Float(), nullable=True))
    if 'lng' not in columns:
        op.add_column('alerts', sa.Column('lng', sa.Float(), nullable=True))
    if 'zone_label' not in columns:
        op.add_column('alerts', sa.Column('zone_label', sa.String(), nullable=True))
    if 'created_by' not in columns:
        op.add_column('alerts', sa.Column('created_by', sa.String(), nullable=True))
    if 'notification_sent' not in columns:
        op.add_column('alerts', sa.Column('notification_sent', sa.Boolean(), nullable=False, server_default='0'))
    if 'notification_timestamp' not in columns:
        op.add_column('alerts', sa.Column('notification_timestamp', sa.DateTime(), nullable=True))
    if 'message' not in columns:
        op.add_column('alerts', sa.Column('message', sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove alert trigger fields."""
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('alerts')]

    # Drop columns only if present
    for col_name in [
        'type', 'severity', 'source', 'notes', 'lat', 'lng', 'zone_label',
        'created_by', 'notification_sent', 'notification_timestamp', 'message'
    ]:
        if col_name in columns:
            op.drop_column('alerts', col_name)
