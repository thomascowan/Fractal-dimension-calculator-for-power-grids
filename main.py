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
import math

from libraries.fractal_analysis_fxns import fractal_dimension_grayscale
from PIL import Image, ImageTk
from scipy.ndimage import gaussian_filter
from tkinter import Label, StringVar, IntVar, OptionMenu, Button, Checkbutton, Tk, DISABLED, NORMAL, Radiobutton, W
from tkcalendar import Calendar


df = {}
MW = {}
dateTime = ["01-JUL-20","11:00:00 AM"]
__name__ = "__main__"
     
"""
    @name: loadMWData
    @param: 
        directory: The given directory the data is in
    @description: Loads in data from csv files found on Energex and Ausgrid website make all of the substation power
    usage data more easily accessible within the program
"""                  
def loadMWData(directory):
    """ uses the global MW variable so that it is available anywhere throughout the program """
    global MW
    """ Checks if the a preproccessed dictionary exists and loads that file into the variable if it does exist """
    fileLocation = "./Data/MW_Data_Brisbane.pkl" if locationRadioButton.get() == "Brisbane" else "./Data/MW_Data_Sydney.pkl"
    if os.path.exists(fileLocation):
        print('### Loading previously loaded data ###')
        with open(fileLocation, 'rb') as f:
            MW = pickle.load(f)
    else:
        """ This runs if there is no preprocessed data to load """
        print('### Loading new data ###')
        """ two different methods required for Brisbane and Sydney as data layouts differ """
        if locationRadioButton.get() == "Brisbane":
            """ Iterates over each file in the directory with all stored Brisbane Data """
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
                """ Only actions csv files as they are the only ones that would contain the data"""
                if filename.endswith(".csv"): 
                    """ create a data fram of each file so as to make the data easily accessible """
                    df[filename] = pd.read_csv(os.path.join(directory,filename))
                    """ iterate over each item in the dataframe and add each date and time to the dictionary """
                    for (idx, row) in enumerate(df[filename].iterrows()):
                        """ creates new substation location in dictionary if it doesn't exist """
                        if filename not in MW:
                             MW[filename] = {}
                        """ formats date to be consistent throughout the program """
                        currDate = str(row[1]['Date'])[:3] + str(row[1]['Date'])[3:6].upper() + str(row[1]['Date'])[6:]
                        """ creates new date dictioanry in the substation dictionary if it doesn't exist """
                        if currDate not in MW[filename]:
                             MW[filename][currDate] = {}
                        """ adds the value of the power usage at the date and time of the substation to the dictionary for later use """
                        MW[filename][currDate][row[1]["Time"]] = row[1]["MW"]
        else:  
            """ Sydney data processing """
            """ Iterates over each file in the directory with all stored Brisbane Data """
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
                """ Only actions csv files as they are the only ones that would contain the data"""
                if filename.endswith(".csv"): 
                    """ create a data fram of each file so as to make the data easily accessible """
                    df[filename] = pd.read_csv(os.path.join(directory,filename))
                    """ iterate over each item in the dataframe and add each date and time to the dictionary """
                    for (idx, row) in enumerate(df[filename].iterrows()):
                        """ creates new substation location in dictionary if it doesn't exist """
                        if filename not in MW:
                            MW[filename] = {}
                        """ formats date to be consistent throughout the program """
                        currDate = row[1]['Date'].zfill(9)[:2] + "-" + row[1]['Date'].zfill(9)[2:5] + "-" + row[1]['Date'].zfill(9)[-2:]
                        """ creates new date dictioanry in the substation dictionary if it doesn't exist """
                        MW[filename][currDate] = {}
                        """ Sydney data is available in 15 minute increments so it is converted to 30 minutes but adding 
                            two together. This is done to match Brisbane data and have consistent data formats. They are not 
                            iterated over as it is complicated to make a for loop for that and this is actually much faster """
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
        """ Once data has been loaded into MW variable, it is the saved locally for faster processing later """
        with open(fileLocation, 'wb') as f:
            pickle.dump(MW, f)
            

    """
        @name: createArray
        @params:
            directory: The directory that the location data of each substation is stored in
            dateTime: The dateTime of the current plot being generated
        @description: Generates a graph of the current array and saves it to the machine locally for 
        the program to then have it display within the main screen
    """
