#!/bin/bash

current_dir=$(pwd)

# List of services to remove
services=("auth_monitor" "login_monitor" "ufw_block_monitor")

for service in "${services[@]}"; do
    # Stop and disable services
    sudo systemctl stop "${service}.service"
    sudo systemctl disable "${service}.service"

    # Remove service files
    sudo rm -f "/etc/systemd/system/${service}.service"
    sudo systemctl daemon-reload
done
