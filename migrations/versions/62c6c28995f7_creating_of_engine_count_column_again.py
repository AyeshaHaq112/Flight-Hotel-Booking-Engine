"""Column added to aircrafttype table

Revision ID: 9bb4c487f1f2
Revises: 99565cac3599
Create Date: 2026-07-30 12:25:38.947957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62c6c28995f7'
down_revision: Union[str, None] = '99565cac3599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'aircraft_types',
        sa.Column(
            'engine_count',
            sa.Integer(),
            nullable=False,
            server_default="2"
        )
    )

    op.alter_column(
        'aircraft_types',
        'engine_count',
        server_default=None
    )
    
def downgrade() -> None:
    op.drop_column('aircraft_types','engine_count')
