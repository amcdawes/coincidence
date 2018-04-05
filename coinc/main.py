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
import serial.tools.list_ports

useSerial = False
# To debug away from the device. True connects for real, False uses fake data

if useSerial:
    # Use serial tools to find the port for the coincidence counter
    EJAdevices = list(serial.tools.list_ports.grep("04b4:f232"))
    portstring = EJAdevices[0][0]
    #print(portstring)
    s = serial.Serial(portstring,250000,timeout=2)

# Set up data
channels = ["A","B","B'","C"]
coinc = ["AB","AB'","NA","ABB'"]
counts = [0,0,0,0]
source = ColumnDataSource(data=dict(x=channels, y=counts))
source2 = ColumnDataSource(data=dict(x=coinc, y=counts))

a = []
b = []
ab = []
abp = []
abbp = []

# Set up plot
plot = figure(plot_height=400, plot_width=1000, title="Single counts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=channels, y_range=[0, 70000])

plot.background_fill_color = "black"
plot.border_fill_color = "black"

plot.vbar(x='x', top='y', width=0.5, source=source, color="red")

plot2 = figure(plot_height=400, plot_width=1000, title="Coincidence counts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=coinc, y_range=[0, 4000])

plot2.background_fill_color = "black"
plot2.border_fill_color = "black"

plot2.vbar(x='x', top='y', width=0.5, source=source2, color="yellow")


# Set up widgets to control scale of plots
# TODO change these to actual range sliders
command = TextInput(title="Command Entry:", value='raw counts')
scalemin = Slider(title="Singles Scale minimum", value=0.0, start=0.0, end=1000.0, step=100)
scalemax = Slider(title="Singles Scale maximum", value=70000.0, start=1000.0, end=500000.0, step=100)
scalemin2 = Slider(title="Coinc. Scale minimum", value=0.0, start=0.0, end=5000.0, step=100)
scalemax2 = Slider(title="Coinc. Scale maximum", value=4000.0, start=1000.0, end=100000.0, step=100)
phase = Slider(title="phase", value=0.0, start=0.0, end=5.0, step=0.1)
points = Slider(title="data points", value=20, start=0, end=500, step=1)
statsA = Paragraph(text="100", width=400, height=40)
statsB = Paragraph(text="100", width=400, height=40)
g2 = Paragraph(text="100", width=400, height=40)
g2_2d = Paragraph(text="100", width=400, height=40)


# Set up callbacks
def send_command(attrname, old, new):
    #TODO turn into a raw command area for sending any device command
    plot.title.text = command.value

command.on_change('value', send_command)

last_time = time.time()

datapoints = 20

def update_data():
    # TODO: store data in a stream for charting vs time

    global last_time
    T = time.time() - last_time
    last_time = time.time()
    #print(T)

    # get data:
    if useSerial:
        s.write("c\n".encode())
        serialData = s.readline()
        data = [int(x) for x in serialData.decode('ascii').rstrip().split(' ')]
        #print(data)
    else:
        mockdata = [57000,27000,27000,100,3000,3000,10,60,0]
        data = [(1 + 0.1*random.rand())*x for x in mockdata]

    raw = data[0:4]
    coinc = data[4:8]
    err = data[8]

    a.append(raw[0])
    b.append(raw[1])
    ab.append(coinc[0])
    abp.append(coinc[1])
    abbp.append(coinc[3])

    while len(a) > datapoints: a.pop(0)
    while len(b) > datapoints: b.pop(0)
    while len(ab) > datapoints: ab.pop(0)
    while len(abp) > datapoints: abp.pop(0)
    while len(abbp) > datapoints: abbp.pop(0)
    #print(a)

    statsA.text = "A: %d +/- %d" % (np.mean(a), np.std(a))
    statsB.text = "B: %d +/- %d" % (np.mean(b), np.std(b))
    try:
        g2value = (np.sum(a)*np.sum(abbp)) / (np.sum(ab) * np.sum(abp))
        g2dev = g2value * np.sqrt((np.std(a) / np.mean(a))**2 +
                            (np.std(abbp) / np.mean(abbp))**2 +
                            (np.std(ab) / np.mean(ab))**2 +
                            (np.std(abp) / np.mean(abp))**2)
    except ValueError:
        print("value error calculating g2")
        g2value = 0
    try:
        g2.text = "g(2) = %3.2f +/- %4.3f" % ( g2value, g2dev )
    except ValueError:
        print("value error printing g2")
        g2.text = "g(2) = NaN"

    try:
        g2_2d_value = (np.sum(bbp)*np.sum(abbp)) / (np.sum(ab) * np.sum(abp))
        g2_2d_dev = g2value * np.sqrt((np.std(a) / np.mean(a))**2 +
                            (np.std(abbp) / np.mean(abbp))**2 +
                            (np.std(ab) / np.mean(ab))**2 +
                            (np.std(abp) / np.mean(abp))**2)
    except ValueError:
        print("value error calculating g2")
        g2value = 0
    try:
        g2.text = "g(2) = %3.2f +/- %4.3f" % ( g2value, g2dev )
    except ValueError:
        print("value error printing g2")
        g2.text = "g(2) = NaN"

    #print(raw)
    plot.title.text = "A:%d B:%d" % (raw[0], raw[1])
    # Get the current slider values
    # a = scalemax.value
    # b = scalemin.value
    # w = phase.value
    # k = freq.value

    # Generate the new curve
    channels = ["A","B","B'","C"]
    chan2 = ["AB","AB'","NA","ABB'"]

    source.data = dict(x=channels, y=raw)
    source2.data = dict(x=chan2, y=coinc)

def update_scales(attrname, old, new):
    global datapoints
    # Get the current slider values
    smin = scalemin.value
    smax = scalemax.value
    s2max = scalemax2.value
    s2min = scalemin2.value
    w = phase.value
    datapoints = points.value

    #update()

    plot.y_range.start = smin
    plot.y_range.end = smax
    plot2.y_range.start = s2min
    plot2.y_range.end = s2max

for w in [scalemin, scalemax, scalemin2, scalemax2, points]:
    w.on_change('value', update_scales)


# Set up layouts and add to document
countControls = widgetbox(command, scalemin, scalemax)
coincControls = widgetbox(scalemin2,scalemax2)

curdoc().add_root(row(countControls, plot, column(statsA, statsB, g2, points), width=1800))
curdoc().add_root(row(coincControls, plot2, width=1800))
curdoc().title = "Coincidence"
curdoc().add_periodic_callback(update_data, 100)
