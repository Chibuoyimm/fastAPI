"""add user table

Revision ID: 1535a1bb2839
Revises: bb924dc03f92
Create Date: 2022-08-26 19:20:03.812924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1535a1bb2839'
down_revision = 'bb924dc03f92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint('id'), # another way to set primary key, does not differ from the first way
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
