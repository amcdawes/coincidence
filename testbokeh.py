'''
A bokeh-based interface for Eric Ayars coincidence counter
First-draft attempt at controls, graphs and values.
'''
import numpy as np

import numpy.random as random

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


import serial

useSerial = False

if useSerial:
    s = serial.Serial("/dev/ttyACM1",250000,timeout=2)

# Set up data
channels = ["A","B","A'","B'"]
counts = [0,0,0,0]
source = ColumnDataSource(data=dict(x=channels, y=counts))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="raw counts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=channels, y_range=[0, 100000])

plot.vbar(x='x', top='y', width=0.5, source=source)

#plot.bars('x', 'y', source=source, line_width=3, line_alpha=0.6)
# plot = Bar(data, values='y', label='interpreter', stack='sample', agg='mean',
#           title="Raw counts", legend='top_right', plot_width=400, plot_height=400)

# Set up widgets
text = TextInput(title="title", value='raw counts')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update():

    # get data:
    if useSerial:
        s.write("c\n".encode())
        serialData = s.readline()
        data = [int(x) for x in data.decode('ascii').rstrip().split(' ')]
    else:
        mockdata = [80000,75043,1000,800,20,20,0,0,0]
        data = [random.rand()*x for x in mockdata]

    raw = data[0:4]
    coinc = data[4:8]
    err = data[8]

    # Generate the new curve
    x = ["A","B","A'","B'"]
    y = raw

    source.data = dict(x=x, y=y)

def update_data(attrname, old, new):

    # get data:
    if useSerial:
        s.write("c\n".encode())
        serialData = s.readline()
        data = [int(x) for x in data.decode('ascii').rstrip().split(' ')]
    else:
        mockdata = [80000,75043,1000,800,20,20,0,0,0]
        data = [random.rand()*x for x in mockdata]

    raw = data[0:4]
    coinc = data[4:8]
    err = data[8]

    print(raw)

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = ["A","B","A'","B'"]
    y = raw

    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
curdoc().add_periodic_callback(update, 100)
