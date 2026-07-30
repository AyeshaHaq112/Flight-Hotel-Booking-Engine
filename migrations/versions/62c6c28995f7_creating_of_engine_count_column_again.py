"""Creating of engine_count column again

Revision ID: 62c6c28995f7
Revises: 99565cac3599
Create Date: 2026-07-30 14:41:26.236356

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
    pass


def downgrade() -> None:
    pass
