#!/bin/bash

# TODO make this into a git template for dev environments that require SSHing into a pi that can't host a proper VSCode ssh server

if [[ $# -ne 0 ]]; then
	echo $0: error: this script does not take any arguments! >&2
	exit -1
fi

HOST="buckshot"

cd $(dirname $0)

mkdir -p copyback && rm -rf copyback/**

rsync -avz --delete \
	--exclude='.venv/' \
	--filter='protect .venv/' \
	--exclude='uv.lock' \
	--filter='protect uv.lock' \
	--exclude='.git' \
	--exclude='__pycache__' \
	--exclude='*.pyc' \
	--exclude='pi.sh' \
	--exclude='images/' \
	. $HOST:/home/reuben/Code

ssh $HOST "sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"

echo -e \\nStarting interactive shell...
ssh -t $HOST "cd /home/reuben/Code && bash -l"

echo -e \\nCleaning up...
ssh $HOST "sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
rsync -avz $HOST:/home/reuben/Code/copyback/** ./copyback/