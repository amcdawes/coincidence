'''
A bokeh-based interface for Eric Ayars coincidence counter
First-draft attempt at controls, graphs and values.
'''
import numpy as np

import numpy.random as random

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


import serial

useSerial = True

if useSerial:
    s = serial.Serial("/dev/ttyACM1",250000,timeout=2)

# Set up data
channels = ["A","B","A'","B'"]
coinc = ["C1","C2","C3","C4"]
counts = [0,0,0,0]
source = ColumnDataSource(data=dict(x=channels, y=counts))
source2 = ColumnDataSource(data=dict(x=coinc, y=counts))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="raw counts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=channels, y_range=[0, 100000])

plot.vbar(x='x', top='y', width=0.5, source=source)

plot2 = figure(plot_height=400, plot_width=400, title="raw coinc",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=coinc, y_range=[0, 1000])

plot2.vbar(x='x', top='y', width=0.5, source=source2)

# Set up widgets
text = TextInput(title="Command Entry:", value='raw counts')
scalemin = Slider(title="Scale minimum", value=0.0, start=0.0, end=5000.0, step=100)
scalemax = Slider(title="Scale maximum", value=1000.0, start=1000.0, end=5500.0, step=100)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi, step=0.1)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
def update_title(attrname, old, new):
    #TODO turn into a raw command area?
    plot.title.text = text.value

text.on_change('value', update_title)

def update():
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

    print(raw)

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

def update_data(attrname, old, new):

    # Get the current slider values
    a = scalemax.value
    b = scalemin.value
    w = phase.value
    k = freq.value

    #update()

    plot2.y_range.start = b
    plot2.y_range.end = a

for w in [scalemin, scalemax, phase, freq]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, scalemin, scalemax, phase, freq)

curdoc().add_root(row(inputs, plot, plot2, width=1200))
curdoc().title = "Sliders"
curdoc().add_periodic_callback(update, 100)
