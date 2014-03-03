import serial
import struct
import array
from bitstring import BitArray
import matplotlib.pyplot as plt
import time

fig=plt.figure()
plt.axis([0,10,0,50000])

s = serial.Serial("COM1",19200,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE)

buffer = []
while True:
    try:
        data = s.read()
        if data == "\x7f":
            bits = BitArray(bytes=buffer)
	    # test length:
	    if bits.length == 8*40:
		time.sleep(0.1)
            	a, b, c, d, c4, c5, c6, c7 = bits.unpack('uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40,uintle:40')
		print a, b, c, d, c4, c5, c6, c7
		plt.scatter((a,b,c,d,c4,c5,c6,c7),(0,1,2,3,4,5,6,7))
		plt.draw()
            else:
                print "short packet"
            buffer = []
        else:
            buffer.append(data)
    except KeyboardInterrupt:
        print "W: interrupt received, ending data collection"
        break

s.close()
