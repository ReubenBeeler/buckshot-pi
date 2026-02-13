#!/bin/bash

if [[ $(hostname) != 'pi-zero-2-W-buckshot' ]]; then
	echo "$0: error: trying to execute on wrong device! Expected hostname=pi-zero-2-W-buckshot but instead got hostname=$(hostname)" >&2
	exit -1
fi

cd /home/reuben/Code

./drop_pi_caches.sh

uv run main.py

./drop_pi_caches.sh
