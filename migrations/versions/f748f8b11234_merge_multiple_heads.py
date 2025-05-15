"""merge multiple heads

Revision ID: f748f8b11234
Revises: d263092639bc, e77662d2cb91
Create Date: 2025-05-13 16:47:08.924994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f748f8b11234'
down_revision = ('d263092639bc', 'e77662d2cb91')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
