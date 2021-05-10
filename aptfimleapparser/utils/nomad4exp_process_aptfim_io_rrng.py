#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuehbach at fhi - berlin . mpg . de
parser for file formats
processtype: post-processing/analyze
methodgroup: aptfim
methodtype: parser
methodvariant: rrng file format, ###MK::give more detail what this format is
2021/03/01
"""

import os, sys, glob, re
import numpy as np

from aptfimleapparser.utils.nomad4exp_keyvalue_struct import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *


class rrng_range():
    def __init__(self, i, line, ionnm_dict, *args, **kwargs):
        #i = 1
        #line = txt_stripped[fp]        
        #line = txt_stripped[85]
        self.id = None
        self.mqmin = None
        self.mqmax = None
        self.comp = []
        self.vol = None
        self.color = None
        tmp = re.split(r'[\s=]+', line)
        if tmp[0] == 'Range' + str(i) and len(tmp) >= 6:
            self.id = 'Range' + str(i)
        else:
            raise ValueError('RRNG file is corrupted in line for ' + line + ' for range keyword and/or insufficient number of key-value pairs !')
        ###MK::color field is an optional entry
        ###MK::D. J. Larson et al. 2013 book p253 report that
        ###MK::mqmin, mqmax, vol, ion composition is required, name and color fields are optional
        ###MK::'Range6 = 106.1250 213.4110 vol:0.00000 Name: Noise Color:0000FF'
        ###MK::'Range7 = 42.8160 43.3110 vol:0.04543 Al:1 O:1 Name: AlOLikely Color:00FFFF'
        ###MK::the Name: field is optional for giving ranges custom names.
        ###MK::custom ion names cannot be used to define ion types
        if tmp[-1].lower().startswith('color:') and len(re.split(r':', tmp[-1])[1]) == 6: ##MK::make more robust to handle optionality of color and 
            self.color = '#' + re.split(r':', tmp[-1])[1]
            #HEX_COLOR_REGEX = r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$' #replace r'^#( ...
            #regexp = re.compile(HEX_COLOR_REGEX)
            #if regexp.search(tmp[-1].split(r':')):
            #   return True
            #return False
        else:
            raise ValueError('RRNG file is corrupted in line ' + line + ' for color keyword !')
        if np.float64(tmp[1]) > 0.0 and np.float64(tmp[2]) > 0.0:
            if (np.float64(tmp[2]) - np.float64(tmp[1])) > np.float64(MQ_EPSILON):
                self.mqmin = tmp[1]
                self.mqmax = tmp[2]
            else:
                raise ValueError('RRNG file is corrupted in line ' + line + ' for mqmin <= mqmax !')
        else:
            raise ValueError('RRNG file is corrupted in line ' + line + ' for mqmax and/or mqmin <= 0.0 !')
        if tmp[3].lower().startswith('vol:'):
            V = re.split(r':', tmp[3])[1]
            if np.float64(V) > 0.0:
                self.vol = V
            else:
                Warning('RRNG file is corrupted in line ' + line + ' for volume <= 0.0 !')
        else:
            raise ValueError('RRNG file is corrupted in line ' + line + ' for volume keyword !')
        components = tmp[4:-1]
        for c in components:
            name_mult = re.split(r':+', c)
            if name_mult[0] in ionnm_dict['metadata']['ionnames'].values() and np.uint8(name_mult[1]) > 0:
                for j in np.arange(0,int(name_mult[1])):
                    self.comp.append( name_mult[0] )


class n4e_parser_aptfim_io_read_rrng():
    def __init__(self, fn, *args, **kwargs):
        """
        reads all content from a RRNG file
        in: string fn, name of file to be read
        out: class object instance representing content of rrng file
        """
        #specify which information content, (meta)data-wise an RRNG file holds to parse for/inform nomad
        self.a = {}
        self.a['metadata'] = {}
        self.a['metadata']['ionnames'] = {}
        self.a['metadata']['ranges'] = {}
        self.a['metadata']['species'] = {}
        #self.a['metadata']['colors'] = {}
         
        #read the ASCII textfile RRNG format and interpret it
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/usa_richland_pnnl/R31_06365-v02.rrng'
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/deu_duesseldorf_mpie/Se Ho Beispiel R5076_44076-v02.rrng'        
        #fnm = '/home/kuehbach/FHI_FHI_FHI/Paper/xxxx_ParaprobeAnalyticsAsAFairMatPlugin/research/aus_sydney_rielli_primig/R04_22071.RRNG'
        fnm = fn
        with open( fnm, mode='r', encoding='utf8' ) as rrngf: 
            txt = rrngf.read()
            
        #replace eventual windows line breaks with unix line feeds, ##MK::required for the splitting in next line to work
        txt = txt.replace('\r\n', '\n')
    
        #replace eventual comma decimal points by dots
        txt = txt.replace(',', '.')

        #strip empty lines and lines with comments (see D. J. Larson et al. book 2013)
        txt_stripped = [line for line in txt.split('\n') if line.strip() != '' and '#' not in line]
        del txt
        
        #the equivalent of a file respective line pointer, here an index which line we process
        fp = 0
        #parse ion names including real periodic table element names, as well as user specified ranges
        ###MK::needed because sometimes experimentalists hijack the RRNG file format to define custom names for post-processing certain regions of
        ###MK::a mass-to-charge-state spectrum
        #a = {}
        #a['metadata'] = {}
        #a['metadata']['ionnames'] = {}
        if txt_stripped[fp] == '[Ions]':
            fp += 1
            tmp = re.split(r'[\s=]+', txt_stripped[fp])
            if tmp[0] == 'Number' and np.int64(tmp[1]) > 0:
                Nions = int(tmp[1])
                fp += 1
                for i in np.arange(0,Nions):
                    tmp = re.split(r'[\s=]+', txt_stripped[fp+i])
                    if tmp[0] == 'Ion' + str(i+1) and type(tmp[1]) == str and len(tmp[1]) > 0:
                        self.a['metadata']['ionnames'][tmp[0]] = tmp[1]
                    else:
                        raise ValueError('RRNG file is corrupted because Ion*= line is incorrectly formatted !')
                fp += Nions
            else:
                raise ValueError('RRNG file is corrupted because [Ions] Number=* line is incorrectly formatted !')
        else:
            raise ValueError('RRNG file is corrupted because [Ions] list header is not at expected position !')

        #parse range specifications
        #a['metadata']['ranges'] = {}
        if txt_stripped[fp] == '[Ranges]':
            fp += 1
            tmp = re.split(r'[\s=]+', txt_stripped[fp])
            if tmp[0] == 'Number' and np.int64(tmp[1]) > 0:
                Nranges = int(tmp[1])
                fp += 1
                for i in np.arange(0,Nranges):
                    obj = None
                    obj = rrng_range(i+1, txt_stripped[fp+i], self.a)
                    if obj != None:
                        self.a['metadata']['ranges'][obj.id] = obj
                    else:
                        raise ValueError('RRNG file is corrupted because Range*= line is incorrectly formatted !')
                fp += Nranges
            else:
                raise ValueError('RRNG file is corrupted because [Ranges] Number=* line is incorrectly formatted !')
        else:
            raise ValueError('RRNG file is corrupted because [Ranges] list header is not at expected position !')
            
        #build NOMAD ion species
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
            #create an identifier
            hashvector = np.empty(0, dtype=np.uint16())
            for c in obj.comp:
                if c in element_symbols:
                    nprotons = element_z[element_symbols.index(c)]
                    nneutrons = 0 ###MK::rrng stores no isotope pieces of information
                else:
                    raise Warning('Skipping user type for now !')
                hashvector = np.append( hashvector, hash_isotope(nprotons, nneutrons) )
            hashvector = np.flip(np.sort(hashvector, kind='stable')) #[::-1] #stable descending sorting
            identifier = []
            for hv in hashvector:
                identifier.append(str(hv))                
            identifier = ','.join(identifier)
            #populate the species object
            iontype = ion()
            iontype.set_name( identifier )
            iontype.set_id( None ) 
            iontype.set_charge( 0 ) ###MK::RRNG file does not resolve the charge state !
            iontype.set_ivec( hashvector )          
            if identifier not in self.a['metadata']['species']:
                self.a['metadata']['species'][identifier] = iontype
                self.a['metadata']['species'][identifier].mq.append( [obj.mqmin, obj.mqmax] )
            else:
                #check if mass-to-charge-ratio interval does not overlap with one of the existent
                for ival in self.a['metadata']['species'][identifier].mq:
                    if obj.mqmax < ival[0] or obj.mqmin > ival[1]:
                        continue
                    else:
                        raise ValueError('RRNG file is corrupted because I found an overlapping mass-to-charge-state interval !')
                self.a['metadata']['species'][identifier].mq.append( [obj.mqmin, obj.mqmax] )
        #self.a['metadata']['species']

###MK::test
#parsedFile = n4e_parser_aptfim_io_read_rrng('')