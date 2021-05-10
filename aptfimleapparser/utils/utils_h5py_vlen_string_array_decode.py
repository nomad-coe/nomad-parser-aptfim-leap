#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:40:26 2021
@author: kuehbach
convenience function to decode HDF5 array of Fortran C1 null-terminated strings into a list of regular Python string
"""

def h5py_vlen_string_array_decode(bytesarr64):
    #h5r = h5py.File( mainfile, 'r')
    #a = h5r['MeasurementID1/Metadata/Sample/Material/Constituents/0/Elements'][:]
    #h5r.close()
    #bytesarr64 = a
    n = np.shape(bytesarr64)[0]
    lst = []
    for i in np.arange(0,n):
        lst.append( bytesarr64[i].tostring().decode('utf-8').replace('\x00','') )
    return lst
