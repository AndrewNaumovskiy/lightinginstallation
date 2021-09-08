#!/bin/sh

#### FTDI installation script

# update and upgrade before installation

#sudo apt-get update

#sudo apt-get upgrade

mkdir lighting

cd lighting

wget https://raw.githubusercontent.com/AndrewNaumovskiy/lightinginstallation/master/main.py

sudo apt install python3-pip

sudo pip3 install pyserial

wget https://raw.githubusercontent.com/AndrewNaumovskiy/lightinginstallation/master/SetLightingValues.sh

sudo chmod +x SetLightingValues.sh

sudo mv SetLightingValues.sh /usr/local/bin