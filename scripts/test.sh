#!/bin/bash


set -a
source .env
set +a

set -e
export MODE=testing
export TEST_POSTGRES_PORT=54321

# Register cleanup function on exit
clean_up () {
    ARG=$?
		echo 'Stopping the test database container...'
		docker stop test_postgres_boggle > /dev/null 2>&1
    exit $ARG
}
trap clean_up EXIT

# Set up test environment
echo 'Starting the test container...'

# Credit from pythonspeed.com/articles/faster-db-tests
docker create --rm --name test_postgres_boggle -v test_postgres_boggle_dbdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p 54321:5432 postgres:11 -c fsync=off

# Wait until the DB finishes setting up / starts running
docker start test_postgres_boggle
sleep 2
docker exec -it test_postgres_boggle psql -U postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"

# Update to the latest dependencies
bash $PWD/scripts/lock_requirements.sh

# Run tests
poetry run tox
