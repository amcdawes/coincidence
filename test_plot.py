from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

fig = plt.figure()

x = [1,2,3,4,5]
y = [0.5,1.0,0.2,0.5,0.3] # set these to be less silly ranges.

data = np.column_stack([np.linspace(0, yi, 50) for yi in y])

rects = plt.bar(x, y, color='c')
plt.ylim(0, max(y))
def animate(i):
    # get data from serial
    newdata = np.random.random(5)
    for rect, yi in zip(rects, newdata):
        rect.set_height(yi)
    return rects

# TODO: tune interval with actual hardware.
anim = animation.FuncAnimation(fig, animate, blit=True, interval=100)
plt.show()
