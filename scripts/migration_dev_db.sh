#!/bin/bash

export PYTHONPATH=.

# Export all environment variables from .env
set -a
source .env
set +a

# Clean the old versions
rm -r migrations/versions/*
docker-compose exec postgres psql -U postgres -c "DROP TABLE IF EXISTS alembic_version;"

# Run the migration
poetry run alembic revision --autogenerate --head head
poetry run alembic upgrade head

# Or migration for the service in docker-compose
# docker-compose exec web alembic revision --autogenerate --head head
# docker-compose exec web alembic upgrade head
