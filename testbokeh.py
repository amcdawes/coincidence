'''
A bokeh-based interface for Eric Ayars coincidence counter
First-draft attempt at controls, graphs and values.
'''
import numpy as np

import numpy.random as random
import time
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput, Paragraph
from bokeh.plotting import figure


import serial

useSerial = False

if useSerial:
    # TODO automatic search for correct port:
    # make use of linux command: ls -l /dev/serial/by-id/*EJA*
    # which will link to the correct /dev/tty*
    s = serial.Serial("/dev/ttyACM2",250000,timeout=2)

# Set up data
channels = ["A","B","A'","B'"]
coinc = ["C1","C2","C3","C4"]
counts = [0,0,0,0]
source = ColumnDataSource(data=dict(x=channels, y=counts))
source2 = ColumnDataSource(data=dict(x=coinc, y=counts))

a = []
b = []

# Set up plot
plot = figure(plot_height=400, plot_width=800, title="Single counts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=channels, y_range=[0, 100000])

plot.vbar(x='x', top='y', width=0.5, source=source)

plot2 = figure(plot_height=400, plot_width=800, title="Coincidence counts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=coinc, y_range=[0, 1000])

plot2.vbar(x='x', top='y', width=0.5, source=source2)

# Set up widgets
command = TextInput(title="Command Entry:", value='raw counts')
scalemin = Slider(title="Singles Scale minimum", value=0.0, start=0.0, end=1000.0, step=100)
scalemax = Slider(title="Singles Scale maximum", value=1000.0, start=1000.0, end=500000.0, step=100)
scalemin2 = Slider(title="Coinc. Scale minimum", value=0.0, start=0.0, end=5000.0, step=100)
scalemax2 = Slider(title="Coinc. Scale maximum", value=1000.0, start=1000.0, end=100000.0, step=100)
phase = Slider(title="phase", value=0.0, start=0.0, end=5.0, step=0.1)
statsA = Paragraph(text="100", width=100, height=20)
statsB = Paragraph(text="100", width=100, height=20)


# Set up callbacks
def send_command(attrname, old, new):
    #TODO turn into a raw command area?
    plot.title.text = command.value

command.on_change('value', send_command)

last_time = time.time()
def update_data():
    # TODO: store data in stream for charting vs time

    global last_time
    T = time.time() - last_time
    last_time = time.time()
    print(T)

    # get data:
    if useSerial:
        s.write("c\n".encode())
        serialData = s.readline()
        data = [int(x) for x in serialData.decode('ascii').rstrip().split(' ')]
    else:
        mockdata = [80000,75043,1000,800,20,20,0,0,0]
        data = [random.rand()*x for x in mockdata]

    raw = data[0:4]
    coinc = data[4:8]
    err = data[8]

    a.append(raw[0])
    b.append(raw[1])
    if len(a) > 10: a.pop(0)
    if len(b) > 10: b.pop(0)

    statsA.text = "A: %d +/- %d" % (np.mean(a), np.std(a))
    statsB.text = "B: %d +/- %d" % (np.mean(b), np.std(b))

    #print(raw)
    plot.title.text = "A:%d B:%d" % (raw[0], raw[1])
    # Get the current slider values
    # a = scalemax.value
    # b = scalemin.value
    # w = phase.value
    # k = freq.value

    # Generate the new curve
    channels = ["A","B","A'","B'"]
    chan2 = ["C1","C2","C3","C4"]

    source.data = dict(x=channels, y=raw)
    source2.data = dict(x=chan2, y=coinc)

def update_scales(attrname, old, new):

    # Get the current slider values
    smin = scalemin.value
    smax = scalemax.value
    s2max = scalemax2.value
    s2min = scalemin2.value
    w = phase.value

    #update()

    plot.y_range.start = smin
    plot.y_range.end = smax
    plot2.y_range.start = s2min
    plot2.y_range.end = s2max

for w in [scalemin, scalemax, scalemin2, scalemax2]:
    w.on_change('value', update_scales)


# Set up layouts and add to document
countControls = widgetbox(command, scalemin, scalemax)
coincControls = widgetbox(scalemin2,scalemax2)

curdoc().add_root(row(countControls, plot, column(statsA, statsB), width=1250))
curdoc().add_root(row(coincControls, plot2, width=1250))
curdoc().title = "Coincidence"
curdoc().add_periodic_callback(update_data, 100)
