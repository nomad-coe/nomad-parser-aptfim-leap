#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 14:50:59 2021
@author: kuehbach

a utility to create a small test file matching the specifications of an atom probe microscopy community POS file format
"""

import numpy as np

posfn = 'example.pos'

# a file with only ten atoms, unrealistically small solely to test the parser implementation
N = 10
# pos files have always the same structure, see B. Gault et al. (2012) or D. J. Larson (2013) books on atom probe microscope

# unphysical dummy data
# a pos file has four data columns
dummydata = np.array([np.linspace(1,N,N),]*4).transpose()


dtyp_names = ['Reconstructed position along the x-axis (nm)',
              'Reconstructed position along the y-axis (nm)', 
              'Reconstructed position along the z-axis (nm)', 
              'Reconstructed mass-to-charge-state ratio (amu)']
#big-endian single precision floating point numbers
dtyp_formats = ['>f4', '>f4', '>f4', '>f4'] 

pos = np.zeros( N, dtype={ 'names': dtyp_names, 
                           'formats': dtyp_formats } )

for i in np.arange(0,4):
    pos[dtyp_names[i]] = dummydata[:,i]

pos.tofile( posfn )
