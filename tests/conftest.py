import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from flightdb.config import settings


@pytest.fixture(scope="session")
def engine():
    """Create an engine connected to the test database.

    The test database must already have migrations applied via:
        DATABASE_URL=$TEST_DATABASE_URL make upgrade
    """
    eng = create_engine(settings.TEST_DATABASE_URL)
    yield eng
    eng.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(bind=engine)


@pytest.fixture()
def db_session(session_factory):
    """Fast rollback-based fixture.

    Wraps each test in a transaction that is rolled back at the end.
    Good for read-heavy tests or tests that don't need to verify
    constraint enforcement (constraints fire on COMMIT in some cases).

    The test sees its own uncommitted writes via the session, but
    nothing is persisted to the database.
    """
    connection = session_factory.kw["bind"].connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def db_session_committed(session_factory):
    """Commit-and-cleanup fixture.

    Actually commits data so that database-level constraints (CHECK,
    UNIQUE, EXCLUDE, deferred FKs) are fully enforced. Cleans up by
    truncating all tables after the test.

    Use this when testing constraint violations — a rollback fixture
    wouldn't trigger deferred constraints or see database-generated
    values (sequences, server defaults on other transactions).
    """
    session = session_factory()

    yield session

    session.close()

    # Truncate all application tables (not alembic_version)
    with session_factory.kw["bind"].connect() as conn:
        conn.execute(text(
            "DO $$ "
            "DECLARE r RECORD; "
            "BEGIN "
            "  FOR r IN "
            "    SELECT tablename FROM pg_tables "
            "    WHERE schemaname = 'public' AND tablename != 'alembic_version' "
            "  LOOP "
            "    EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE'; "
            "  END LOOP; "
            "END $$;"
        ))
        conn.commit()
