#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuehbach at fhi - berlin . mpg . de
parser for file formats
processtype: post-processing/analyze
methodgroup: aptfim
methodtype: parser
methodvariant: apt6 file format, ###MK::give more detail what this format is
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
from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *
from aptfimleapparser.utils.utils_np_uint16_to_string import *
from aptfimleapparser.utils.utils_string_to_np_uint16 import *
from aptfimleapparser.utils.nomad4exp_numpy_chunked_fromfile import *


class apt6file_header_metadata():
    def __init__(self, cSignature=None, iHeaderSize=None, iHeaderVersion=None, wcFilename=None, ftCreationTime=None, llIonCount=None, *args, **kwargs):
        #self.a['sectionname'] = n4eKeyValue('software', 'APSuite/NOMAD resolved name of the section', 1, np.str(), None, None, None)
        self.a = {}
        self.a['cSignature'] = n4eKeyValue('software', 'AMETEK-way file format signature', 4*1, np.uint8(), None, cSignature, 'APT\0')
        self.a['iHeaderSize'] = n4eKeyValue('software', 'AMETEK-way byte length of the file header', 1, np.int32(), 'byte', iHeaderSize, '540 byte expected')
        self.a['iHeaderVersion'] = n4eKeyValue('software', 'AMETEK-way version number of the file header', 1, np.int32(), None, iHeaderVersion, 'currently expecting 2')
        self.a['wcFilename'] = n4eKeyValue('software', 'AMETEK-way string representation of the original file name', 256, np.uint16(), None, wcFilename, 'UTF-16 null terminated')
        self.a['ftCreationTime'] = n4eKeyValue('software','AMETEK-way of storing original file creation time', 1, np.uint64(), None, ftCreationTime, 'uint or int ???, FILETIME is a 64-bit value representing the number of 100-nanosecond intervals since January 1, 1601, per MSDN specification.')
        self.a['llIonCount'] = n4eKeyValue('software','AMETEK-way of number of ions represented by file', 1, np.int64(), None, llIonCount, None)

expected_header = apt6file_header_metadata( np.array([ord('A'), ord('P'), ord('T'), ord('\0')], dtype=np.uint8), 540, 2, None, None, None )

class apt6file_section_metadata():
    def __init__(self, sectionname=None, cSignature=None, iHeaderSize=None, iHeaderVersion=None, wcSectionType=None, iSectionVersion=None, eRelationshipType=None, 
                 eRecordType=None, eRecordDataType=None, iDataTypeSize=None, iRecordSize=None, wcDataUnit=None, llRecordCount=None, llByteCount=None, *args, **kwargs):
        ###MK::I follow here the AMETEK implementation definitions
        self.a = {}
        self.a['sectionname'] = n4eKeyValue('software','APSuite/NOMAD resolved name of the section', 1, np.str(), None, sectionname, None)
        self.a['cSignature'] = n4eKeyValue('software', 'AMETEK-way section format signature', 4*1, np.uint8(), None, cSignature, 'SEC\0')
        self.a['iHeaderSize'] = n4eKeyValue('software', 'AMETEK-way byte length of the section header', 1, np.int32(), 'byte', iHeaderSize, None)
        self.a['iHeaderVersion'] = n4eKeyValue('software', 'AMETEK-way version number of the section header', 1, np.int32(), None, iHeaderVersion, None)
        self.a['wcSectionType'] = n4eKeyValue('software', 'AMETEK-way string representation of the section header', 32, np.uint16(), None, wcSectionType, None)
        self.a['iSectionVersion'] = n4eKeyValue('software', 'AMETEK-way version of this section data', 1, np.int32(), None, iSectionVersion, None)
        self.a['eRelationshipType'] = n4eKeyValue('software', 'AMETEK-way enum value specifying how the records relate to ion #', 1, np.uint32(), None, eRelationshipType, '0 (unknown), 1 (one-to-one mapping), 2 (sparse 64bit ion index as first element), 3 (unrelated), 4 (first element is # of indices, then a list, then the record itself)')
        self.a['eRecordType'] = n4eKeyValue('software', 'AMETEK-way enum value specifying type of record', 1, np.uint32(), None, eRecordType, '0 (unknown), 1( vairable size), 2 (variable indexed)')
        self.a['eRecordDataType'] = n4eKeyValue('software', 'AMETEK-way enum value specifying data type of records', 1, np.uint32(), None, eRecordDataType, '0 (unknown), 1 (int, iDataTypeSize 8, 16, 32, or 64), 2 (uint, iDataTypeSize arbitrary can bit pack within records), 3 (IEEE float 32 or 64), 4 (char string, iDataTypeSize 8, 16, iRecordSize of 0 is null terminated; iRecordSize > 0 is fixed length), 5 (other)')
        self.a['iDataTypeSize'] = n4eKeyValue('software', 'AMETEK-way size in bits of data type', 1, np.int32(), 'bit', iDataTypeSize, None)
        self.a['iRecordSize'] = n4eKeyValue('software', 'AMETEK-way size of the record (bytes) ', 1, np.int32(), 'byte', iRecordSize, 'this must be a multiple of iDataTypeSize and 8, or 0 for variable length')
        self.a['wcDataUnit'] = n4eKeyValue('software', 'AMETEK-way string representation the unit of the data', 16, np.uint16(), None, wcDataUnit, None)
        self.a['llRecordCount'] = n4eKeyValue('software', 'AMETEK-way number of records following this header', 1, np.int64(), None, llRecordCount, '!!! do not use for seeking to next section, use llByteCount')
        self.a['llByteCount'] = n4eKeyValue('software', 'AMETEK-way number of bytes following the header', 1, np.int64(), None, llByteCount, '!!! this may be > llRecordCount * iRecordSize to allow for padding')

        
