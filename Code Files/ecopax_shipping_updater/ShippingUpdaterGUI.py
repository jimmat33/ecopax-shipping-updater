import tkinter as tk
from tkinter import *
import os
 
class ShippingUpdaterGUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ecopax Shipping Updater")
        self.root.geometry('800x600')
        self.root.resizable(False, False)
        img = tk.PhotoImage(file= (os.path.abspath('gui_icon.png')))
        self.root.tk.call('wm', 'iconphoto', self.root._w, img)

    def run_gui(self):
        self.init_widgits()
        self.root.mainloop()


    def init_widgits(self):
        pass



