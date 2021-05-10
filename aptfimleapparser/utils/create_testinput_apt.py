#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:41:48 2021
@author: kuehbach
a utility to create a small test file matching the specifications of the new atom probe microscopy binary APT6 file format
which was introduced first with IVAS 4 / APSuite 6, we call this format the APT6 format to distinguish it from an earlier
format used by the community which unfortunately is also colloquially known as APT file format but has different internal
structure
##MK::issue list:
##MK::get examples for these older formats and write parsers for them as well, however, 
##MK::they are not so frequently use any longer so thats why I put them on the issue list
"""

import numpy as np
from utils_string_to_np_uint16 import *


aptfn = 'example.apt6'

apt = open( aptfn, mode='ba+')

# a file with only ten atoms, unrealistically small solely to test the parser implementation
N = 10

# unphysical dummy data
dummy_xyz = np.float32(np.array([np.linspace(1,N,N),]*3).transpose())
dummy_mass = np.float32(np.array([np.linspace(1,N,N),]).transpose())

#apt file format uses little endian
# apt binary files have a self-describing but data-adaptive structure with header of fixed structure
# see IFES APT TC meeting file format specification private communication from T. Payne, D. Reinhardt (2020)
# apt binary files have a single file header and a list of section block header with immediately preceeding
# data section each, formatted as specified in the header section

#create a file named aptfn if it not exists yet and keep appending
aptheader = np.zeros( 1, dtype= np.dtype( [('cSignature', np.uint8, (4,)), 
                                        ('iHeaderSize', np.int32), 
                                        ('iHeaderVersion', np.int32), 
                                        ('wcFilename', np.uint16, 256), 
                                        ('ftCreationTime', np.uint64),
                                        ('llIonCount', np.uint64)] ) )
aptheader['cSignature'] = np.array([ord('A'), ord('P'), ord('T'), ord('\0')], dtype=np.uint8)
aptheader['iHeaderSize'] = 540
aptheader['iHeaderVersion'] = 2
aptheader['wcFilename'] = string_to_np_uint16(aptfn, 256)
aptheader['ftCreationTime'] = 0
aptheader['llIonCount'] = N
aptheader.tofile(apt)

#the minimum sections in an APT file have to be 'Position' and 'Mass'
xyz_sect = np.zeros( 1, dtype = np.dtype( [('cSignature', np.int8, (4,)), 
                                           ('iHeaderSize', np.int32), 
                                           ('iHeaderVersion', np.int32), 
                                           ('wcSectionType', np.uint16, 32), 
                                           ('iSectionVersion', np.int32), 
                                           ('eRelationshipType', np.uint32), 
                                           ('eRecordType', np.uint32), 
                                           ('eRecordDataType', np.uint32), 
                                           ('iDataTypeSize', np.int32), 
                                           ('iRecordSize', np.int32), 
                                           ('wcDataUnit', np.uint16, 16), 
                                           ('llRecordCount', np.uint64),
                                           ('llByteCount', np.uint64),
                                           ('xmin', np.float32),
                                           ('xmax', np.float32),
                                           ('ymin', np.float32),
                                           ('ymax', np.float32),
                                           ('zmin', np.float32),
                                           ('zmax', np.float32)] ) )

xyz_sect['cSignature'] = np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8)
xyz_sect['iHeaderSize'] = 148+6*4 #the Position section is so far the only section known which encodes an extra-header
xyz_sect['iHeaderVersion'] = 2
xyz_sect['wcSectionType'] = string_to_np_uint16('Position', 32)
xyz_sect['iSectionVersion'] = 1
xyz_sect['eRelationshipType'] = 1
xyz_sect['eRecordType'] = 1
xyz_sect['eRecordDataType'] = 3
xyz_sect['iDataTypeSize'] = 32
xyz_sect['iRecordSize'] = 12
xyz_sect['wcDataUnit'] = string_to_np_uint16('nm', 16)
xyz_sect['llRecordCount'] = N
xyz_sect['llByteCount'] = xyz_sect['llRecordCount'] * xyz_sect['iRecordSize']
xyz_sect['xmin'] = np.float32(np.min(dummy_xyz[:,0]))
xyz_sect['xmax'] = np.float32(np.max(dummy_xyz[:,0]))
xyz_sect['ymin'] = np.float32(np.min(dummy_xyz[:,1]))
xyz_sect['ymax'] = np.float32(np.max(dummy_xyz[:,1]))
xyz_sect['zmin'] = np.float32(np.min(dummy_xyz[:,2]))
xyz_sect['zmax'] = np.float32(np.max(dummy_xyz[:,2]))
xyz_sect.tofile(apt)
dummy_xyz.tofile(apt)


mss_sect = np.zeros( 1, dtype = np.dtype( [('cSignature', np.int8, (4,)), 
                                           ('iHeaderSize', np.int32), 
                                           ('iHeaderVersion', np.int32), 
                                           ('wcSectionType', np.uint16, 32), 
                                           ('iSectionVersion', np.int32), 
                                           ('eRelationshipType', np.uint32), 
                                           ('eRecordType', np.uint32), 
                                           ('eRecordDataType', np.uint32), 
                                           ('iDataTypeSize', np.int32), 
                                           ('iRecordSize', np.int32), 
                                           ('wcDataUnit', np.uint16, 16), 
                                           ('llRecordCount', np.uint64),
                                           ('llByteCount', np.uint64)] ) )

mss_sect['cSignature'] = np.array([ord('S'), ord('E'), ord('C'), ord('\0')], np.uint8)
mss_sect['iHeaderSize'] = 148 #normal size of a section with wcSectionType other than Position
mss_sect['iHeaderVersion'] = 2
mss_sect['wcSectionType'] = string_to_np_uint16('Mass', 32)
mss_sect['iSectionVersion'] = 1
mss_sect['eRelationshipType'] = 1
mss_sect['eRecordType'] = 1
mss_sect['eRecordDataType'] = 3
mss_sect['iDataTypeSize'] = 32
mss_sect['iRecordSize'] = 4
mss_sect['wcDataUnit'] = string_to_np_uint16('Da', 16)
mss_sect['llRecordCount'] = N
mss_sect['llByteCount'] = mss_sect['llRecordCount'] * mss_sect['iRecordSize']
mss_sect.tofile(apt)
dummy_mass.tofile(apt)

apt.close()
