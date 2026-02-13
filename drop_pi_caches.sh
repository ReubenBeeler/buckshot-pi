#!/bin/bash

if [[ $(hostname) = 'pi-zero-2-W-buckshot' ]]; then
	sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
else
	ssh buckshot "sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
fi