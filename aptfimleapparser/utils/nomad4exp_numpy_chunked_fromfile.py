#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 16:25:00 2021
@author: kuehbach
convenience function for chunked reading of large binary files where I figured running out 
of fopen buffer space when calling numpy.fromfile(fn)
###MK::issue:
###MK::replace use of this function via memory-mapping/lazy loading
"""

#import os, sys
#from pathlib import Path

import numpy as np

CHUNK_SIZE = 50*1024*1024 ###MK::how much to read with one call here 50MiB


def np_chunked_reading( fp, dty, bytlen, nrows, ncols ):
    """
    read a contiguous block of nrows*ncols dtyp-typed data elements from opened file pointed to by bytlen in chunks of at most CHUNK_SIZE
    at once, with chunks multiples of ncols
    """
    #dtyp = np.float32
    #bytlen = 4
    #nrows = 1*1000*1000
    #ncols = 3
    #bytlen = fid
    #allocate space for total array
    print('Chunked reading from file pointer byte position ' + str(fp.tell()))
    ret = np.zeros([nrows, ncols], dtype=dty)    
    nrows_curr = 0
    nrows_read = 0
    while True:
        nrows_curr = int(CHUNK_SIZE/(bytlen*ncols))
        if (nrows_read + nrows_curr) < nrows:
            #print(str(nrows_curr))
            print('Byte position ' + str(fp.tell()))
            nparr = np.fromfile(fp, dtype=dty, count = int(nrows_curr*ncols))
            print(nparr)
            #catch cases where APT6 file is incomplete
            nrows_now = nrows_curr
            ncols_now = ncols
            print('np.shape(nparr)[0]')
            print(np.shape(nparr))
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
            print('Byte position ' + str(fp.tell()))
            nparr = np.fromfile(fp, dtype=dty, count = int(nrows_curr*ncols))
            print(nparr)
            #catch cases where APT6 file is incomplete
            nrows_now = nrows_curr
            ncols_now = ncols
            print('np.shape(nparr)[0]')
            print(np.shape(nparr))
            if np.shape(nparr)[0] != nrows_now*ncols_now:
                if np.shape(nparr)[0] % ncols == 0:
                    nrows_now = int(np.shape(nparr)[0])/int(ncols)
                    ncols_now = int(ncols)
                else:
                    raise ValueError('Chunked reading read-in nparray object has an unexpected number of elements, APT6 is likely corrupted !')
            ret[int(nrows_read):int(nrows_read)+int(nrows_now),:] = np.reshape( nparr, (int(nrows_now), int(ncols_now)), order='C')
            #print('nparr: ' + str(np.shape(nparr)[0]))
            nrows_read += nrows_now
            #ret[nrows_read:nrows_read+nrows_curr,:] = np.reshape(np.fromfile(fp, dtyp, count = np.int64(nrows_curr*ncols)), 
            #                                                     (np.int64(nrows_curr), np.int64(ncols)), order='C')
            #print(str(nrows_curr))
            #nrows_read += nrows_curr
            return ret
    return ret
