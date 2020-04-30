#!/bin/bash

# Load environment variables
scriptPath=$(dirname $(readlink -f "${0}"))
source "${scriptPath}/.env.sh"

# Run bot
python "${scriptPath}/twitter_bot.py"
