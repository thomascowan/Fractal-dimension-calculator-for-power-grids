# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:42:34 2022

- Add TKinter
- add bar to cycle through graphs
- add bar to cycle through times

- add bar to set to entire day

@author: Thomas
"""


import pandas as pd
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
# import time
from scipy.ndimage import gaussian_filter
from tkinter import Label, StringVar, IntVar, OptionMenu, Button, Checkbutton, Tk
from PIL import Image, ImageTk
from tkcalendar import Calendar
import pickle

from fractal_analysis_fxns import fractal_dimension_grayscale_DBC

df = {}
MW = {}
MVA = {}
dateTime = ["01-Jul-20","11:00:00 AM"]
LocationsDF = None
__name__ = "__main__"
# 0 for MW, 1 for MVA, anything else for both
SelectedData = 0
# Only loads 5 suburbs
subsetData = 0
#Print debug statements
DEBUG = 0
#only load data from 1 July 2020
quickLoad = 0
skip = 1
                        
def loadMWData(directory):
    global MW
    if os.path.exists("./Data/MW_Data.pkl"):
        print('### Loading previously loaded data')
        with open('./Data/MW_Data.pkl', 'rb') as f:
            MW = pickle.load(f)
    else:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
            if filename.endswith(".csv"): 
                df[filename] = pd.read_csv(os.path.join(directory,filename))
                for (idx, row) in enumerate(df[filename].iterrows()):
                    if filename not in MW:
                         MW[filename] = {}
                    if(quickLoad and row[1]['Date'] == '02-Jul-20'):
                       break
                    if row[1]['Date'] not in MW[filename]:
                         MW[filename][row[1]['Date']] = {}
                    MW[filename][row[1]["Date"]][row[1]["Time"]] = row[1]["MW"]
        print("\r" + str(len(os.listdir(directory))) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
        with open('./Data/MW_Data.pkl', 'wb') as f:
            pickle.dump(MW, f)

def createArray(directory):
    locationsDF = pd.read_csv(os.path.join(directory,"locations.csv"))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    locationCoords = [list(),list(),list()]
    uneditedLocationCoords = [list(),list()]
    counter = 0
    precisionValue = 4
    Subbox = ((-27.795713993519306, 153.29807187264893), (-26.998858301659403, 152.72594294487124))
    global loadSubbox
    print()
    for row in locationsDF.iterrows():
        ### Loading coordinates in as integer values basing precision of precisionValue variable
        if loadSubbox.get() == 1:
            if (row[1]["Longitude"] < Subbox[0][1] and row[1]["Longitude"] > Subbox[1][1] and row[1]["Latitude"] > Subbox[0][0] and row[1]["Latitude"] < Subbox[1][0]):
                counter+=1
                print("\r" + str(counter) + " / " + str(len(locationsDF)) + " Geo Locations loaded", end = '')
                uneditedLocationCoords[0].append(float(row[1]["Latitude"]))
                uneditedLocationCoords[1].append(float(row[1]["Longitude"]))
                
                latDotSpot = str(row[1]["Latitude"]).index('.')
                lonDotSpot = str(row[1]["Longitude"]).index('.')
                
                convertedLat = int(str(row[1]["Latitude"])[0:latDotSpot] + str(row[1]['Latitude'])[latDotSpot+1:latDotSpot+precisionValue])
                convertedLon = int(str(row[1]["Longitude"])[0:lonDotSpot] + str(row[1]['Longitude'])[lonDotSpot+1:lonDotSpot+precisionValue])
               
                locationCoords[0].append(row[1]["Location"])
                locationCoords[1].append(convertedLat)
                locationCoords[2].append(convertedLon)
        else:
            counter+=1
            print("\r" + str(counter) + " / " + str(len(locationsDF)) + " Geo Locations loaded", end = '')
            uneditedLocationCoords[0].append(float(row[1]["Latitude"]))
            uneditedLocationCoords[1].append(float(row[1]["Longitude"]))
            
            latDotSpot = str(row[1]["Latitude"]).index('.')
            lonDotSpot = str(row[1]["Longitude"]).index('.')
            
            convertedLat = int(str(row[1]["Latitude"])[0:latDotSpot] + str(row[1]['Latitude'])[latDotSpot+1:latDotSpot+precisionValue])
            convertedLon = int(str(row[1]["Longitude"])[0:lonDotSpot] + str(row[1]['Longitude'])[lonDotSpot+1:lonDotSpot+precisionValue])
           
            locationCoords[0].append(row[1]["Location"])
            locationCoords[1].append(convertedLat)
            locationCoords[2].append(convertedLon)
            
    print()

    ### Follow values are calculated to define size of array
    ### Array is brought closer to origin to help with defining array size without wasting space
    arrayWidth = int((max(locationCoords[1]) - min(locationCoords[1])) * 1.2)
    arrayHeight = int((max(locationCoords[2]) - min(locationCoords[2])) * 1.2)
    
    minHeight = min(locationCoords[1])
    minWidth = min(locationCoords[2])
    
    widthOffset = int(arrayWidth * 0.12)
    heightOffset = int(arrayHeight * 0.12)
    
    ### Moving coordinates to new location
    adjustedDisplayCoords = []
    for i in range(len(locationCoords[0])):
        adjustedDisplayCoords.append((locationCoords[0][i], locationCoords[1][i]-minHeight+heightOffset, locationCoords[2][i]-minWidth+widthOffset))

    global dateTime
    ### Create an empty array and then populate with data of a set datetime
    DisplayArray = np.zeros([arrayWidth + widthOffset*2,arrayHeight + heightOffset*2],dtype=np.float32())
    for l in adjustedDisplayCoords:
        DisplayArray[l[1]][l[2]] = MW[l[0]][dateTime[0]][dateTime[1]] + 1
    
    ### Apply Gaussian filter to 'blur' around the given area to show results whilst ensuring they still sum to the original
    gauss = gaussian_filter(DisplayArray, sigma=20)
    
    minValue = np.min(DisplayArray)
    DisplayArray = [[np.log(0.5 * float(val+minValue) + 1) for val in row] for row in DisplayArray]
            
    print("### Creating new Save file ###")
    np.save("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"),gauss)

def displayArray(arr):
    global dateTime    
    print("### Displaying graph ###")
    plt.clf()
    plt.imshow(arr)
    plt.axis('off')
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.title(dateTime[0] + " " + dateTime[1] + " Graph " + ("Subplot" if loadSubbox.get() == 1 else ""))
    plt.savefig('./Data/plot.png',bbox_inches='tight')
    # bg = Image.open('./Data/plot.png')
    # fg = Image.open('./Images/Subbox.png')
    # Image.blend(bg, fg, .7).save("pic.png")
    
    img2 = ImageTk.PhotoImage(Image.open('./Data/plot.png'))
    graphPlot.configure(image = img2)
    graphPlot.image = img2
    
def calculateFractal(arr):
    print()
    
def loadData():
    global dateTime
    date = str(cal.get_date()).split("/")
    dateTime = [date[1].zfill(2) + "-" + datetime.datetime.strptime(date[0], "%m").strftime("%b")  + "-" + date[2],hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get()]
    
    if not os.path.exists("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy")):
        if skip and subsetData:
            loadMWData(".\Data\subset")
        elif skip:
            loadMWData(".\Data\Substations")
        createArray(".\Data")
        
    currentArray = np.load("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"))
    displayArray(currentArray)
    print(fractal_dimension_grayscale_DBC(currentArray))

def timeUpdate(*args):
    timeLable.configure(text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())


window = Tk()
if __name__ == "__main__":
    window.title("Power Grid Fractal Dimesnions Calculator")
    
    # load image
    photo = ImageTk.PhotoImage(Image.open('.\Data\plot.png'))
    graphPlot = Label(window, image = photo)
    graphPlot.image = photo
    graphPlot.grid(column=0, row=0, rowspan=10)
    
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
    ampmLabel =Label(window, text="AM/PM")
    ampmLabel.grid(column=3,row=2)
    
    hourVar = StringVar(window)
    hourVar.set("1")
    minuteVar = StringVar(window)
    minuteVar.set("00")
    ampmVar = StringVar(window)
    ampmVar.set("AM")
    
    hourPicker = OptionMenu(window, hourVar , '1','2','3','4','5','6','7','8','9','10','11','12')
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
    
    #load Subbox checkbox
    loadSubbox = IntVar()
    subboxButton = Checkbutton(window, text = "Subbox", variable=loadSubbox)
    subboxButton.grid(column=2,row=6)
    
    # Load button
    btn = Button(window, text="Load Data", command=loadData)
    btn.grid(column=2, row=8)
    window.mainloop()