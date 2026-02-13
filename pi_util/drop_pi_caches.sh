#!/bin/bash

### Run this every so often on the raspi to prevent running out of memory

# TODO get from enviroment (and ensure they exist)
BUCKSHOT_HOSTNAME='pi-zero-2-W-buckshot'
BUCKSHOT_SSH_HOSTNAME='buckshot'

if [[ $(hostname) = "$BUCKSHOT_HOSTNAME" ]]; then
	sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
else
	ssh "$BUCKSHOT_SSH_HOSTNAME" "sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
fi