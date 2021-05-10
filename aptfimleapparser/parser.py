#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import h5py
import json
import numpy as np
from datetime import datetime
import logging
from nomad.units import ureg

from nomad.datamodel import EntryArchive
from nomad.parsing import FairdiParser

from . import metainfo  # pylint: disable=unused-import
from .metainfo import *
'''
This is a parser to inject APT/FIM-community-specific file formats into NOMAD for experimental data
'''

logger = logging.getLogger(__name__)

#import user-defined convenience functions
from aptfimleapparser.utils.utils_h5py_string_decode import *
from aptfimleapparser.utils.utils_h5py_vlen_string_array_decode import *
from aptfimleapparser.utils.utils_dict_unique_typed_files import *

#import user/community-defined I/O functions to parse the APT/FIM-community-specific file formats
from aptfimleapparser.utils.nomad4exp_process_aptfim_utils_ranging import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_rng import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_rrng import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_apt6 import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_pos import *
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_epos import *

#import user/community-defined I/O functions to parse information from vendor-specific databases
from aptfimleapparser.utils.nomad4exp_process_aptfim_io_isdb import *

#import user/community-defined class definitions of concepts and logical instances
#from aptfimleapparser.utils.nomad4exp_concept_aptfim_measurement import *
#from aptfimleapparser.utils.nomad4exp_concept_aptfim_calibration import *
from aptfimleapparser.utils.nomad4exp_concept_aptfim_reconstruction import *
from aptfimleapparser.utils.nomad4exp_concept_aptfim_ranging import *


#for atom probe microscopy such instances are measurement, calibration, reconstruction, ranging
#the classes have members which keep what ideally we want to keep track of for
#an apt experiment, in most cases, most file formats, though, do not store all these relevant
#metadata, so we define such classes to decouple the process inside the APT/FIM community
#what constitutes useful metadata and decouple their definition from the question which of these
#quantities should be uploaded into a nomad(OASIS), specifically to decouple it also from the
#terminology-used inside NOMAD and the terminology used in the APT/FIM community
#in an ideal world there would be a community manifest what constitutes (meta)data for each
#method and corresponding file formats which represent these concepts
###MK::in reality this is not the situation in the APT/FIM community yet, so 
#we have an inclusive approach which translates between terms APT/FIM-specific and their
#representation in NOMAD. Thereby, we can reduce the complexity of NOMAD normalizers but distill
#the information already inside the classes and then just transfer pieces of information


class AptFimLeapParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/aptfimleapparser', code_name='APTFIMLEAP', code_homepage='https://www.example.eu/',
            mainfile_mime_re=r'(application/json)'
        )
        
    def add_measurement(self, concept, archive: EntryArchive, logger, simid = 1):
        pass
    
    def add_calibration(self, concept, archive: EntryArchive, logger, simid = 1):
        pass
    
    def add_reconstruction(self, concept, archive: EntryArchive, logger, simid = 1):
        
        recon = archive.m_create(Reconstruction)
        
        #Create metadata holding sections
        metadata = recon.m_create(ReconstructingMetadata)         
        analysis = metadata.m_create(ReconstructingAnalysis)
        time_stamp = analysis.m_create(TimeStamps)             
        author = metadata.m_create(ReconstructingAuthor)
        data_header = metadata.m_create(ReconstructingDataHeader)
        dataset = metadata.m_create(ReconstructingDataset)
        instrument = metadata.m_create(ReconstructingInstrument)
        components = instrument.m_create(ReconstructingComponent)
        coordinates = instrument.m_create(ReconstructingCoordinateSystem)
        user_generated = metadata.m_create(ReconstructingUserGenerated)
        
        #Create data holding sections
        data = recon.m_create(ReconstructingData)
        
        #transfer results from concept instance
        #if concept.a['metadata']['user_generated']['process_status'] != None: 
        user_generated.process_status = concept.a['metadata']['user_generated']['process_status']
        
        data.ion_records = concept.a['data']['ion_positions'].val
        data.mass_to_charge_state_ratio = concept.a['data']['mass_to_charge_state_ratio'].val
    
    def add_ranging(self, concept, archive: EntryArchive, logger, simid = 1):
         
         ranging = archive.m_create(Ranging)
         
         #Create metadata holding sections
         metadata = ranging.m_create(RangingMetadata)         
         analysis = metadata.m_create(RangingAnalysis)
         time_stamp = analysis.m_create(TimeStamps)             
         author = metadata.m_create(RangingAuthor)
         data_header = metadata.m_create(RangingDataHeader)
         dataset = metadata.m_create(RangingDataset)
         instrument = metadata.m_create(RangingInstrument)
         components = instrument.m_create(RangingComponent)
         tof_to_mq_mapping = components.m_create(TimeOfFlightToMassToChargeMapping)
         filters = components.m_create(RangingFilter)
         filter_mass_to_charge = filters.m_create(FilterMassToCharge)
         filter_multiplicity = filters.m_create(FilterMultiplicity)
         filter_ion_position = filters.m_create(FilterIonPosition)
         filter_ion_id = filters.m_create(FilterIonID)
         binning = components.m_create(Binning)
         background = components.m_create(BackgroundQuantification)
         peak_deconvolution = components.m_create(PeakDeconvolution)
         peak_detection = components.m_create(PeakDetection)
         signal_smooth = components.m_create(SignalSmoothing)         
         user_generated = metadata.m_create(RangingUserGenerated)
                
         # Create data holding sections
         data = ranging.m_create(RangingData)
         #profiling = data.m_create(ExecutionDetails)
         ion_species = data.m_create(IonSpecies)
         
         #transfer results from concept instance
         #analysis section
         if concept.a['method'] != None: analysis.name = concept.a['method']
         
         #author section        
         actor = metadata.m_create(RangingAuthor)
         actor.name = 'MarkusK'
         actor.affiliation = 'NOMAD'
         actor.email = 'dummy@nomad.de'
         actor = metadata.m_create(RangingAuthor)
         actor.name = 'MarkusS'
         actor.affiliation = 'NOMAD'
         actor.email = 'dummy@nomad.de'
         
         #data_header section
         #nothing to do for data_header so far
         
         #dataset section
         dset = metadata.m_create(RangingDataset)
         if concept.a['input']['dataset'] != None: dset.name = concept.a['input']['dataset']
         dset.uuid = 'none' #if concept.a['input']['uuid'] != None: dset.uuid = concept.a['input']['uuid']
         
         #instrument section
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/TimeOfFlightToMassToCharge/Comment'
         #         if node in keys: tof_to_mq_mapping.comment = h5py_string_decode(h5main[node][()])
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/MassToCharge/Name'
         #         if node in keys: filter_mass_to_charge.name = h5py_string_decode(h5main[node][()])
         #         ###MK::
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/Multiplicity/Name'
         #         if node in keys: filter_multiplicity.name = h5py_string_decode(h5main[node][()])
         #         ###MK::
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonPosition/Name'
         #         if node in keys: filter_ion_position.name = h5py_string_decode(h5main[node][()])
         #         ###MK::
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonID/Name'
         #         if node in keys: filter_ion_id.name = h5py_string_decode(h5main[node][()])
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonID/MinIncrMaxLinearSubSampling'
         #         if node in keys: filter_ion_id.min_incr_max = h5main[node][:].flatten()
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/BinningAlgorithm/MassToCharge/Type'
         #         if node in keys: binning.name = h5py_string_decode(h5main[node][()])
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/BackgroundAlgorithm/Name'
         #         if node in keys: background.name = h5py_string_decode(h5main[node][()])
         #         ###MK::node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/BinningAlgorithm/Ranges'
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDeconvolutionAlgorithm/Name'
         #         if node in keys: peak_deconvolution.name = h5py_string_decode(h5main[node][()])
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDetectionAlgorithm/Name'
         #         ###MK::node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDetectionAlgorithm/Ranges'
         #         if node in keys: peak_detection.name = h5py_string_decode(h5main[node][()])
         #         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/SignalSmoothingAlgorithm/Name'
         #         if node in keys: signal_smooth.name = h5py_string_decode(h5main[node][()])
         #         ###MK::node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/SignalSmoothingAlgorithm/Ranges'

         #user_generated section
         if concept.a['status'] != None: user_generated.process_status = concept.a['status']

         #data section
         ion_species.ndisjoint_ion_species = len(concept.a['ion_species'])
         ion_species.max_natoms_per_ion = concept.a['default']['max_number_of_atoms_per_molecular_ion']
         for obj in concept.a['ion_species']:
             speci = ion_species.m_create(MolecularIonDef)
             speci.identifier = obj.id
             speci.charge = obj.charge
             speci.isotope_vector = obj.ivec
             speci.mass_to_charge_ranges = obj.mq
             

    def parse(self, mainfile: str, archive: EntryArchive, logger):
        # we assume a general APT/FIM parser for experiments with AMETEK LEAP instrument faces a situation where users may have uploaded a bunch of files
        # these are the files from which we want to sug metadata honey for NOMAD
        # specific for APT/FIM we can imagine the following situations:
        # measurements are accepted only in one of the following formats (*.pos, *.epos, *.apt6) #, *.h5)
        # ranging definitions are accepted only in one of the following formats (*.rng, *.rrng)
        # supplementary infos might be delivered ###MK::are not supported yet
        # ###MK::but when FAIRmat gets funded we should here offer to inject data from the ISDB database via *.isdb files
        # such a step is necessary because file formats in APT/FIM at the moment do not contain all the data of interest for NOMAD
        
        # most common is user has uploaded a pair of a reconstructed dataset and a ranging definition
        # usually users store the reconstructed dataset as pos, epos, or apt6 file format
        # usually users store the associated ranging definition as rng/rrng file format alongside their reconstructed dataset
        # eventually users upload supplementary pieces of information
        # people make often multiple versions of ranging definitions for the same reconstructed dataset, which should NOMAD choose?
        # in effect,
        # we need a mechanism which distinguishes inputted files and add multiple such definitions to a single reconstructed dataset (RDS)
        # we have to distinguish the following cases when processing a generic ensemble of file upload for APT/FIM LEAP experiments 
        # people may upload files without appropriate endings
        # --> we do nothing for the respective files, i.e. reject files currently not supported by NOMAD
        # people may upload with capitalized file endings instead of lower case ending
        # --> by default we transcode all file endings to lower-case first
        # people may upload only RDS and none, one, or more than one range files, the latter case should be rejected because *.rng or *.rrng do not store to which measurement/dataset they belong
        # --> one or multiple range files only, we reject this because ranging definitions alone without a dataset associated is not useful ###MK::but mere documentation
        # --> no range file is accepted but we fire a warning telling there is no ranging associated with the dataset
        # --> one range file is accepted this but give a message telling that we assume the user wishes to associate the range file with the RDS
        # --> if users use this to (intentionally) upload unrelated stuff file exploiting that rangefile do not have link to RDS files, bad luck ###MK::at least for now
        # --> more than one range file, we currently reject this case ###MK::in the future accept but give a warning telling that we assume all ranging definitions apply to the same file    
        # people may upload very large (how do we define large?) files, need to have a mechanism above which data arrays are downsampled
        # --> currently we just accept these files, ##MK::the largest range files I have seen are in the order of KB so no worries
        # --> ###MK::but the largest RDS I have seen are in the order of theoretically 100 GB, typically, though, smaller, usually between 100 MB and 10 GB
        # people may upload range files with inconsistent definitions or errors
        # --> ###MK::currently the individual parsers for the specific file formats throw errors when detecting inconsistencies
        # --> ###MK::these tests should be improved to make the parsing even more robust when FAIRmat gets funded
        
        #in general we can not expect that a single file format keeps all data nomad metainfo asks for,
        #so instead of the naive direct passing of file content to nomad metainfo class instances, we populate first concepts of the methods we employ in APT/FIM
        mymeasurement = None
        mycalibration = None
        myreconstruction = None
        myranging = None
        #the benefit is that this decouples the technical implementation of a file format from its representation in nomad
        #there might be N formats reporting similar quantities, copying naively parsers for each format will create many places
        #where nomad developers would need to make changes once sth changes on the nomad metainfo side
        #concepts allow the nomad core team developers to focus on the nomad metainfo side and domain-specialists to focus on file format details
        #and should help with reducing the amount of infrastructure code to be duplicated
        
        # parsing begins with a user passing a list of filenames representing the uploaded files
        ###MK::Markus Scheidgen and team: please inject here the part where such a list comes from e.g. browser input
        prefix = '/home/kuehbach/GITHUB/NOMAD-COE/nomad-parser-aptfim-leap/tests/data/'
        mainfile = prefix + 'example.upload.json'
        with open(mainfile, 'rt') as f:
             user_upload = set(json.load(f)) #only unique names not-capitalization-sensitive
    
        case0 = []
        case1 = ['example']
        case2 = ['example.rng']
        case3 = ['example.pos']
        case4 = [prefix + 'example.pos', prefix + 'example.rng']
        case5 = [prefix + 'example.pos', prefix + 'example.rrng']
        case6 = ['example.pos', 'example1.rng', 'example2.rng']
        # people may upload such a combination with the aim to be efficient
        case7 = ['example1.pos', 'example1.rng', 'example2.epos', 'example2.rrng']
        # --> as an intelligent human we may guess that in case6 that the user has consistently named his reconstruction(s) with suffix 1 and 2
        # and we may face here in fact two different measurements? in one upload. However, pos, epos, and apt6 file formats make no statement which measurement
        # they detail. So case6 is not distinguishable from a case where a person performed two reconstructions for the same physically measured specimen 
        #(because recon is a post-processing tasks on the measured raw data!) or a case where this person has just offered in fact an upload of two reconstructions
        # one for each physically disjoint APT/FIM specimen.
        # --> we should reject such source of inconsistence
        # --> ###MK::for more metadata containing file formats we may lift this constraint provided the file are sufficiently instructive via e.g. measurement UUID
        case8 = ['example.apt6', 'example.rrng']
        
        #lets structure the collection of files by file type and remove duplicates
        user_upload = case5
        files = unique_list_typed_files( user_upload )

        #lets execute the different parsers based on which combinations of file formats the user has delivered
        #in this process we translate community-method-file-format-specific knowledge into the idea of the concept behind the method
        #to abstract the technical details of the file format and parsing process
        if files.get_total_number_of_files() > 0:
            
            if files.only_typed_ranging_files() == False: #not only range files
            
                #process reconstruction file first
                stop = False
                typ = files.get_typed_reconstruction_file()
                if typ == '.h5':
                    print('Using h5 file parser')
                    myreconstruction = n4e_concept_aptfim_reconstruction()
                    myreconstruction.inform_concept_via_h5( files.file_types[typ][0] )
                elif typ == '.pos':
                    print('Using pos file parser')
                    myreconstruction = n4e_concept_aptfim_reconstruction()
                    myreconstruction.inform_concept_via_pos( files.file_types[typ][0] )
                elif typ == '.epos':
                    print('Using epos file parser')
                    myreconstruction = n4e_concept_aptfim_reconstruction()
                    myreconstruction.inform_concept_via_epos( files.file_types[typ][0] )
                elif typ == '.apt6':
                    myreconstruction = n4e_concept_aptfim_reconstruction()
                    myreconstruction.inform_concept_via_apt6( files.file_types[typ][0] )
                    print('Using apt6 file parser')
                else:
                    print('Either none or more than one relevant reonstruction file was uploaded !')
                    stop = True
                    #exit()
                    
                if stop == False:                    
                    #next process associated range file
                    typ = files.get_typed_ranging_file()         
                    if typ != None:
                        if typ == '.rng':
                            print('Using rng file parser')
                            myranging = n4e_concept_aptfim_ranging()
                            print( files.file_types[typ][0] )
                            myranging.inform_concept_via_rng( files.file_types[typ][0] )        
                        elif typ == '.rrng':
                            print('Using rrng file parser')
                            myranging = n4e_concept_aptfim_ranging()
                            myranging.inform_concept_via_rrng( files.file_types[typ][0] )
                        else:
                            print('Unexpected logical error in the case selector, contact NOMAD developers...')
                else:
                    print('WARNING: you uploaded only a reconstruction without an associated ranging file or a reconstruction with multiple (associated) range files !')
                    print('WARNING: in the latter case, this is an ambiguous situation, which we currently reject for lacking data consistency !')                   
            else:
                print('Only ranging file(s) were uploaded, without contextualization these are useless because rng and rrng file formats do not document for which reconstruction they were defined !')
        else:
            print('No relevant interpretable files of supported format were uploaded !')
        
        #with the concepts initialized properly we can enter the NOMAD world and instantiate a method-specific particularly structured instance of NOMAD metainfo
        if myreconstruction != None:
            print('Creating JSON section_measurement for measured raw data')
            self.add_measurement( mymeasurement, archive, logger, 1 )
            print('Creating JSON section_data_processing for calibration of measurement data prior reconstruction')
            self.add_calibration( mycalibration, archive, logger, 1 )
            print('Creating JSON section_data_processing for building reconstruction from measured data')
            self.add_reconstruction( myreconstruction, archive, logger, 1 )
            
        if myranging != None:
            print('Creationg JSON section_data_processing for labeling ions as specific ionspecies (ranging)')
            self.add_ranging( myranging, archive, logger, 1 )
            
        #done, the callee will manage the rest and print the JSONized NOMAD MetaInfo entry

        
        # # Log a hello world, just to get us started.
        # logger.info('Testing the APTFIM LEAP World')
        
        # #mainfile = '..tests/data/example.nx5'
        # #mainfile = '/home/kuehbach/GITHUB/NOMAD-COE/nomad-parser-aptfim-leap/tests/data/example.nx5'
        # if not mainfile.endswith('.nx5'):
        #     raise ValueError('Mainfile needs to have *.nx5 file ending !')
        # ###MK::add check for existence of the file
        
        # #if not supplfile.endswith('.nx5'):
        # #    raise ValueError('Supplementary file needs to have *.nx5 file ending !')
        
        #self.parse_nx5_measurement( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_measurement')
        #self.parse_nx5_calibration( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_calibration')
        #self.parse_nx5_reconstruction( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_reconstruction')
        #self.parse_nx5_ranging( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_ranging')
        
        
