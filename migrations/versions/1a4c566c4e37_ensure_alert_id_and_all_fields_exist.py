"""Ensure alert_id and all fields exist

Revision ID: 1a4c566c4e37
Revises: 801ef9ce7fd2
Create Date: 2025-11-11 20:46:17.368405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '1a4c566c4e37'
down_revision: Union[str, Sequence[str], None] = '801ef9ce7fd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('alerts')]

    # Only add if not already present
    if 'notification_sent' not in columns:
        op.add_column(
            'alerts',
            sa.Column('notification_sent', sa.Boolean(), nullable=False, server_default='0')
        )

def downgrade():
    op.drop_column('alerts', 'notification_sent')


def downgrade() -> None:
    """Downgrade schema safely."""
    with op.batch_alter_table('alerts') as batch_op:
        if 'alert_id' in [col['name'] for col in inspect(op.get_bind()).get_columns('alerts')]:
            batch_op.drop_column('alert_id')
        # Optionally rename detection_id back to detection if needed
        if 'detection_id' in [col['name'] for col in inspect(op.get_bind()).get_columns('alerts')]:
            batch_op.alter_column(
                'detection_id',
                new_column_name='detection',
                existing_type=sa.String(),
                existing_nullable=False
            )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'alerts', type_='unique')
    op.drop_column('alerts', 'alert_id')
    with op.batch_alter_table('alerts') as batch_op:
        batch_op.alter_column('detection_id', new_column_name='detection', existing_type=sa.String(), existing_nullable=False)
        batch_op.alter_column('detection', type_=sa.INTEGER(), existing_type=sa.String(), existing_nullable=False)
    op.alter_column('alerts', 'severity',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('alerts', 'source',
               existing_type=sa.VARCHAR(),
               nullable=True)
