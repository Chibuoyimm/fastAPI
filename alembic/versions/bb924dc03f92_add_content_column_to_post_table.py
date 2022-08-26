"""add content column to post table

Revision ID: bb924dc03f92
Revises: 64ea80060dd4
Create Date: 2022-08-26 19:14:53.871601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb924dc03f92'
down_revision = '64ea80060dd4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
