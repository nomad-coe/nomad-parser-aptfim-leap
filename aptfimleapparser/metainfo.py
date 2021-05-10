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

from nomad.metainfo import Section, Quantity, MSection, SubSection
import numpy as np

from nomad.datamodel import EntryArchive
from nomad.metainfo.metainfo import Datetime, MCategory


# =============================================================================
# class UserProvided(MCategory):
#     pass
# 
# 
# class MeasureMethod(MSection):
#     name = Quantity(type=str, description='')
# 
# class Constituent(MSection):
#     elements = Quantity(type=np.dtype(np.str), description='')
#     description = Quantity(type=str, description='')
#     crystal_structure = Quantity(type=str, description='')
#     nominal_composition = Quantity(type=np.dtype(np.float64), description='')
#     
# #class RegionOfInterest(MSection):
# #    shape = Quantity(type=str, description='')
# #    dimensions = Quantity(type=np.dtype(np.float64), shape=['*'], unit='m', description='')
# #    offset = Quantity(type=np.dtype(np.uint32), shape=[3], description='')
# #    stride = Quantity(type=np.dtype(np.uint32), shape=[3], description='')
# 
# class Material(MSection):
#     trivial_name = Quantity(type=str, description='')
#     elements = Quantity(type=np.dtype(np.str), shape=['*'])
#     ###MK::atomic percent how accepted in Nomad using ureg ?
#     nominal_composition = Quantity(type=np.dtype(np.float64), description='')
#     shape = Quantity(type=str, description='')
#     dimensions = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     section_constituents = SubSection(sub_section=Constituent, repeats=True)
#     ###MK::section_roi = SubSection(sub_section=RegionOfInterest)
# 
# class Sample(MSection):
#     name = Quantity(type=str, description='')
#     uuid = Quantity(type=str, description='')
#     section_material = SubSection(sub_section=Material)
#     
# class CPUSocket(MSection):
#     name = Quantity(type=str, description='')
#     
# class GPGPUSlot(MSection):
#     name = Quantity(type=str, description='')
#     
# class MountedDisk(MSection):
#     name = Quantity(type=str, description='')   
# 
# class Computer(MSection):
#     name = Quantity(type=str, description='given name for the computer')
#     uuid = Quantity(type=str, description='hardware hash value to identify the system')
#     operating_system = Quantity(type=str, description='')
#     main_memory = Quantity(type=str, description='which main memory and total capacity')
#     section_cpus = SubSection(sub_section=CPUSocket, repeats=True)
#     section_gpgpus = SubSection(sub_section=GPGPUSlot, repeats=True)
#     section_disks = SubSection(sub_section=MountedDisk, repeats=True)
# 
# class MeasureEnvironment(MSection):
#     section_computers = SubSection(sub_section=Computer, repeats=True)
#      
# class CoordinateSystemDef(MSection):
#     origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
# =============================================================================
    
class ReferenceCS(MSection):
    origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
    matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
    #map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
    #map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
    
# =============================================================================
# class SpecimenChamberCS(MSection):
#     origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')   
# 
# class SpecimenHolderCS(MSection):
#     origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     
# class SpecimenCS(MSection):
#     origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     
# class LaserProbeCS(MSection):
#     origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     
# class MultiChannelPlateCS(MSection):
#     origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
#     map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
#     map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
# 
# class CoordinateSystems(MSection):
#     ###MK::would it be possible to have multiple inheritance ?
#     section_reference = SubSection(sub_section=ReferenceCS)
#     section_specimen_chamber = SubSection(sub_section=SpecimenChamberCS)
#     section_specimen_holder = SubSection(sub_section=SpecimenHolderCS)
#     section_specimen = SubSection(sub_section=SpecimenCS)
#     section_laser_probe = SubSection(sub_section=LaserProbeCS)
#     section_detectors = SubSection(sub_section=MultiChannelPlateCS) #repeats=True)
# 
# class MeasureEmitter(MSection):
#     name = Quantity(type=str, description='')
#     
# class MeasureLaser(MSection):
#     name = Quantity(type=str, description='')
#     section_emitter = SubSection(sub_section=MeasureEmitter)
# 
# class MeasureHighVoltagePulser(MSection):
#     name = Quantity(type=str, description='')
# 
# class MeasureReflectron(MSection):
#     name = Quantity(type=str, description='')
# 
# class MeasureAperture(MSection):
#     name = Quantity(type=str, description='')
#     
# class MeasureSpecimenChamber(MSection):
#     name = Quantity(type=str, description='')
# 
# class MeasureUltraHighVacuumPump(MSection):
#     name = Quantity(type=str, description='')
# 
# class MeasureSpecimenHolder(MSection):
#     name = Quantity(type=str, description='')
#     
# class MeasureDetectors(MSection):
#     pass
# 
# class MeasureComponents(MSection):
#     #name = Quantity(type=str, description='')
#     section_laser = SubSection(sub_section=MeasureLaser)
#     section_high_voltage_pulser = SubSection(sub_section=MeasureHighVoltagePulser)
#     section_reflectron = SubSection(sub_section=MeasureReflectron)
#     section_aperture = SubSection(sub_section=MeasureAperture)
#     section_specimen_chamber = SubSection(sub_section=MeasureSpecimenChamber)
#     section_ultra_high_vacuum_pump = SubSection(sub_section=MeasureUltraHighVacuumPump)
#     section_specimen_holder = SubSection(sub_section=MeasureSpecimenHolder)
#     section_detectors = SubSection(sub_section=MeasureDetectors)    
# 
# class MeasureTool(MSection):
#     name = Quantity(type=str, description='')
#     section_components = SubSection(sub_section=MeasureComponents)
#     section_coordinates = SubSection(sub_section=CoordinateSystems)
# 
# class Operator(MSection):
#     name = Quantity(type=str, description='')
# =============================================================================

