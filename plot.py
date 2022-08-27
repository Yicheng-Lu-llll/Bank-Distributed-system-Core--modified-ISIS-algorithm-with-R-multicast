import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import MaxNLocator

num_node = 3
scenario = 1
bandwidths = []     # bandwidth of each node, unit: bps
times = []      # average time for processing a message of each node unit: ms

path = './plots/scenario%s' % scenario
if not os.path.exists(path):
    os.mkdir(path)

for i in range(1, num_node + 1):
    filename = "./stats/scenarios%s/node%s_stats.csv" % (scenario, i)
    stats = np.array(pd.read_csv(filename))
    if not len(stats):
        raise ValueError("None csv data!")

    messages = np.array(stats[:, 0])
    num_message = len(messages)
    receive_time = np.array(stats[:, 1], dtype='float')
    process_time = np.array(stats[:, 2], dtype='float')
    total_bytes = np.array(stats[:, 3], dtype='int')

    # calculate average time for processing a message after receiving
    total_time_diff = np.sum(process_time - receive_time)
    average_time = total_time_diff / num_message * 1000
    # calculate bandwidth
    bandwidth = 8 * (total_bytes[-1] - total_bytes[0]) / (process_time[-1] - process_time[0])

    times.append(average_time)
    bandwidths.append(bandwidth)


fig1 = plt.figure()
plt.plot(range(1, num_node + 1), times)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.title("Average Delay")
plt.xlabel("node")
plt.ylabel("delay per message [msec]")
fig1.savefig('./plots/scenario%s/delay.png' % scenario, dpi=fig1.dpi)
plt.show()

fig2 = plt.figure()
plt.plot(range(1, num_node + 1), bandwidths)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.title("Bandwidth")
plt.xlabel("node")
plt.ylabel("bandwidth [bps]")
fig2.savefig('./plots/scenario%s/bandwidth.png' % scenario, dpi=fig2.dpi)
plt.show()
