import socket
import time
import threading as th
import json
import os
import matplotlib.pyplot as plt
from drawnow import *
import paho.mqtt.client as mqtt
import os

#192.168.40.132
fig = plt.figure()
data_dict = {}     # {temp_server:{Temperature:[], Memory:[], CPU:[]}, humidity_server:{Humidity:[], Memory:[], CPU:[]}}


def start_up():
    global username, password, broker_ip, topic, broker_port_no
    os.system('clear')
    print('-----------------------------------')
    print('Welcome to MQTT Subscriber client')
    print('-----------------------------------')

    username = input('Username of Broker: ').strip()
    password = input('Password of Broker: ').strip()
    broker_ip = input("Broker's IP: ").strip()
    broker_port_no = 1883
    topic = input("Topic: ").strip()   # topic layering use iot/#
    print('-----------------------------------')
    br = th.Thread(target=broker_loop())
    br.start()


# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    data = str(msg.payload, 'utf-8').split()
    topic = msg.topic
    #data format = 'title sensor_data memory_util cpu_util'
    if topic not in data_dict:
        data_dict[topic] = {data[0]: data[1], 'Memory': data[2], 'CPU': data[3]}
    else:
        keys = [data[0], 'Memory', 'CPU']
        for i in range(3):
            data_dict[topic][keys[i]] = data[i+1]


def broker_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port_no, 60)

    client.loop_forever()


def define_axis():
    global fig

    axis = []
    size = len(data_dict)
    for i in range(size*3):
        axis.append(fig.add_subplot(size,3,i+1))

    return axis


def _mov_avg(a1):
    ma1 = []   # moving average list
    avg1 = 0   # moving average pointwise
    count = 0
    for i in range(len(a1)):
        count += 1
        avg1 = ((count-1)*avg1+a1[i])/count
        ma1.append(round(avg1, 4))    # cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def plot_me():
    axes = define_axis()
    a_c = -3
    a_i = -2
    a_e = -1
    hold_ax = [a_c, a_i, a_e]
    for topic_ in data_dict:
        a_c += 3
        a_i += 3
        a_e += 3
        h = 0
        for data_set in data_dict[topic_]:
            plotter(ax=axes[hold_ax[h]], data=data_dict[topic_][data_set], key=topic_, name=data_set, col='c')
            h+=1

    fig.suptitle('IoT Sensor Network Smart City')


def plotter(ax, data, key, name, col):
    ax.grid(True)
    ax.plot(list(range(len(_mov_avg(data)))), _mov_avg(data), linewidth=2, label='{} {}'.format(name, key), color=col)
    #ax.set_ylabel('Moving {}'.format(name))
    ax.set_xlabel('Time (seconds)')
    ax.fill_between(list(range(len(_mov_avg(data)))), _mov_avg(data), 0, alpha=0.5, color=col)
    if name == "Memory":
        ax.set_ylabel('Client: {}'.format(key), rotation=0, fontsize=10, labelpad=30)
    ax.legend()
    plt.subplot(ax)


def show_graphs():
    drawnow(plot_me)
