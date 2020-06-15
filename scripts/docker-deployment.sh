#!/usr/bin/env bash

echo "Checking if .env exists ..."

if [[ -f .env ]] ; then

    echo "Exporting parameters from .env ..."

    export $(cat .env | sed 's/#.*//g' | xargs)

fi

echo "Checking if all parameters are set ..."

if [[ -z "${CONSUMER_KEY}" ]]; then

    echo "CONSUMER_KEY not found!"
    exit 1

fi

if [[ -z "${CONSUMER_SECRET}" ]]; then

    echo "CONSUMER_SECRET not found!"
    exit 1

fi

if [[ ( -z "${HOST_OUTPUT}" || -z "${BRIEF_OUTPUT}" ) && -z "${DROPBOX_ACCESS_TOKEN}" ]]; then

    echo "No storage found!"
    echo "The following options are currently supported:"
    echo -e "\tHOST_OUTPUT and BRIEF_OUTPUT for local storage"
    echo -e "\tDROPBOX_ACCESS_TOKEN for storage on Dropbox"
    exit 1

fi

if [[ -z "${TARGET_USERNAME}" ]]; then

    echo "TARGET_USERNAME not found!"
    exit 1

fi

echo "Bulding Python function ..."

docker build -t tweetbrief -f Dockerfile.local .

echo "Deploying Python fuction as Docker container ..."

if [[ ! ( -z "${HOST_OUTPUT}" && -z "${BRIEF_OUTPUT}" ) ]]; then

    docker run -d \
        --name tweetbrief \
        -e CONSUMER_SECRET \
        -e CONSUMER_SECRET \
        -e BRIEF_OUTPUT \
        -e TARGET_USERNAME \
        -v "${HOST_OUTPUT}:${BRIEF_OUTPUT}" \
        --restart unless-stopped \
        tweetbrief

else 

    docker run -d \
        --name tweetbrief \
        -e CONSUMER_SECRET \
        -e CONSUMER_SECRET \
        -e DROPBOX_ACCESS_TOKEN \
        -e TARGET_USERNAME \
        --restart unless-stopped \
        tweetbrief

fi

echo "Deployment completed successfully"