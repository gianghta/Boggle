#!/bin/bash

# Run a local dev environment
set -e
export MODE=production

# Register cleanup function on exit
clean_up () {
    ARG=$?
		echo 'Stopping the database container...'
		docker-compose down
    exit $ARG
}
trap clean_up EXIT

bash $PWD/scripts/lock_requirements.sh
docker-compose up
