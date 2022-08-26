"""add last few columns to posts table

Revision ID: 0ae90470be4b
Revises: 3b5ec454bc51
Create Date: 2022-08-26 20:35:02.400576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ae90470be4b'
down_revision = '3b5ec454bc51'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE")),
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
