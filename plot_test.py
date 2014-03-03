from pylab import *

ion()
line, = plot((0,0,0,0,0,0,0,0))

for i in range(10):
	line.set_ydata((i,i,i,i,i,i,i,i))
	draw()
