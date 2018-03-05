import numpy as np
from matplotlib.widgets import Button
import sys
import serial
import struct
import array
#from bitstring import BitArray
import matplotlib.pyplot as plt
import time

scale1 = 1000
scale2 = 1000

plt.ion()
fig = plt.figure()

index = np.arange(4)
bar_width = 0.4

axes = fig.add_subplot(121)
axes2 = fig.add_subplot(122)

# axes.set_xticks(("A", "B", "A'", "B'"))
# axes2.set_xticks(("C4", "C5", "C6", "C7"))
# axes.set_autoscale_on(True)
# axes.autoscale_view(True,True,True)
# axes2.set_autoscale_on(True)
# axes2.autoscale_view(True,True,True)
# axes.set_ylim([0,scale1])
# axes2.set_ylim([0,scale2])

dataset = (1,1,1,1)
dataset2 = (1,1,1,1)


rects = axes.bar(index,dataset,bar_width)
rects2 = axes2.bar(index,dataset2,bar_width)


#s = serial.Serial("/dev/ttyS0",19200,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE)
s = serial.Serial("/dev/ttyACM1",250000,timeout=2)

buffer = []
s.flushInput()
while True:
    try:
        s.write("c\n".encode())
        data = s.readline()
        if data: # TODO do I need to do this?
            #bits = BitArray(bytes=buffer)
            # test length:
            if True:
                #time.sleep(0.1)
                a, b, c, d, c4, c5, c6, c7, err = data.decode('ascii').rstrip().split(' ') # TODO parse as ints
                # print(a, b, c, d, c4, c5, c6, c7)
                newdata = (a, b, c, d)
                newdata = map(int,newdata)
                newdata2 = (c4, c5, c6, c7)
                newdata2 = map(int,newdata2)
                for rect, h in zip(rects, newdata):
                    rect.set_height(h)

                for rect2, h in zip(rects2, newdata2):
                    rect2.set_height(h)

                if int(a) > scale1 or  int(b) > scale1:
                    scale1 = 1.2*max(int(a),int(b))
                    axes.set_ylim([0,scale1])
                elif int(a) < (scale1/2) and int(b) < (scale1/2):
                    scale1 = 1.2*max(int(a),int(b))
                    axes.set_ylim([0,scale1])
                if int(c4) > scale2 or int(c5) > scale2:
                    scale2 = 1.2*max(int(c4),int(c5))
                    axes2.set_ylim([0,scale2])
                elif int(c4) < (scale2/2) or int(c5) < scale2:
                    scale2 = 1.2*max(int(c4),int(c5))
                    axes2.set_ylim([0,scale2])
                # axes.relim()
                # axes.autoscale_view(True,True,True)
                # axes2.relim()
                # axes2.autoscale_view(True,True,True)

                plt.pause(0.001)
                plt.draw()
            else:
                print("short packet")
            buffer = []
            s.flushInput()
        else:
            buffer.append(data)
    except KeyboardInterrupt:
        print("W: interrupt received, ending data collection")
        s.close()
        break
