# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 22:25:53 2022

@author: Thomas
"""

# Importing Numpy package
import numpy as np
from scipy.ndimage import gaussian_filter


mat = [[4.0,0.3,0.0,0.0],
       [0.0,0.0,0.0,0.0],
       [0.0,1.0,0.0,0.0],
       [0.0,0.0,0.0,4.0]]
 
gauss = gaussian_filter(mat, sigma=6.9)
 
# print("2D Gaussian array :\n")
print(gauss)
print(sum(sum(gauss)))