class TimeStamps(MSection):
    start_utc = Quantity(type=str, description='')
    end_utc = Quantity(type=str, description='')
    start_local = Quantity(type=str, description='')
    end_local = Quantity(type=str, description='')

# =============================================================================
# class ProcessStatus(MSection):
#     comment = Quantity(type=str, description='')
# 
# class MeasureMetadata(MSection):
#     section_method = SubSection(sub_section=MeasureMethod)
#     section_sample = SubSection(sub_section=Sample)
#     section_environment = SubSection(sub_section=MeasureEnvironment)
#     section_tool = SubSection(sub_section=MeasureTool)
#     section_operators = SubSection(sub_section=Operator, repeats=True)
#     section_time_stamps = SubSection(sub_section=TimeStamps)
#     section_process_status = SubSection(sub_section=ProcessStatus)
#     #notes = Quantity(type=str, categories=[UserProvided])
# 
# 
# class MeasureDataFlightPath(MSection):
#     spatial = Quantity(type=str, description='')
#     timing = Quantity(type=str, description='')
#     
# class MeasureDataEmitter(MSection):
#     current = Quantity(type=np.dtype(np.float64), unit='', description='')
#     wavelength = Quantity(type=np.dtype(np.float64), unit='', description='')
#     incidence = Quantity(type=np.dtype(np.float64), unit='', description='')
# 
# class MeasureDataLaser(MSection):
#     section_emitter = SubSection(sub_section=MeasureDataEmitter)
#     
# class MeasureData(MSection):
#     section_flight_path = SubSection(sub_section=MeasureDataFlightPath)
#     section_laser = SubSection(sub_section=MeasureDataLaser)
#     section_high_voltage_pulser = SubSection(sub_section=MeasureHighVoltagePulser)
#     section_specimen_chamber = SubSection(sub_section=MeasureSpecimenChamber)
#     section_ulra_high_vacuum_pump = SubSection(sub_section=MeasureUltraHighVacuumPump)
#     section_specimen_holder = SubSection(sub_section=MeasureSpecimenHolder)
#     section_detectors = SubSection(sub_section=MeasureDetectors, repeats=True)
#     notes = Quantity(type=str, categories=[UserProvided])
# =============================================================================

class Measurement(MSection):
    pass
    #section_metadata = SubSection(sub_section=MeasureMetadata)
    #section_data = SubSection(sub_section=MeasureData)
    #description = Quantity(type=str, categories=[UserProvided])
 
