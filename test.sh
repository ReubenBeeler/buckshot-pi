#!/bin/bash

HOST="buckshot"

ssh $HOST 'bash -ls' <<EOF
	hostname
EOF

hostname