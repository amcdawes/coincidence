import matplotlib.pyplot as plt
import time
import numpy as np
from matplotlib.widgets import Button
import sys

plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
axes.set_autoscale_on(True)
axes.autoscale_view(True,True,True)

dataset = (1,1,1,1,1,1,1,1)

index = np.arange(8)
bar_width = 0.3

rects = axes.bar(index,dataset,bar_width)
plt.xticks(index + bar_width/2.0, ("A", "B", "A'", "B'", "C4", "C5", "C6", "C7"))



while True:
    try:
        newdata = np.random.random(8)
        for rect, h in zip(rects, newdata):
            rect.set_height(h)

        axes.relim()
        axes.autoscale_view(True,True,True)
        plt.pause(0.001)
        plt.draw()
        time.sleep(0.05)
    except KeyboardInterrupt:
        print "Keyboard stop"
        break


