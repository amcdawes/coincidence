'''
A module for controlling the Eric Ayars coincidence counter
'''

import numpy as np
import numpy.random as random
import time
import serial
import serial.tools.list_ports

class CoincidenceCounter(object):
    # Set up data variables and names
    singleLabels = ["A","B","B'","C"]
    coincLabels = ["AB","AB'","NA","ABB'"]
    counts = [0,0,0,0]

    # these lists will be filled with the raw data
    a = []
    b = []
    ab = []
    abp = []
    abbp = []
    bbp = []

    last_time = time.time()

    # start out keeping 20 data points (2 seconds worth)
    datapoints = 20

    def __init__(self):
        """Try to connect to  the device.
        If not found, generate fake data.
        """
        self.last_time = time.time()
        try:
            # Use serial tools to find the port for the coincidence counter
            # this is based on the information for my device, I hope it's true in general
            # there is a small chance this will find something else on your usb bus too
            # but only if you have another device using the same UID/VID.
            EJAdevices = list(serial.tools.list_ports.grep("04b4:f232"))
            if len(EJAdevices) > 0:
                portstring = EJAdevices[0][0]
                print(portstring)
                self._ser = serial.Serial(portstring,250000,timeout=2)
                self.useSerial = True
                print("Using real data")
        except Exception as e:
            print(e)
        else:
            self.useSerial = False
            print("Using fake data")

    def __del__(self):
        if (self.useSerial):
            self._ser.close()

    def update_data(self):
        # TODO: store data in a stream for charting vs time
        # this function is called every 100 ms (set below if you want to change it)

        # keep track of time interval for accurate counting calculations
        # TODO how to do this inside a class?
        T = time.time() - self.last_time
        self.last_time = time.time()
        #print(T)

        # get data via serial (or fake):
        if self.useSerial:
            self._ser.write("c\n".encode())
            serialData = self._ser.readline()
            data = [int(x) for x in serialData.decode('ascii').rstrip().split(' ')]
            #print(data)
        else:
            mockdata = [57000,27000,27000,100,3000,3000,10,60,0]
            data = [(1 + 0.1*random.rand())*x for x in mockdata]

        self.singles = data[0:4]
        self.coinc = data[4:8]
        self.err = data[8]

        # populate the lists
        self.a.append(self.singles[0])
        self.b.append(self.singles[1])
        self.ab.append(self.coinc[0])
        self.abp.append(self.coinc[1])
        self.abbp.append(self.coinc[3])
        self.bbp.append(self.coinc[2]) # TODO fix the settings on coinc unit

        # resize this lists to keep only datapoints
        # TODO use a better data structure for this!
        while len(self.a) > self.datapoints: self.a.pop(0)
        while len(self.b) > self.datapoints: self.b.pop(0)
        while len(self.ab) > self.datapoints: self.ab.pop(0)
        while len(self.abp) > self.datapoints: self.abp.pop(0)
        while len(self.abbp) > self.datapoints: self.abbp.pop(0)
        while len(self.bbp) > self.datapoints: self.bbp.pop(0)
        #print(a)
