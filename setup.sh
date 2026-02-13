#!/bin/bash

set -e

if [[ ! -f '.env' ]]; then
	cp .env.example .env
	echo >&2 '⚠️ Make sure that your local machine provides values for all environment variables in .env (or have them in your environment) before proceeding with this project'
	exit -1
fi

echo 'Installing to Raspberry Pi via SSH...'

# Copy all the necessary files to the pi (btw ./ssh is very handy for development)
./ssh </dev/null

# Install uv
ssh "$BUCKSHOT_SSH_HOSTNAME" 'curl -LsSf https://astral.sh/uv/install.sh | sh'

# Create the venv and install dependencies
ssh "$BUCKSHOT_SSH_HOSTNAME" "bash -lc 'mkdir -p $BUCKSHOT_PROJECT_DIR && cd $BUCKSHOT_PROJECT_DIR && uv venv --system-site-packages --clear && uv lock && uv sync'"