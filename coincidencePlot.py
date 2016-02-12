import numpy as np
from matplotlib.widgets import Button
import sys
import serial
import struct
import array
from bitstring import BitArray
import matplotlib.pyplot as plt
import time

scale1 = 1000
scale2 = 1000

plt.ion()
fig = plt.figure()
axes = fig.add_subplot(121)
axes2 = fig.add_subplot(122)
# axes.set_autoscale_on(True)
# axes.autoscale_view(True,True,True)
# axes2.set_autoscale_on(True)
# axes2.autoscale_view(True,True,True)
axes.set_ylim([0,scale1])
axes2.set_ylim([0,scale2])

dataset = (1,1,1,1)
dataset2 = (1,1,1,1)

index = np.arange(4)
bar_width = 0.3

rects = axes.bar(index,dataset,bar_width)
rects2 = axes2.bar(index,dataset2,bar_width)
plt.xticks(index + bar_width/2.0, ("A", "B", "A'", "B'", "C4", "C5", "C6", "C7"))


s = serial.Serial("/dev/ttyS0",19200,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE)
buffer = []
s.flushInput()
while True:
    try:
        data = s.read()
        if data == "\x7f":
            bits = BitArray(bytes=buffer)
            # test length:
            if bits.length == 8*40:
                #time.sleep(0.1)
                a, b, c, d, c4, c5, c6, c7 = bits.unpack('uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40')
                print a, b, c, d, c4, c5, c6, c7
                newdata = (a, b, c, d)
                newdata2 = (c4, c5, c6, c7)
                for rect, h in zip(rects, newdata):
                    rect.set_height(h)

                for rect2, h in zip(rects2, newdata2):
                    rect2.set_height(h)
                if a > scale1 or  b > scale1:
                    scale1 = 1.2*max(a,b)
                    axes.set_ylim([0,scale1])
                elif a < (scale1/2) and b < (scale1/2):
                    scale1 = 1.2*max(a,b)
                    axes.set_ylim([0,scale1])
                if c4 > scale2:
                    scale2 = c4*1.2
                    axes2.set_ylim([0,scale2])
                elif c4 < (scale2/2):
                    scale2 = c4*1.2
                    axes2.set_ylim([0,scale2])
                # axes.relim()
                # axes.autoscale_view(True,True,True)
                #
                # axes2.relim()
                # axes2.autoscale_view(True,True,True)

                plt.pause(0.001)
                plt.draw()
            else:
                print "short packet"
            buffer = []
            s.flushInput()
        else:
            buffer.append(data)
    except KeyboardInterrupt:
        print "W: interrupt received, ending data collection"
        s.close()
        break
