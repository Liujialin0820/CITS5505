"""merge branches

Revision ID: e64ffd69bb0a
Revises: d263092639bc, e77662d2cb91
Create Date: 2025-05-14 09:28:53.972769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e64ffd69bb0a'
down_revision = ('d263092639bc', 'e77662d2cb91')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
