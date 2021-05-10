#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:38:46 2021
@author: kuehbach
convenience function to decode HDF5 Fortran C1 null-terminated string into a regular Python string
"""

def h5py_string_decode(astring):
    return str(astring).replace("b'",'').replace("'",'"').replace("\"",'')
