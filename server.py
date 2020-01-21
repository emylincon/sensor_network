import socket
import time
from threading import Thread
import os
import matplotlib.pyplot as plt
from drawnow import *
import paho.mqtt.client as mqtt


fig = plt.figure()
data_dict = {}     # {temp_server:{Temperature:[], Memory:[], CPU:[], x_list: []}, humidity_server:{Humidity:[], Memory:[], CPU:[], x_list: []}}
window = 9
style = ['g--^', 'r--', 'b-.s']


def window_check():
    data_length = len(data_dict)
    for i in range(data_length):
        first = list(data_dict.values())[i]
        d_ = list(first.values())[0]
        if len(d_) > window:
            dict_key = list(data_dict.keys())[i]
            for data in data_dict[dict_key]:
                data_dict[dict_key][data].pop(0)
                #data.pop(0)
                print('length: ', len(data_dict[dict_key][data]))


def start_up():
    global username, password, broker_ip, topic, broker_port_no
    os.system('clear')
    print('-----------------------------------')
    print('Welcome to MQTT Subscriber client')
    print('-----------------------------------')

    username = 'admin'
    password = 'password'
    broker_ip = input("Broker's IP: ").strip()
    broker_port_no = 1883
    topic = 'iot/#'
    print('-----------------------------------')



# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    data = str(msg.payload, 'utf-8').split()
    print('received: ', data)
    #print(data_dict)
    topic_recv = msg.topic.split('/')[1]
    #data format = 'title sensor_data memory_util cpu_util'
    if topic_recv not in data_dict:
        data_dict[topic_recv] = {data[0]: [float(data[1])], 'Memory': [float(data[2])], 'CPU': [float(data[3])], 'x_list': [1]}
    else:
        keys = [data[0], 'Memory', 'CPU']
        for i in range(3):
            data_dict[topic_recv][keys[i]].append(float(data[i+1]))
        last = data_dict[topic_recv]['x_list'][-1]
        data_dict[topic_recv]['x_list'].append(last+1)
        for i in data_dict[topic_recv]:
            if len(data_dict[topic_recv][i]) > window:
                data_dict[topic_recv][i].pop(0)
                #print('len: ', len(data_dict[topic_recv][i]))


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
        for i in range(len(hold_ax)):
            hold_ax[i] += 3
        h = 0
        for data_set in data_dict[topic_]:
            x_list = data_dict[topic_]['x_list']
            if data_set != 'x_list':
                #print('axis: ', hold_ax[h])
                plotter(ax=axes[hold_ax[h]], data=data_dict[topic_][data_set], key=topic_, name=data_set, col=style[h], x_axis=x_list)
                h+=1

    fig.suptitle('IoT Sensor Network Smart City')
    #print('here: ', data_dict)


def plotter(ax, data, key, name, col, x_axis):
    ax.grid(True)

    ax.plot(x_axis, _mov_avg(data), col, linewidth=2, label='{}'.format(name))
    #ax.set_ylabel('Moving {}'.format(name))
    ax.set_xlabel('Time (seconds)')
    if name == 'Memory':
        ax.fill_between(x_axis, _mov_avg(data), 0, alpha=0.5, color='r')
        ax.set_ylim(top=2)
    if name == 'CPU':
        ax.set_ylim(top=30)
    if (name != "Memory") and (name != "CPU"):
        ax.set_ylabel('{}'.format(key.replace('_', ' ')), rotation=0, fontsize=10, labelpad=40)
        ax.set_ylim(top=30)
    ax.legend()
    #print('plot')
    plt.subplots_adjust(left=0.2)
    plt.subplot(ax)


def show_graphs():
    drawnow(plot_me)


def main():
    start_up()
    h1 = Thread(target=broker_loop)
    h1.start()
    a = 1
    #print('okay now')
    while True:
        if len(data_dict) == 0:
            if a == 1:
                print('Waiting for Data')
                a = 0
        else:
            #if len(data_dict) > 0:
            #    window_check()
            show_graphs()
            #print('here')
        time.sleep(1)


if __name__ == '__main__':
    main()
