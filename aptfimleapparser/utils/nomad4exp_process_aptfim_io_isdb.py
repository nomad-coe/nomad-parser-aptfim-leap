#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:00:02 2021
@author: kuehbach
parser for content from the IVAS/APSuite 6 instrument database
processtype: experiment/collect
methodgroup: aptfim
methodtype: parser
methodvariant: isdb ###MK::give more detail what this format is
2021/05/04
"""

import os, sys, glob, re
import numpy as np

###MK::issues:
###MK::implement access to the ISDB database when FAIRmat gets funded
