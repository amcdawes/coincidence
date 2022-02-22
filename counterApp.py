# from example here: https://stackoverflow.com/questions/69597448/embedding-matplotlib-graph-on-tkinter-gui
# a tkinter app with live data

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import serial as sr
import numpy as np

from tkinter import *
from counter import CoincidenceCounter
from countPlotter import countFig

cc = CoincidenceCounter()

data = []

def start_plot():
    cc.update_data()
    data = cc.a
    data2 = cc.ab
    ax.clear() # this clears too much, gridlines and labels, tried del ax.lines but warning
    ax.plot(data, color="blue")
    canvas.draw_idle()
    ax2.clear()
    ax2.bar(x=cc.singleLabels, height=cc.singles, color="red")
    canvas2.draw_idle()
    ax4.clear()
    ax4.bar(x=cc.coincLabels, height=cc.coinc, color="orange")
    canvas4.draw_idle()
    main_window.after(100, start_plot) # in milliseconds, 1000 for 1 second

main_window = Tk()
main_window.configure(background='grey')
main_window.iconbitmap('lardmon_icon.ico')
main_window.title("Coincidence")
main_window.geometry('1300x800')
main_window.resizable(width=False, height=False)

plotting_frame = LabelFrame(main_window, text='Real Time', bg='white', width=300, height=700, bd=0)
controls_frame = LabelFrame(main_window, text='Controls', background='light grey', height=100, bd=0)

controls_frame.pack(fill='both', expand='1', side=TOP, padx=20, pady=10)
plotting_frame.pack(fill='both', expand='yes', side=BOTTOM, padx=20)

start_button = Button(controls_frame, text='Start Monitoring', width=16, height=2, borderwidth=1, command=start_plot)
start_button.pack(side=LEFT, padx=26)

exit_button = Button(controls_frame, text='Close', width=10, height=2, borderwidth=1, command=main_window.destroy)
exit_button.pack(side=RIGHT, padx=26)


fig, ax = countFig()
canvas = FigureCanvasTkAgg(fig, master=plotting_frame)
canvas.get_tk_widget().place(x = 0, y = 0, width = 600, height = 200)
canvas.draw()

fig2, ax2 = countFig()
canvas2 = FigureCanvasTkAgg(fig2, master=plotting_frame)
canvas2.get_tk_widget().place(x = 0, y = 200, width = 600, height = 400)
canvas2.draw()

fig3, ax3 = countFig()
canvas3 = FigureCanvasTkAgg(fig3, master=plotting_frame)
canvas3.get_tk_widget().place(x = 600, y = 0, width = 600, height = 200)
canvas3.draw()

fig4, ax4 = countFig()
canvas4 = FigureCanvasTkAgg(fig4, master=plotting_frame)
canvas4.get_tk_widget().place(x = 600, y = 200, width = 600, height = 400)
canvas4.draw()

main_window.mainloop()
