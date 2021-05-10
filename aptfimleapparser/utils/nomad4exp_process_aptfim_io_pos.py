#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuehbach at fhi - berlin . mpg . de
parser for file formats
processtype: post-processing/analyze
methodgroup: aptfim
methodtype: parser
methodvariant: pos file format, ###MK::give more detail what this format is
2021/03/01
"""

import os, sys, glob, re
import numpy as np

from aptfimleapparser.utils.nomad4exp_keyvalue_struct import *
from aptfimleapparser.utils.nomad4exp_numpy_chunked_fromfile import *


class n4e_parser_aptfim_io_read_pos():
    def __init__(self, fn, *args, **kwargs):
        """
        reads all content from a POS file
        in: string fn, name of file to be read
        out: class object instance representing content of pos file
        """
        #specify which information content, (meta)data-wise a POS file holds to parse for/inform nomad
        self.a = {}
        self.a['metadata'] = {}
        self.a['data'] = {}
              
        #read the binary POS format and interpret it
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/usa_richland_pnnl/R31_06365-v02.pos'
        #fnm = '/home/kuehbach/FHI_FHI_FHI/Paper/xxxx_ParaprobeAnalyticsAsAFairMatPlugin/research/aus_sydney_rielli_primig/R04_22071.pos'
        fnm = '/home/kuehbach/GITHUB/NOMAD-COE/nomad-parser-aptfim-leap/tests/data/example.pos'
        #fnm = fn
        dtyp_names = ['Reconstructed position along the x-axis (nm)',
                      'Reconstructed position along the y-axis (nm)', 
                      'Reconstructed position along the z-axis (nm)', 
                      'Reconstructed mass-to-charge-state ratio (amu)']
        
        ###MK::POS file format does not store endianness information, assumption is big-endian, see https://doi.org/10.1007/978-1-4614-3436-8
        raw = np.fromfile( fnm, dtype= {'names': dtyp_names,
                                        'formats': ('>f4', '>f4', '>f4', '>f4') } )
        ###MK::used chunked loading
        
        ###MK::add data consistence checks
        refshape = np.shape(raw[dtyp_names[0]])
        for i in np.arange(1,len(dtyp_names)):
            if np.shape(raw[dtyp_names[i]]) != refshape:
                raise ValueError('POS file corrupted because data array shape inconsistencies exist for ' + dtyp_names[i] + ' !')
        
        ###MK::reduce memory footprint
        self.a['data']['IonPositions'] = n4eKeyValue( 'software', 'reconstructed positions along the x-, y-, and z-axis respectively', 
                                                     [refshape[0], 3], np.float32, 'nm', np.zeros((refshape[0], 3), dtype=np.float32), 
                                                     '!!! in most cases the unmodified reconstructed positions from IVAS/ AP Suite, however, sometimes people edit these columns !!!')
        self.a['data']['IonPositions'].val[:,0] = raw['Reconstructed position along the x-axis (nm)']
        self.a['data']['IonPositions'].val[:,1] = raw['Reconstructed position along the y-axis (nm)']
        self.a['data']['IonPositions'].val[:,2] = raw['Reconstructed position along the z-axis (nm)']
        self.a['data']['MassToChargeRatio'] = n4eKeyValue( 'software', 'reconstructed mass-to-charge-state ratio', refshape[0], np.float32, 'Da', 
                                                          raw['Reconstructed mass-to-charge-state ratio (amu)'], '!!! in most cases the quantity intended but sometimes people edit especially this column to store e.g. results of e.g. cluster search analyses where then the column encodes arbitrary cluster labels !!!')

###test
#a = n4e_parser_aptfim_io_read_pos('')
