#!/bin/bash

# TODO get BUCKSHOT_HOSTNAME from enviroment
BUCKSHOT_HOSTNAME='pi-zero-2-W-buckshot'

if [[ $(hostname) != "$BUCKSHOT_HOSTNAME" ]]; then
	echo "$0: error: trying to execute on wrong device! Expected hostname="$BUCKSHOT_HOSTNAME" but instead got hostname=$(hostname)" >&2
	exit -1
fi

cd /home/reuben/Code

./pi_util/drop_pi_caches.sh

uv run main.py

./pi_util/drop_pi_caches.sh
