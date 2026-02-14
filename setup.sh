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

# TODO create the crontab

# # Upload a photo every 5 minutes from 5:45am-9:15am daily
# 45-55/5 5 * * * reuben cd $BUCKSHOT_PROJECT_DIR && ./cronjob.sh main.py >> /var/log/buckshot.log 2>&1
# */5 6-20 * * * reuben cd $BUCKSHOT_PROJECT_DIR && ./cronjob.sh main.py >> /var/log/buckshot.log 2>&1
# 0-15/5 21 * * * reuben cd $BUCKSHOT_PROJECT_DIR && ./cronjob.sh main.py >> /var/log/buckshot.log 2>&1

# # Validate photos at 9:30pm daily
# 30 21 * * * reuben cd $BUCKSHOT_PROJECT_DIR && ./cronjob.sh lib/validate.py >> /var/log/buckshot.log 2>&1