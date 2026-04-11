"""fix users table columns

Revision ID: 999999999999
Revises: b2db0d085533
Create Date: 2026-04-11 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '999999999999'
down_revision: Union[str, Sequence[str], None] = 'b2db0d085533'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR')
    op.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE')
    op.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_superuser BOOLEAN DEFAULT FALSE')
    op.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS totp_secret VARCHAR')
    op.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_2fa_enabled BOOLEAN DEFAULT FALSE')
    op.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS recovery_codes JSON')

def downgrade() -> None:
    pass
