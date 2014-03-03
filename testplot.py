from pylab import *
import numpy as np
import time

ion()
x = linspace(-1,1,51)
plot(sin(x))
for i in range(10):
    plot([sin(i+j) for j in x])
    # make it appear immediately
    draw()
    time.sleep(1)
