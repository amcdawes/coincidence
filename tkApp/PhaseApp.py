# from example here: https://stackoverflow.com/questions/69597448/embedding-matplotlib-graph-on-tkinter-gui
# a tkinter app with live data

import serial
import numpy as np

from tkinter import *

class phaseController():
    position = 0
    pcSer = serial.Serial("/dev/ttyS0",baudrate=19200,xonxoff=True,rtscts=True,timeout=1)

    def get_position(self):
        # get the current position from the controller
        print("get pos")
        pcSer.write("1PA?".encode())
        answer = pcSer.readline()
        print(answer)
        updatePhaseText(self.position)
        
    def plus_position(self):
        # move forward 10 units
        print("plus")
        self.position+=20
        pcSer.write("1PR20".encode())
        answer = pcSer.readline()
        print(answer)
        updatePhaseText(self.position)

    def minus_position(self):
        # move backward 10 units
        print("minus")
        self.position-=10
        pcSer.write("1PR-20".encode())
        answer = pcSer.readline()
        print(answer)        
        updatePhaseText(self.position)

def updatePhaseText(text):
    phaseDisplay.delete(1.0,"end")
    phaseDisplay.insert(1.0, text)

pc = phaseController()

main_window = Tk()
main_window.configure(background='grey')
main_window.iconbitmap('lardmon_icon.ico')
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

main_window.mainloop()
