'''
A bokeh-based interface to collect photon interference data

Assumes a newport newstep controller is available for the
interferometer phase knob
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
# If the counter is not connected, you can set this to False in order to try it
# out, or edit the calculations etc.

if useSerial:
    # Use serial tools to find the port for the coincidence counter
    # this is based on the information for my device, I hope it's true in general
    # there is a small chance this will find something else on your usb bus too
    # but only if you have another device using the same UID/VID.
    EJAdevices = list(serial.tools.list_ports.grep("04b4:f232"))
    EJAportstring = EJAdevices[0][0]
    print("EJA at: ", EJAportstring)
    # we connect via a Prolific Technology, Inc. PL2303 Serial Port:
    NSdevices = list(serial.tools.list_ports.grep("067b:2303"))
    NSportstring = NSdevices[0][0]
    print("Found NewStep port at: ", NSportstring)
    s = serial.Serial(EJAportstring,250000,timeout=2)
    newstep = serial.Serial(NSportstring,baudrate=19200,xonxoff=True,rtscts=True,timeout=250)

# Set up data variables and names
phase = [] #np.arange(-50,50,100)
ABcounts = [] #np.zeros(len(phase))
deltaABcounts = []
ABPcounts = [] #np.zeros(len(phase))
deltaABPcounts = []

# create bokeh data sources for the two graphs
source = ColumnDataSource(data=dict(x=phase, y=ABcounts, d=deltaABcounts))
source2 = ColumnDataSource(data=dict(x=phase, y=ABPcounts, d=deltaABPcounts))

# these lists will be filled with the raw data
a = []
b = []
ab = []
abp = []
abbp = []
bbp = []
abcounts = []
abpcounts = []


# Set up plot
plot = figure(plot_height=400, plot_width=1000, title="Single counts",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.ygrid.grid_line_alpha = 0.3
plot.xgrid.grid_line_alpha = 0.3
plot.yaxis.axis_label = "AB Coincidence Counts"
plot.yaxis.axis_label_text_color = "white"
plot.yaxis.major_label_text_color = "white"
plot.yaxis.axis_label_text_color = "white"
plot.xaxis.major_label_text_color = "white"

# colors are dark for use in the dark optics labs
plot.background_fill_color = "MidnightBlue"
plot.border_fill_color = "MidnightBlue"

plot.scatter(x="x", y="y", radius="d",
          fill_color="green", fill_alpha=0.3,
          line_color="white", source=source)

plot2 = figure(plot_height=400, plot_width=1000, title="Coincidence counts",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot2.ygrid.grid_line_alpha = 0.3
plot2.xgrid.grid_line_alpha = 0.3
plot2.yaxis.axis_label = "AB' Coincidence Counts"
plot2.yaxis.axis_label_text_color = "white"
plot2.yaxis.major_label_text_color = "white"
plot2.xaxis.major_label_text_color = "white"

plot2.background_fill_color = "MidnightBlue"
plot2.border_fill_color = "MidnightBlue"

plot2.scatter(x="x", y="y", radius="d",
          fill_color="blue", fill_alpha=0.3,
          line_color="white", source=source2)


# Set up widgets to control scale of plots
# TODO change these to actual range sliders
command = TextInput(title="Command Entry:", value='raw counts')
scalemin = Slider(title="Singles Scale minimum", value=0.0, start=0.0, end=1000.0, step=100)
scalemax = Slider(title="Singles Scale maximum", value=70000.0, start=1000.0, end=500000.0, step=100)
scalemin2 = Slider(title="Coinc. Scale minimum", value=0.0, start=0.0, end=5000.0, step=100)
scalemax2 = Slider(title="Coinc. Scale maximum", value=4000.0, start=1000.0, end=100000.0, step=100)

# other widgets (not all are used yet)
setphase = Slider(title="phase", value=5000, start=4000, end=6000, step=100)
points = Slider(title="data points", value=20, start=0, end=500, step=1)
statsA = Paragraph(text="100", width=400, height=40)
statsB = Paragraph(text="100", width=400, height=40)
statsAB = Paragraph(text="100", width=400, height=40)
statsABP = Paragraph(text="100", width=400, height=40)
g2 = Paragraph(text="100", width=400, height=80)
g2_2d = Paragraph(text="100", width=400, height=40)


# Set up callbacks
def send_command(attrname, old, new):
    # not implemented yet
    # TODO turn into a raw command area for sending any device command
    plot.title.text = command.value

command.on_change('value', send_command)

last_time = time.time()

# start out keeping 20 data points
datapoints = 20

def set_phase(attrname, old, new):
    targetPhase = setphase.value
    print("stepper going to: ", targetPhase)
    if useSerial:
        phaseString = "1PA%d\r\n" % targetPhase
        print(phaseString)
        newstep.write(phaseString.encode()) # set the phase
        newstep.write("1PA?\r\n".encode()) # ask current phase
        # TODO this is going to break, the phase can't be negative
        phaseBytes = newstep.readline()
        # returns in the form: b'\r1PA? 46774\n'
        phaseString = phaseBytes.decode("utf-8")
        current_phase = int(phaseString.split(" ")[1])
    else:
        # assume phase from slider
        current_phase = setphase.value

def save_phase():
    # store current phase value and the mean/stdev
    # from latest run in new graph source
    # get current value from stepper:
    if useSerial:
        newstep.write("1PA?\r\n".encode())
        phaseBytes = newstep.readline()
        # returns in the form: b'\r1PA? 46774\n'
        phaseString = phaseBytes.decode("utf-8")
        current_phase = int(phaseString.split(" ")[1])
    else:
        # assume phase from slider
        current_phase = setphase.value
    abcounts.append(np.mean(ab))
    deltaABcounts.append(np.std(ab))
    #print(deltaABcounts)
    abpcounts.append(np.mean(abp))
    deltaABPcounts.append(np.std(ab))
    phase.append(current_phase)
    source.data = dict(x=phase, y=abcounts, d=deltaABcounts)
    source2.data = dict(x=phase, y=abpcounts, d=deltaABPcounts)

def update_data():
    # TODO: store data in a stream for charting vs time
    # this function is called every 100 ms (set below if you want to change it)

    # keep track of time interval for accurate counting calculations
    global last_time
    T = time.time() - last_time
    last_time = time.time()
    #print(T)

    # get data via serial (or fake):
    if useSerial:
        s.write("c\n".encode())
        serialData = s.readline()
        data = [int(x) for x in serialData.decode('ascii').rstrip().split(' ')]
    else:
        mockdata = [57000,27000,27000,100,3000,3000,10,60,0]
        data = [(1 + 0.1*random.rand())*x for x in mockdata]

    raw = data[0:4]
    coinc = data[4:8]
    err = data[8]

    # populate the lists
    a.append(raw[0])
    b.append(raw[1])
    ab.append(coinc[0])
    abp.append(coinc[1])
    abbp.append(coinc[3])
    bbp.append(coinc[2]) # TODO fix the settings on coinc unit
    # resize this lists to keep only datapoints
    while len(a) > datapoints: a.pop(0)
    while len(b) > datapoints: b.pop(0)
    while len(ab) > datapoints: ab.pop(0)
    while len(abp) > datapoints: abp.pop(0)
    while len(abbp) > datapoints: abbp.pop(0)
    while len(bbp) > datapoints: bbp.pop(0)
    #print(a)

    # set the A and B count displays
    statsA.text = "A: %d +/- %d" % (np.mean(a), np.std(a))
    statsB.text = "B: %d +/- %d" % (np.mean(b), np.std(b))
    statsAB.text = "AB: %d +/- %d" % (np.mean(ab), np.std(ab))
    statsABP.text = "AB': %d +/- %d" % (np.mean(abp), np.std(abp))

    # calculate g(2):
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

    # calculate the 2-detector version (i.e. non-gated, classical light)
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
        g2.text = "g(2) = %3.2f +/- %4.3f (%2.2f st.devs)" % ( g2value, g2dev, (1-g2value)/g2dev )
    except ValueError:
        print("value error printing g2")
        g2.text = "g(2) = NaN"

    #print(raw)

    plot.title.text = "A:%d B:%d" % (raw[0], raw[1])


def update_scales(attrname, old, new):
    global datapoints

    # Get the current slider values
    smin = scalemin.value
    smax = scalemax.value
    s2max = scalemax2.value
    s2min = scalemin2.value
    #w = phase.value
    datapoints = points.value

    plot.y_range.start = smin
    plot.y_range.end = smax
    plot2.y_range.start = s2min
    plot2.y_range.end = s2max

# Add on_change listener to each widget that we're using:
for w in [scalemin, scalemax, scalemin2, scalemax2, points]:
    w.on_change('value', update_scales)

setphase.on_change('value', set_phase)

# Set up layouts and add to document
countControls = widgetbox(command, scalemin, scalemax)
coincControls = widgetbox(scalemin2,scalemax2)

# build the app document, this is just layout control and arranging the interface
curdoc().add_root(row(countControls, plot, column(statsA, statsB, g2, points, statsAB, statsABP, setphase), width=1800))
curdoc().add_root(row(coincControls, plot2, width=1800))
curdoc().title = "Coincidence"

# set the callback to pull the data every 100 ms:
curdoc().add_periodic_callback(update_data, 100)
# TODO add callback on button press to store ab and abp mean and stddev in new graph sources
curdoc().add_periodic_callback(save_phase, 1000)
