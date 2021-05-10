#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:05:**
@author: kuehbach at fhi - berlin mpg de
"""

### components of a from nomad4exp_python_modules import *

class n4eKeyValue():
    def __init__(self, src=None, dscr=None, shp=None, dtyp=None, unit=None, val=None, info=None, *args, **kwargs):
        self.src = src
        self.dscr = dscr
        self.shp = shp
        self.dtyp = dtyp
        self.unit = unit
        self.val = val
        self.ifo = info

