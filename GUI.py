#----------------------CAUTION------------------------
#How to use the method .pack() to place any Tk widget:

# - Wrong way:
#   myWidget = TkWidget(master=None).pack()

# - Correct way: 
#   myWidget = TkWidget(master=None)
#   myWidget.pack()
#------------------------------------------------------

from tkinter import *
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import irsdk
import time
# Choosing the pyplot style
plt.style.use('dark_background')
widgetsBackground = 'white'
labelsColor = 'black'

class iRacing(object):
	ir = irsdk.IRSDK()
	def __init__(self):
		self.ir_connected = False

	# here we check if we are connected to iracing
	# so we can retrieve some data
	def check_iracing(self):
		root.after(1000, self.check_iracing)

		if self.ir_connected and not (self.ir.is_initialized and self.ir.is_connected):
		    self.ir_connected = False
		    # we are shutting down ir library (clearing all internal variables)
		    self.ir.shutdown()
		    warMsgBox('irsdk disconnected')
		    root.after_cancel(self.id)
		elif not self.ir_connected and self.ir.startup() and self.ir.is_initialized and self.ir.is_connected:
		    self.ir_connected = True
		    infoMsgBox('irsdk connected')
		    self.loop()

	# our main loop, where we retrieve data
	# and do something useful with it
	def loop(self):
		# every amount of time (ms) defined on the
		# after function the loop is called
		# maximum you can use is 16.5ms
        # cause iracing updates data with 60 fps
		self.id = root.after(1000, self.loop)
		
	# retrieve live telemetry data
    # check here for list of available variables:
    # channels.txt
    # this is not full list, because some cars has additional
    # specific variables, like break bias, wings adjustment, etc
		print(self.ir['SessionTime'])
		
		
 
class Root(Tk):
	def __init__(self):
		super(Root, self).__init__()

		
		# Main window atributes
		self.title('Interface Telemetria')	
		self.minsize(640, 500)
		self.iconbitmap('Images\\ico.ico')
		self.state('normal')


		## FRAMES ##
		self.mainFrame = Frame(self,
							   width=1000,
							   height=1000, 
							   bg=widgetsBackground) # Main frame
		self.mainFrame.pack(fill=BOTH, expand=True, side=LEFT)

		self.comboWidgetFrame = ttk.Labelframe(self.mainFrame, # Combobox widget frame
											   text="Channels") 
		self.comboWidgetFrame.pack(side=LEFT, anchor=N) 


		# Adding the combobox widgets
		self.comboWidget1 = self.addComboWidget('Graph 1')
		self.comboWidget2 = self.addComboWidget('Graph 2')
		self.comboWidget3 = self.addComboWidget('Graph 3')
		self.comboWidget4 = self.addComboWidget('Graph 4')
		
		
	# Method that create the combobox widget
	def addComboWidget(self, name):
		frame = Frame(self.comboWidgetFrame, bg=widgetsBackground) 
		frame.pack(fill=BOTH, expand=True) # Comboboxes and label frame

		# Widget Label 
		label_name = Label(frame, text=name,
								  font='Arial 12 bold',
								  justify=LEFT,
								  anchor=W,
								  fg=labelsColor,
								  bg=widgetsBackground).pack(anchor=W, fill=BOTH)


		# Creating a combobox object 
		combo1 = ttk.Combobox(frame, state='readonly')
		combo1.pack(side=TOP, anchor=W)

		combo2 = ttk.Combobox(frame, state='readonly')
		combo2.pack(side=TOP, anchor=W)

		combo3 = ttk.Combobox(frame, state='readonly')
		combo3.pack(side=TOP, anchor=W)

		combo4 = ttk.Combobox(frame, state='readonly')
		combo4.pack(side=TOP, anchor=W)

	
	
	# For embedding the matplotlib widgets on the GUI
	# we have to create a canvas frame on the system 
	# backend and use the Figure() to place the subplots

	# in this block of code we are just creating 4 subplots
	# that gonna receive data later
	def subplots(self):
		self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(nrows=4,
												      ncols=1, 
												      sharex=True,
												      gridspec_kw={'hspace': 0.13})

		self.canvas = FigureCanvasTkAgg(self.fig, self.mainFrame)
		self.canvas.get_tk_widget().pack(fill=BOTH, expand=True, anchor=N)
	
	




# Message box popups
def infoMsgBox(text):
	from tkinter import messagebox
	messagebox.showinfo('iRacing Status', text)

def warMsgBox(text):
	from tkinter import messagebox
	messagebox.showwarning('Interface Telemetria', text)

def erorMsgBox(self):
	msg.showerror('Python Error Message Box', 'ERROR!!')


if __name__ == '__main__':
	# initializing iracing and root
	iracing = iRacing()
	root = Root()
	# check if we are connected to iracing
	iracing.check_iracing()
	# Tkinter mainloop
	root.mainloop()
