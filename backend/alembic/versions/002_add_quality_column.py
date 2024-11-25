"""add quality column

Revision ID: 002
Revises: 001
Create Date: 2024-03-11 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('animations', sa.Column('quality', sa.String(), nullable=False, server_default='medium'))

def downgrade() -> None:
    op.drop_column('animations', 'quality') 