"""create post table

Revision ID: 64ea80060dd4
Revises:
Create Date: 2022-08-26 19:01:00.928504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64ea80060dd4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
