#!/bin/bash
#
# Setup Mustang Streamer services, libraries, utils and backgrounds

echo -e "Mustang streamer setup.."

# Copy backgrounds to data folder
cp app_setup/*.jpg /data/backgrounds/

# GPIO



# Python3 modules
sudo pip3 install requests

# WiringPi unofficial fork (Support new devices like CM4)
git clone https://github.com/WiringPi/WiringPi.git
cd WiringPi
./build

# Finishing..
sudo ldconfig


# Setting up services
sudo cp /home/volumio/mustang_control/app_setup/mustang_control.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mustang_control.service
echo -e "\nStarting Mustang streamer service.."
sudo systemctl start mustang_control.service
sudo systemctl status mustang_control.service

echo -e "\n\nInstallation complete!\n"