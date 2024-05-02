"""add reviews count to movies

Revision ID: 573896e2ed6e
Revises: 5bfac377bea7
Create Date: 2024-05-02 11:28:04.035947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '573896e2ed6e'
down_revision: Union[str, None] = '5bfac377bea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movies', sa.Column('reviewer_count', sa.Integer))


def downgrade() -> None:
    op.drop_column('movies', 'reviewer_count')
