# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:42:34 2022

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
        
#     fig, ax = plt.subplots()
#     for i in range(0,len(scatterPlots[0])):
# #        print("aaaa:  " + str(scatterPlots[0][i]) + " - " + str(scatterPlots[1][i]) + " - " + str(scatterPlots[2][i]))
#         ax.scatter(scatterPlots[0][i],scatterPlots[1][i],s=MW[scatterPlots[2][i]]["01-Jul-20"]["12:00:00 AM"])
#     plt.show()
#     plt.scatter(scatterPlots[0],scatterPlots[1],c=MW[scatterPlots[2]]["01-Jul-20"]["12:00:00 AM"], cmap='gray')

def createArray(directory):
    locationsDF = pd.read_csv(os.path.join(directory,"locations.csv"))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    locationCoords = [list(),list(),list()]
    uneditedLocationCoords = [list(),list()]
    counter = 0
    precisionValue = 4
    print()
    for row in locationsDF.iterrows():
        ### Loading coordinates in as integer values basing precision of precisionValue variable
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
        DisplayArray[l[1]][l[2]] = MW[l[0]]["01-Jul-20"]["12:00:00 AM"]
    
    ### Apply Gaussian filter to 'blur' around the given area to show results whilst ensuring they still sum to the original
    gauss = gaussian_filter(DisplayArray, sigma=5)
    
    ### Place existing data into heatmap
    plt.imshow(gauss)
    plt.gca().invert_yaxis()
    
    
        
if __name__ == "__main__":
    if skip and subsetData:
        if SelectedData == 0:
            loadMWData(".\Data\subset")
        elif SelectedData == 1:    
            loadMVAData(".\Data\subset")
        else:
            loadAllData(".\Data\subset")
    elif skip:
        if SelectedData == 0:
            loadMWData(".\Data\Energex-Network-Substation-Load-Data-2020-21")
        elif SelectedData == 1:    
            loadMVAData(".\Data\Energex-Network-Substation-Load-Data-2020-21")
        else:
            loadAllData(".\Data\Energex-Network-Substation-Load-Data-2020-21")
    
    createArray(".\Data")
    # LoadCoordsOntoMap(".\Data")