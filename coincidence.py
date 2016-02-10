import serial
import struct
import array
from bitstring import BitArray
import time

s = serial.Serial("/dev/ttyUSB0",19200,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE)

buffer = []
s.flushInput()
while True:
    try:
        while s.read() != "\x7f":
            pass
        #bytesToRead = s.inWaiting()
        #if bytesToRead == 41:
        inbuffer = s.read(41)
        #print repr(inbuffer)
        bits = BitArray(bytes=inbuffer[:-1])
        a, b, c, d, c4, c5, c6, c7 = bits.unpack('uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40')
        print a, b, c, d, c4, c5, c6, c7
    except KeyboardInterrupt:
        print "W: interrupt received, ending data collection"
        s.close()
        break
