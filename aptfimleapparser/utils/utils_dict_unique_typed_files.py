#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:50:57 2021
@author: kuehbach
convenience function transforming a list of files with endings to a dictionary of the unique file names, tested and categorized for their type 
"""

import numpy as np

class unique_list_typed_files():
    def __init__(self, fnlst, *args, **kwargs):
        """
        passing a list of file names with ending we filter out the unique and characterize them for their type
        """
        #fnlst = ['example.pos', 'example.h5', 'example.hdf5']
        search_types = np.asarray(['.h5', '.hdf5', '.pos', '.epos', '.apt6','.apt','.rrng', '.rng'], np.str)
        tmp = {}
        for typ in search_types:
            tmp[typ] = []
            for i in fnlst: ###MK::implement more efficiently
                if i.lower().endswith(typ):
                    tmp[typ].append(i)
        #implementing fusing rules, which files should be treated the same way and remove duplicates
        self.file_types = {}
        self.file_types['.h5'] = np.unique(tmp['.h5'] + tmp['.hdf5'])
        self.file_types['.pos'] = np.unique(tmp['.pos'])
        self.file_types['.epos'] = np.unique(tmp['.epos'])
        self.file_types['.apt6'] = np.unique(tmp['.apt6'] + tmp['.apt'])
        self.file_types['.rng'] = np.unique(tmp['.rng'])
        self.file_types['.rrng'] = np.unique(tmp['.rrng'])
        
    def get_typed_number_of_files(self, typ):
        if typ in self.file_types.keys():
            return len(self.file_types[typ])
        return 0
    
    def get_total_number_of_files(self):
        n = 0
        for key in self.file_types.keys():
            n += len(self.file_types[key])
        return n
    
    def only_typed_ranging_files(self):
        if self.get_typed_number_of_files('.rng') + self.get_typed_number_of_files('.rrng') != self.get_total_number_of_files(): #not only range files
            return False
        return True

    def get_typed_reconstruction_file(self):
        if self.get_typed_number_of_files('.h5') == 1:
            if self.get_typed_number_of_files('.pos') + self.get_typed_number_of_files('.epos') + self.get_typed_number_of_files('.apt6') == 0:
                return '.h5'
            else:
                return None
        if self.get_typed_number_of_files('.pos') == 1:
            if self.get_typed_number_of_files('.h5') + self.get_typed_number_of_files('.epos') + self.get_typed_number_of_files('.apt6') == 0:
                return '.pos'
            else:
                return None
        if self.get_typed_number_of_files('.epos') == 1:
            if self.get_typed_number_of_files('.h5') + self.get_typed_number_of_files('.pos') + self.get_typed_number_of_files('.apt6') == 0:
                return '.epos'
            else:
                return None
        if self.get_typed_number_of_files('.apt6') == 1:
            if self.get_typed_number_of_files('.h5') + self.get_typed_number_of_files('.pos') + self.get_typed_number_of_files('.epos') == 0:
                return '.apt6'
            else:
                return None
        #more than one or other unsupported configuration
        return None
    
    def get_typed_ranging_file(self):
        if self.get_typed_number_of_files('.rng') == 1:
            return '.rng'
        if self.get_typed_number_of_files('.rrng') == 1:
            return '.rrng'
        #more than one or other unsupported configuration
        return None

#test
#fnlst = ['example.pos', 'example.h5', 'example.hdf5']
#a = unique_file_type_list( fnlst )   
