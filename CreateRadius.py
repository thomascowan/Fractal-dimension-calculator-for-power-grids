# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 20.0:54:51 20.022

@author: Thomas Cowan
"""

import math

mat = [[0.0,0.0,0.0,0.0],
       [0.0,0.0,0.0,0.0],
       [0.0,0.0,4.0,0.0],
       [0.0,0.0,0.0,0.0]]

def addRadius(matrix,radius=1.5):
    ep = getExistingPoints(matrix)
    pointsInRadius = list()
    for p in ep:        
        for i in range(p[0]-int(radius),p[0]+int(radius+1)+1):
            for j in range(p[1]-int(radius),p[1]+int(radius+1)+1):
                    pointsInRadius.append((i,j))
        print('temp')

def getExistingPoints(matrix):
    existingPoints = list()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0.0:
                existingPoints.append((i,j))
    return existingPoints

def printMat(matrix):
    for row in matrix:
        print(row)

# printMat(mat)
print()
addRadius(mat)