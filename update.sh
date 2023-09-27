#!/bin/bash
#
# Update tool for Mustang Control

echo -e "Updating ..\n"
git pull
sudo systemctl restart mustang_control.service
sudo systemctl status mustang_control.service

echo -e "\nUpdate complete"
