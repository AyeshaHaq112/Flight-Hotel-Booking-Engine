from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from flightdb.config import settings
from flightdb.models.base import Base

# Alembic Config object — access to alembic.ini values
config = context.config

# Override sqlalchemy.url from our application settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """Filter objects that Alembic should NOT autogenerate.

    Hand-written migrations handle: EXCLUDE constraints, partial indexes,
    triggers, and partitions. We filter them here so autogenerate doesn't
    try to drop them.
    """
    if type_ == "index" and name and name.startswith("ix_partial_"):
        return False
    if type_ == "unique_constraint" and name and name.startswith("excl_"):
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — generates SQL without a live DB."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode — connects to the database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
