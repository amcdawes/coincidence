# from example here: https://stackoverflow.com/questions/69597448/embedding-matplotlib-graph-on-tkinter-gui
# a tkinter app with live data

import serial
import numpy as np

from tkinter import *

class phaseController():
    position = 0
    pcSer = serial.Serial("/dev/ttyS0",baudrate=19200,xonxoff=True,rtscts=True,timeout=0.1)

    def get_position(self):
        # get the current position from the controller
        print("get pos")
        self.pcSer.write("1PA?\r".encode())
        # read until return (interface sends \n\r so readline doesn't work)
        answer = self.pcSer.read_until(b'\r')
        # decode bytes to string, pull out value as int:
        try:
            self.position = int(answer.decode().split()[-1])
            print(self.position)
            updatePhaseText(self.position)
        except:
            print("error getting position")

    #TODO create a button and text field for this!
    def set_position(self,intposition):
        # send command to go to a specific absolute position
        print("setting position")
        commandString = "1PA" + str(intposition) + "\r"
        self.pcSer.write(commandString.encode())
        self.get_position()
        
    def plus_position(self):
        # move forward 10 units
        print("plus")
        #self.position+=20
        self.pcSer.write("1PR10\r".encode())
        answer = self.pcSer.read_until(b'\r')
        #print(answer)
        self.get_position()

    def minus_position(self):
        # move backward 10 units
        print("minus")
        #self.position-=10
        self.pcSer.write("1PR-10\r".encode())
        answer = self.pcSer.read_until(b'\r')
        self.get_position()

def updatePhaseText(text):
    phaseDisplay.delete(1.0,"end")
    phaseDisplay.insert(1.0, text)

pc = phaseController()

main_window = Tk()
main_window.configure(background='grey')
#main_window.iconbitmap('lardmon_icon.ico')
main_window.title("Phase Controller")
main_window.geometry('600x150')
main_window.resizable(width=False, height=False)

value_frame = LabelFrame(main_window, text='Phase reading', bg='white', height=20, bd=0)
value_frame.pack(fill='both', expand='yes', side=TOP, padx=20, pady=10)

controls_frame = LabelFrame(main_window, text='Controls', background='light grey', height=20, bd=0)
controls_frame.pack(fill='both', expand='yes', side=TOP, padx=20, pady=10)

phaseDisplay = Text(value_frame, height=2)
phaseDisplay.pack(side=LEFT, padx=5)

get_button = Button(controls_frame, text='Get position', width=10, height=2, borderwidth=1, command=pc.get_position)
get_button.pack(side=LEFT, padx=5)

plus_button = Button(controls_frame, text='+ position', width=10, height=2, borderwidth=1, command=pc.plus_position)
plus_button.pack(side=LEFT, padx=5)

minus_button = Button(controls_frame, text='- position', width=10, height=2, borderwidth=1, command=pc.minus_position)
minus_button.pack(side=LEFT, padx=5)

exit_button = Button(controls_frame, text='Close', width=10, height=2, borderwidth=1, command=main_window.destroy)
exit_button.pack(side=LEFT, padx=5)

phaseDisplay.insert(1.0, "123456")
pc.get_position()

main_window.mainloop()
