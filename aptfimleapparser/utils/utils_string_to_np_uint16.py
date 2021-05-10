#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:57:42 2021
@author: kuehbach
convenience function to create an array of unsigned 16-bit integers from a string
"""

import numpy as np

def string_to_np_uint16( s, l ):
    if len(s) < l:
        #s = 'abc'
        #l = 32
        nparr = np.zeros( l, np.uint16 )
        for c in np.arange(0,len(s)):
            nparr[c] = ord(s[c])
        return nparr
    else:
        raise ValueError('Inputted string is longer than number of array elements !')
