# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:42:34 2022
@author: Thomas Cowan 
MQID: 45321760
"""


import datetime
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle

from PIL import Image, ImageTk
from scipy.ndimage import gaussian_filter
from tkinter import Label, StringVar, IntVar, OptionMenu, Button, Checkbutton, Tk, DISABLED, NORMAL, Radiobutton
from tkcalendar import Calendar

from fractal_analysis_fxns import fractal_dimension_grayscale
# from FractalDimension import fractal_dimension

df = {}
MW = {}
dateTime = ["01-JUL-20","11:00:00 AM"]
LocationsDF = None
__name__ = "__main__"
                        
def loadMWData(directory):
    global MW
    fileLocation = "./Data/MW_Data_Brisbane.pkl" if locationRadioButton.get() == "Brisbane" else "./Data/MW_Data_Sydney.pkl"
    if os.path.exists(fileLocation):
        print('### Loading previously loaded data ###')
        print(fileLocation)
        with open(fileLocation, 'rb') as f:
            MW = pickle.load(f)
    else:
        print('### Loading new data ###')
        if locationRadioButton.get() == "Brisbane":
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
                if filename.endswith(".csv"): 
                    df[filename] = pd.read_csv(os.path.join(directory,filename))
                    for (idx, row) in enumerate(df[filename].iterrows()):
                        if filename not in MW:
                             MW[filename] = {}
                        currDate = str(row[1]['Date'])[:3] + str(row[1]['Date'])[3:6].upper() + str(row[1]['Date'])[6:]
                        if currDate not in MW[filename]:
                             MW[filename][currDate] = {}
                        MW[filename][currDate][row[1]["Time"]] = row[1]["MW"]
        else:  
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
                if filename.endswith(".csv"): 
                    df[filename] = pd.read_csv(os.path.join(directory,filename))
                    for (idx, row) in enumerate(df[filename].iterrows()):
                        if filename not in MW:
                            MW[filename] = {}
                        currDate = row[1]['Date'].zfill(9)[:2] + "-" + row[1]['Date'].zfill(9)[2:5] + "-" + row[1]['Date'].zfill(9)[-2:]
                        MW[filename][currDate] = {}
                        MW[filename][currDate]['12:00:00 AM'] = float(row[1]['0:15']) + float(row[1]['0:30'])
                        MW[filename][currDate]['12:30:00 AM'] = float(row[1]['0:45']) + float(row[1]['1:00'])
                        MW[filename][currDate]['1:00:00 AM'] = float(row[1]['1:15']) + float(row[1]['1:30'])
                        MW[filename][currDate]['1:30:00 AM'] = float(row[1]['1:45']) + float(row[1]['2:00']) 
                        MW[filename][currDate]['2:00:00 AM'] = float(row[1]['2:15']) + float(row[1]['2:30']) 
                        MW[filename][currDate]['2:30:00 AM'] = float(row[1]['2:45']) + float(row[1]['3:00']) 
                        MW[filename][currDate]['3:00:00 AM'] = float(row[1]['3:15']) + float(row[1]['3:30'])
                        MW[filename][currDate]['3:30:00 AM'] = float(row[1]['3:45']) + float(row[1]['4:00']) 
                        MW[filename][currDate]['4:00:00 AM'] = float(row[1]['4:15']) + float(row[1]['4:30']) 
                        MW[filename][currDate]['4:30:00 AM'] = float(row[1]['4:45']) + float(row[1]['5:00'])
                        MW[filename][currDate]['5:00:00 AM'] = float(row[1]['5:15']) + float(row[1]['5:30'])
                        MW[filename][currDate]['5:30:00 AM'] = float(row[1]['5:45']) + float(row[1]['6:00']) 
                        MW[filename][currDate]['6:00:00 AM'] = float(row[1]['6:15']) + float(row[1]['6:30'])
                        MW[filename][currDate]['6:30:00 AM'] = float(row[1]['6:45']) + float(row[1]['7:00'])
                        MW[filename][currDate]['7:00:00 AM'] = float(row[1]['7:15']) + float(row[1]['7:30']) 
                        MW[filename][currDate]['7:30:00 AM'] = float(row[1]['7:45']) + float(row[1]['8:00'])
                        MW[filename][currDate]['8:00:00 AM'] = float(row[1]['8:15']) + float(row[1]['8:30']) 
                        MW[filename][currDate]['8:30:00 AM'] = float(row[1]['8:45']) + float(row[1]['9:00'])
                        MW[filename][currDate]['9:00:00 AM'] = float(row[1]['9:15']) + float(row[1]['9:30']) 
                        MW[filename][currDate]['9:30:00 AM'] = float(row[1]['9:45']) + float(row[1]['10:00'])
                        MW[filename][currDate]['10:00:00 AM'] = float(row[1]['10:15']) + float(row[1]['10:30'])
                        MW[filename][currDate]['10:30:00 AM'] = float(row[1]['10:45']) + float(row[1]['11:00'])
                        MW[filename][currDate]['11:00:00 AM'] = float(row[1]['11:15']) + float(row[1]['11:30']) 
                        MW[filename][currDate]['11:30:00 AM'] = float(row[1]['11:45']) + float(row[1]['12:00']) 
                        MW[filename][currDate]['12:00:00 PM'] = float(row[1]['12:15']) + float(row[1]['12:30']) 
                        MW[filename][currDate]['12:30:00 PM'] = float(row[1]['12:45']) + float(row[1]['13:00']) 
                        MW[filename][currDate]['1:00:00 PM'] = float(row[1]['13:15']) + float(row[1]['13:30']) 
                        MW[filename][currDate]['1:30:00 PM'] = float(row[1]['13:45']) + float(row[1]['14:00'])
                        MW[filename][currDate]['2:00:00 PM'] = float(row[1]['14:15']) + float(row[1]['14:30'])
                        MW[filename][currDate]['2:30:00 PM'] = float(row[1]['14:45']) + float(row[1]['15:00'])
                        MW[filename][currDate]['3:00:00 PM'] = float(row[1]['15:15']) + float(row[1]['15:30']) 
                        MW[filename][currDate]['3:30:00 PM'] = float(row[1]['15:45']) + float(row[1]['16:00'])
                        MW[filename][currDate]['4:00:00 PM'] = float(row[1]['16:15']) + float(row[1]['16:30'])
                        MW[filename][currDate]['4:30:00 PM'] = float(row[1]['16:45']) + float(row[1]['17:00']) 
                        MW[filename][currDate]['5:00:00 PM'] = float(row[1]['17:15']) + float(row[1]['17:30'])
                        MW[filename][currDate]['5:30:00 PM'] = float(row[1]['17:45']) + float(row[1]['18:00']) 
                        MW[filename][currDate]['6:00:00 PM'] = float(row[1]['18:15']) + float(row[1]['18:30']) 
                        MW[filename][currDate]['6:30:00 PM'] = float(row[1]['18:45']) + float(row[1]['19:00']) 
                        MW[filename][currDate]['7:00:00 PM'] = float(row[1]['19:15']) + float(row[1]['19:30'])
                        MW[filename][currDate]['7:30:00 PM'] = float(row[1]['19:45']) + float(row[1]['20:00']) 
                        MW[filename][currDate]['8:00:00 PM'] = float(row[1]['20:15']) + float(row[1]['20:30'])
                        MW[filename][currDate]['8:30:00 PM'] = float(row[1]['20:45']) + float(row[1]['21:00'])
                        MW[filename][currDate]['9:00:00 PM'] = float(row[1]['21:15']) + float(row[1]['21:30'])
                        MW[filename][currDate]['9:30:00 PM'] = float(row[1]['21:45']) + float(row[1]['22:00']) 
                        MW[filename][currDate]['10:00:00 PM'] = float(row[1]['22:15']) + float(row[1]['22:30']) 
                        MW[filename][currDate]['10:30:00 PM'] = float(row[1]['22:45']) + float(row[1]['23:00']) 
                        MW[filename][currDate]['11:00:00 PM'] = float(row[1]['23:15']) + float(row[1]['23:30']) 
                        MW[filename][currDate]['11:30:00 PM'] = float(row[1]['23:45']) + float(row[1]['24:00'])
        print("\r" + str(len(os.listdir(directory))) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
        with open(fileLocation, 'wb') as f:
            pickle.dump(MW, f)

def createArray(directory, dateTime):
    locationFile = "locationsBrisbane.csv" if locationRadioButton.get() == "Brisbane" else "locationsSydney.csv"
    locationsDF = pd.read_csv(os.path.join(directory,locationFile))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    locationCoords = [list(),list(),list()]
    uneditedLocationCoords = [list(),list()]
    counter = 0
    precisionValue = 4
    Subbox = None
    
    if locationRadioButton.get() == "Brisbane":
        Subbox = ((-27.795713993519306, 153.19807187264893), (-27.298858301659403, 152.82594294487124))
    else: 
        Subbox = ((-33.682774118437905, 151.02984591706766), (-34.01072565610798, 151.3238529358113))
    
    global loadSubbox
    for row in locationsDF.iterrows():
        ### Loading coordinates in as integer values basing precision of precisionValue variable
        if (loadSubbox.get() == 0 or (loadSubbox.get() == 1 and (row[1]["Longitude"] < Subbox[0][1] and row[1]["Longitude"] > Subbox[1][1] and row[1]["Latitude"] > Subbox[0][0] and row[1]["Latitude"] < Subbox[1][0]))):
            counter+=1
            uneditedLocationCoords[0].append(float(row[1]["Latitude"]))
            uneditedLocationCoords[1].append(float(row[1]["Longitude"]))
            
            latDotSpot = str(row[1]["Latitude"]).index('.')
            lonDotSpot = str(row[1]["Longitude"]).index('.')
            
            convertedLat = int(str(row[1]["Latitude"])[0:latDotSpot] + str(row[1]['Latitude'])[latDotSpot+1:latDotSpot+precisionValue])
            convertedLon = int(str(row[1]["Longitude"])[0:lonDotSpot] + str(row[1]['Longitude'])[lonDotSpot+1:lonDotSpot+precisionValue])

            locationCoords[0].append(row[1]["Location"])
            locationCoords[1].append(convertedLat)
            locationCoords[2].append(convertedLon)
            
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

    ### Create an empty array and then populate with data of a set datetime
    DisplayArray = np.zeros([arrayWidth + widthOffset*2,arrayHeight + heightOffset*2],dtype=np.float32())
    for l in adjustedDisplayCoords:
        DisplayArray[l[1]][l[2]] = float(MW[l[0]][dateTime[0]][dateTime[1]])*1000000
    DisplayArray = np.nan_to_num(DisplayArray) 
    
    ### Apply Gaussian filter to 'blur' around the given area to show results whilst ensuring they still sum to the original

    gauss = gaussian_filter(DisplayArray, sigma=25)
    arrLen = len(gauss)
    gauss = gauss[int(arrLen*0.12):int(arrLen-arrLen*0.12)][int(arrLen*0.12):int(arrLen-arrLen*0.12)]
    np.save("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Bris" if locationRadioButton.get() == "Brisbane" else "Syd") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"),gauss)

def displayArray(arr):
    global dateTime    
    plt.clf()
    plt.imshow(arr, cmap='gray')
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

def saveGifFrames(arr,dateTime):
    plt.clf()
    plt.imshow(arr, vmax=50000, vmin = 0)
    plt.axis('off')
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.title(dateTime[0] + " " + (dateTime[1] if len(dateTime[1]) == 11 else "0" + str(dateTime[1])) + " Graph " + ("Subplot" if loadSubbox.get() == 1 else ""))
    plt.savefig('./gif/frames/' + (dateTime[1] if len(dateTime[1]) == 11 else "0" + str(dateTime[1])).replace(":","-") + '.png',bbox_inches='tight')
    
def timeUpdate(*args):
    timeLable.configure(text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())

def grayOptions(*args):
    if GIFtoDayState.get() == 1:
        hourPicker['state'] = DISABLED
        minutePicker['state'] = DISABLED
        ampnPicker['state'] = DISABLED
    else:
        hourPicker['state'] = NORMAL
        minutePicker['state'] = NORMAL
        ampnPicker['state'] = NORMAL
    
def generateGIF():
    dataTimes = ["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM","4:00:00 AM",
                 "4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM",
                 "9:00:00 AM","9:30:00 AM","10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM",
                 "1:30:00 PM","2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM",
                 "6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM","8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"]
    counter=0
    loadMWData(".\Data\Substations\Brisbane" if locationRadioButton.get() == "Brisbane" else ".\Data\Substations\Sydney")
    for times in dataTimes:
        print("\r" + str(counter) + " / " + str(len(dataTimes)) + " Frames Generated", end = '')
        date = str(cal.get_date()).split("/")
        dateTime = [date[1].zfill(2) + "-" + datetime.datetime.strptime(date[0], "%m").strftime("%b").upper()  + "-" + date[2],times]
        if not os.path.exists("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Bris" if locationRadioButton.get() == "Brisbane" else "Syd") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy")):
            createArray(".\Data", dateTime)
        currentArray = np.load("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Bris" if locationRadioButton.get() == "Brisbane" else "Syd") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"))
        saveGifFrames(currentArray,dateTime)
        counter += 1
    print("\r48 / 48 Frames Generated")
    
    filenames = ['./gif/frames/' + f for f in os.listdir('./gif/frames') if os.path.isfile(os.path.join('./gif/frames', f))]
    filesAM = [f for f in filenames if f[-6:-4] == 'AM']
    filesPM = [f for f in filenames if f[-6:-4] == 'PM']
    with imageio.get_writer('./gif/' + dateTime[0].upper()  + '.gif', mode='I') as writer:
        for filename in filesAM:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)
        for filename in filesPM:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)
    os.startfile(os.getcwd() + '/gif/' + dateTime[0].upper() + '.gif')
    
def loadData():
    global dateTime
    if GIFtoDayState.get() == 0:
        date = str(cal.get_date()).split("/")
        dateTime = [date[1].zfill(2) + "-" + datetime.datetime.strptime(date[0], "%m").strftime("%b").upper()  + "-" + date[2],hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get()]
        
        if not os.path.exists("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Bris" if locationRadioButton.get() == "Brisbane" else "Syd") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy")):
            loadMWData(".\Data\Substations\Brisbane" if locationRadioButton.get() == "Brisbane" else ".\Data\Substations\Sydney")
            createArray(".\Data", dateTime)
            
        currentArray = np.load("./Data/preprocessedPlots/" + dateTime[0] + "-" + dateTime[1].replace(":","-") + ("Bris" if locationRadioButton.get() == "Brisbane" else "Syd") + ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"))
        displayArray(currentArray)
        fractalValue.set(fractal_dimension_grayscale(currentArray)[0])
    else:
        generateGIF()
        

window = Tk()

if __name__ == "__main__": 
    #Create directory structure
    os.mkdir('./Images') if not os.path.exists('./Images') else ""
    os.mkdir('./gif') if not os.path.exists('./gif') else ""
    os.mkdir('./gif/frames') if not os.path.exists('./gif/frames') else ""
    os.mkdir('./Data') if not os.path.exists('./Data') else ""
    os.mkdir('./Data/Substations') if not os.path.exists('./Data/Substations') else ""
    os.mkdir('./Data/Substations/Sydney') if not os.path.exists('./Data/Substations/Sydney') else ""
    os.mkdir('./Data/Substations/Brisbane') if not os.path.exists('./Data/Substations/Brisbane') else ""
    os.mkdir('./Data/preprocessedPlots') if not os.path.exists('./Data/preprocessedPlots') else ""
    
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
    
    #load Subbox checkbox
    GIFtoDayState = IntVar()
    subboxButton = Checkbutton(window, text = "GIF of Day", variable=GIFtoDayState)
    subboxButton.grid(column=3,row=6)
    
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
    GIFtoDayState.trace("w",grayOptions)
    
    timeLable =Label(window, text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())
    timeLable.grid(column=1,row=5,columnspan=3)
    
    #load Subbox checkbox
    loadSubbox = IntVar()
    subboxButton = Checkbutton(window, text = "Subbox", variable=loadSubbox)
    subboxButton.grid(column=2,row=6)
    loadSubbox.set(1)
    
    #radio button for Sydney and Brisbane
    locationRadioButton = StringVar(window, "Brisbane")
    radioBrisbane = Radiobutton(window, text="Brisbane", value="Brisbane", variable=locationRadioButton)
    radioSydney = Radiobutton(window, text="Sydney", value="Sydney", variable=locationRadioButton)
    radioBrisbane.grid(column=1,row=6)
    radioSydney.grid(column=1,row=7)
    
    #Fractal Display
    fractalValue = StringVar(window, "Load data first")
    fractalLabelTitle = Label(window, text="Fractal Value")
    fractalLabel = Label(window, textvariable=fractalValue)
    fractalLabelTitle.grid(column=5, row=2)
    fractalLabel.grid(column=5, row=3)

    # Load button
    btn = Button(window, text="Load Data", command=loadData)
    btn.grid(column=2, row=8)
    window.mainloop()