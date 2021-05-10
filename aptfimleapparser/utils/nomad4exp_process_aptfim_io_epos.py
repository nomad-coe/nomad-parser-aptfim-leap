#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuehbach at fhi - berlin . mpg . de
parser for file formats
processtype: post-processing/analyze
methodgroup: aptfim
methodtype: parser
methodvariant: epos file format, ###MK::give more detail what this format is
2021/03/01
"""

import os, sys, glob, re
import numpy as np
#from pathlib import Path
#replace by packages later
#from ....fairmat_areab_parser.utils.nomad4exp_keyvalue_struct import n4eKeyValue
#basePath = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser'
#sys.path.append(basePath + '/utils/')
from aptfimleapparser.utils.nomad4exp_keyvalue_struct import *
from aptfimleapparser.utils.nomad4exp_numpy_chunked_fromfile import *

class n4e_parser_aptfim_io_read_epos():
    def __init__(self, fn, *args, **kwargs):
        """
        reads all content from an EPOS file
        in: string fn, name of file to be read
        out: class object instance representing content of epos file
        """
        #specify which information content, (meta)data-wise an EPOS file holds to parse for/inform nomad
        self.a = {}
        self.a['metadata'] = {}
        self.a['data'] = {}
        self.a['data']['x'] = n4eKeyValue()
        self.a['data']['y'] = n4eKeyValue()
        self.a['data']['z'] = n4eKeyValue()
        self.a['data']['mq'] = n4eKeyValue()
        self.a['data']['tof'] = n4eKeyValue()
        self.a['data']['vdc'] = n4eKeyValue()
        self.a['data']['vp'] = n4eKeyValue() ###MK::for laser runs, this is zero
        self.a['data']['xdet'] = n4eKeyValue()
        self.a['data']['ydet'] = n4eKeyValue()
        self.a['data']['delta_p'] = n4eKeyValue() ###MK::for multi-hit records, after the first record, this is zero
        self.a['data']['n_m'] = n4eKeyValue() ###MK::for multi-hit records, after the first record, this is zero
        ###MK::see book B. Gault, 2012 for details, 
        
        #read the binary POS format and interpret it
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/deu_duesseldorf_mpie/R18_53222_W_18K-v01.epos'
        fnm = fn
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
        raw = np.fromfile( fnm, dtype= {'names': dtyp_names,
                                        'formats': ('>f4', '>f4', '>f4', '>f4','>f4','>f4','>f4','>f4','>f4','>u4','>u4') } ) 
        ###MK::needs 'names': ('name1','name2'),
        ###MK::are the last u4 big-endian or just u4 ?
        ###MK::add data consistence checks
        refshape = np.shape(raw[dtyp_names[0]])
        for i in np.arange(1,len(dtyp_names)):
            if np.shape(raw[dtyp_names[i]]) != refshape:
                raise ValueError('POS file corrupted because data array shape inconsistencies exist for ' + dtyp_names[i] + ' !')
            
        ###MK::EPOS file format does not store endianness information, assumption is big-endian, see B. Gault et al. book 2012
        raw['Hit multiplicity (ions)']
        
    
###test
#parsedFile = n4e_parser_aptfim_io_read_epos('')


# import matplotlib.pyplot as plt
# #https://realpython.com/python-histograms/#histograms-in-pure-python
# n, bins, patches = plt.hist(x=raw['Hit multiplicity (ions)'], bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Multiplicity')
# plt.ylabel('Frequency')
# plt.title('Multiplicity plot')
# #plt.text(23, 45, r'$\mu=15, b=3$')
# #maxfreq = n.max()
# plt.yscale('log')
# ## Set a clean upper y-axis limit.
# #plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
