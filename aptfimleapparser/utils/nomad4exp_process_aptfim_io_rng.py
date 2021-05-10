#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuehbach at fhi - berlin . mpg . de
parser for file formats
processtype: post-processing/analyze
methodgroup: aptfim
methodtype: parser
methodvariant: rng file format, ###MK::give more detail what this format is
2021/03/01
"""

import os, sys, glob, re
import numpy as np

from aptfimleapparser.utils.nomad4exp_keyvalue_struct import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *


class rng_range():
    def __init__(self, i, line, c2l_dict, nc_constraint, *args, **kwargs):
        ###MK::next three lines only for debugging purposes
        #line = '. 107.7240 108.0960  1  0  0  0  0 0 0  0  0  0 3  0  0 0'
        #c2l_dict = col2lbl
        #nc_constraint = 17
        self.id = 'Range' + str(i)
        self.mqmin = None
        self.mqmax = None
        self.comp = []
        #self.color = None ###MK::do not parse out color for now
        tmp = re.split(r'\s+', line)
        if len(tmp) != nc_constraint:
            raise ValueError('RNG file is corrupted in line for ' + line + ' for inconsistent number of columns !')
        if tmp[0] != '.':
            raise ValueError('RNG file is corrupted in line for ' + line + ' for inconsistent prefix number of columns !')
        #tmp[1] is the mqmin
        #tmp[2] is the mqmax
        if np.float64(tmp[1]) > 0.0 and np.float64(tmp[2]) > 0.0:
            if (np.float64(tmp[2]) - np.float64(tmp[1])) > np.float64(MQ_EPSILON):
                self.mqmin = tmp[1]
                self.mqmax = tmp[2]
            else:
                raise ValueError('RNG file is corrupted in line ' + line + ' for mqmin <= mqmax !')
        else:
            raise ValueError('RNG file is corrupted in line ' + line + ' for mqmax and/or mqmin <= 0.0 !')
        flags_all = np.uint32(tmp[3:len(tmp)]) #this is the multiplicity vector
        flags_sum = np.sum(flags_all)
        #check that at least one flag is set
        if flags_sum == 0:
            raise ValueError('RNG file is corrupted in line ' + line + ' for no flag set !')
        for j in np.arange(0,len(flags_all)):
            if flags_all[j] == 0: #most flags are zero
                continue
            else:
                if flags_all[j] < 0:
                    raise ValueError('RNG file is corrupted in line ' + line + ' for negative flag value set !')
                for mult in np.arange(0,flags_all[j]):
                    #get the element number Z, as many times as multiplicity
                    self.comp.append( c2l_dict[j+1] )


class n4e_parser_aptfim_io_read_rng():
    def __init__(self, fn, *args, **kwargs):
        """
        reads all relevant non-duplicated content from a RNG file
        in: string fn, name of file to be read
        out: class object instance representing content of rng file
        """
        #specify which information content, (meta)data-wise an RNG file holds to parse for/inform nomad
        self.a = {}
        self.a['metadata'] = {}
        self.a['metadata']['ionnames'] = {}
        self.a['metadata']['ranges'] = {}
        self.a['metadata']['species'] = {}
        #self.a['metadata']['colors'] = {}
         
        #read the ASCII textfile RRNG format and interpret it
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/deu_duesseldorf_mpie/Se Ho Beispiel R5076_44076-v02.rng'
        fnm = fn
        with open( fnm, mode='r', encoding='utf8' ) as rngf: 
            txt = rngf.read()
            
        #replace eventual windows line breaks with unix line feeds, ##MK::required for the splitting in next line to work
        txt = txt.replace('\r\n', '\n')
    
        #replace eventual comma decimal points by dots
        txt = txt.replace(',', '.')

        #strip empty lines #and lines with comments (see D. J. Larson et al. book 2013)
        txt_stripped = [line for line in txt.split('\n') if line.strip() != ''] #and '#' not in line]
        del txt     
        
        #for a RNG range file only the first ------ line is relevant: this is the header of a table
        #which details all labels for species, RNG files created with AMETEK IVAS contain a trailing
        #polyatomic extension section with a similarly prefixed header line but this information
        #is insofar redundant as it specifies only a string representation of concatenated labels for species and their multiplicity
        #the multiplicity though is resolved already in the table below the first header line
        
        #first, find the this key header line
        tmp = None
        fp = 0
        for line in txt_stripped:
            tmp = re.search(r'----', line)
            if tmp == None:
                fp += 1
                continue
            else:
                #found the table, parse out the tokens to get the disjoint element names
                break
        if tmp == None:
            raise ValueError('RNG file is corrupted because key header line with labels of ion species not included !')
        
        #as soon as key header line was found, parse out all labels from this key header line
        tmp = re.split(r'\s+', txt_stripped[fp])
        if len(tmp) > 1:
            #at least we have one label and expect space-separated disjoint element names
            #lbl2col = {}
            col2lbl = {}
            for i in np.arange(1,len(tmp)):
                #lbl2col[tmp[i]] = i
                col2lbl[i] = tmp[i]
        else:
            raise ValueError('RNG file is corrupted because key header line with labels of ion species has no label !')
        
        #second, find how many mqmin, mqmax ranging interval definitions exist
        #to be consistent the number of such ranges needs to be specified in the first line of the RNG file via the second integer in this line
        tmp = re.split(r'\s+', txt_stripped[0]) ###MK::make regex more robust to include only numbers !
        if len(tmp) != 2 or np.int64(tmp[0]) < 1 or np.int64(tmp[1]) < 1:
            raise ValueError('RNG file is corrupted because the first line in an RNG range file has to give two integers, separated by spaces, first for labels of species, second for number of mq intervals')
        Ncolumns = int(tmp[0])+3
        Nmq = int(tmp[1])
        #read in these ranges now
        for i in np.arange(fp+1,fp+1+Nmq):
            obj = None
            obj = rng_range( i-fp, txt_stripped[i], col2lbl, Ncolumns )
            if obj != None:
                self.a['metadata']['ranges'][obj.id] = obj
            else:
                raise ValueError('RNG file is corrupted because a line with . mqmin mqmax and multiplicity vector is incorrectly formatted !')
            #print(txt_stripped[i])

        #third, build NOMAD ion species
        #b = aa.a
        #b['metadata']['species'] = {}
        #iontype_id = 1
        #usertype_id = 1
        element_symbols = [] #create lookup table for known elements
        element_z = []
        for el in pse.elements:
            element_symbols.append(el.symbol)
            element_z.append(el.number)
        for obj in self.a['metadata']['ranges'].values():
            #obj = b['metadata']['ranges']['Range65']         
            #create a unique identifier for molecular ions
            hashvector = np.empty(0, dtype=np.uint16())
            for c in obj.comp:
                if c in element_symbols:
                    nprotons = element_z[element_symbols.index(c)]
                    nneutrons = 0 ###MK::rng stores no isotope pieces of information
                else:
                    raise Warning('Skipping user type for now !')
                hashvector = np.append( hashvector, hash_isotope(nprotons, nneutrons) )
            hashvector = np.flip(np.sort(hashvector, kind='stable')) #stable descending sorting
            identifier = []
            for hv in hashvector:
                identifier.append(str(hv))
            identifier = ','.join(identifier)
            #populate the species object
            iontype = ion()
            iontype.set_name( identifier )
            iontype.set_id( None )
            iontype.set_charge = 0 ##MK::RRNG file does not resolve the charge state !
            iontype.set_ivec( hashvector ) ###MK::RRNG file format does not resolve isotope only element name !
            if identifier not in self.a['metadata']['species']:
                self.a['metadata']['species'][identifier] = iontype
                self.a['metadata']['species'][identifier].mq.append( [obj.mqmin, obj.mqmax] )
            else:
                #check if mass-to-charge-ratio interval does not overlap with one of the existent
                for ival in self.a['metadata']['species'][identifier].mq:
                    if obj.mqmax < ival[0] or obj.mqmin > ival[1]:
                        continue
                    else:
                        raise ValueError('RNG file is corrupted because I found an overlapping mass-to-charge-state interval !')
                self.a['metadata']['species'][identifier].mq.append( [obj.mqmin, obj.mqmax] )
        #self.a['metadata']['species']

###MK::test
#parsedFile = n4e_parser_aptfim_io_read_rng('')