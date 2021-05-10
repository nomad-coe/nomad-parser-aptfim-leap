#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:53:48 2021
@author: kuehbach at fhi - berlin mpg de
"""

### Python modules
#import os, sys, glob
#from pathlib import Path
import re, mmap

try:
    import numpy as np
except ImportError as e:
   raise ValueError('Install numpy Python package via e.g pip install numpy !')
try:
    import h5py as h5
except ImportError as e:
   raise ValueError('Install h5py Python package via e.g pip install h5py !')
try:
    import warnings
except ImportError as e:
    raise ValueError('Install warnings !')
try:
    import periodictable as pse
except ImportError as e:
   raise ValueError('Install periodictable Python package via e.g pip install periodictable !')
