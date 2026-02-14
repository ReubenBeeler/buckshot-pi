#!/bin/bash

{
	# TODO get from enviroment
	BUCKSHOT_HOSTNAME='pi-zero-2-W-buckshot'
	BUCKSHOT_PROJECT_DIR='/home/reuben/Code'

	if [[ $(hostname) != "$BUCKSHOT_HOSTNAME" ]]; then
		echo "$0: error: trying to execute on wrong device! Expected hostname=$BUCKSHOT_HOSTNAME but instead got hostname=$(hostname)" >&2
		exit -1
	fi

	cd "$BUCKSHOT_PROJECT_DIR"

	./pi_util/drop_pi_caches.sh
	sudo iw wlan0 set power_save off # let WiFi chip consume more power for faster & more reliable connections 
	uv run main.py
	sudo iw wlan0 set power_save on # optional, you may want power_save off for debugging...
	./pi_util/drop_pi_caches.sh
}