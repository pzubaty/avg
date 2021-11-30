#!/usr/bin/env bash

gunicorn --chdir /opt handle_requests:app -w 4 --threads 4 -b 0.0.0.0:8080

# In case the prior fails
while true
do
    sleep 1
done
