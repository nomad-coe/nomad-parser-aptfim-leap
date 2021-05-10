#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:56:07 2021
@author: kuehbach
convenience function to create a string from an array of unsigned 16-bit integers
"""

import numpy as np

def np_uint16_to_string( nparr ):
    str_parsed = ''
    for el in nparr:
        if el != 0: #'\x00'
            str_parsed += chr(el)
    return np.str(str_parsed)
