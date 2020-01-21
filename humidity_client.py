#import RPi.GPIO as GPIO
#import dht11
import time
import paho.mqtt.client as mqtt
import os
import psutil
import random as r
# initialize GPIO
'''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()

# read data using Pin GPIO21
instance = dht11.DHT11(pin=21)
'''
algo = psutil.Process()
prev_t = 0

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Publisher client')
print('-----------------------------------')
client = mqtt.Client()
username = input('Username of Broker: ').strip()
password = input('Password of Broker: ').strip()
broker_ip = input("Broker's IP: ").strip()
broker_port_no = 1883
topic = 'iot/Humidity_server'
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


def main():
    '''
    result = instance.read()
    if result.is_valid():
        print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)
    temp = result.temperature
    hum=result.humidity
    '''
    while True:
        hum = r.randrange(20)
        if hum != 0:
            cpu = plot_cpu()
            mem = round(algo.memory_percent(), 4)
            message = f'Humidity {hum} {mem} {cpu}'
            client.publish(topic, message)
        time.sleep(1)


if __name__ == '__main__':
    main()



