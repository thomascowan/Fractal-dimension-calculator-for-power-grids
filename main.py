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
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

df = {}
MW = {}
MVA = {}
dataTime = ["01-Jul-20","11:00:00 AM"]
LocationsDF = None
__name__ = "__main__"
# 0 for MW, 1 for MVA, anything else for both
SelectedData = 0
# Only loads 5 suburbs
subsetData = 0
#Print debug statements
DEBUG = 0
#only load data from 1 July 2020
quickLoad = 1
skip = 1
            
def loadAllData(directory):
    timeStarted = datetime.now() if DEBUG else ""
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
        if filename.endswith(".csv"): 
            df[filename] = pd.read_csv(os.path.join(directory,filename))
            for row in df[filename].iterrows():
                if filename not in MW:
                    MW[filename] = {}
                if(quickLoad and row[1]['Date'] == '02-Jul-20'):
                   break
                if row[1]['Date'] not in MW[filename]:
                    MW[filename][row[1]['Date']] = {}
                if filename not in MVA:
                    MVA[filename] = {}
                if row[1]['Date'] not in MVA[filename]:
                    MVA[filename][row[1]['Date']] = {}
                MW[filename][row[1]["Date"]][row[1]["Time"]] = row[1]["MW"]
                MVA[filename][row[1]["Date"]][row[1]["Time"]] = row[1]["MVA"]
    timeEnded = datetime.now() if DEBUG else ""
    print("\r" + str(len(os.listdir(directory))) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
    print("\tTime Elapsed: " + str(timeEnded - timeStarted)) if DEBUG else ""
    print("length of dictionary is MW: " + str(len(MW)) + " MVA: " + str(len(MVA))) if DEBUG else ""
            
def loadMWData(directory):
    timeStarted = datetime.now() if DEBUG else ""
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
    timeEnded = datetime.now() if DEBUG else ""
    print("\r" + str(len(os.listdir(directory))) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
    print(" - Time Elapsed: " + str(timeEnded - timeStarted)) if DEBUG else ""
    print("length of dictionary is " + str(len(MW))) if DEBUG else ""
                    
            
def loadMVAData(directory):
    timeStarted = datetime.now() if DEBUG else ""
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print("\r" + str(os.listdir(directory).index(file)) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
        if filename.endswith(".csv"): 
            df[filename] = pd.read_csv(os.path.join(directory,filename))
            for row in df[filename].iterrows():
                if filename not in MVA:
                    MVA[filename] = {}
                if quickLoad and row[1]['Date'] == '02-Jul-20':
                    break
                if row[1]['Date'] not in MVA[filename]:
                    MVA[filename][row[1]['Date']] = {}
                MVA[filename][row[1]["Date"]][row[1]["Time"]] = row[1]["MW"]
    timeEnded = datetime.now() if DEBUG else ""
    print("\r" + str(len(os.listdir(directory))) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
    print(" - Time Elapsed: " + str(timeEnded - timeStarted)) if DEBUG else ""
    print("length of dictionary is " + str(len(MVA))) if DEBUG else ""
            
def LoadCoordsOntoMap(directory):
    locationsDF = pd.read_csv(os.path.join(directory,"locations.csv"))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    
    scatterPlots = [list(),list(),list(),list()]
    for row in locationsDF.iterrows():
        scatterPlots[0].append(row[1]["Longitude"])
        scatterPlots[1].append(row[1]["Latitude"])
        scatterPlots[2].append(row[1]["Location"])
        scatterPlots[3].append(MW[row[1]["Location"]]["01-Jul-20"]["12:00:00 AM"]*1000)
        
    heatmap, xedges, yedges = np.histogram2d(scatterPlots[0], scatterPlots[1], weights=scatterPlots[3], density=True, bins=500)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    plt.clf()
    plt.figure(figsize = (7, 14))
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()

def createArray(directory):
    locationsDF = pd.read_csv(os.path.join(directory,"locations.csv"))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    locationCoords = [list(),list(),list()]
    uneditedLocationCoords = [list(),list()]
    counter = 0
    precisionValue = 4
    loadSubbox = False
    Subbox = ((-27.795713993519306, 153.29807187264893), (-27.298858301659403, 152.72594294487124))
    print()
    for row in locationsDF.iterrows():
        ### Loading coordinates in as integer values basing precision of precisionValue variable
        # print(str(row[1]["Latitude"]) + "\t>\t" + str(Subbox[0][0]) + "\t" + str(row[1]["Latitude"] > Subbox[0][0]))
        # print(row[1]["Longitude"] < Subbox[0][1] and row[1]["Longitude"] > Subbox[1][1] and row[1]["Latitude"] > Subbox[0][0] and row[1]["Latitude"] < Subbox[1][0])
        if loadSubbox:
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
    # print("arrayHeight:\t" + str(arrayHeight))
    # print("arrayWidth:\t\t" + str(arrayWidth))
    
    minHeight = min(locationCoords[1])
    minWidth = min(locationCoords[2])
    # print("minHeight:\t\t" + str(minHeight))
    # print("minWidth:\t\t" + str(minWidth))
    
    widthOffset = int(arrayWidth * 0.12)
    heightOffset = int(arrayHeight * 0.12)
    # print("heightOffset:\t" + str(heightOffset))
    # print("widthOffset:\t" + str(widthOffset))
    
    ### Moving coordinates to new location
    adjustedDisplayCoords = []
    for i in range(len(locationCoords[0])):
        adjustedDisplayCoords.append((locationCoords[0][i], locationCoords[1][i]-minHeight+heightOffset, locationCoords[2][i]-minWidth+widthOffset))

    ### Create an empty array and then populate with data of a set datetime
    DisplayArray = np.zeros([arrayWidth + widthOffset*2,arrayHeight + heightOffset*2],dtype=np.float32())
    for l in adjustedDisplayCoords:
        if MW[l[0]]["01-Jul-20"]["12:00:00 AM"] >= 0:
            DisplayArray[l[1]][l[2]] = np.log(float(0.5 * MW[l[0]]["01-Jul-20"]["12:00:00 AM"]) + 1)
        else: 
            DisplayArray[l[1]][l[2]] = -np.log(float(-0.5 * MW[l[0]]["01-Jul-20"]["12:00:00 AM"]) + 1)
    
    ### Apply Gaussian filter to 'blur' around the given area to show results whilst ensuring they still sum to the original
    gauss = gaussian_filter(DisplayArray, sigma=10)
    
    for i in range(len(DisplayArray)):
        for j in range(len(DisplayArray[i])):
            if DisplayArray[i][j] >= 0:
                DisplayArray[i][j]  = np.log(0.5 * float(DisplayArray[i][j]) + 1)
            else: 
                DisplayArray[i][j]  = -np.log(-0.5 *float(DisplayArray[i][j]) + 1)
            
    
    print("### Creating new Save file ###")
    np.save("./preprocessedPlots/" + dataTime[0] +  dataTime[1].replace(":","") + "Plot.npy",gauss)
    
def loadSaved():
    print("### Loading file ###")
    return np.load("./preprocessedPlots/" + dataTime[0] +  dataTime[1].replace(":","") + "Plot.npy")


def displayArray(arr):
    print("### Displaying graph ###")
    plt.clf()
    plt.imshow(arr)
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.savefig('pic.png',bbox_inches='tight')
    
def calculateFractal(arr):
    print()
    
if __name__ == "__main__":
    if not os.path.exists("./preprocessedPlots/" + dataTime[0] +  dataTime[1].replace(":","") + "Plot.npy"):
        if skip and subsetData:
            if SelectedData == 0:
                loadMWData(".\Data\subset")
            elif SelectedData == 1:    
                loadMVAData(".\Data\subset")
            else:
                loadAllData(".\Data\subset")
        elif skip:
            if SelectedData == 0:
                loadMWData(".\Data\Substations")
            elif SelectedData == 1:    
                loadMVAData(".\Data\Substations")
            else:
                loadAllData(".\Data\Substations")
        createArray(".\Data")
    currentArray = loadSaved()
    displayArray(currentArray)
    # calculateFractal(currentArray)