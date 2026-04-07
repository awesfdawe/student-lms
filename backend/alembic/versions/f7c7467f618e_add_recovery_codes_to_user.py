"""add_recovery_codes_to_user

Revision ID: f7c7467f618e
Revises: d65be2e35a4e
Create Date: 2026-04-07 20:29:46.775596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f7c7467f618e'
down_revision: Union[str, Sequence[str], None] = 'd65be2e35a4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('recovery_codes', sa.JSON(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'recovery_codes')
