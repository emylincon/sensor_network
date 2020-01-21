#!/usr/bin/env bash

apt update && apt upgrade -y
apt install python3 -y
apt install python3-pip -y
apt install python3-psutil -y
pip3 install paho-mqtt
apt install python3-numpy -y