from datetime import datetime

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# The naming convention MUST be set before any model is defined (and therefore
# before the first migration is generated). Here's why:
#
# When Alembic autogenerates a migration, it records constraint names literally
# in op.create_index(), op.create_unique_constraint(), etc. The downgrade()
# function uses those same names in op.drop_constraint(). If you let PostgreSQL
# pick names implicitly, you get non-deterministic names that differ between
# machines — and downgrade() breaks on any machine that didn't generate the
# migration.
#
# By attaching a naming_convention to MetaData, SQLAlchemy generates the SAME
# predictable name everywhere: "uq_airports_iata_code", "fk_routes_origin_id_airports",
# etc. Alembic picks those up, migrations are portable, and downgrade() always
# finds the constraint it's trying to drop.
#
# This must exist before the first migration because once a constraint name is
# baked into a migration file, changing the convention later won't fix those
# already-generated names — you'd have to rewrite every migration.

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