def createArray(directory, dateTime):
    """   Sets the location file based on state of button on interface and loads data from it, also removes any missing entries   """
    locationFile = "locationsBrisbane.csv" if locationRadioButton.get() == "Brisbane" else "locationsSydney.csv"
    locationsDF = pd.read_csv(os.path.join(directory,locationFile))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    """   Creates variables for various sections of the program    """
    locationCoords = [list(),list(),list()]
    uneditedLocationCoords = [list(),list()]
    counter = 0
    """   Controls the precision of the coordinates being used, i.e. 4 means 4 decimal spots   """
    precisionValue = 4
    
    """   Sets the subbox based on which city has been selected   """
    Subbox = ((-34.08139338661285, 151.32981008988398), (-33.6251192125217, 150.88801323260108))
    if locationRadioButton.get() == "Brisbane":
        Subbox = ((-27.61328568848432, 153.21056146895143), (-27.253886818529896, 152.92951384959727))
    
    """   iterate over each location to store the coordinates of each substation, does not include substation if subbox is active
          and it is outside the subbox area    """
    for row in locationsDF.iterrows():
        """   Allows if subbox is false, or subbox is true and within areas   """
        if (loadSubbox.get() == 0 or (loadSubbox.get() == 1 and (row[1]["Longitude"] < Subbox[0][1] and row[1]["Longitude"] > Subbox[1][1] and row[1]["Latitude"] > Subbox[0][0] and row[1]["Latitude"] < Subbox[1][0]))):
            counter+=1
            """   Loads in coordinates, finds the location of the decimal within them   """
            uneditedLocationCoords[0].append(float(row[1]["Latitude"]))
            uneditedLocationCoords[1].append(float(row[1]["Longitude"]))
            
            latDotSpot = str(row[1]["Latitude"]).index('.')
            lonDotSpot = str(row[1]["Longitude"]).index('.')
            
            """   Converts the coordinates to integer values by only keeping changing numbers (i.e. remoing 15 from front of 153.245... as it will always be the case)   
                  Also removes the precision points on the end to reduce spacial complexity of array that will be generated   """
            convertedLat = int(str(row[1]["Latitude"])[0:latDotSpot] + str(row[1]['Latitude'])[latDotSpot+1:latDotSpot+precisionValue])
            convertedLon = int(str(row[1]["Longitude"])[0:lonDotSpot] + str(row[1]['Longitude'])[lonDotSpot+1:lonDotSpot+precisionValue])

            """   attaches the location to the coordinates so we can place values into array at later stage   """
            locationCoords[0].append(row[1]["Location"])
            locationCoords[1].append(convertedLat)
            locationCoords[2].append(convertedLon)
            
    """   Calculates the dimensions of the array, adds padding for when guassian filter is applied so that numbers 
          bunched up on the edge in spot   """
    arrayHeight = int((max(locationCoords[1]) - min(locationCoords[1])) * 1.2)
    minHeight = min(locationCoords[1])
    heightOffset = int((max(locationCoords[1]) - min(locationCoords[1])) * 0.12)
    
    arrayWidth = int((max(locationCoords[2]) - min(locationCoords[2])) * 1.2)
    minWidth = min(locationCoords[2])
    widthOffset = int((max(locationCoords[2]) - min(locationCoords[2])) * 0.12)
    
    """   transforms the coordinates into the new range of the array such that it takes up less space   """
    adjustedDisplayCoords = []
    for i in range(len(locationCoords[0])):
        adjustedDisplayCoords.append((locationCoords[0][i], locationCoords[1][i]-minHeight+heightOffset, locationCoords[2][i]-minWidth+widthOffset))
    
    """  Creates an empty array for values to be inserted into   """
    DisplayArray = np.zeros([arrayHeight + heightOffset*2,arrayWidth + widthOffset*2],dtype=np.float32())
    """   iterates over all substations and inserts power generated at each substation into the relevant coordinate on the array   """
    """   Also multiplies each value by 1000000 to convert MV to V   """
    """   Also uses 0 (zero) if no value is present within data   """
    for l in adjustedDisplayCoords:
        """   Checks for is interface has selected average throughout the year   """
        if yearAverage.get() == 1:
            """ Calculates the hour but taking the average of the substation at the specified hour on every day """
            if timeFrame.get() == "Hour":
                a = 0
                for x in MW[l[0]]:
                    if x != "nan":
                        a += (MW[l[0]][x][dateTime[1]]*1000000 if not math.isnan(MW[l[0]][x][dateTime[1]]) else 0)
                DisplayArray[l[1]][l[2]] = a / len(MW[l[0]])
            
                """ Calculates the day but taking the average of the cumulative value of hours between 6 AM and 6 PM for every day """
            elif timeFrame.get() == "Day":
                times = ["6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM","9:00:00 AM","9:30:00 AM",
                        "10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM","1:30:00 PM",
                        "2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM"]
                everyDaySum = 0
                for date in MW[l[0]]:
                    if date != "nan":
                        for t in times:
                            everyDaySum += (float(MW[l[0]][date][t])*1000000 if not math.isnan(MW[l[0]][date][t]) else 0)
                DisplayArray[l[1]][l[2]] = everyDaySum / len(MW[l[0]])
                 
                """ Calculates the night but taking the average of the cumulative value of hours between 6 PM and 6 AM for every day """
            elif timeFrame.get() == "Night":
                times = ["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM",
                         "4:00:00 AM","4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM",
                         "8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"]
                everyNightSum = 0
                for date in MW[l[0]]:
                    if date != "nan":
                        for t in times:
                            everyNightSum += (float(MW[l[0]][date][t])*1000000 if not math.isnan(MW[l[0]][date][t]) else 0)
                DisplayArray[l[1]][l[2]] = everyNightSum / len(MW[l[0]])
            
                """ Calculates the entire day by taking the sum of all hours, and taking the average throughout the entire year """
            else:
                everyDaySum = 0
                for date in MW[l[0]]:
                    if date != "nan":
                        everyDaySum += (sum(MW[l[0]][date].values())*1000000 if not math.isnan(sum(MW[l[0]][date].values())) else 0)
                DisplayArray[l[1]][l[2]] = everyDaySum / len(MW[l[0]])
        else:
            """   This case is for when it is not the average of the entire year, uses the specified date to determine with day to use   """
            """ Sets the value to the value set for the substation at the given time at the given hour """
            if timeFrame.get() == "Hour":
                DisplayArray[l[1]][l[2]] = (float(MW[l[0]][dateTime[0]][dateTime[1]])*1000000 if not math.isnan(MW[l[0]][dateTime[0]][dateTime[1]]) else 0)
            
                """ Sets the value to the sum of each hour between 6 AM and 6 PM on the given day """
            elif timeFrame.get() == "Day":
                times = ["6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM","9:00:00 AM","9:30:00 AM",
                        "10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM","1:30:00 PM",
                        "2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM"]
                daySum = 0
                for t in times:
                    daySum += (float(MW[l[0]][dateTime[0]][t])*1000000 if not math.isnan(MW[l[0]][dateTime[0]][t]) else 0)
                DisplayArray[l[1]][l[2]] = daySum
            
                """ Sets the value to the sum of each hour between 6 PM and A PM on the given day """
            elif timeFrame.get() == "Night":
                times = ["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM",
                         "4:00:00 AM","4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM",
                         "8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"]
                nightSum = 0
                for t in times:
                    nightSum += (float(MW[l[0]][dateTime[0]][t])*1000000 if not math.isnan(MW[l[0]][dateTime[0]][t]) else 0)
                DisplayArray[l[1]][l[2]] = nightSum
            
                """ Sets the value to the sum of each hour in the day on the given day """
            else:
                DisplayArray[l[1]][l[2]] = (sum(MW[l[0]][dateTime[0]].values())*1000000 if not math.isnan(sum(MW[l[0]][dateTime[0]].values())) else 0)
    
    """   Removes all nan values from empty cells in the data provided   """
    DisplayArray = np.nan_to_num(DisplayArray) 

    """   Applys a Gaussian filter to 'blur' the data to more accurately represent power distribution   """
    gauss = gaussian_filter(DisplayArray, sigma=25)
    """   Saved the array under the configuration to be loaded after in the program   """
    np.save("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
            (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
            (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
            (" AVG " if yearAverage.get()==1 else "") + 
            ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"),
            gauss)
    
    
    """
        @name: displayArray
        @params:
            arr: the current array of the frame being saved
        @description: Generates a graph of the current array and saves it to the machine locally for 
        the program to then have it display within the main screen
    """
def displayArray(arr):
    global dateTime   
    """   Generate the array onto the plot   """
    plt.clf()
    plt.imshow(arr, vmin=0)
    plt.gca().invert_yaxis()
    plt.xlabel("Fractal dimension\n" + str(fractal_dimension_grayscale(arr)[0]))
    plt.colorbar()
    plt.ticklabel_format(useOffset=False)
    
    plt.title(
            (dateTime[0] if yearAverage.get()==0 else "Year AVG") + "_" + 
            (dateTime[1] if timeFrame.get() == "Hour"  else timeFrame.get()) + " - Graph -" + 
            (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
            ("- Subplot" if loadSubbox.get() == 1 else "")
        )
    """   Save the picture to the computer   """
    plt.savefig('./Data/plot.png',bbox_inches='tight')
    """   Update the image on the main screen to the new plot   """
    img2 = ImageTk.PhotoImage(Image.open('./Data/plot.png'))
    graphPlot.configure(image = img2)
    graphPlot.image = img2

        
    """
        @name: saveGifFrames
        @params:
            arr: the current array of the frame being saved
            dateTime: The current dateTime of the array in order to write onto each frame
        @description: Saves the frame to local storage so it can be added together after and create a gif
    """
def saveGifFrames(arr,dateTime):
    plt.clf()
    plt.imshow(arr, vmax=(75000 if locationRadioButton.get() == "Brisbane" else 100000), vmin = 0)
    plt.gca().invert_yaxis()
    plt.xlabel("Fractal dimension\n" + str(fractal_dimension_grayscale(arr)[0]))
    plt.colorbar()
    plt.title(dateTime[0] + " " + (dateTime[1] if len(dateTime[1]) == 11 else "0" + str(dateTime[1])) + " Graph " + ("Subplot" if loadSubbox.get() == 1 else ""))
    plt.savefig('./gif/frames/' + (dateTime[1] if len(dateTime[1]) == 11 else "0" + str(dateTime[1])).replace(":","-") + '.png',bbox_inches='tight')
    
    
    """
        @name: generateGIF
        @description: Generates all arrays into a graph, stores the image of the graph, and then concatinates them
        together to create a gif file and displays it for the user
    """
def generateGIF():
    """   Uses the following list to iterate over all times of the day as they are index under these as keys   """
    dataTimes = ["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM","4:00:00 AM",
                 "4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM",
                 "9:00:00 AM","9:30:00 AM","10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM",
                 "1:30:00 PM","2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM",
                 "6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM","8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"]
    """   counter variable is used to keep track of how many the program has currently processed   """
    counter=0
    """   FDs holds the fractal dimensions of each plot to later put them on the line graph   """
    FDs = []
    """   Ensure that that data has been loaded into the program from csv files   """
    loadMWData(".\Data\Substations\Brisbane" if locationRadioButton.get() == "Brisbane" else ".\Data\Substations\Sydney")
    """   Iterate over all times within a day to show change in Fractal dimension through the day   """
    for times in dataTimes:
        print("\r" + str(counter) + " / " + str(len(dataTimes)) + " Frames Generated", end = '')
        date = str(cal.get_date()).split("/")
        dateTime = [date[1].zfill(2) + "-" + datetime.datetime.strptime(date[0], "%m").strftime("%b").upper()  + "-" + date[2],times]
        """   Checks for preprocessed data and creates it if it cannot find it   """
        if not os.path.exists("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
                              (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
                              (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
                              (" AVG " if yearAverage.get()==1 else "") + 
                              ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy")):
            createArray(".\Data", dateTime)
        """   Sets the current array to the locally stored array   """
        currentArray = np.load("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
                               (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
                               (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
                               (" AVG " if yearAverage.get()==1 else "") + 
                               ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"))
        """   Generates the gif frame   """
        saveGifFrames(currentArray,dateTime)
        """   Adds the latest fractal dimension to the array at same index as the time appears in dataTimes   """
        FDs.append((times, fractal_dimension_grayscale(currentArray)[0]))
        counter += 1
    print("\r48 / 48 Frames Generated")
    
    """   Creates an array of each stored frame's name and splits them into AM and PM so as to add them in the correct order   """
    filenames = ['./gif/frames/' + f for f in os.listdir('./gif/frames') if os.path.isfile(os.path.join('./gif/frames', f))]
    filesAM = [f for f in filenames if f[-6:-4] == 'AM']
    filesPM = [f for f in filenames if f[-6:-4] == 'PM']
    """   Writes to the gif file under the game of the date it is of and adds each image of the graph to the gif   """
    with imageio.get_writer('./gif/' + str(dateTime[0].upper()) +  + '.gif', mode='I') as writer:
        """   Adds AM files first the PM files. Also appends each image twice in order to slow down the speed of the gif   """
        for filename in filesAM:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)
        for filename in filesPM:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)
    """   Opens the gif file on the users computter   """
    os.startfile(os.getcwd() + '/gif/' + str(dateTime[0].upper()) + '.gif')
    
    
    """
        @name: createLineGraph
        @description: Calculates all fractal dimensions throught a day and plots them onto a line graph
    """
def createLineGraph():
    """   Uses the following list to iterate over all times of the day as they are index under these as keys   """
    dataTimes = ["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM","4:00:00 AM",
                 "4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM",
                 "9:00:00 AM","9:30:00 AM","10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM",
                 "1:30:00 PM","2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM",
                 "6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM","8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"]
    """   counter variable is used to keep track of how many the program has currently processed   """
    counter=0
    """   FDs holds the fractal dimensions of each plot to later put them on the line graph   """
    FDs = []
    """   Ensure that that data has been loaded into the program from csv files   """
    loadMWData(".\Data\Substations\Brisbane" if locationRadioButton.get() == "Brisbane" else ".\Data\Substations\Sydney")
    """   Iterate over all times within a day to show change in Fractal dimension through the day   """
    for times in dataTimes:
        print("\r" + str(counter) + " / " + str(len(dataTimes)) + " Fractal Dimensions Generated", end = '')
        date = str(cal.get_date()).split("/")
        dateTime = [date[1].zfill(2) + "-" + datetime.datetime.strptime(date[0], "%m").strftime("%b").upper()  + "-" + date[2],times]
        """   Checks for preprocessed data and creates it if it cannot find it   """
        if not os.path.exists("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
                              (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
                              (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
                              (" AVG " if yearAverage.get()==1 else "") + 
                              ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy")):
            createArray(".\Data", dateTime)
        """   Sets the current array to the locally stored array   """
        currentArray = np.load("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
                               (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
                               (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
                               (" AVG " if yearAverage.get()==1 else "") + 
                               ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"))
        """   Adds the latest fractal dimension to the array at same index as the time appears in dataTimes   """
        FDs.append(fractal_dimension_grayscale(currentArray)[0])
        counter += 1
    print("\r48 / 48 Fractal Dimensions Generated")
    """   Plots all the fractal dimensions onto a line graph at each time increment   """
    plt.xticks(range(len(dataTimes)), dataTimes, rotation=45)
    plt.plot(range(len(dataTimes)), FDs)
    plt.title('Fractal Dimension over time')
    plt.xlabel('Time')
    plt.ylabel('Fractal Dimension')
    plt.show()
    
    
    """
        @name: loadData
        @description: Controls the initial procedures of the program and accoutns for generating the gif, line graph, 
        or image of each configuration
    """    
def loadData():
    global dateTime
    if GIFtoDayState.get() == 1:
        """   Check to see if gif has already been created and saved, if not generates new gif   """
        if(os.path.exists('./gif/' + dateTime[0].upper() + (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ")  + '.gif')):
            os.startfile(os.getcwd() + '/gif/' + dateTime[0].upper() + '.gif')
        else:
            generateGIF()
    
    elif lineGraphState.get() == 1:
        """   Generates the line graph   """
        createLineGraph()
    else:
        date = str(cal.get_date()).split("/")
        """   Saves date time in a consistent format used throughout the program   """
        dateTime = [date[1].zfill(2) + "-" + datetime.datetime.strptime(date[0], "%m").strftime("%b").upper()  + "-" + date[2],hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get()]
        """   Check to see if graph has been processed already, not creates the array of the graph   """
        """   program configuration is used when saving and loading preprocessed data   """
        if not os.path.exists("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
                                (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
                                (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
                                (" AVG " if yearAverage.get()==1 else "") + 
                                ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy")):
            loadMWData(".\Data\Substations\Brisbane" if locationRadioButton.get() == "Brisbane" else ".\Data\Substations\Sydney")
            createArray(".\Data", dateTime)
        """    loads the processed array from locally saved file   """
        currentArray = np.load("./Data/preprocessedPlots/" + dateTime[0] + "-" + 
                                (dateTime[1].replace(":","-") if timeFrame.get() == "Hour"  else timeFrame.get()) + 
                                (" Bris " if locationRadioButton.get() == "Brisbane" else " Syd ") + 
                                (" AVG " if yearAverage.get()==1 else "") + 
                                ("Subplot.npy" if loadSubbox.get() == 1 else "Plot.npy"))
        """   Uses matplot library to display the produced array   """
        displayArray(currentArray)
        
"""
    The following functions are used to enable and disable various interface buttons.
    This is to ensure that only valid configurations can be set and that information is 
    converyed to the user
"""
def GIFtoDayStateGray(*args):
    if GIFtoDayState.get() == 1:
        hourPicker['state'] = DISABLED
        minutePicker['state'] = DISABLED
        ampnPicker['state'] = DISABLED
        radTimeHour['state'] = DISABLED
        radTimeDay['state'] = DISABLED
        radTimeNight['state'] = DISABLED
        radTimeAllDay['state'] = DISABLED
        lineGraphButton['state'] = DISABLED
    else:
        hourPicker['state'] = NORMAL
        minutePicker['state'] = NORMAL
        ampnPicker['state'] = NORMAL
        radTimeHour['state'] = NORMAL
        radTimeDay['state'] = NORMAL
        radTimeNight['state'] = NORMAL
        radTimeAllDay['state'] = NORMAL
        lineGraphButton['state'] = NORMAL
        
def timeFrameStateGray(*args):
    if timeFrame.get() == "Hour":
        hourPicker['state'] = NORMAL
        minutePicker['state'] = NORMAL
        ampnPicker['state'] = NORMAL
    else:
        hourPicker['state'] = DISABLED
        minutePicker['state'] = DISABLED
        ampnPicker['state'] = DISABLED
    
def yearAverageStateGray(*args):
    if yearAverage.get() == 1:
        cal['state'] = DISABLED
    else:
        cal['state'] = NORMAL
        
def lineGraphStateGray(*args):
    if lineGraphState.get() == 0:
        hourPicker['state'] = NORMAL
        minutePicker['state'] = NORMAL
        ampnPicker['state'] = NORMAL
        radTimeHour['state'] = NORMAL
        radTimeDay['state'] = NORMAL
        radTimeNight['state'] = NORMAL
        radTimeAllDay['state'] = NORMAL
        GIFtoDayButton['state'] = NORMAL
    else:
        hourPicker['state'] = DISABLED
        minutePicker['state'] = DISABLED
        ampnPicker['state'] = DISABLED
        radTimeHour['state'] = DISABLED
        radTimeDay['state'] = DISABLED
        radTimeNight['state'] = DISABLED
        radTimeAllDay['state'] = DISABLED
        GIFtoDayButton['state'] = DISABLED
        
def timeUpdate(*args):
    timeLable.configure(text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())
     
window = Tk()
window.iconbitmap('./Images/icon.ico')

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
    graphPlot.grid(column=0, row=0, rowspan=11)
    
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
    
    hourVar = StringVar(window, "1")
    minuteVar = StringVar(window, "00")
    ampmVar = StringVar(window, "AM")
    
    hourPicker = OptionMenu(window, hourVar , '1','2','3','4','5','6','7','8','9','10','11','12')
    hourPicker.grid(column=1,row=3)
    minutePicker = OptionMenu(window, minuteVar , '00','30')
    minutePicker.grid(column=2,row=3)
    ampnPicker = OptionMenu(window, ampmVar , 'AM','PM')
    ampnPicker.grid(column=3,row=3)
    
    timeLable = Label(window, text= hourVar.get() + ":" + minuteVar.get() + ":00 " + ampmVar.get() + " on " + cal.get_date())
    timeLable.grid(column=1,row=5,columnspan=3)
    
    #load Subbox checkbox
    loadSubbox = IntVar()
    subboxButton = Checkbutton(window, text = "Subbox", variable=loadSubbox)
    subboxButton.grid(column=2,row=6,sticky=W)
    
    #Filters data to average of all data
    yearAverage= IntVar()
    yearAverageButton = Checkbutton(window, text = "Year Average", variable=yearAverage)
    yearAverageButton.grid(column=2,row=7,sticky=W)
    
    #load GIF of day checkbox
    GIFtoDayState = IntVar()
    GIFtoDayButton = Checkbutton(window, text = "GIF of Day", variable=GIFtoDayState)
    GIFtoDayButton.grid(column=2,row=8,sticky=W)
    
    #load line graph of fractal dimensions
    lineGraphState = IntVar()
    lineGraphButton = Checkbutton(window, text = "Line Graph", variable=lineGraphState)
    lineGraphButton.grid(column=2,row=9,sticky=W)
    
    #radio button for Sydney and Brisbane
    locationRadioButton = StringVar(window, "Brisbane")
    radioBrisbane = Radiobutton(window, text="Brisbane", value="Brisbane", variable=locationRadioButton)
    radioSydney = Radiobutton(window, text="Sydney", value="Sydney", variable=locationRadioButton)
    radioBrisbane.grid(column=1,row=6,sticky=W)
    radioSydney.grid(column=1,row=7,sticky=W)
    
    #radio button for time frame
    timeFrame = StringVar(window, "Hour")
    radTimeHour = Radiobutton(window, text="Hour", value="Hour", variable=timeFrame)
    radTimeDay = Radiobutton(window, text="Day", value="Day", variable=timeFrame)
    radTimeNight = Radiobutton(window, text="Night", value="Night", variable=timeFrame)
    radTimeAllDay = Radiobutton(window, text="Entire Day", value="Entire Day", variable=timeFrame)
    
    radTimeHour.grid(column=3,row=6,sticky=W)
    radTimeDay.grid(column=3,row=7,sticky=W)
    radTimeNight.grid(column=3,row=8,sticky=W)
    radTimeAllDay.grid(column=3,row=9,sticky=W)
    
    #Tracing variables in event buttons needed to be disabled    
    hourVar.trace("w",timeUpdate)
    minuteVar.trace("w",timeUpdate)
    ampmVar.trace("w",timeUpdate)
    GIFtoDayState.trace("w",GIFtoDayStateGray)
    timeFrame.trace("w",timeFrameStateGray)
    yearAverage.trace("w",yearAverageStateGray)
    lineGraphState.trace("w",lineGraphStateGray)

    # Load button
    btn = Button(window, text="Load Data", command=loadData)
    btn.grid(column=2, row=10)
    window.mainloop()