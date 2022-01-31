#!/bin/bash

set -e

./docker/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT

exec "$@"