import socket
import time
import threading as th
import json
import os
import matplotlib.pyplot as plt
from drawnow import *


plot_data = {}
data_arr = []
thread_list = []
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

data_dict = {}


def define_axis():
    global fig

    axis = []
    size = len(data_dict)
    for i in range(size*4):
        axis.append(fig.add_subplot(size,4,i+1))

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


def  plot_me():
    axes = define_axis()
    a_m = -4
    a_c = -3
    a_i = -2
    a_e = -1
    for k in plot_data:
        a_m += 4
        a_c += 4
        a_i += 4
        a_e += 4
        plotter(ax=axes[a_m], data=plot_data[k]['mem'], key=k, name='Memory', col='m')
        plotter(ax=axes[a_c], data=plot_data[k]['cpu'], key=k, name='CPU', col='c')
        plotter(ax=axes[a_i], data=plot_data[k]['net_i'], key=k, name='NetI', col='g')
        plotter(ax=axes[a_e], data=plot_data[k]['net_e'], key=k, name='NetE', col='r')
    fig.suptitle('ShellMon Experiment')


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
