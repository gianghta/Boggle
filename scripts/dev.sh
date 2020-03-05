#!/bin/bash

# Run a local dev environment
set -e
export MODE=development

# Hide pre-commit set up log
pre-commit install > /dev/null 2>&1 || true

# Register cleanup function on exit
clean_up () {
    ARG=$?
		echo 'Stopping the database container...'
		docker-compose down
    exit $ARG
}
trap clean_up EXIT

# Run the Database in Docker environment
docker-compose up -d postgres

# Wait until the DB finishes setting up / starts running
bash -c "
    while ! docker-compose exec postgres pg_isready -h localhost -p 5432 -q -U postgres; do
      sleep 1
    done
  "

# Install the dependencies
poetry install
bash $PWD/scripts/lock_requirements.sh

# Run the app
poetry run python app.py
