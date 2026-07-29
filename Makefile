.PHONY: psql upgrade down roundtrip reset test

psql:
	psql -U flight -d flightdb

upgrade:
	uv run alembic upgrade head

down:
	uv run alembic downgrade -1

roundtrip:
	uv run alembic downgrade -1
	uv run alembic upgrade head

reset:
	uv run alembic downgrade base
	uv run alembic upgrade head

test:
	uv run pytest
