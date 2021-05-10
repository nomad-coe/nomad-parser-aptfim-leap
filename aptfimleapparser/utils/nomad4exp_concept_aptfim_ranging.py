#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:03:19 2021
@author: kuehbach
concepts are classes, representing what a specific method, here specific for the APT/FIM-community, is about and which metadata it has etc. 
"""

import numpy as np
from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_rng import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_rrng import *

#from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *
##MK::issues define concepts general to many methods e.g. what is a background model, EM, XPS, and APT have many similarities here


class n4e_concept_aptfim_ranging():
    """
    ranging is the process of defining which mass-to-charge-state ratios represent which ions of elements or molecular ions, 
    i.e. ions with more than two isotope which can be the same
    """
    
    def __init__(self, *args, **kwargs ):
        self.a = {}
        self.a['method'] = None
        self.a['status'] = 'successfully accepted ranging'
        self.a['input'] = {}
        self.a['input']['dataset'] = None
        self.a['input']['uuid'] = None
        self.a['input']['type'] = 'vector'
        self.a['mass_spectrum'] = {}
        #when we compute a mass spectrum we might not take all input into account, which choices?
        self.a['mass_spectrum']['input_filter'] = None
        #how do we define the background of the spectrum?
        self.a['mass_spectrum']['background'] = None
        #how do we define signal smoothing operations on the spectrum?
        self.a['mass_spectrum']['signal_smoothing'] = None
        #how we deconvolute peaks?
        self.a['mass_spectrum']['peak_deconvolution'] = None
        #how do we identify peaks in the spectrum?
        self.a['mass_spectrum']['peak_finding'] = None
        #which are the peaks in the spectrum at which locations are they and what is their ionspecies label?
        self.a['mass_spectrum']['peaks'] = []
        #which ionspecies do we distinguish?
        self.a['default'] = {}
        self.a['default']['max_number_of_atoms_per_molecular_ion'] = MAX_NUMBER_OF_ATOMS_PER_MOLECULAR_ION
        self.a['ion_species'] = []
        
    def inform_concept_via_rng(self, rngfn, *args, **kwargs ):
        print('parse rng and populate concept')
        
        rng = n4e_parser_aptfim_io_read_rng( rngfn )
        
        self.a['method'] = 'aptfim-ranging'
        self.a['status'] = 'successfully accepted ranging from rng file'
        self.a['input'] = {}
        self.a['input']['dataset'] = str(rngfn)
        self.a['ion_species'] = []
        for identifier in rng.a['metadata']['species'].keys():
            self.a['ion_species'].append( rng.a['metadata']['species'][identifier] )
        
    def inform_concept_via_rrng(self, rrngfn, *args, **kwargs ):
        print('parse rrng and populate concept')
        
        rrng = n4e_parser_aptfim_io_read_rrng( rrngfn )
        
        self.a['method'] = 'aptfim-ranging'
        self.a['status'] = 'successfully accepted ranging from rrng file'
        self.a['input'] = {}
        self.a['input']['dataset'] = str(rrngfn)
        self.a['ion_species'] = []
        for identifier in rrng.a['metadata']['species'].keys():
            self.a['ion_species'].append( rrng.a['metadata']['species'][identifier] )
    
# =============================================================================
#     def init_from_rng(self, rng, *args, **kwargs):
#         """
#         in the APT/FIM communities different file formats have been defined which store results and metadata of ranging tasks
#         input: take an instance of a parsed *.rng file, fish how this specifies the concept
#         output: an instance of the concept ranging, i.e. the metadata which for atom probers define what is required for ranging
#         """
#         #none is equivalent to unknown
#         self.a['input'] = {}
#         self.a['input']['dataset'] = None
#         self.a['input']['uuid'] = None
#         self.a['input']['type'] = 'vector'
#         self.a['mass_spectrum'] = {}
#         #when we compute a mass spectrum we might not take all input into account, which choices?
#         self.a['mass_spectrum']['input_filter'] = None
#         #how do we define the background of the spectrum?
#         self.a['mass_spectrum']['background'] = None
#         #how do we define signal smoothing operations on the spectrum?
#         self.a['mass_spectrum']['signal_smoothing'] = None
#         #how we deconvolute peaks?
#         self.a['mass_spectrum']['peak_deconvolution'] = None
#         #how do we identify peaks in the spectrum?
#         self.a['mass_spectrum']['peak_finding'] = None
#         #which are the peaks in the spectrum at which locations are they and what is their ionspecies label?
#         self.a['mass_spectrum']['peaks'] = []
#         #which ionspecies do we distinguish?
#         for i in rng.a[species]:
#             self.a['mass_spectrum']['ionspecies']
# =============================================================================

#test
#a = n4e_concept_aptfim_ranging()