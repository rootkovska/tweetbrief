#!/usr/bin/env bash

# Load environment variables
scriptPath=$(dirname $(readlink -f "${0}"))
source "${scriptPath}/.env.sh"

# Run bot
python "${scriptPath}/runner.py"
