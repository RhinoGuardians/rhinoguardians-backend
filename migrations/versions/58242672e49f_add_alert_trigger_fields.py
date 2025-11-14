"""add_alert_trigger_fields

Revision ID: 58242672e49f
Revises: 4161c4cf01ff
Create Date: 2025-11-08 17:50:46.987413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58242672e49f'
down_revision: Union[str, Sequence[str], None] = '4161c4cf01ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
