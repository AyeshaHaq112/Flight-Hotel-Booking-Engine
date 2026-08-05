"""Deleting engine_count

Revision ID: 2a42ae99ce7b
Revises: 62c6c28995f7
Create Date: 2026-07-30 15:25:12.990809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a42ae99ce7b'
down_revision: Union[str, None] = '62c6c28995f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.drop_column('aircraft_types','engine_count')
  


def downgrade() -> None:
    op.add_column(
        'aircraft_types',
        sa.Column(
            'engine_count',
            sa.Integer(),
            nullable=False,
            server_default="2",))
    op.alter_column('aircraft_types', 'engine_count', server_default=None)  