# ============================================================================= 
# class CalibrateMethod(MSection):
#     name = Quantity(type=str, description='')
# 
# class Dataset(MSection):
#     name = Quantity(type=str, description='')
#     uuid = Quantity(type=str, description='')
# 
# class CalibrateEnvironment(MSection):
#     section_computers = SubSection(sub_section=Computer, repeats=True)
# 
# class FilterHitPositions(MSection):
#     name = Quantity(type=str, description='')
#     
# class FilterTimeOfFlight(MSection):
#     name = Quantity(type=str, description='')
#    
# class BowlCorrection(MSection):
#     name = Quantity(type=str, description='')
# 
# class CalibrateComponents(MSection):
#     section_filter_hit_positions = SubSection(sub_section=FilterHitPositions)
#     section_filter_time_of_flight = SubSection(sub_section=FilterTimeOfFlight)
#     section_bowl_correction = SubSection(sub_section=BowlCorrection)
# 
# class CalibrateCoordinateSystems(MSection):
#     ###MK::would it be possible to have multiple inheritance ?
#     section_reference = SubSection(sub_section=ReferenceCS)
# 
# class CalibrateTool(MSection):
#     name = Quantity(type=str, description='')
#     version = Quantity(type=str, description='')
#     uuid = Quantity(type=str, description='')
#     section_coordinates = SubSection(sub_section=CalibrateCoordinateSystems)
#     section_components = SubSection(sub_section=CalibrateComponents)
#     section_operators = SubSection(sub_section=Operator, repeats=True)
#     section_time_stamps = SubSection(sub_section=TimeStamps)
#     section_process_status = SubSection(sub_section=ProcessStatus)    
# 
# class CalibrateMetadata(MSection):
#     section_method = SubSection(sub_section=CalibrateMethod)
#     section_dataset = SubSection(sub_section=Dataset)
#     section_environment = SubSection(sub_section=CalibrateEnvironment)
#     section_tool = SubSection(sub_section=CalibrateTool)
#     section_operators = SubSection(sub_section=Operator, repeats=True)
#     section_time_stamps = SubSection(sub_section=TimeStamps)
#     section_process_status = SubSection(sub_section=ProcessStatus)
#     
# class CalibrateData(MSection):
#     pass
# =============================================================================
 
class Calibration(MSection):
    pass
    #section_metadata = SubSection(sub_section=CalibrateMetadata)
    #section_data = SubSection(sub_section=CalibrateData)
   


class ReconstructingAnalysis(MSection):
    name = Quantity(type=str, description='')
    section_time_stamp = SubSection(sub_section=TimeStamps)

class ReconstructingAuthor(MSection):
    name = Quantity(type=str, description='')
    affiliation = Quantity(type=str, description='')
    email = Quantity(type=str, description='')    
    
class ReconstructingDataHeader(MSection):
    pass
    #section_computers = SubSection(sub_section=Computer, repeats=True)

class ReconstructingDataset(MSection):
    name = Quantity(type=str, description='')
    uuid = Quantity(type=str, description='')
    
class ReconstructionCS(MSection):
    origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
    matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
    map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
    map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
    
class IonCollectorCS(MSection):
    origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
    matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
    map_to_ref_origin = Quantity(type=np.dtype(np.float64), shape=[3], unit='m', description='')
    map_to_ref_matrix = Quantity(type=np.dtype(np.float64), shape=[4,4], description='')
    
class ReconstructingCoordinateSystem(MSection):
    ###MK::would it be possible to have multiple inheritance ?
    section_reference = SubSection(sub_section=ReferenceCS)
    section_reconstruction = SubSection(sub_section=ReconstructionCS)
    section_ion_collector = SubSection(sub_section=IonCollectorCS)
   
class ReconstructionAlgorithm(MSection):
    name = Quantity(type=str, description='')
    protocol = Quantity(type=str, description='which reconstruction approach see for instance book by Gault et al. (2012) Springer')
    field_factor = Quantity(type=np.dtype(np.float32), unit='1.0', description='kf field factor parameter')
    image_compression_factor = Quantity(type=np.dtype(np.float32), unit='1.0', description='image compression parameter')
    atomic_volume = Quantity(type=np.dtype(np.float32), unit='1/nm^3', description='average volume of an ion')

class ReconstructingComponent(MSection):
    section_reconstruction_algorithm = SubSection(sub_section=ReconstructionAlgorithm)

class ReconstructingInstrument(MSection):
    name = Quantity(type=str, description='')
    version = Quantity(type=str, description='')
    uuid = Quantity(type=str, description='')
    section_component = SubSection(sub_section=ReconstructingComponent)
    section_coordinate_system = SubSection(sub_section=ReconstructingCoordinateSystem)
    
class ReconstructingUserGenerated(MSection):
    process_status = Quantity(type=str, description='result of the analysis task')

