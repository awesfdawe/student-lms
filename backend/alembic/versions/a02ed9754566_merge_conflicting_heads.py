"""Merge conflicting heads

Revision ID: a02ed9754566
Revises: 8a9ac76bb38f, 999999999999
Create Date: 2026-04-12 10:47:23.410055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a02ed9754566'
down_revision: Union[str, Sequence[str], None] = ('8a9ac76bb38f', '999999999999')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
