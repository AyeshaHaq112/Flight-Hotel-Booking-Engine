# CLAUDE.md

## What this project is

A flight & hotel booking engine built **as a database learning exercise**. The
schema, constraints, and queries are the deliverable. There is no application
layer and there will never be one.

I am building this to learn PostgreSQL, SQLAlchemy 2.0, and Alembic deeply. If
you write code I don't understand, the project has failed even if the code is
correct.

## Stack

- PostgreSQL 17, installed natively (NOT Docker)
- Python 3.12+
- SQLAlchemy >= 2.0, ORM style only (`Mapped[]`, `mapped_column()`, `select()`)
- psycopg 3 (`postgresql+psycopg://`), never psycopg2
- Alembic >= 1.13
- pytest
- uv for dependency management

## Hard rules

1. **No web framework.** No FastAPI, Flask, uvicorn, routes, or HTTP anything.
2. **No Pydantic models for data.** `pydantic-settings` for config only.
3. **No async.** Sync SQLAlchemy throughout.
4. **No SQLModel, Tortoise, Peewee, or Prisma.**
5. **No Docker.** Native Postgres on localhost:5432.
6. **SQLAlchemy 2.0 style only.** If you write `session.query(...)`, that is a bug.
7. **Money is `Numeric(19, 4)`.** Never `Float`, never `Integer` cents.
8. **Timestamps are `timestamptz`.** Never naive `timestamp`.
9. **Nothing is ever hard-deleted.** Bookings, tickets, and payments are
   append-only; state changes via status columns and reversal rows.
10. **Test schema is built by running Alembic migrations**, never
    `Base.metadata.create_all()`.

## Teaching mode (important)

For anything in the **learning list** below, do NOT write the implementation.
Instead:

- Write the surrounding scaffolding (model class, function signature, test
  file with the test names)
- Leave a `# TODO(me):` marker where the interesting code goes
- Above it, write a comment explaining the *concept* and what the tradeoffs are
- Tell me in chat what to read and what I should try first

Then wait. I will write it, and you review it.

### Learning list — scaffold only, do not implement

- Any `EXCLUDE` constraint
- Any partial unique index
- Any `CHECK` constraint expressing business logic
- Any `WITH RECURSIVE` CTE
- The atomic inventory decrement (`UPDATE ... WHERE sold < authorized RETURNING`)
- Any window function
- Any query being optimized after an `EXPLAIN ANALYZE`
- The deliberately-broken race condition demos
- Migration `upgrade()`/`downgrade()` bodies that move data between tables

### Fair game — just write it

- Project scaffolding, Makefile, `.env.example`, `pyproject.toml`
- `alembic.ini`, `migrations/env.py`
- Declarative base, naming convention, engine/session setup
- Plain column definitions and relationships on models
- Reference-data seed scripts (airports, aircraft types)
- pytest fixtures and conftest plumbing
- Docstrings, type hints, ruff/mypy config

## Layout

```
src/flightdb/
  config.py  db.py
  models/    base.py geography.py fleet.py schedule.py inventory.py booking.py
  queries/   availability.py search.py booking.py reporting.py
  seed/      reference.py generate.py
migrations/versions/
tests/       conftest.py test_constraints.py test_concurrency.py
             test_booking_flow.py test_migrations.py
benchmarks/  explain.py
docs/        decisions.md
```

`models/` defines structure. `queries/` holds the SQL. Business logic must not
leak into model classes.

## Database

```
DATABASE_URL=postgresql+psycopg://flight:flight@localhost:5432/flightdb
TEST_DATABASE_URL=postgresql+psycopg://flight:flight@localhost:5432/flightdb_test
```

Role `flight` is NOT a superuser. If a migration needs superuser rights, tell me
rather than working around it.

## Modeling decisions already made — don't relitigate

- `scheduled_flights` (recurring schedule) is separate from `flights` (one
  service date, has seats).
- `bookings` (PNR) / `tickets` (per passenger) / `ticket_segments` (per
  passenger per flight) are three distinct tables.
- Fare amounts are **snapshotted** onto `ticket_segments` at purchase time,
  never joined from `fares` for display.
- Seat availability uses a partial unique index on
  `(flight_id, seat_no) WHERE status IN ('held','confirmed')`, not a plain
  UNIQUE, so releases keep history.
- Hotel stays use `daterange` with `'[)'` bounds — checkout day is free.
- `airports.tz` holds an IANA name; local departure times are stored as bare
  `time` and converted to `timestamptz` at schedule generation.

## Workflow

- Every phase ends with: migration applied, tests passing, `make roundtrip` clean.
- After each modeling decision, append a short entry to `docs/decisions.md`
  saying *why*.
- Autogenerate does not see EXCLUDE constraints, partial indexes, triggers, or
  partitions. Those are hand-written with `op.execute()` and filtered out in
  `include_object`.
- Every constraint needs a test that tries to violate it and asserts failure.

## When I ask you something

Explain before you code. If there are two reasonable designs, show me both and
say which you'd pick and why. If I'm about to do something that will hurt later,
say so directly — don't just implement what I asked.
