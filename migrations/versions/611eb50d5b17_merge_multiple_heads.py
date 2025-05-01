"""Merge multiple heads

Revision ID: 611eb50d5b17
Revises: 36c183ba601a, bcc6e94649b7
Create Date: 2025-05-01 20:38:04.504274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '611eb50d5b17'
down_revision = ('36c183ba601a', 'bcc6e94649b7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
