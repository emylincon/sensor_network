# This is a property of London South Bank University developed by EMEKA UGWUANYI

import os
import glob
import time
import paho.mqtt.client as mqtt
import os
import psutil
import random as r


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


algo = psutil.Process()
prev_t = 0
temp_ = []

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Publisher client')
print('-----------------------------------')
client = mqtt.Client()
username = 'admin'
password = 'password'
broker_ip = input("Broker's IP: ").strip()
broker_port_no = 1883
topic = 'iot/Temperature_server'
print('-----------------------------------')


client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)


def plot_cpu():
    global prev_t

    # get cpu
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    return round(delta, 4)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0

        temp_.append(temp_c)


def main():
    print('herre')
    while True:
        read_temp()
        print(temp_)
        if temp_ > 0:
            temp = temp_.pop()
            cpu = plot_cpu()
            mem = round(algo.memory_percent(), 4)
            message = 'Temperature {} {} {}'.format(temp, mem, cpu)
            client.publish(topic, message)
            print(message)
            time.sleep(1)


if __name__ == '__main__':
    main()
