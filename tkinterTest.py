from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar

window = Toplevel()

window.title("Welcome to LikeGeeks app")
# window.withdraw()

# window.geometry('350x200')

    
def timeUpdate(*args):
    timeLable.configure(text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())

# load image
image = Image.open('.\pic.png')
photo = ImageTk.PhotoImage(image)
label = Label(window, image = photo)
label.image = photo
label.grid(column=0, row=0, rowspan=10)


#Top text
lbl = Label(window, text="Select Date")
lbl.grid(column=2, row=0)

#Set Calendar
cal = Calendar(window, selectmode = 'day', year = 2020, month = 7, day = 1)
cal.grid(column=1, row=1,columnspan=3)

#time picker
hourLabel =Label(window, text="Hour")
hourLabel.grid(column=1,row=2)
minuteLabel =Label(window, text="Minutes")
minuteLabel.grid(column=2,row=2)
minuteLabel =Label(window, text="AM/PM")
minuteLabel.grid(column=3,row=2)

hourVar = StringVar(window)
hourVar.set("01")
minuteVar = StringVar(window)
minuteVar.set("00")
ampmVar = StringVar(window)
ampmVar.set("AM")

hourPicker = OptionMenu(window, hourVar , '01','02','03','04','05','06','07','08','09','10','11','12')
hourPicker.grid(column=1,row=3)
minutePicker = OptionMenu(window, minuteVar , '00','30')
minutePicker.grid(column=2,row=3)
ampnPicker = OptionMenu(window, ampmVar , 'AM','PM')
ampnPicker.grid(column=3,row=3)

hourVar.trace("w",timeUpdate)
minuteVar.trace("w",timeUpdate)
ampmVar.trace("w",timeUpdate)

timeLable =Label(window, text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())
timeLable.grid(column=1,row=5,columnspan=3)

# Load button
btn = Button(window, text="Click Me")
btn.grid(column=2, row=6)