class ReconstructingMetadata(MSection):
    #section_method = SubSection(sub_section=ReconstructMethod)
    #section_dataset = SubSection(sub_section=Dataset)
    #section_environment = SubSection(sub_section=ReconstructEnvironment)
    #section_tool = SubSection(sub_section=ReconstructTool)
    #section_operators = SubSection(sub_section=Operator, repeats=True)
    #section_time_stamps = SubSection(sub_section=TimeStamps)
    #section_process_status = SubSection(sub_section=ProcessStatus)
    section_analysis = SubSection(sub_section=ReconstructingAnalysis)
    section_author = SubSection(sub_section=ReconstructingAuthor, repeats=True)
    section_data_header = SubSection(sub_section=ReconstructingDataHeader)
    section_dataset = SubSection(sub_section=ReconstructingDataset, repeats=True)
    section_instrument = SubSection(sub_section=ReconstructingInstrument)
    section_user_generated = SubSection(sub_section=ReconstructingUserGenerated) 

class ReconstructingData(MSection):
    ion_records = Quantity(type=np.dtype(np.uint32), description='total number of detected evaporated ions')
    pulse_number = Quantity(type=np.dtype(np.float32), shape=['ion_records'], description='???')
    pulse_frequency = Quantity(type=np.dtype(np.float32), unit='Hz', description='frequency of the pulser')
    hit_positions = Quantity(type=np.dtype(np.float32), shape=['ion_records', 2], unit='mm', description='positions of ion impact on the detector')
    laser_energy = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='J', description='')
    laser_position = Quantity(type=np.dtype(np.float32), shape=['ion_records', 3], unit='', description='???')
    standing_voltage = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='V', description='???')
    pulse_voltage = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='V', description='???')
    reflectron_voltage = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='V', description='???')
    specimen_holder_position = Quantity(type=np.dtype(np.float32), shape=['ion_records', 3], unit='', description='???')
    time_of_flight = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='ns', description='???') #calibrations involved?
    mass_to_charge_state_ratio = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='Da', description='???')
    specimen_temperature = Quantity(type=np.dtype(np.float32), shape=['ion_records'], unit='K', description='???')
    ion_multiplicity = Quantity(type=np.dtype(np.uint8), shape=['ion_records'], description='???')
    pulse_since_last_event_pulse = Quantity(type=np.dtype(np.uint32), shape=['ion_records'], description='???')
    ions_per_pulse = Quantity(type=np.dtype(np.uint32), shape=['ion_records'], description='???')
    ion_positions = Quantity(type=np.dtype(np.float32), shape=['ion_records', 3], unit='nm', description='reconstructed positions')
    
class Reconstruction(MSection):
    section_metadata = SubSection(sub_section=ReconstructingMetadata)
    section_data = SubSection(sub_section=ReconstructingData)


class RangingAnalysis(MSection):
    name = Quantity(type=str, description='')
    section_time_stamp = SubSection(sub_section=TimeStamps)

class RangingAuthor(MSection):
    name = Quantity(type=str, description='')
    affiliation = Quantity(type=str, description='')
    email = Quantity(type=str, description='')    
    
class RangingDataHeader(MSection):
    pass
    #section_computers = SubSection(sub_section=Computer, repeats=True)

class RangingDataset(MSection):
    name = Quantity(type=str, description='')
    uuid = Quantity(type=str, description='')

class TimeOfFlightToMassToChargeMapping(MSection):
    comment = Quantity(type=str, description='')

###MK::can we add dtype let inherit MSection, and more?
class LinearRangeMassToCharge(MSection): #, dtype):
    min_incr_max = Quantity(type=np.dtype(np.float32), shape=[3], unit='Da', description='min, incr, max of range intervals')

class FilterMassToCharge(MSection):
    name = Quantity(type=str, description='')
    section_linear_range = SubSection(sub_section=LinearRangeMassToCharge, repeats=True)

class LinearRangeMultiplicity(MSection):
    min_incr_max = Quantity(type=np.dtype(np.uint8), shape=[3], description='')

class FilterMultiplicity(MSection):
    name = Quantity(type=str, description='')
    section_linear_range = SubSection(sub_section=LinearRangeMultiplicity, repeats=True)

class AxisAlignedBoundingBox(MSection):
    min_max = Quantity(type=np.dtype(np.float32), shape=[3,2], unit='nm', description='')

class FilterIonPosition(MSection):
    name = Quantity(type=str, description='')
    section_aabb_ensemble = SubSection(sub_section=AxisAlignedBoundingBox, repeats=True)

class FilterIonID(MSection):
    name = Quantity(type=str, description='')
    min_incr_max = Quantity(type=np.dtype(np.uint32), shape=[3], description='')

class RangingFilter(MSection):
    section_filter_mass_to_charge = SubSection(sub_section=FilterMassToCharge)
    section_filter_multiplicity = SubSection(sub_section=FilterMultiplicity)
    section_filter_ion_position = SubSection(sub_section=FilterIonPosition)
    section_filter_ion_id = SubSection(sub_section=FilterIonID)