expected_sections = {}
#fieldname communicated F. F. M. de Oliveira, MPIE, 2021/03/01
#{'z'}    {'tof'}    {'Voltage'}    {'pulse'}    {'freq'}    {'tElapsed'}    {'erate'}    {'xstage'}    {'ystage'}    {'zstage'}    {'tstage'}
#{'TargetErate'}    {'TargetFlux'}    {'pulseDelta'}    {'Pres'}    {'VAnodeMon'}    {'Temp'}    {'AmbTemp'}    {'laserx'}    {'lasery'}
#{'laserz'}    {'laserpower'}    {'FractureGuard'}    {'Noise'}    {'Uniformity'}    {'Mass'}    {'tofc'}    {'tofb'}    {'xs'}    {'ys'}
#{'zs'}    {'rTip'}    {'zApex'}    {'zSphereCorr'}    {'Position_0'}    {'Position_1'}    {'Position_2'}    {'XDet_mm'}    {'YDet_mm'}
#{'Multiplicity'}    {'Vap'}    {'DetectorCoordin…'}    {'DetectorCoordin…'}    {'Var44'}
expected_sections['z'] = apt6file_section_metadata('z', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('z', 32), 1, 1, 1, 1, 64, 8, string_to_np_uint16('ions', 16), None, None)
expected_sections['tof'] = apt6file_section_metadata('tof', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('tof', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('ns', 16), None, None)
expected_sections['Voltage'] = apt6file_section_metadata('pulse', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Voltage', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None) #new fieldname as communicated by F. F. M. de Oliveira MPIE
###MK::would have expected that Voltage has units but current flat test shows these are not shown
expected_sections['pulse'] = apt6file_section_metadata('pulse', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('pulse', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['freq'] = apt6file_section_metadata('freq', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('freq', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('Hz', 16), None, None)
expected_sections['tElapsed'] = apt6file_section_metadata('tElapsed', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('tElapsed', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['erate'] = apt6file_section_metadata('erate', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('erate', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('%/100', 16), None, None)
expected_sections['xstage'] = apt6file_section_metadata('xstage', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('xstage', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['ystage'] = apt6file_section_metadata('ystage', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('ystage', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['zstage'] = apt6file_section_metadata('zstage', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('zstage', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['tstage'] = apt6file_section_metadata('tstage', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('tstage', 32), 1, 1, 1, 2, 16, 2, string_to_np_uint16('', 16), None, None)
expected_sections['TargetErate'] = apt6file_section_metadata('TargetErate', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('TargetErate', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('%/100', 16), None, None)
expected_sections['TargetFlux'] = apt6file_section_metadata('TargetFlux', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('TargetFlux', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['pulseDelta'] = apt6file_section_metadata('pulseDelta', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('pulseDelta', 32), 1, 1, 1, 1, 16, 2, string_to_np_uint16('', 16), None, None)
expected_sections['Pres'] = apt6file_section_metadata('Pres', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Pres', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('torr', 16), None, None)
expected_sections['VAnodeMon'] = apt6file_section_metadata('VAnodeMon', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('VAnodeMon', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['Temp'] = apt6file_section_metadata('Temp', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Temp', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('K', 16), None, None)
expected_sections['AmbTemp'] = apt6file_section_metadata('AmbTemp', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('AmbTemp', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('C', 16), None, None)
expected_sections['laserx'] = apt6file_section_metadata('laserx', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('laserx', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None) #new field
expected_sections['lasery'] = apt6file_section_metadata('lasery', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('lasery', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None) #new field
expected_sections['laserz'] = apt6file_section_metadata('laserz', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('laserz', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None) #new field
expected_sections['laserpower'] = apt6file_section_metadata('laserpower', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('', 16), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None) #new field
expected_sections['FractureGuard'] = apt6file_section_metadata('FractureGuard', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('laserpower', 32), 1, 1, 1, 2, 16, 2, string_to_np_uint16('', 16), None, None)
expected_sections['Noise'] = apt6file_section_metadata('Noise', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Noise', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['Uniformity'] = apt6file_section_metadata('Uniformity', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Uniformity', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['Mass'] = apt6file_section_metadata('Mass', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Mass', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('Da', 16), None, None)
expected_sections['tofc'] = apt6file_section_metadata('tofc', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('tofc', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('ns', 16), None, None)
expected_sections['tofb'] = apt6file_section_metadata('tofb', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('tofb', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('ns', 16), None, None)
expected_sections['xs'] = apt6file_section_metadata('xs', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('xs', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('nm', 16), None, None)
expected_sections['ys'] = apt6file_section_metadata('ys', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('ys', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('nm', 16), None, None)
expected_sections['zs'] = apt6file_section_metadata('zs', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('zs', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('nm', 16), None, None)
expected_sections['rTip'] = apt6file_section_metadata('rTip', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('rTip', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('nm', 16), None, None)
expected_sections['zApex'] = apt6file_section_metadata('zApex', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('zApex', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('nm', 16), None, None)
expected_sections['zSphereCorr'] = apt6file_section_metadata('zSphereCorr', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('zSphereCorr', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('nm', 16), None, None)
expected_sections['Position_0'] = apt6file_section_metadata('Position', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148+6*4, 2, 
        string_to_np_uint16('Position_0', 32), 1, 1, 1, 3, 32, 12, string_to_np_uint16('', 16), None, None) #three new fields for in replacement for position
expected_sections['Position_1'] = apt6file_section_metadata('Position', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148+6*4, 2, 
        string_to_np_uint16('Position_1', 32), 1, 1, 1, 3, 32, 12, string_to_np_uint16('', 16), None, None)
expected_sections['Position_2'] = apt6file_section_metadata('Position', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148+6*4, 2, 
        string_to_np_uint16('Position_2', 32), 1, 1, 1, 3, 32, 12, string_to_np_uint16('', 16), None, None)
expected_sections['XDet_mm'] = apt6file_section_metadata('XDet_mm', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('XDet_mm', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('mm', 16), None, None)
expected_sections['YDet_mm'] = apt6file_section_metadata('YDet_mm', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('YDet_mm', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('mm', 16), None, None)
expected_sections['Multiplicity'] = apt6file_section_metadata('Multiplicity', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Multiplicity', 32), 1, 1, 1, 1, 32, 4, string_to_np_uint16('', 16), None, None)
expected_sections['Vap'] = apt6file_section_metadata('Vap', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Vap', 32), 1, 1, 1, 3, 32, 4, string_to_np_uint16('V', 16), None, None)
expected_sections['Detector Coordinates'] = apt6file_section_metadata('Detector Coordinates', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Detector Coordinates', 32), 1, 1, 1, 3, 32, 8, string_to_np_uint16('mm', 16), None, None) #two new fields for posuitions in replacement for position
#expected_sections['Detector Coordinates'] = apt6file_section_metadata('Detector Coordinates', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
#        string_to_np_uint16('Detector Coordinates', 32), 1, 1, 1, 3, 32, 8, string_to_np_uint16('', 16), None, None) #two new fields for posuitions in replacement for position
###MK::magic section, likely a section for development purposes, here we will not parse it
expected_sections['Var44'] = apt6file_section_metadata('Var44', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
        string_to_np_uint16('Var44', 32), 1, 1, 1, 3, 32, 8, string_to_np_uint16('', 16), None, None) #two new fields for posuitions in replacement for position
expected_sections['Position'] = apt6file_section_metadata('Position', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148+6*4, 2, 
        string_to_np_uint16('Position', 32), 1, 1, 1, 3, 32, 12, string_to_np_uint16('nm', 16), None, None) #F. M. M. de Oliveira reported this to be deprecated but here I find it now for a flat test weird ##MK..
###MK::so for flat test data it seems that one can export a section named 'Position' but this has then no leading or trailing 6*np.float32 to give the #
###MK::maximum positions of the reconstructed coordinates, so it seems that this field is adaptive wrt to whether a reconstruction was perform or not
###MK::148+6*4
#expected_sections['Vref'] = apt6file_section_metadata('Vref', np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8), 148, 2, 
#        'ADD', 1, 1, 1, 3, 32, 4, 'ADD', None, None) #deprecated, likely the one replaced by Voltage


def apt6_read_section_data_fixed_onetoone(fid, llIonCount, section_info ):
    ###MK::currently the section Position is the only one with an extra header of six floats to give the AABB to the reconstructed positions
    ###MK::next two lines only for debugging, extra header handling of 'Position' section
    #llIonCount = header.a['llIonCount'].val
    #section_info = sect
    if section_info.a['sectionname'].val == 'Position':
        #tipbox = np.reshape(np.fromfile( fid, np.float32, count = int(2*3) ), (int(2), int(3) ), order='C') #old alignment
        tipbox = np.reshape(np.fromfile( fid, np.float32, count = int(3*2) ), (int(3), int(2) ), order='C') #new alignment
        print('Tip AABB')
        print(tipbox)
        
    #which datatype to use, interpret from the section header
    #llIonCount = 782
    #section_info = sect
    ni = np.int64(llIonCount)
    print('ni ' + str(ni))
    nj = np.int64(np.int64(section_info.a['iRecordSize'].val) / (np.int64(section_info.a['iDataTypeSize'].val)/np.int64(8)))
    print('nj ' + str(nj))
    dtyp = None #eRecordDataType == 3 and iDataTypeSize == 32
    bytelength = section_info.a['iDataTypeSize'].val/8
    if section_info.a['eRecordDataType'].val == 1: #integers
        if bytelength == 2:
            dtyp = np.int16
        elif bytelength == 4:
            dtyp = np.int32
        elif bytelength == 8:
            dtyp = np.int64
        else:
            raise ValueError('APT6 file parsing problem, unknown eRecordDataType for integers when reading section ' + section_info.a['sectionname'].val + ' !')
    elif section_info.a['eRecordDataType'].val == 2:
        ###MK::currently only one type used uint16
        dtyp = np.uint16
    elif section_info.a['eRecordDataType'].val == 3:
        dtyp = np.float32
    else:
        raise ValueError('APT6 file parsing problem, unknown eRecordDataType for every known type when reading section ' + section_info.a['sectionname'].val + ' !')
    #print(dtyp)
    ##MK::stop when this can not be read
    #fp_current = fid.tell()
    #fp_end = fid.seek(0,os.SEEK_END)
    #fid.seek(fp_current, os.SEEK_SET)
    #if (fp_end - fp_current) >= ni*nj:
    #print('fp_current:\t\t\t' + str(fp_current))
    #print('fp_end:\t\t\t\t' + str(fp_end))
    #print('ni*nj:\t\t\t\t' + str(ni*nj))
    #print('np.int64(ni*nj):\t' + str(np.int64(ni*nj)))
    #print(dtyp)
    #myarr = np_chunked_reading(fid, dtyp, bytelength, ni, nj)
    #return myarr
    
    print('Chunked reading from file pointer byte position ' + str(fid.tell()))
    nrows = ni
    ncols = nj
    ret = np.zeros([nrows, ncols], dtype=dtyp)    
    nrows_curr = 0
    nrows_read = 0
    while True:
        nrows_curr = int(CHUNK_SIZE/(bytelength*ncols))
        if (nrows_read + nrows_curr) < nrows:
            #print(str(nrows_curr))
            #print('Byte position ' + str(fid.tell()))
            nparr = np.fromfile(fid, dtype=dtyp, count = int(nrows_curr*ncols))
            #print(nparr)
            #catch cases where APT6 file is incomplete
            nrows_now = nrows_curr
            ncols_now = ncols
            #print('np.shape(nparr)[0]')
            #print(np.shape(nparr))
            if np.shape(nparr)[0] != nrows_now*ncols_now:
                if np.shape(nparr)[0] % ncols == 0:
                    nrows_now = int(np.shape(nparr)[0])/int(ncols)
                    ncols_now = int(ncols)
                else:
                    raise ValueError('Chunked reading read-in array object has an unexpected number of elements, APT6 is likely corrupted !')
            ret[int(nrows_read):int(nrows_read)+int(nrows_now),:] = np.reshape( nparr, (int(nrows_now), int(ncols_now)), order='C')
            #print('nparr: ' + str(np.shape(nparr)[0]))
            nrows_read += nrows_now
        else:
            nrows_curr = nrows - nrows_read
            #print('Byte position ' + str(fid.tell()))
            nparr = np.fromfile(fid, dtype=dtyp, count = int(nrows_curr*ncols))
            #print(nparr)
            #catch cases where APT6 file is incomplete
            nrows_now = nrows_curr
            ncols_now = ncols
            #print('np.shape(nparr)[0]')
            #print(np.shape(nparr))
            if np.shape(nparr)[0] != nrows_now*ncols_now:
                if np.shape(nparr)[0] % ncols == 0:
                    nrows_now = int(np.shape(nparr)[0])/int(ncols)
                    ncols_now = int(ncols)
                else:
                    raise ValueError('Chunked reading read-in nparray object has an unexpected number of elements, APT6 is likely corrupted !')
            ret[int(nrows_read):int(nrows_read)+int(nrows_now),:] = np.reshape( nparr, (int(nrows_now), int(ncols_now)), order='C')
            #print('nparr: ' + str(np.shape(nparr)[0]))
            nrows_read += nrows_now
            #ret[nrows_read:nrows_read+nrows_curr,:] = np.reshape(np.fromfile(fid, dtyp, count = np.int64(nrows_curr*ncols)), 
            #                                                     (np.int64(nrows_curr), np.int64(ncols)), order='C')
            #print(str(nrows_curr))
            #nrows_read += nrows_curr
            return ret
    return ret
    
    #nparr = np.fromfile(fid, dtyp, count = np.int64(ni*nj)) #, (np.int64(ni*nj), np.int64(1)), order='C')
    ##MK::we need to wrap the call to np.fromfile via chunking
    #arr = np.fromfile(fid, dtyp, count = np.int64(ni*nj))
    #print('arr: ' + str(np.shape(arr)[0]))
    #return np.reshape(arr, (np.int64(ni), np.int64(nj)), order='C')
    #return np.reshape(np.fromfile(fid, dtyp, count = np.int64(ni*nj)), (np.int64(ni), np.int64(nj)), order='C') ###MK::likely the interleave alignment has been swopped here as well from the old to the new for position, needs to be tested !!
    #else:
    #    return None

class n4e_parser_aptfim_io_read_apt6():
    def __init__(self, fn, *args, **kwargs):
        """
        reads all content from an APT6 file, the format introduced by AMETEK with APSuite6 aka IVAS4
        in: string fn, name of file to be read
        out: class object instance representing content of apt6 file
        """
        #specify which information content, (meta)data-wise an APT6 file holds to parse for/inform nomad
        self.a = {}
        self.a['metadata'] = {}        
        self.a['data'] = {}
        #see M. K\"uhbach et al. ,npj Comp Mat, 2021 for further details
              
        #read the binary APT6 format and interpret it
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/deu_duesseldorf_mpie/FlatTest_f903a3f2-6aa0-4019-9890-3c983b43d513.apt'
        #fnm = '/home/kuehbach/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser/tutorials/aptfim/examples/deu_duesseldorf_mpie/c2fe4adf-f6f4-44aa-b6ec-76345fe88269.apt'
        fnm = fn
        #file_stats = os.stat(fnm)
        #print(file_stats)
        #print('File Size is ' + str(file_stats.st_size) + ' Bytes')
        
        fid = open(fnm, 'rb')
        ###MK::implicitly advancing the file pointer !
        
        #first, read the file header
        header = apt6file_header_metadata()
        ht = np.dtype( [('cSignature', np.uint8, (4,)), ('iHeaderSize', np.int32), ('iHeaderVersion', np.int32), 
                       ('wcFilename', np.uint16, 256), ('ftCreationTime', np.uint64), ('llIonCount', np.uint64)] )
        tmp = np.fromfile( fid, ht, count = 1 )
        expected = expected_header.a['cSignature'].val
        if np.all(tmp['cSignature'].flatten() == expected):
            header.a['cSignature'].val = tmp['cSignature'].flatten()
        else:
            print(np_uint16_to_string(tmp['cSignature'].flatten()))
            raise ValueError('APT6 file is corrupted, file header field cSignature not matching expectation !')
        expected = expected_header.a['iHeaderSize'].val
        if tmp['iHeaderSize'][0] == expected:
            header.a['iHeaderSize'].val = tmp['iHeaderSize'][0]
        else:
            print(str(tmp['iHeaderSize'][0]))
            raise ValueError('APT6 file is not parseable, file header field iHeaderSize is unexpectedly different !')
        expected = expected_header.a['iHeaderVersion'].val
        if tmp['iHeaderVersion'][0] == expected:
            header.a['iHeaderVersion'].val = tmp['iHeaderVersion'][0]
        else:
            print(str(tmp['iHeaderVersion'][0]))
            raise ValueError('APT6 file is not parseable, file header field iHeaderVersion is unexpectedly different !')
        ###MK::parsing UTF-16 works currently only for the lower bit, for the APTV2 draft specification this is not a problem
        ###MK::because currently the internal section identifiers use only UTF-8 characters
        header.a['wcFilename'].val = tmp['wcFilename'].flatten()
        header.a['ftCreationTime'].val = tmp['ftCreationTime'][0]
        if tmp['llIonCount'][0] > 0:
            header.a['llIonCount'].val = tmp['llIonCount'][0]
        else:
            raise ValueError('APT6 file is parseable but file header field llIonCount indicates there are 0 ions !')
            
        self.a['metadata']['file_header'] = header.a
        print('APT file ' + fnm)
        print('File header successfully parsed, indicating ' + str(header.a['llIonCount'].val) + ' ions in the dataset')
        
        #keep track which sections we visited
        visited = {}
        for key in expected_sections.keys():
            visited[key] = False
            
        #second, keep reading sections until there are none left        
        #for ii in np.arange(0,35):
        while not all(val == True for val in visited.values()):
            sect = apt6file_section_metadata()
            ht = np.dtype([('cSignature', np.int8, (4,)), ('iHeaderSize', np.int32), ('iHeaderVersion', np.int32), ('wcSectionType', np.uint16, 32), ('iSectionVersion', np.int32), 
                           ('eRelationshipType', np.uint32), ('eRecordType', np.uint32), ('eRecordDataType', np.uint32), ('iDataTypeSize', np.int32), ('iRecordSize', np.int32), 
                           ('wcDataUnit', np.uint16, 16), ('llRecordCount', np.uint64), ('llByteCount', np.uint64)])
            #fish the next section header from the file stream
            tmp = np.fromfile( fid , ht, count = 1 )
            if len(tmp['cSignature']) == 0: ###MK::currently this is a weak break criterion
                break
            expected = np.array([ord('S'), ord('E'), ord('C'), ord('\0')], dtype=np.uint8)
            if np.all(tmp['cSignature'].flatten() == expected):
                sect.a['cSignature'].val = tmp['cSignature'].flatten()
            else:
                print('cSignature: ' + np_uint16_to_string(tmp['cSignature'].flatten()))
                raise ValueError('APT6 file is corrupted, section header field cSignature not matching expectation !')
            sect.a['sectionname'].val = np_uint16_to_string( tmp['wcSectionType'].flatten() )
            
            #for each section, first check if this is a section that is formatted in a way the current parser implementation can understand
            if sect.a['sectionname'].val in expected_sections.keys():
                curr_section_name = sect.a['sectionname'].val
                print('Verifying metadata from section header for section ' + curr_section_name + '...')
                if visited[curr_section_name] == False:
                    visited[curr_section_name] = True
                    #print(np_uint16_to_string(tmp['wcDataUnit'].flatten()))
                    #for j in np.arange(0,len(tmp)):
                    #    print(tmp[j])
                    #    print('\n')
                    print('wcSectionType: ' + np_uint16_to_string(tmp['wcSectionType'].flatten()))
                    expected = string_to_np_uint16(sect.a['sectionname'].val, sect.a['wcSectionType'].shp)
                    if np.all(tmp['wcSectionType'].flatten() == expected):
                        sect.a['wcSectionType'].val = tmp['wcSectionType'].flatten()
                    else:
                        print('wcSectionType: ' + np_uint16_to_string(tmp['wcSectionType'].flatten()))
                        raise ValueError('APT6 file is corrupted, section header field wcSectionType not matching expectation !')
                    print('iHeaderSize: ' + str(tmp['iHeaderSize'][0]))
                    expected = expected_sections[curr_section_name].a['iHeaderSize'].val
                    if tmp['iHeaderSize'][0] == expected:
                        sect.a['iHeaderSize'].val = tmp['iHeaderSize'][0]
                    else:
                        print('iHeaderSize: ' + str(tmp['iHeaderSize'][0]))
                        raise ValueError('APT6 file is parseable but section header field iHeaderSize does not match expectation !')
                    print('iHeaderVersion: ' + str(tmp['iHeaderVersion'][0]))
                    expected = expected_sections[curr_section_name].a['iHeaderVersion'].val
                    if tmp['iHeaderVersion'][0] == expected:
                        sect.a['iHeaderVersion'].val == tmp['iHeaderVersion'][0]
                    else:
                        print('iHeaderVersion: ' + str(tmp['iHeaderVersion'][0]))
                        raise ValueError('APT6 file is parseable but section header field iHeaderVersion does not match expectation !')
                    print('iSectionVersion: ' + str(tmp['iSectionVersion'][0]))
                    expected = expected_sections[curr_section_name].a['iSectionVersion'].val
                    if tmp['iSectionVersion'][0] == expected:
                        sect.a['iSectionVersion'].val = tmp['iSectionVersion'][0]
                    else:
                        print('iSectionVersion: ' + str(tmp['iSectionVersion'][0]))
                        raise ValueError('APT6 file is parseable but section header field iSectionVersion does not match expectation !')
                    print('eRelationshipType: ' + str(tmp['eRelationshipType'][0]))
                    expected = expected_sections[curr_section_name].a['eRelationshipType'].val
                    if tmp['eRelationshipType'][0] == expected:
                        sect.a['eRelationshipType'].val = tmp['eRelationshipType'][0]
                    else:
                        print('eRelationshipType: ' + str(tmp['eRelationshipType'][0]))
                        raise ValueError('APT6 file is parseable but section header field eRelationshipType does not match expectation !')
                    print(str(tmp['eRecordType'][0]))
                    expected = expected_sections[curr_section_name].a['eRecordType'].val
                    if tmp['eRecordType'][0] == expected:
                        sect.a['eRecordType'].val = tmp['eRecordType'][0]
                    else:
                        print(str(tmp['eRecordType'][0]))
                        raise ValueError('APT6 file is parseable but section header field eRecordType does not match expectation !')
                    print('eRecordDataType: ' + str(tmp['eRecordDataType'][0]))
                    expected = expected_sections[curr_section_name].a['eRecordDataType'].val
                    if tmp['eRecordDataType'][0] == expected:
                        sect.a['eRecordDataType'].val = tmp['eRecordDataType'][0]
                    else:
                        print('eRecordDataType: ' + str(tmp['eRecordDataType'][0]))
                        raise ValueError('APT6 file is parseable but section header field eRecordDataType does not match expectation !')
                    print('iDataTypeSize: ' + str(tmp['iDataTypeSize'][0]))
                    expected = expected_sections[curr_section_name].a['iDataTypeSize'].val
                    if tmp['iDataTypeSize'][0] == expected:
                        sect.a['iDataTypeSize'].val = tmp['iDataTypeSize'][0]
                    else:
                        print('iDataTypeSize: ' + str(tmp['iDataTypeSize'][0]))
                        raise ValueError('APT6 file is parseable but section header field iDataTypeSize does not match expectation !')
                    print('iRecordSize: ' + str(tmp['iRecordSize'][0]))
                    expected = expected_sections[curr_section_name].a['iRecordSize'].val
                    if tmp['iRecordSize'][0] == expected:
                        sect.a['iRecordSize'].val = tmp['iRecordSize'][0]
                    else:
                        print('iRecordSize: ' + str(tmp['iRecordSize'][0]))
                        raise ValueError('APT6 file is parseable but section header field iRecordSize does not match expectation !')
                    print(np_uint16_to_string(tmp['wcDataUnit'].flatten()))
                    expected = expected_sections[curr_section_name].a['wcDataUnit'].val
                    if np.all(tmp['wcDataUnit'].flatten() == expected):
                        sect.a['wcDataUnit'].val = tmp['wcDataUnit'].flatten()
                    else:
                        print(np_uint16_to_string(tmp['wcDataUnit'].flatten()))
                        raise ValueError('APT6 file is parseable but section header field wcDataUnit does not match expectation !')
                    print(tmp['llRecordCount'][0])
                    sect.a['llRecordCount'].val = tmp['llRecordCount'][0]
                    ###MK::test implementation remaining
                    print(tmp['llByteCount'][0])
                    sect.a['llByteCount'].val = tmp['llByteCount'][0]
                    print('File section ' + curr_section_name + ' metadata successfully parsed')
                    ###MK::implement checks
                    
                    #for each section read out binary data only if we have really understood the formatting of the section
                    #read numerical data
                    self.a['metadata'][curr_section_name] = sect.a
                    self.a['data'][curr_section_name] = apt6_read_section_data_fixed_onetoone(fid, header.a['llIonCount'].val, sect)
                    print('File section ' + curr_section_name + ' numerical data successfully parsed')
                    #print(np.shape(a['data'][curr_section_name]))
                else:
                    raise Warning('APT file is likely corrupted because I came across an already visited section !')
                    break
            else:
                raise ValueError('APT6 file is parseable but we found a section that is unexpected (not supported by current parser implementation) !')
            

###test
#parsedFile = n4e_parser_aptfim_io_read_apt6('')

#print(str(np.min(parsedFile.a['data']['laserpower'])) + '\t' + str(np.max(parsedFile.a['data']['laserpower'])))



# s = ''
# for k in dict_kwnsect.keys():
#     s += 'expected_sections[' + '\'' + dict_kwnsect[k] + '\'' + '] = apt6file_section_metadata(' + '\'' + dict_kwnsect[k] + '\'' + ', ' + str(dict_iHeaderSize[k]) + ', ' + str(dict_iHeaderVersion[k]) + ', \'ADD\'' + ', ' + str(dict_iSectionVersion[k]) + ', ' + str(dict_eRelationshipType[k]) + ', ' + str(dict_eRecordType[k]) + ', ' + str(dict_eRecordDataType[k]) + ', ' + str(dict_iDataTypeSize[k]) + ', ' + str(dict_iRecordSize[k]) + ', \'ADD\'' + ', ' + 'xxxx)' + '\n'
        
# dict_kwnsect = {  1: 'tof', 2: 'pulse', 3: 'freq', 4: 'tElapsed', 5: 'erate', 6: 'tstage', 7: 'TargetErate',
#                          8: 'TargetFlux', 9: 'pulseDelta', 10: 'Pres', 11: 'VAnodeMon', 12: 'Temp', 13: 'AmbTemp', 14: 'FractureGuard',
#                          15: 'Vref', 16: 'Noise', 17: 'Uniformity', 18: 'xstage', 19: 'ystage', 20: 'zstage', 21: 'z', 22: 'tofc', 23: 'Mass', 24: 'tofb',
#                          25: 'xs', 26: 'ys', 27: 'zs', 28: 'rTip', 29: 'zApex', 30: 'zSphereCorr', 31: 'XDet_mm', 32: 'YDet_mm', 33: 'Multiplicity',
#                          34: 'Vap', 35: 'Detector Coordinates', 36: 'Position'}
        
# dict_sectionid = { 'Failure': 0, 
#                         'tof': 1, 'pulse': 2, 'freq': 3, 'tElapsed': 4, 'erate': 5, 'tstage': 6, 'TargetErate': 7,
#                         'TargetFlux': 8, 'pulseDelta': 9, 'Pres': 10, 'VAnodeMon': 11, 'Temp': 12, 'AmbTemp': 13, 'FractureGuard': 14,
#                         'Vref': 15, 'Noise': 16, 'Uniformity': 17, 'xstage': 18, 'ystage': 19, 'zstage': 20, 'z': 21, 'tofc': 22, 'Mass': 23, 'tofb': 24,
#                         'xs': 25, 'ys': 26, 'zs': 27, 'rTip': 28, 'zApex': 29, 'zSphereCorr': 30, 'XDet_mm': 31, 'YDet_mm': 32, 'Multiplicity': 33,
#                         'Vap': 34, 'Detector Coordinates': 35, 'Position': 36 }
                
# dict_iHeaderSize = all 148 except for 36 148+6*4 { 1: 148, 2: 148, 3: 148, 4: 148, 5: 148, 6: 148, 7: 148,  8: 148, 9: 148, 10: 148, 11: 148, 12: 148, 13: 148, 14: 148, 
#                      15: 148, 16: 148, 17: 148, 18: 148, 19: 148, 20: 148, 21: 148, 22: 148, 23: 148, 24: 148,   25: 148, 26: 148, 27: 148, 28: 148, 29: 148, 30: 148, 
#                      31: 148, 32: 148, 33: 148, 34: 148, 35: 148, 36: 148+6*4 }

# dict_iHeaderVersion = all 2 { 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2,  15: 2, 16: 2, 17: 2, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 
#                              23: 2, 24: 2, 25: 2, 26: 2, 27: 2, 28: 2, 29: 2, 30: 2, 31: 2, 32: 2, 33: 2, 34: 2, 35: 2, 36: 2 }

# dict_iSectionVersion = all 1 { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 
#                         23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1 }

# dict_eRelationshipType = all 1 { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 
#                                 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1 }

# dict_eRecordType = all 1 { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 
#                           23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1 }

# dict_eRecordDataType = { 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 3, 
#                          8: 3, 9: 1, 10: 3, 11: 3, 12: 3, 13: 3, 14: 2,
#                          15: 3, 16: 3, 17: 3, 18: 1, 19: 1, 20: 1,  21: 1, 22: 3, 23: 3, 24: 3, 
#                          25: 3, 26: 3, 27: 3, 28: 3, 29: 3, 30: 3, 31: 3, 32: 3, 33: 1, 
#                          34: 3, 35: 3, 36: 3}

# dict_iDataTypeSize = { 1: 32, 2: 32, 3: 32, 4: 32, 5: 32, 6: 16, 7: 32, 
#                        8: 32, 9: 16, 10: 32, 11: 32, 12: 32, 13: 32, 14: 16, 
#                        15: 32, 16: 32, 17: 32, 18: 32, 19: 32, 20: 32, 21: 64, 22: 32, 23: 32, 24: 32, 
#                        25: 32, 26: 32, 27: 32, 28: 32, 29: 32, 30: 32, 31: 32, 32: 32, 33: 32, 
#                        34: 32, 35: 32, 36: 32 }

# dict_iRecordSize = { 1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 2, 7: 4, 
#                      8: 4, 9: 2, 10: 4, 11: 4, 12: 4, 13: 4, 14: 2, 
#                      15: 4, 16: 4, 17: 4, 18: 4, 19: 4, 20: 4, 21: 8, 22: 4, 23: 4, 24: 4, 
#                      25: 4, 26: 4, 27: 4, 28: 4, 29: 4, 30: 4, 31: 4, 32: 4, 33: 4, 
#                      34: 4, 35: 8, 36: 12 }
#with open(fnm, mode="r", encoding="utf16") as file_obj:
        #    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
        #        print(str(mmap_obj[0:4],'utf-16')) #.find(b'\r\n'))