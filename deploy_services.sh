#!/bin/bash

set -e

current_dir=$(pwd)

# List of services to deploy
services=("auth_monitor" "login_monitor")

for service in "${services[@]}"; do
    # Create the service files from templates
    sed "s|__DIR__|$current_dir|g" "${service}.template.service" > "${service}.service"

    # Copy to systemd and enable & start services
    sudo cp "${service}.service" /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable "${service}.service"
    sudo systemctl start "${service}.service"
done
