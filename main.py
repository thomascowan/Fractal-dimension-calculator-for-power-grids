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



df = {}
MW = {}
MVA = {}
LocationsDF = None
__name__ = "__main__"
subsetData = 1
# 0 for MW, 1 for MVA, anything else for both
SelectedData = 0
DEBUG = 1
            
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
                if(subsetData and row[1]['Date'] == '15-Jul-20'):
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
                if(subsetData and row[1]['Date'] == '02-Jul-20'):
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
                if subsetData and row[1]['Date'] == '05-Jul-20':
                    break
                if row[1]['Date'] not in MVA[filename]:
                    MVA[filename][row[1]['Date']] = {}
                MVA[filename][row[1]["Date"]][row[1]["Time"]] = row[1]["MW"]
    timeEnded = datetime.now() if DEBUG else ""
    print("\r" + str(len(os.listdir(directory))) + " / " + str(len(os.listdir(directory))) + " Locations loaded", end = '')
    print(" - Time Elapsed: " + str(timeEnded - timeStarted)) if DEBUG else ""
    print("length of dictionary is " + str(len(MVA))) if DEBUG else ""
            
#def getLocations(directory):
##    print(locationsDF)

def LoadCoordsOntoMap(directory):
    locationsDF = pd.read_csv(os.path.join(directory,"locations.csv"))
    locationsDF = locationsDF[locationsDF["Longitude"] != 0.0]
    BBox = ((locationsDF['Longitude'].min(), locationsDF['Longitude'].max()),(locationsDF['Latitude'].min(),locationsDF['Latitude'].max()))    
#    print(MW["Acacia Ridge_EGX_20202021.csv"])
    scatterPlots = [list(),list(),list()]
    for row in locationsDF.iterrows():
        scatterPlots[0].append(row[1]["Longitude"])
        scatterPlots[1].append(row[1]["Latitude"])
        scatterPlots[2].append(row[1]["Location"])
        
    plt.figure(figsize = (14, 7))
    fig, ax = plt.subplots()
    for i in range(0,len(scatterPlots[0])):
#        print("aaaa:  " + str(scatterPlots[0][i]) + " - " + str(scatterPlots[1][i]) + " - " + str(scatterPlots[2][i]))
        ax.scatter(scatterPlots[0][i],scatterPlots[1][i],s=MW[scatterPlots[2][i]]["01-Jul-20"]["12:00:00 AM"])
        
    plt.show()
#    plt.scatter(scatterPlots[0],scatterPlots[1],c=MW[scatterPlots[2]]["01-Jul-20"]["12:00:00 AM"], cmap='gray')
    
if __name__ == "__main__":
    if subsetData:
#        if SelectedData == 0:
#            loadMWData(".\Data\subset")
#        elif SelectedData == 1:    
#            loadMVAData(".\Data\subset")
#        else:
#            loadAllData(".\Data\subset")
#    else:
#        if SelectedData == 0:
            loadMWData(".\Data\Energex-Network-Substation-Load-Data-2020-21")
#        elif SelectedData == 1:    
#            loadMVAData(".\Data\Energex-Network-Substation-Load-Data-2020-21")
#        else:
#            loadAllData(".\Data\Energex-Network-Substation-Load-Data-2020-21")
            
#    getLocations(".\Data")
    
    LoadCoordsOntoMap(".\Data")
    
    
    

#print(MW)