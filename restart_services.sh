#!/bin/bash

set -e

# List of services to restart
services=("auth_monitor" "login_monitor" "ufw_block_monitor")

for service in "${services[@]}"; do
    sudo systemctl restart "${service}.service"
done
