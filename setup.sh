#!/bin/bash
#
# Setup Mustang Streamer services, libraries, utils and backgrounds

echo -e "Mustang streamer setup.."

# Copy backgrounds to data folder
cp app_setup/*.jpg /data/backgrounds/

# GPIO



# Python3 modules
sudo pip3 install requests


# Setting up services
sudo cp app_setup/mustang_control.service /lib/system/systemd/
sudo systemctl daemon reload
sudo systemctl enable mustang_control.service
sudo systemctl start mustang_control.service

