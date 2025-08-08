import RPi.GPIO as gg
import time
from time import sleep

gg.setwarnings(False)
import matplotlib.pyplot as plt
import numpy as np


def find_defect_position(graph1, graph2, threshold, time):
    graph1 = np.array(graph1)
    graph2 = np.array(graph2)
    g1copy = {}
    g3 = graph1[::-1]
    t3 = time[::-1]
    for i in range(len(graph1)):
        if len(str(graph1[i])) < 13:
            g1copy["start"] = [graph1[i], time[i]]
            break
    for i in range(len(g3)):
        if len(str(g3[i])) < 13:
            g1copy["end"] = [g3[i], t3[i]]
            break
    diff = np.abs(graph1 - graph2)
    defect_positions = np.where(diff > threshold)[0]
    print(defect_positions)
    print()
    print("The Defect positions in graph:")
    dp = []
    tp = [0]
    for i in defect_positions:
        if graph1[i] < 200:
            dp.append(graph1[i])
            tp.append(abs(time[i] - time[-1]))
    plt.plot(graph1)
    plt.plot(graph2)
    plt.plot(defect_positions, graph1[defect_positions], 'r.', label='Defect Positions')
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.ylim(0, 200)
    light(dp)
    plt.show()
    tp.pop(0)
    return dp, tp, g1copy


def light(l):
    gg.setmode(gg.BCM)
    gg.setwarnings(False)
    gg.setup(4, gg.OUT)
    gg.setup(24, gg.OUT)
    if l != [] or l == [0]:
        for i in range(5):
            gg.output(4, gg.HIGH)
            sleep(1)
            gg.output(4, gg.LOW)
            sleep(1)

    else:
        for i in range(5):
            gg.output(24, gg.HIGH)
            sleep(1)
            gg.output(24, gg.LOW)
            sleep(1)


def chkdist():
    start = 0
    end = 0
    e = 17
    t = 27
    gg.setmode(gg.BCM)
    gg.setup(t, gg.OUT)
    gg.setup(e, gg.IN)
    gg.output(t, False)
    time.sleep(0.2)
    gg.output(t, True)
    time.sleep(0.00001)
    gg.output(t, False)
    while gg.input(e) == 0:
        start = time.time()
    while gg.input(e) == 1:
        end = time.time()
        d = (end - start) * 100000
        t = end
    return d, t


graph1 = []

while True:
    try:
        k = chkdist()
        print(k)
        graph1.append(k)
    except KeyboardInterrupt:
        break

g1 = []
g2 = []
t1 = []
for i in graph1:
    t1.append(i[1])
for i in graph1:
    g1.append(int(i[0]))

for i in g1:
    k = g1.count(i)
    g2.append(k)
p = max(g2)
for i in g1:
    if g1.count(i) == p:
        temp = i
graph2 = [temp]
print("temp=", temp)

s = find_defect_position(g1, graph2, threshold=0.5, time=t1)

print(s)
print()
import math as m

c = 0
ml1 = []
ml2 = []
for i in range(len(s[0])):
    try:
        y = m.dist(s[-1]["start"], [s[0][i], s[1][i]])
        k = (s[-1]['start'][-1] - y)
        c += k
        ml1.append((c + 7.8) / 2)
        ml2.append(k)
    except:
        pass
print("Defect Positions : ", ml1[:6])