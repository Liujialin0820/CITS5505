"""merge multiple heads

Revision ID: e77662d2cb91
Revises: 495c3a70a8a8, cd1ba88a1c0a
Create Date: 2025-05-13 14:14:09.886261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e77662d2cb91'
down_revision = ('495c3a70a8a8', 'cd1ba88a1c0a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
