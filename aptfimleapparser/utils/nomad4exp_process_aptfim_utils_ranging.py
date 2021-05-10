#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuehbach at fhi - berlin . mpg . de
utilities for parsing ranging definitions for aptfim
2021/03/02
"""

import os, sys, glob
#from pathlib import Path
import re, mmap
import numpy as np
import warnings
import periodictable as pse

#replace by packages later
#from ....fairmat_areab_parser.utils.nomad4exp_keyvalue_struct import n4eKeyValue
#basePath = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser'
#sys.path.append(basePath + '/utils/')
#from nomad4exp_python_modules import *
from aptfimleapparser.utils import nomad4exp_keyvalue_struct
##MK::move to the above module

#numerical constants
MQ_EPSILON = 1.0e-4
MAX_NUMBER_OF_ATOMS_PER_MOLECULAR_ION = 8

#https://stackoverflow.com/questions/3663450/remove-substring-only-at-the-end-of-string
def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s


def hash_isotope(Nprotons,Nneutrons):
    if Nprotons >= 0 and Nprotons < 256 and Nneutrons >= 0 and Nneutrons < 256:
        return np.uint16(Nprotons) + np.uint16(256)*np.uint16(Nneutrons)
    else:
        raise ValueError('Nprotons and Nneutrons need to be on interval [0, 256) !')


def unhash_isotope(hashval):
    if type(hashval) == np.uint16: #implicit on [0,2**16-1]
        Nneutrons = np.uint16(hashval / np.uint16(256))
        Nprotons = np.uint16(hashval - Nneutrons*np.uint16(256))
        return [Nprotons, Nneutrons]
    else:
        raise ValueError('Hashval needs to be a np.uint16 !')


class ion():
    def __init__(self, *args, **kwargs):
        self.name = None
        self.id = np.uint8(0)
        self.charge = np.int8(0)
        self.ivec = np.zeros( 32, np.dtype(np.uint16) ) #list of isotope hash values
        self.mq = [] #list of associated mass-to-charge state ratios in Da

    def set_name(self, nm):
        if nm == None:
            self.name = None
        else:
            if type(nm) == str and len(nm) > 0:
                self.name = np.str(nm)
            else:
                raise ValueError('Name has to be a string and must not be an empty string !')

    def set_id(self, id):
        if id == None:
            self.id = None
        else:
            if (id >= 0 and id < 256):
                self.id = np.uint8(id)
            else:
                raise ValueError('ID needs to be on [0, 255] !')

    def set_charge(self, chrg):
        if chrg == None:
            self.charge = np.int8(0)
        else:
            if np.int8(abs(chrg)) <= np.int8(8):
                self.charge = np.int8(chrg)
            else:
                raise ValueError('Charge needs to be on (-8,+8) !')
            
    def set_ivec(self, ivec):
        if len(np.shape(ivec)) == 1:
            if np.shape(ivec)[0] > 0 and np.shape(ivec)[0] <= MAX_NUMBER_OF_ATOMS_PER_MOLECULAR_ION:
                self.ivec = np.zeros( MAX_NUMBER_OF_ATOMS_PER_MOLECULAR_ION, np.dtype(np.uint16) )
                for i in np.arange(0,np.shape(ivec)[0]):
                    self.ivec[i] = np.uint16(ivec[0])
            else:
                raise ValueError('Isotope vector needs to be an uint16 array with at most ' + str(MAX_NUMBER_OF_ATOMS_PER_MOLECULAR_ION) + ' values !')
        else:
            raise ValueError('Isotope vector needs to be an uint16 array with at most ' + str(MAX_NUMBER_OF_ATOMS_PER_MOLECULAR_ION) + ' values !')