###binning, backgr, peak deconvol, peak detect, signal smooth
class Binning(MSection):
    name = Quantity(type=str, description='')
    section_mass_to_charge = SubSection(sub_section=LinearRangeMassToCharge)
    
class BackgroundQuantification(MSection):
    name = Quantity(type=str, description='')
    #section_range = SubSection(sub_section=Ranges)
    
class PeakDeconvolution(MSection):
    name = Quantity(type=str, description='')
    
class PeakDetection(MSection):
    name = Quantity(type=str, description='')
    #section_range = SubSection(sub_section=Ranges)
    
class SignalSmoothing(MSection):
    name = Quantity(type=str, description='')
    #section_range = SubSection(sub_section=Ranges)

class RangingComponent(MSection):
    section_tof_to_mq_mapping = SubSection(sub_section=TimeOfFlightToMassToChargeMapping)
    ###MK::sub-sampling
    section_filter = SubSection(sub_section=RangingFilter)
    section_binning = SubSection(sub_section=Binning)
    section_background = SubSection(sub_section=BackgroundQuantification)
    section_peak_deconvolution = SubSection(sub_section=PeakDeconvolution)
    section_peak_detection = SubSection(sub_section=PeakDetection)
    section_signal_smoothing = SubSection(sub_section=SignalSmoothing)

class RangingInstrument(MSection):
    name = Quantity(type=str, description='')
    version = Quantity(type=str, description='')
    uuid = Quantity(type=str, description='')
    section_component = SubSection(sub_section=RangingComponent)

class RangingUserGenerated(MSection):
    process_status = Quantity(type=str, description='result of the analysis task')

class RangingMetadata(MSection):
    section_analysis = SubSection(sub_section=RangingAnalysis)
    section_author = SubSection(sub_section=RangingAuthor, repeats=True)
    section_data_header = SubSection(sub_section=RangingDataHeader)
    section_dataset = SubSection(sub_section=RangingDataset, repeats=True)
    section_instrument = SubSection(sub_section=RangingInstrument)
    section_user_generated = SubSection(sub_section=RangingUserGenerated) 

#class ExecutionDetails(MSection):
#    max_nthreads_per_process = Quantity(type=np.dtype(np.uint32), description='how many (OpenMP) threads were spawn per thread')
#    max_ngpgpus_per_process = Quantity(type=np.dtype(np.uint32), description='how many GPGPUs were used per process')
#    max_nprocesses = Quantity(type=np.dtype(np.uint32), description='how many (MPI) processes were used')

#class Profiling(MSection):
#    #section_exec_details = SubSection(sub_section=ExecutionDetails)
  
class MolecularIonDef(MSection):
    identifier = Quantity(type=np.dtype(np.uint8), unit='', description='unique identifier')
    charge = Quantity(type=np.dtype(np.int8), unit='eV', description='charge of the molecular ion')
    isotope_vector = Quantity(type=np.dtype(np.uint16), description='matrix of hash values specifying the isotopes in each molecular ion, one row per molecular ion, hash value nprotons + nneutrons*256, descending order')
    mass_to_charge_ranges = Quantity(type=np.dtype(np.float32), unit='Da', description='matrix of left (min) and right (max) bounds [] where ions are labelled, each row one interval definition')
    
class IonSpecies(MSection):
    ndisjoint_ion_species = Quantity(type=np.dtype(np.uint32), description='how many different species do we distinguish')
    max_natoms_per_ion = Quantity(type=np.dtype(np.uint32), description='how many atoms are at most accepted to build a molecular ion')
    section_ions = SubSection(sub_section=MolecularIonDef, repeats=True)

class RangingData(MSection):
    #section_profiling = SubSection(sub_section=ExecutionDetails)
    section_ion_species = SubSection(sub_section=IonSpecies)
    ion_labels = Quantity(type=np.dtype(np.uint8), description='ID resolving which atoms were ranged as which ion species')    

class Ranging(MSection):
    section_metadata = SubSection(sub_section=RangingMetadata)
    section_data = SubSection(sub_section=RangingData)

class MyEntryArchive(EntryArchive):
    m_def = Section(extends_base_section=True)
    section_measurement = SubSection(sub_section=Measurement)
    section_calibration = SubSection(sub_section=Calibration)
    section_reconstruction = SubSection(sub_section=Reconstruction)
    section_ranging = SubSection(sub_section=Ranging)