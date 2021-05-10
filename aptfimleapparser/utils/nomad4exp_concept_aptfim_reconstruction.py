#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:03:19 2021
@author: kuehbach
concepts are classes, representing what a specific method, here specific for the APT/FIM-community, is about and which metadata it has etc. 
"""

import numpy as np
#from aptfimleapparser.utils.nomad4exp_process_aptfim_io_h5 import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_pos import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_epos import *
#from aptfimleapparser.utils.nomad4exp_process_aptfim_io_apt6 import *

#from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *
##MK::issues define concepts general to many methods e.g. what is a background model, EM, XPS, and APT have many similarities here

class n4e_concept_aptfim_reconstruction():
    """
    reconstructing is the process of post-processing a point cloud of calibrated detector hit positions (x,y) and calibrated time-of-flight spectrometry 
    data with the aim to identify and approximate answer to the original spatial positions of the atoms from which the ions were formed
    """
    
    def __init__(self, *args, **kwargs ):
        self.a = {}
        self.a['metadata'] = {}
        self.a['metadata']['analysis'] = {}
        self.a['metadata']['analysis']['name'] = None
        self.a['metadata']['analysis']['time_stamp'] = {}
        self.a['metadata']['analysis']['time_stamp']['end_local'] = None
        self.a['metadata']['analysis']['time_stamp']['end_utc'] = None
        self.a['metadata']['analysis']['time_stamp']['start_local'] = None
        self.a['metadata']['analysis']['time_stamp']['start_utc'] = None
        self.a['metadata']['author'] = {}
        self.a['metadata']['data_header'] = {}
        self.a['metadata']['dataset'] = {}
        self.a['metadata']['instrument'] = {}
        self.a['metadata']['instrument']['name'] = None
        self.a['metadata']['instrument']['uuid'] = None
        self.a['metadata']['instrument']['version'] = None
        self.a['metadata']['instrument']['component'] = {}
        self.a['metadata']['instrument']['component']['reconstruction_algorithm'] = {}
        self.a['metadata']['instrument']['component']['reconstruction_algorithm']['atomic_volume'] = None
        self.a['metadata']['instrument']['component']['reconstruction_algorithm']['field_factor'] = None
        self.a['metadata']['instrument']['component']['reconstruction_algorithm']['image_compression_factor'] = None
        self.a['metadata']['instrument']['component']['reconstruction_algorithm']['name'] = None
        self.a['metadata']['instrument']['component']['reconstruction_algorithm']['protocol'] = None #according to B. Gault et al. 2012 APT book Springer on distinguishing reconstruction protocols
        self.a['metadata']['instrument']['coordinate_system'] = {}
        self.a['metadata']['instrument']['coordinate_system']['reference'] = {}
        self.a['metadata']['instrument']['coordinate_system']['reference']['origin'] = None
        self.a['metadata']['instrument']['coordinate_system']['reference']['matrix'] = None
        self.a['metadata']['instrument']['coordinate_system']['reconstruction'] = {}
        self.a['metadata']['instrument']['coordinate_system']['reconstruction']['origin'] = None
        self.a['metadata']['instrument']['coordinate_system']['reconstruction']['matrix'] = None
        self.a['metadata']['instrument']['coordinate_system']['reconstruction']['map_to_reference_origin'] = None
        self.a['metadata']['instrument']['coordinate_system']['reconstruction']['map_to_reference_matrix'] = None
        self.a['metadata']['instrument']['coordinate_system']['ion_collector'] = {}
        self.a['metadata']['instrument']['coordinate_system']['ion_collector']['origin'] = None
        self.a['metadata']['instrument']['coordinate_system']['ion_collector']['matrix'] = None
        self.a['metadata']['instrument']['coordinate_system']['ion_collector']['map_to_reference_origin'] = None
        self.a['metadata']['instrument']['coordinate_system']['ion_collector']['map_to_reference_matrix'] = None
        self.a['metadata']['user_generated'] = {}
        self.a['metadata']['user_generated']['process_status'] = None
        
        self.a['data'] = {}
        self.a['data']['hit_positions'] = None
        self.a['data']['ion_positions'] = None
        self.a['data']['ions_per_pulse'] = None
        self.a['data']['laser_energy'] = None
        self.a['data']['laser_position'] = None
        self.a['data']['mass_to_charge_state_ratio'] = None
        self.a['data']['multiplicity'] = None
        self.a['data']['pulse_frequency'] = None
        self.a['data']['pulse_number'] = None
        self.a['data']['pulse_since_last_event_pulse'] = None
        self.a['data']['pulse_voltage'] = None
        self.a['data']['reflectron_voltage'] = None
        self.a['data']['specimen_holder_position'] = None
        self.a['data']['specimen_temperature'] = None
        self.a['data']['standing_voltage'] = None
        self.a['data']['time_of_flight'] = None

    def inform_concept_via_h5(self, h5fn, *args, **kwargs ):      
        print('parse h5 and populate concept')
        
    def inform_concept_via_pos(self, posfn, *args, **kwargs ):
        print('parse pos and populate concept')
        
        self.__init__()
        
        pos = n4e_parser_aptfim_io_read_pos( posfn )
        
        self.a['metadata']['user_generated']['process_status'] = 'accepting a reconstruction from a pos file'
        self.a['data']['ion_positions'] = pos.a['data']['IonPositions']
        self.a['data']['mass_to_charge_state_ratio'] = pos.a['data']['MassToChargeRatio']
        
        #what to do for the normalizer
        #mqmin = 0.0 #Da
        #mqincr = 0.001
        #mqmax = 1000.0
        #nomad_normalized_mass_spectrum = np.histogram( self.a['data']['mass_to_charge_state_ratio'], bins=np.linspace(mqmin, mqmax, np.uint64((mqmax-mqmin)/mqincr), endpoint=True), range=(mqmin, mqmax) )

    def inform_concept_via_epos(self, eposfn, *args, **kwargs ):
        print('parse epos and populate concept')
        
        self.__init__()
        #eposfn = '/home/kuehbach/GITHUB/NOMAD-COE/nomad-parser-aptfim-leap/tests/data/example.epos'
        
        #self.a['metadata']['user_generated']['process_status'] = 'accepting a reconstruction from a epos file'
        #self.a['data']['ion_positions'] = self.a['data']['IonPositions']
        #self.a['data']['mass_to_charge_state_ratio'] = self.a['data']['MassToChargeRatio']

    def inform_concept_via_apt6(self, apt6fn, *args, **kwargs ):
        print('parse apt6 and populate concept')
