import RPi.GPIO as GPIO
import dht11
import time
from matplotlib import pyplot as plt

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()

# read data using Pin GPIO21
instance = dht11.DHT11(pin=21)

temp = []
hum = []


def main():
    global temp
    global hum
    result = instance.read()
    if result.is_valid():
        print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)
    temp.append(result.temperature), hum.append(result.humidity)
    time.sleep(1)


def plot_normal_graph():
    global temp
    fig1 = plt.figure('Temperature Readings in Celsius')

    fig1 = plt.clf()
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot([x for x in temp if x != 0], linewidth=5, label='Temp C')
    fig1 = plt.plot(calculate_mov_avg(temp), linewidth=5, label='Moving Temp')
    fig1 = plt.title('Temperature graph')
    fig1 = plt.ylabel('Temperature')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)

    # plt.show()


def calculate_mov_avg(a1):
    ma1 = []  # moving average list
    avg1 = 0  # moving average point-wise
    count = 0
    for i in range(len(a1)):
        count += 1
        avg1 = ((count-1)*avg1+a1[i])/count
        ma1.append(avg1)  # cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def plot_moving_graph():
    global hum
    fig1 = plt.figure('Humidity Graph')

    fig1 = plt.clf()
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot([x for x in hum if x != 0], linewidth=5, label='Humidity in percent')
    fig1 = plt.plot(calculate_mov_avg(hum), linewidth=5, label='Moving Hum')
    fig1 = plt.title('Moving Average Humidity graph')
    fig1 = plt.ylabel('Humidity')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)


def plot_graphs():
    while True:
        main()
        plot_normal_graph()
        plot_moving_graph()
        plt.show()


plot_graphs()