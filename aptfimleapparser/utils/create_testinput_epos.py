#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 14:50:59 2021
@author: kuehbach

a utility to create a small test file matching the specifications of an atom probe microscopy community extended POS file format
"""

import numpy as np

eposfn = 'example.epos'

# a file with only ten atoms, unrealistically small solely to test the parser implementation
N = 10
# pos files have always the same structure, see B. Gault et al. (2012) or D. J. Larson (2013) books on atom probe microscope

# unphysical dummy data
# an epos file has eleven data columns
dummydata = np.array([np.linspace(1,N,N),]*11).transpose()

# correct architecture of the extended POS file format
dtyp_names = ['Reconstructed position along the x-axis (nm)', 
              'Reconstructed position along the y-axis (nm)', 
              'Reconstructed position along the z-axis (nm)', 
              'Reconstructed mass-to-charge-state ratio (Da)',
              'Raw time-of-flight (ns)',
              'Standing voltage (V)',
              'Pulsed voltage (V)',
              'Ion impact x-coordinate at the detector (mm)',
              'Ion impact y-coordinate at the detector (mm)',
              'Number of pulses since the last detected ion (pulses)',
              'Hit multiplicity (ions)']
#big-endian single precision floating point numbers and (unsigned) integers
dtyp_formats = ['>f4', '>f4', '>f4', '>f4','>f4','>f4','>f4','>f4','>f4','>u4','>u4']
 

epos = np.zeros( N, dtype={ 'names': dtyp_names, 
                           'formats': dtyp_formats } )

for i in np.arange(0,11):
    epos[dtyp_names[i]] = dummydata[:,i]

epos.tofile( eposfn )