# =============================================================================
#     def parse_nx5_measurement(self, mainfile: str, archive: EntryArchive, logger, simid = 1):
#         #parse mainfile
#         h5main = h5py.File( mainfile, 'r')
#         #h5supp = h5py.File( supplfile, 'r')
#         keys = h5main.keys()
#                     
#         measurement = archive.m_create(Measurement)
#         #Create metadata-holding sections
#         metadata = measurement.m_create(MeasureMetadata)
#         
#         method = metadata.m_create(MeasureMethod)
#         sample = metadata.m_create(Sample)
#         material = sample.m_create(Material)
#         #roi = material.m_create(RegionOfInterest)
#         environment = metadata.m_create(MeasureEnvironment)
#                 
#         tool = metadata.m_create(MeasureTool)
#         components = tool.m_create(MeasureComponents)
#         laser = components.m_create(MeasureLaser)
#         emitter = laser.m_create(MeasureEmitter)
#         high_voltage_pulser = components.m_create(MeasureHighVoltagePulser)
#         reflectron = components.m_create(MeasureReflectron)
#         aperture = components.m_create(MeasureAperture)
#         specimen_chamber = components.m_create(MeasureSpecimenChamber)
#         ultra_high_vacuum_pump = components.m_create(MeasureUltraHighVacuumPump)
#         specimen_holder = components.m_create(MeasureSpecimenHolder)
#         
#         coordinate_systems = tool.m_create(CoordinateSystems)
#         #cs_reference = coordinate_systems.m_create(CoordinateSystemDef) #, 'SubSection' == section_reference)
#         ###MK::how to make disjoint? or map more elegantly without having to redefine CS class objects for each
#         ###MK::individual coordinate system?
#         cs_reference = coordinate_systems.m_create(ReferenceCS)
#         cs_specimen_chamber = coordinate_systems.m_create(SpecimenChamberCS)
#         cs_specimen_holder = coordinate_systems.m_create(SpecimenHolderCS)
#         cs_specimen = coordinate_systems.m_create(SpecimenCS)
#         cs_laser_probe = coordinate_systems.m_create(LaserProbeCS)
#         cs_multi_channel_plate = coordinate_systems.m_create(MultiChannelPlateCS)
#         ###MK::cs_detectors
#         
#         #operators = metadata.m_create(Operator)
#         time_stamps = metadata.m_create(TimeStamps)
#         process_status = metadata.m_create(ProcessStatus)
#         
#         # Create data-holding sections
#         data = measurement.m_create(MeasureData)
#         d_flight_path = data.m_create(MeasureDataFlightPath)
#         d_laser = data.m_create(MeasureDataLaser)
#         d_emitter = d_laser.m_create(MeasureDataEmitter)
#         ###MK::add remaining
#         
#         #fill in existent metadata
#         ###MK::ID management nx5 stores user-defined ID suffix how should the parser filter this from the groupname?
#         #simid = 1 ###MK::for debugging for now
#         ###MK::currently my policy is I fish what exists, but I do not complain if metadata entries are non-existent
#         
#         node = 'MeasurementID'+str(simid)+'/Metadata/Method/Name'
#         if node in keys: method.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Name'
#         if node in keys: sample.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/UUID'
#         if node in keys: sample.uuid = h5py_string_decode(h5main[node][()])
#         
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Material/TrivialName'
#         if node in keys: material.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Material/Elements'
#         a = h5main[node][:].flatten()
#         if node in keys: material.elements = h5py_vlen_string_array_decode(h5main[node])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Material/NominalComposition'
#         if node in keys: material.nominal_composition = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Material/Shape'
#         if node in keys: material.shape = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Material/Dimensions'
#         if node in keys: material.dimensions = h5main[node][:].flatten()
#         
#         node = 'MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents'
#         if node in keys:
#             for obj in h5main[node].keys():
#                 constituents = material.m_create(Constituent)
#                 node_obj = node + '/' + obj + '/Elements'
#                 if node_obj in keys: constituents.elements = h5py_vlen_string_array_decode(h5main[node_obj][:])
#                 node_obj = node + '/' + obj + '/Description'
#                 if node_obj in keys: constituents.description = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/CrystalStructure'
#                 if node_obj in keys: constituents.crystal_structure = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/NominalComposition'
#                 if node_obj in keys: constituents.nominal_composition = h5main[node_obj][:].flatten()
#         ###MK::roi
#         node = 'MeasurementID'+str(simid)+'/Metadata/Environment/Computers'
#         if node in keys:
#             for obj in h5main[node].keys():
#                 computer = environment.m_create(Computer)
#                 node_obj = node + '/' + obj + '/Name'
#                 if node_obj in keys: computer.name = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/UUID'
#                 if node_obj in keys: computer.uuid = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/OperatingSystem'
#                 if node_obj in keys: computer.operating_system = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/MainMemory'
#                 if node_obj in keys: computer.mainmemory = h5py_string_decode(h5main[node_obj][()])
#                 sub_node = node + '/' + obj + '/CPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         cpu = computer.m_create(CPUSocket)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: cpu.name = h5py_string_decode(h5main[sub_node_obj][()])                     
#                 sub_node = node + '/' + obj + '/GPGPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         accl = computer.m_create(GPGPUSlot)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: accl.name = h5py_string_decode(h5main[sub_node_obj][()])
#                 sub_node = node + '/' + obj + '/Storage'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         dsk = computer.m_create(MountedDisk)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: dsk.name = h5py_string_decode(h5main[sub_node_obj][()])
#               
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Name'
#         if node in keys: tool.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/Laser/Emitter/Name'
#         if node in keys: emitter.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/HighVoltagePulser/Name'
#         if node in keys: high_voltage_pulser.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/Reflectron/Name'
#         if node in keys: reflectron.name = h5py_string_decode(h5main[node][()])
#         ###MK::add apertures
#         # node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/Aperture/Name'
#         # #if node in keys: aperture.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/SpecimenChamber/Name'
#         if node in keys: specimen_chamber.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/UlraHighVacuumPump/Name'
#         if node in keys: ultra_high_vacuum_pump.name = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/Components/SpecimenHolder/Name'
#         if node in keys: specimen_holder.name = h5py_string_decode(h5main[node][()])
#         
#         # ###MK::add detectors
#         #node = 'MeasurementID'+str(simid)+'/Metadata/Environment/Detectors'
#         #if node in keys:
#         #    for obj in h5main[node].keys():
#         #        detector = environment.m_create(Computer)
#         #        node_obj = node + '/' + obj + '/Name'
#         #        if node_obj in keys: computer.name = h5py_string_decode(h5main[node_obj][()])
#         #        node_obj = node + '/' + obj + '/UUID'
#         
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Origin'
#         if node in keys: cs_reference.origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Matrix'
#         if node in keys: cs_reference.matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/Origin'
#         if node in keys: cs_specimen_chamber.origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/Matrix'
#         if node in keys: cs_specimen_chamber.matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/MapToRefOrigin'
#         if node in keys: cs_specimen_chamber.map_to_ref_origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/MapToRefMatrix'
#         if node in keys: cs_specimen_chamber.map_to_ref_matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/Origin'
#         if node in keys: cs_specimen_holder.origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/Matrix'
#         if node in keys: cs_specimen_holder.matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/MapToRefOrigin'
#         if node in keys: cs_specimen_holder.map_to_ref_origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/MapToRefMatrix'
#         if node in keys: cs_specimen_holder.map_to_ref_matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/Origin'
#         if node in keys: cs_specimen.origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/Matrix'
#         if node in keys: cs_specimen.matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/MapToRefOrigin'
#         if node in keys: cs_specimen.map_to_ref_origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/MapToRefMatrix'
#         if node in keys: cs_specimen.map_to_ref_matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/Origin'
#         if node in keys: cs_laser_probe.origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/Matrix'
#         if node in keys: cs_laser_probe.matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/MapToRefOrigin'
#         if node in keys: cs_laser_probe.map_to_ref_origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/MapToRefMatrix'
#         if node in keys: cs_laser_probe.map_to_ref_matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/Origin'
#         if node in keys: cs_multi_channel_plate.origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/Matrix'
#         if node in keys: cs_multi_channel_plate.matrix = h5main[node][:,:]
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/MapToRefOrigin'
#         if node in keys: cs_multi_channel_plate.map_to_ref_origin = h5main[node][:].flatten()
#         node = 'MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/MapToRefMatrix'
#         if node in keys: cs_multi_channel_plate.map_to_ref_matrix = h5main[node][:,:]
#         
#         ##how many detectors?
#         #node = 'MeasurementID'+str(simid)+'/Tool/CoordinateSystems/Detector'
#         
#         #how many operators?
#         ###MK::handling of multiple operators?
#         node = 'MeasurementID'+str(simid)+'/Metadata/Operators'
#         for obj in h5main[node].keys():
#             actor = metadata.m_create(Operator)
#             keyword = node + '/' + obj + '/Name'
#             if keyword in keys: actor.name = h5py_string_decode(h5main[keyword][()])
#         
#         node = 'MeasurementID'+str(simid)+'/Metadata/Timestamps/StartUtc'
#         if node in keys: time_stamps.start_utc = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Timestamps/EndUtc'       
#         if node in keys: time_stamps.end_utc = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Timestamps/StartLocal'       
#         if node in keys: time_stamps.start_local = h5py_string_decode(h5main[node][()])
#         node = 'MeasurementID'+str(simid)+'/Metadata/Timestamps/EndLocal'       
#         if node in keys: time_stamps.end_local = h5py_string_decode(h5main[node][()])       
#         
#         node = 'MeasurementID'+str(simid)+'/Metadata/ProcessStatus/Comment'
#         if node in keys: process_status.comment = h5py_string_decode(h5main[node][()])
#                 
#         #data section
#         node = 'MeasurementID'+str(simid)+'/Data/Laser/Emitter/Current'
#         if node in keys: d_emitter.current = h5main[node][()]
#         node = 'MeasurementID'+str(simid)+'/Data/Laser/Emitter/Wavelength'
#         if node in keys: d_emitter.wavelength = h5main[node][()]
#         node = 'MeasurementID'+str(simid)+'/Data/Laser/Emitter/Incidence'
#         if node in keys: d_emitter.incidence = h5main[node][()]
# 
#         h5main.close()
# 
#         #    # Import Data
#         #    data = measurement.m_create(Data)
#         #    for i, label in enumerate(labels_to_match):
#         #        spectrum = data.m_create(Spectrum)
#         #        if label == 'count':
#         #            value = np.array(item['data'][i])
#         #        else:
#         #            value = np.array(item['data'][i]) * ureg(item['metadata']['data_labels'][i]['unit'])
#         #        setattr(spectrum, label, value)
# 
#     def parse_nx5_calibration(self, mainfile: str, archive: EntryArchive, logger, simid = 1):
#         #parse mainfile
#         h5main = h5py.File( mainfile, 'r')
#         keys = h5main.keys()
#                 
#         #Create metadata-holding sections
#         calibration = archive.m_create(Calibration)
#         metadata = calibration.m_create(CalibrateMetadata)
#         
#         method = metadata.m_create(CalibrateMethod)
#         dataset = metadata.m_create(Dataset)
#         environment = metadata.m_create(CalibrateEnvironment)                
#         tool = metadata.m_create(CalibrateTool)
#         coordinate_systems = tool.m_create(CalibrateCoordinateSystems)
#         cs_reference = coordinate_systems.m_create(ReferenceCS)
#         components = tool.m_create(CalibrateComponents)
#         filter_hit_positions = components.m_create(FilterHitPositions)
#         filter_time_of_flight = components.m_create(FilterTimeOfFlight)
#         bowl_correction = components.m_create(BowlCorrection)
#         
#         #operators = metadata.m_create(Operator)
#         time_stamps = metadata.m_create(TimeStamps)
#         process_status = metadata.m_create(ProcessStatus)
#         
#         # Create data-holding sections
#         data = calibration.m_create(CalibrateData)
#         
#         node = 'CalibrationID'+str(simid)+'/Metadata/Method/Name'
#         if node in keys: method.name = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Dataset/Name'
#         if node in keys: dataset.name = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Dataset/UUID'
#         if node in keys: dataset.uuid = h5py_string_decode(h5main[node][()])
#         
#         node = 'CalibrationID'+str(simid)+'/Metadata/Environment/Computers'
#         if node in keys:
#             for obj in h5main[node].keys():
#                 computer = environment.m_create(Computer)
#                 node_obj = node + '/' + obj + '/Name'
#                 if node_obj in keys: computer.name = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/UUID'
#                 if node_obj in keys: computer.uuid = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/OperatingSystem'
#                 if node_obj in keys: computer.operating_system = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/MainMemory'
#                 if node_obj in keys: computer.mainmemory = h5py_string_decode(h5main[node_obj][()])
#                 sub_node = node + '/' + obj + '/CPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         cpu = computer.m_create(CPUSocket)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: cpu.name = h5py_string_decode(h5main[sub_node_obj][()])                     
#                 sub_node = node + '/' + obj + '/GPGPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         accl = computer.m_create(GPGPUSlot)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: accl.name = h5py_string_decode(h5main[sub_node_obj][()])
#                 sub_node = node + '/' + obj + '/Storage'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         dsk = computer.m_create(MountedDisk)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: dsk.name = h5py_string_decode(h5main[sub_node_obj][()])
#               
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/Name'
#         if node in keys: tool.name = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/Version'
#         if node in keys: tool.version = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/UUID'
#         if node in keys: tool.uuid = h5py_string_decode(h5main[node][()])
#         
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Origin'
#         if node in keys: cs_reference.origin = h5main[node][:].flatten()
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Matrix'
#         if node in keys: cs_reference.matrix = h5main[node][:,:]
#         
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/Components/HitPositionFilter/Name'
#         if node in keys: filter_hit_positions.name = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/Components/TimeOfFlightFilter/Name'
#         if node in keys: filter_time_of_flight.name = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Tool/Components/BowlCorrection/Name'
#         if node in keys: bowl_correction.name = h5py_string_decode(h5main[node][()])
#        
#         node = 'CalibrationID'+str(simid)+'/Metadata/Operators'
#         for obj in h5main[node].keys():
#             actor = metadata.m_create(Operator)
#             keyword = node + '/' + obj + '/Name'
#             if keyword in keys: actor.name = h5py_string_decode(h5main[keyword][()])
#         
#         node = 'CalibrationID'+str(simid)+'/Metadata/Timestamps/StartUtc'
#         if node in keys: time_stamps.start_utc = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Timestamps/EndUtc'       
#         if node in keys: time_stamps.end_utc = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Timestamps/StartLocal'       
#         if node in keys: time_stamps.start_local = h5py_string_decode(h5main[node][()])
#         node = 'CalibrationID'+str(simid)+'/Metadata/Timestamps/EndLocal'       
#         if node in keys: time_stamps.end_local = h5py_string_decode(h5main[node][()])       
#         
#         node = 'CalibrationID'+str(simid)+'/Metadata/ProcessStatus/Comment'
#         if node in keys: process_status.comment = h5py_string_decode(h5main[node][()])
#                 
#         #data section
#         node = 'CalibrationID'+str(simid)+'/Data'
#         ###MK::
#             
#         h5main.close()
# 
#     def parse_nx5_reconstruction(self, mainfile: str, archive: EntryArchive, logger, simid = 1):
#         h5main = h5py.File( mainfile, 'r')
#         keys = h5main.keys()
#                 
#         #Create metadata-holding sections
#         reconstruction = archive.m_create(Reconstruction)
#         metadata = reconstruction.m_create(ReconstructMetadata)
#         
#         method = metadata.m_create(ReconstructMethod)
#         dataset = metadata.m_create(Dataset)
#         environment = metadata.m_create(ReconstructEnvironment)                
#         tool = metadata.m_create(ReconstructTool)
#         coordinate_systems = tool.m_create(ReconstructCoordinateSystems)
#         cs_reference = coordinate_systems.m_create(ReferenceCS)
#         cs_reconstruction = coordinate_systems.m_create(ReconstructionCS)       
#         components = tool.m_create(ReconstructComponents)
#         recon_algo = components.m_create(ReconstructionAlgorithm)
#         
#         time_stamps = metadata.m_create(TimeStamps)
#         process_status = metadata.m_create(ProcessStatus)
#         
#         # Create data-holding sections
#         data = reconstruction.m_create(ReconstructData)
#         
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Method/Name'
#         if node in keys: method.name = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Dataset/Name'
#         if node in keys: dataset.name = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Dataset/UUID'
#         if node in keys: dataset.uuid = h5py_string_decode(h5main[node][()])
#         
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Environment/Computers'
#         if node in keys:
#             for obj in h5main[node].keys():
#                 computer = environment.m_create(Computer)
#                 node_obj = node + '/' + obj + '/Name'
#                 if node_obj in keys: computer.name = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/UUID'
#                 if node_obj in keys: computer.uuid = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/OperatingSystem'
#                 if node_obj in keys: computer.operating_system = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/MainMemory'
#                 if node_obj in keys: computer.mainmemory = h5py_string_decode(h5main[node_obj][()])
#                 sub_node = node + '/' + obj + '/CPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         cpu = computer.m_create(CPUSocket)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: cpu.name = h5py_string_decode(h5main[sub_node_obj][()])                     
#                 sub_node = node + '/' + obj + '/GPGPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         accl = computer.m_create(GPGPUSlot)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: accl.name = h5py_string_decode(h5main[sub_node_obj][()])
#                 sub_node = node + '/' + obj + '/Storage'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         dsk = computer.m_create(MountedDisk)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: dsk.name = h5py_string_decode(h5main[sub_node_obj][()])
#               
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Name'
#         if node in keys: tool.name = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Version'
#         if node in keys: tool.version = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/UUID'
#         if node in keys: tool.uuid = h5py_string_decode(h5main[node][()])
#         
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Origin'
#         if node in keys: cs_reference.origin = h5main[node][:].flatten()
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Matrix'
#         if node in keys: cs_reference.matrix = h5main[node][:,:]
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/Origin'
#         if node in keys: cs_reconstruction.origin = h5main[node][:].flatten()
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/Matrix'
#         if node in keys: cs_reconstruction.matrix = h5main[node][:,:]
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/MapToRefOrigin'
#         if node in keys: cs_reconstruction.map_to_ref_origin = h5main[node][:].flatten()
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/MapToRefMatrix'
#         if node in keys: cs_reconstruction.map_to_ref_matrix = h5main[node][:,:]
#         
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/Name'
#         if node in keys: recon_algo.name = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/Protocol'
#         if node in keys: recon_algo.protocol = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/FieldFactor'
#         if node in keys: recon_algo.field_factor = h5main[node][()]
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/ImageCompressionFactor'
#         if node in keys: recon_algo.image_compression_factor = h5main[node][()]
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/AtomicVolume'
#         if node in keys: recon_algo.atomic_volume = h5main[node][()]
#        
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Operators'
#         for obj in h5main[node].keys():
#             actor = metadata.m_create(Operator)
#             keyword = node + '/' + obj + '/Name'
#             if keyword in keys: actor.name = h5py_string_decode(h5main[keyword][()])
#         
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Timestamps/StartUtc'
#         if node in keys: time_stamps.start_utc = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Timestamps/EndUtc'       
#         if node in keys: time_stamps.end_utc = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Timestamps/StartLocal'       
#         if node in keys: time_stamps.start_local = h5py_string_decode(h5main[node][()])
#         node = 'ReconstructionID'+str(simid)+'/Metadata/Timestamps/EndLocal'       
#         if node in keys: time_stamps.end_local = h5py_string_decode(h5main[node][()])       
#         
#         node = 'ReconstructionID'+str(simid)+'/Metadata/ProcessStatus/Comment'
#         if node in keys: process_status.comment = h5py_string_decode(h5main[node][()])
#                 
#         #data section
#         node = 'ReconstructionID'+str(simid)+'/Data/NumberOfIonRecords'
#         if node in keys: data.ion_records = h5main[node]
#         node = 'ReconstructionID'+str(simid)+'/Data/PulseNumber'
#         if node in keys: data.pulse_number = h5main[node][:] #.flatten()
#         node = 'ReconstructionID'+str(simid)+'/Data/PulseFrequency'
#         if node in keys: data.ion_records = h5main[node][:] #.flatten()
#         node = 'ReconstructionID'+str(simid)+'/Data/HitPositions'
#         if node in keys: data.hit_positions = h5main[node][:,:]
#         node = 'ReconstructionID'+str(simid)+'/Data/LaserEnergy'
#         if node in keys: data.laser_energy = h5main[node][:] #.flatten()
#         node = 'ReconstructionID'+str(simid)+'/Data/LaserPosition'
#         if node in keys: data.laser_position = h5main[node][:,:]
#         node = 'ReconstructionID'+str(simid)+'/Data/StandingVoltage'
#         if node in keys: data.standing_voltage = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/PulseVoltage'
#         if node in keys: data.pulse_voltage = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/ReflectronVoltage'
#         if node in keys: data.reflectron_voltage = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/SpecimenHolderPosition'
#         if node in keys: data.specimen_holder_position = h5main[node][:,:]        
#         node = 'ReconstructionID'+str(simid)+'/Data/TimeOfFlight'
#         if node in keys: data.time_of_flight = h5main[node][:]        
#         node = 'ReconstructionID'+str(simid)+'/Data/MassToChargeRatio'
#         if node in keys: data.mass_to_charge_state_ratio = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/SpecimenTemperature'
#         if node in keys: data.specimen_temperature = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/Multiplicity'
#         if node in keys: data.multiplicity = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/PulseSinceLastEvenPulse'
#         if node in keys: data.pulse_since_last_event_pulse = h5main[node][:]
#         node = 'ReconstructionID'+str(simid)+'/Data/IonsPerPulse'
#         if node in keys: data.ions_per_pulse = h5main[node][:] #.flatten()
#         node = 'ReconstructionID'+str(simid)+'/Data/IonPositions'
#         if node in keys: data.ion_positions = h5main[node][:,:].flatten()
#         
#         h5main.close()
#         
#     def parse_nx5_ranging(self, mainfile: str, archive: EntryArchive, logger, simid = 1):
#         h5main = h5py.File( mainfile, 'r')
#         keys = h5main.keys()
#         
#         #Create metadata-holding sections
#         ranging = archive.m_create(Ranging)
#         metadata = ranging.m_create(RangingMetadata)
#         
#         method = metadata.m_create(RangingMethod)
#         dataset = metadata.m_create(Dataset)
#         environment = metadata.m_create(RangingEnvironment)                
#         tool = metadata.m_create(RangingTool)
#         components = tool.m_create(RangingComponents)
#         tof_to_mq_mapping = components.m_create(TimeOfFlightToMassToChargeMapping)
#         filters = components.m_create(RangingFilters)
#         filter_mass_to_charge = filters.m_create(FilterMassToCharge)
#         filter_multiplicity = filters.m_create(FilterMultiplicity)
#         filter_ion_position = filters.m_create(FilterIonPosition)
#         filter_ion_id = filters.m_create(FilterIonID)
#         binning = components.m_create(Binning)
#         background = components.m_create(BackgroundQuantification)
#         peak_deconvolution = components.m_create(PeakDeconvolution)
#         peak_detection = components.m_create(PeakDetection)
#         signal_smooth = components.m_create(SignalSmoothing)
#         
#         time_stamps = metadata.m_create(TimeStamps)
#         process_status = metadata.m_create(ProcessStatus)
#         
#         # Create data-holding sections
#         data = ranging.m_create(RangingData)
#         profiling = data.m_create(ExecutionDetails)
#         ion_species = data.m_create(IonSpecies)
#         
#         node = 'RangingID'+str(simid)+'/Metadata/Method/Name'
#         if node in keys: method.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Dataset/Name'
#         if node in keys: dataset.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Dataset/UUID'
#         if node in keys: dataset.uuid = h5py_string_decode(h5main[node][()])
#         
#         node = 'RangingID'+str(simid)+'/Metadata/Environment/Computers'
#         if node in keys:
#             for obj in h5main[node].keys():
#                 computer = environment.m_create(Computer)
#                 node_obj = node + '/' + obj + '/Name'
#                 if node_obj in keys: computer.name = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/UUID'
#                 if node_obj in keys: computer.uuid = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/OperatingSystem'
#                 if node_obj in keys: computer.operating_system = h5py_string_decode(h5main[node_obj][()])
#                 node_obj = node + '/' + obj + '/MainMemory'
#                 if node_obj in keys: computer.mainmemory = h5py_string_decode(h5main[node_obj][()])
#                 sub_node = node + '/' + obj + '/CPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         cpu = computer.m_create(CPUSocket)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: cpu.name = h5py_string_decode(h5main[sub_node_obj][()])                     
#                 sub_node = node + '/' + obj + '/GPGPUs'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         accl = computer.m_create(GPGPUSlot)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: accl.name = h5py_string_decode(h5main[sub_node_obj][()])
#                 sub_node = node + '/' + obj + '/Storage'
#                 if sub_node in keys:
#                     for sub_obj in h5main[sub_node].keys():
#                         dsk = computer.m_create(MountedDisk)
#                         sub_node_obj = sub_node + '/' + sub_obj + '/Name'
#                         if sub_node_obj in keys: dsk.name = h5py_string_decode(h5main[sub_node_obj][()])
#               
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Name'
#         if node in keys: tool.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Version'
#         if node in keys: tool.version = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/UUID'
#         if node in keys: tool.uuid = h5py_string_decode(h5main[node][()])
#         ###MK::coordinate systems
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/TimeOfFlightToMassToCharge/Comment'
#         if node in keys: tof_to_mq_mapping.comment = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/MassToCharge/Name'
#         if node in keys: filter_mass_to_charge.name = h5py_string_decode(h5main[node][()])
#         ###MK::
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/Multiplicity/Name'
#         if node in keys: filter_multiplicity.name = h5py_string_decode(h5main[node][()])
#         ###MK::
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonPosition/Name'
#         if node in keys: filter_ion_position.name = h5py_string_decode(h5main[node][()])
#         ###MK::
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonID/Name'
#         if node in keys: filter_ion_id.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonID/MinIncrMaxLinearSubSampling'
#         if node in keys: filter_ion_id.min_incr_max = h5main[node][:].flatten()
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/BinningAlgorithm/MassToCharge/Type'
#         if node in keys: binning.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/BackgroundAlgorithm/Name'
#         if node in keys: background.name = h5py_string_decode(h5main[node][()])
#         ###MK::node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/BinningAlgorithm/Ranges'
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDeconvolutionAlgorithm/Name'
#         if node in keys: peak_deconvolution.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDetectionAlgorithm/Name'
#         ###MK::node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDetectionAlgorithm/Ranges'
#         if node in keys: peak_detection.name = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/SignalSmoothingAlgorithm/Name'
#         if node in keys: signal_smooth.name = h5py_string_decode(h5main[node][()])
#         ###MK::node = 'RangingID'+str(simid)+'/Metadata/Tool/Components/SignalSmoothingAlgorithm/Ranges'
#         
#         node = 'RangingID'+str(simid)+'/Metadata/Operators'
#         for obj in h5main[node].keys():
#             actor = metadata.m_create(Operator)
#             keyword = node + '/' + obj + '/Name'
#             if keyword in keys: actor.name = h5py_string_decode(h5main[keyword][()])
#         
#         node = 'RangingID'+str(simid)+'/Metadata/Timestamps/StartUtc'
#         if node in keys: time_stamps.start_utc = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Timestamps/EndUtc'       
#         if node in keys: time_stamps.end_utc = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Timestamps/StartLocal'       
#         if node in keys: time_stamps.start_local = h5py_string_decode(h5main[node][()])
#         node = 'RangingID'+str(simid)+'/Metadata/Timestamps/EndLocal'       
#         if node in keys: time_stamps.end_local = h5py_string_decode(h5main[node][()])       
#         
#         node = 'RangingID'+str(simid)+'/Metadata/ProcessStatus/Comment'
#         if node in keys: process_status.comment = h5py_string_decode(h5main[node][()])
#                 
#         #data section
#         node = 'RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfThreadsPerProcess'
#         if node in keys: profiling.max_nthreads_per_process = h5main[node][0]
#         node = 'RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfGPGPUsPerProcess'
#         if node in keys: profiling.max_ngpgpus_per_process = h5main[node][0]
#         node = 'RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfProcesses'
#         if node in keys: profiling.max_nprocesses = h5main[node][0]
#         
#         node = 'RangingID'+str(simid)+'/Data/IonSpecies/NumberOfDisjointSpecies'
#         if node in keys: ion_species.ndisjoint_ion_species = h5main[node][()]
#         node = 'RangingID'+str(simid)+'/Data/IonSpecies/MaxNumberOfAtomsPerIon'
#         if node in keys: ion_species.max_natoms_per_ion = h5main[node][()]
#         #N = ion_species.ndisjoint_ion_species
#         node = 'RangingID'+str(simid)+'/Data/IonSpecies'
#         for obj in h5main[node].keys():
#             speci = ion_species.m_create(MolecularIonDef)
#             node_obj = node + '/' + obj + '/ChargeState'
#             if node_obj in keys: speci.charge_state = h5main[node_obj][()]
#             node_obj = node + '/' + obj + '/IsotopeVector'
#             if node_obj in keys: speci.isotope_vector = h5main[node_obj][:]
#             node_obj = node + '/' + obj + '/MassToChargeRanges'
#             if node_obj in keys: speci.mass_to_charge_ranges = h5main[node_obj][:]
#         
#         #node = 'RangingID'+str(simid)+'/Data/IonSpecies/IonIsotopes'
#         ##tmp = h5main[node][:,:]
#         ##n = np.shape(tmp)[0]
#         ##for i in np.arange(0,n):
#         ##    obj = node + '/' + str(i) + '/Isotopes'
#         ####MK::should this matrix be flattened?
#         #if node in keys: ion_species.ion_isotopes = h5main[node][:,:].flatten()
#         #node = 'RangingID'+str(simid)+'/Data/IonSpecies/IonCharges'
#         ####MK::transform into vector
#         #if node in keys: ion_species.ion_charges = np.asarray(h5main[node], dtype=np.uint32) #[:]
#         #node = 'RangingID'+str(simid)+'/Data/IonSpecies/Ranges'
#         #for obj in h5main[node].keys():
#         #    range_def = ion_species.m_create(RangeDef)
#         #    node_obj = node + '/' + obj + '/MinMaxMassToCharge'
#         #    if node_obj in keys: range_def.min_max_mass_to_charge = h5main[node_obj][:,:]
#        
#         h5main.close()
# =============================================================================


    #def parse(self, mainfile: str, archive: EntryArchive, logger):
    #    return
    
        #, supplfile: str = ''
        # mainfile is an *.nx5 NeXuS/HDF5 file with metadata and measured data from the experiment
        # mainfile is expected to contain top-sections MeasurementID*, CalibrationID*, ReconstructionID*
        # mainfile may optionally contain top-section RangingID* given when ranging details were reported
        # made via e.g. AMETEK/Cameca IVAS or APSuite respectively
        # supplfile is an *.nx5 file with preparsed data to feed pieces of information from
        # the AMETEK/Cameca APSuite database to be able to feed pieces of information otherwise
        # inaccessible via classical file formats of the APT/FIM community
        
        # we assume the parser faces a list of random files that a user has uploaded
        # for APT we can imagine the following situations:
        # most common is user has uploaded a pair of pos, epos, or apt6 file respectively plus a single associated range file as rrng or rng
        # people have often multiple versions of ranging definitions which to choose?, need to have a mechanism to distinguish and add multiple to a single reconstruction
        # people may upload only a range file, this should be rejected because rrng and rng do not store the associated dataset
        # people may upload one pos, epos, or apt6 respectively but multiple range files, which range file tochoose?
        # people may upload files without appropriate endings, we need to throw an error here
        # people may upload with capitalized file endings, we need to transform the file endings to lower-case first
        # people may upload without file endings, need to throw
        # people may upload very large (how do we define large?) files, need to have a mechanism above which data arrays are downsampled
        # people may upload range files with inconsistent definitions or errors need to have a policy
        
        # # facing these use cases, we need to make a minimum amount of assumptions
        # # Read the JSON file with the array of uploaded files
        # mainfile = '/home/kuehbach/GITHUB/NOMAD-COE/nomad-parser-aptfim-leap/tests/data/example.upload.json'
        # with open(mainfile, 'rt') as f:
        #     file_data = set(json.load(f)) #only unique names not-capitalization-sensitive
        
        # #detect which use case we are facing
        # file_types = {}
        # search_types = np.asarray(['.nx5', '.h5', '.hdf5', '.pos', '.epos', '.apt', '.rrng', '.rng'], np.str)
        # for typ in search_types:
        #     file_types[typ] = []
        #     for i in file_data: ###MK::implement more efficiently
        #         if i.lower().endswith(typ):
        #             file_types[typ].append(i)
        
        # # pick relevant parser base on the use case faced or throw an error
        # if sum(val != [] for val in file_types.values()) == 1:
        #     # preferred case 0: only a single NeXus/H5/HDF5 file as created from paraprobe-transcoder or
        #     # seldom cases of sharing unranged measurements via pos, epos, or apt file formats
        #     if len(file_types['.nx5']) == 1:
        #         #use parser with *.nx5 file in file_types['.nx5'][0]
        #     else if len(file_types['.h5']) == 1:
        #         #use parser with *.h5 file in file_types['.h5'][0]
        #     else if len(file_types['.hdf5']) == 1:
        #         #use parser with *.h5 file in file_types['.h5'][0]
        #     else if len(file_types['.pos']) == 1:
        #         #use parser with *.pos file in file_types['.pos'][0]
        #     else if len(file_types['.epos']) == 1:
        #         #use parser with *.epos file in file_types['.epos'][0]
        #     else if len(file_types['.apt']) == 1:
        #         #use parser with *.apt file in file_types['.apt'][0]
        #         ###MK::we mean here the new file format introduced with APSuite6
        #         ###MK::and now the magic question is what is the magic file identifier for the old
        #         ###MK::Rouen group ? based APT file format ??????        
        #     else:
        #         raise ValueError('When you upload files of a single filetype these should be either nx5/h5/hdf5 or pos, epos, or apt !')
        # else if sum(val != [] for val in file_types.values()) == 2:
        #     # classical case 1: a single POS||EPOS||APT file plus a single associated RNG||RRNG file, all other files treated as supplementary provided they are not POS||EPOS||APT||RNG||RRNG||NX5
        #     if len(file_types['.pos']) == 1:
        #         if len(file_types['.rrng']) == 1:
        #             #parse pos/rrng pair
        #             pass
        #         else if len(file_types['.rng']) == 1:
        #             #parse pos/rng pair
        #             pass
        #         else:
        #             raise ValueError('When you upload a single *.epos file you need to give a single associated either *.rrng or *.rng range file !')
        #     else if len(file_types['.epos']) == 1:
        #         if len(file_types['.rrng']) == 1:
        #             #parse epos/rrng pair
        #             pass
        #         else if len(file_types['.rng']) == 1:
        #             #parse epos/rng pair
        #             pass
        #         else:
        #             raise ValueError('When you upload a single *.epos file you need to give a single associated either *.rrng or *.rng range file !')
        #     else if len(file_types['.apt']) == 1:
        #         if len(file_types['.rrng']) == 1:
        #             #parse apt/rrng pair
        #             pass
        #         else if len(file_types['.rng']) == 1:
        #             #parse apt/rng pair
        #             pass
        #         else:
        #             raise ValueError('When you upload a single *.apt file you need to give a single associated either *.rrng or *.rng range file !')
        #     else:
        #         raise ValueError('Either deliver nx5/h5/hdf5 file with measurement and ranging or pair of *.pos/*.epos/*.apt with a single associated *.rrng/*.rng range file !')
        # else:
        #     raise ValueError('Either deliver nx5/h5/hdf5 file with measurement and ranging or pair of *.pos/*.epos/*.apt with a single associated *.rrng/*.rng range file !')
   
        # # Log a hello world, just to get us started.
        # logger.info('Testing the APTFIM LEAP World')
        
        # #mainfile = '..tests/data/example.nx5'
        # #mainfile = '/home/kuehbach/GITHUB/NOMAD-COE/nomad-parser-aptfim-leap/tests/data/example.nx5'
        # if not mainfile.endswith('.nx5'):
        #     raise ValueError('Mainfile needs to have *.nx5 file ending !')
        # ###MK::add check for existence of the file
        
        # #if not supplfile.endswith('.nx5'):
        # #    raise ValueError('Supplementary file needs to have *.nx5 file ending !')
        
        #self.parse_nx5_measurement( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_measurement')
        #self.parse_nx5_calibration( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_calibration')
        #self.parse_nx5_reconstruction( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_reconstruction')
        #self.parse_nx5_ranging( mainfile, archive, logger, 1 )
        #logger.info('Parsed section_ranging')
