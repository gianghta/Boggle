#!/bin/bash

set -ex
docker-compose up --build --no-start --force-recreate --renew-anon-volumes
