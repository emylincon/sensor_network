#!/usr/bin/env bash

clear
echo "============ Setting up Your MQTT Broker ================="
sleep 2
apt update && apt upgrade -y
apt install mosquitto mosquitto-clients -y
touch /etc/mosquitto/passwd ; mosquitto_passwd -b /etc/mosquitto/passwd admin password
echo -e 'allow_anonymous false \npassword_file /etc/mosquitto/passwd' > /etc/mosquitto/conf.d/default.conf
/etc/init.d/mosquitto start
apt install python3 -y
apt install python3-pip -y
pip3 install paho-mqtt