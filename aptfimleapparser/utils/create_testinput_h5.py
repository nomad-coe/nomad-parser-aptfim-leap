#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:26:33 2021
@author: kuehbach

a much more covering example with metadata for atom probe microscopy experiments which matches the fields discussed with the
International Field Emission Society's Atom Probe Technical Committee and uses the discussed top-level hierarchy definitions
from the FAIRmat Area B discussions 
"""

import os, sys, glob
from pathlib import Path
import numpy as np
import h5py
from datetime import datetime, timezone

h5fn = 'example.h5'
#h5fn = 'attribute.test.nx5'
h5w = h5py.File( h5fn, 'w')
#dst = h5w.create_group('MeasurementID'+str(simid))
#testing the writing and reading of group/dataset attributes
#dst.attrs['Temperature'] = 273.15
#dst.attrs['Unit'] = 'K'
#h5w.close()
#h5r = h5py.File( h5fn, 'r')
#src = h5r['MeasurementID'+str(simid)]
#src.attrs.keys()
#h5r.close()

#create the HDF5 tree of data and metadata, we populate here with dummy data but make the example packed with
#the most interesting quantities to be reported ideally when measuring an atom probe microscopy specimen
#we make here no attempt to parse results coming from a processing of such measured data, such as iso-surface
#computations or other computational geometry, spatial statistics, or AI-method results applied on APT dataset
#this should be part of another parser, there is a sophisticated open-source alternative to the commercial 
#postprocessing tool of the community available which I contribute as a plugin for the nomad analytics
#toolkit, it makes sense to define then with this tool how we should go about storing results from
#computational and data analytics tasks applied on measured atom probe data sets

#MaRkusKuehbach, I proposed the following structure for such an HDF5 file (needs to be cast into a paper tbd):
    
#Measurement
#Calibration
#Reconstruction
#Ranging

#why is it smart to define these four sections?
#As of 2021 virtually all APT/FIM groups world-wide use microscopes of a single company.
#This company has legally protected their source code so the purest results that experimentalists can get
#from an APT experiment is encoded in a proprietary file format which experimentalists are not allowed 
#legally to get access to for all data fields, plus the format is in key parts undocumented for the public.
#Most importantly, the file contains calibration values and routines which are specific to AMETEK/Cameca
#(the manufacturer) instrument and hence are also not shared with the public.
#The only way that is legally safe prior future negotiations with the company to get your results out of this cage
#is to use the also proprietary analysis software, formerly known as IVAS since version 4 now AP Suite
#During such initial processing after your microscope session the proprietary calibrations
#are applied via this software and you get a reconstructed dataset and calibrated mass-to-charge-state ratio values
#This is what 99% of the community works and is used to work with, so our first aim to get into NOMAD.
#There are very few specialists' groups currently (2021) which build their own microscope from scratch
#e.g. Rouen group (Vurpillot group), FAU Erlangen (Felfer group), Stuttgart (Schmitz group), PNNL group 
#These groups have their own way of storing their data, luckily all of them are open to data sharing.
#Further work is required to get their formats supported as well in NOMAD

#The above concept of having four layers mirrors the current procedure of creating an APT/FIM experiment

#Measurement stores what is immediately relevant to the actual microscope session, i.e. data acquisition while
#evaporating the specimen, i.e. physically destroying the specimen during the measurement by removing atoms

#Calibration stores or could be used to store the calibrations, so delay-line detector settings

#Reconstruction stores or could be used to store all metadata related to the process of evaluating numerically 
#a physical model of how field evaporation proceeds and the physical assumption inherent in this model
#what the initial specimen shape is to compute a model of how the atoms were likely positioned in the 
#evaporated specimen, keep in mind in APT the specimen is the lens of the microscope!

#Ranging is used to store all metadata related how a mass-to-charge-state ratio of an ion is assumed
#to translate into a so-called ion type. Because of facing limited mass-to-charge-resolution and ambiguous case, 
#ranging has to build on assumptions here I use a recently proposed (Kuehbach et al. Microsc. Microanal. 2021)
#very general strategy to store information (metadata) on the ion type definitions, much more covering than are
#current formats (RNG and RRNG)
#It is possible that during field-evaporation not only single element isotopes are detected but also
#combinations of multiple ions or fragments hitting the detector.I n the APT/FIM community such ions
# are known as molecular ions, we can represent each isotope by a unique hash value of Nprotons + 256*Nneutrons, 
#if no isotope information is desired, i.e. we wish to communicate only element names, we set Nneutrons = 0 by definition
#Furthermore, we reserve the special hash value 0, i.e. Nprotons = 0 && Nneutrons = 0, for defining a defaul type
#for ions for which we either have not found or are not interested in performing a ranging.

#This brings an HDF5-based data format which can handle all current ways how APT measurements are accessible
#by experimentalists. If in the future the manufacturers are more willing to share details, we have then
#also with this format the required flexibility to store also such pieces of information in the above sections
#I should say that currently most APT file formats (pos, epos, apt) do not store all (meta)data handled
#by the here instantiated HDF5-based file. So mainly the purpose of this example is here
#to have a tool available for developing the parser and to reality-check this parser to find whether or not
#it is sophisticated enough to handle the cases which the scientists experience and ask for in their daily practice.

#I am a fan of keeping things organized, so have a ID for each section, thereby one could for instance,
#have, and this is common in practice, multiple ranging definitions for the same reconstructed tuple of atom positions 
#and mass-to-charge

simid = 1

#dummy assumed number of atoms. here unrealistically low to keep the example file very small, 
#for real experiments N is between 1.0e6 and 1.0-1.5e9 million ions for larger dataset volume the
#specimens has be longer and longer physically because gaining volume by making wider specimens is limited
#as you cannot realize the high fields at the apex required to provoke atom removal
#however, the longer the specimen gets the less mechanically stable it is the higher the chances for
#for failure, i.e. rupture or what not

N = 10
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Name', data = np.str('My precious PtIr specimen'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/UUID', data = np.str('DummySampleUUID'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/TrivialName', data = np.str('PtIr'))
asciiList = [n.encode("ascii", "ignore") for n in ['Pt', 'Ir']]
charlength = 'S' + str(len(max(asciiList, key = len)))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Elements', (len(asciiList),1), charlength, asciiList)
f32 = [0.9, 0.1]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/NominalComposition', (len(f32),1), 'f4', f32)
dst.attrs['Unit'] = 'at.-%'
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Shape', data = np.str('tip'))
f32 = [24.0, 24.0, 100.0]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Dimensions', (len(f32),1), 'f4', f32)
dst.attrs['Unit'] = 'nm'
###MK::the following should be an array of element names! variable length string array
asciiList = [n.encode("ascii", "ignore") for n in ['Platinum', 'Ir']]
charlength = 'S' + str(len(max(asciiList, key = len)))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/Elements', (len(asciiList),1), charlength, asciiList)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/Description', data = np.str('solid solution'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/CrystalStructure', data = np.str('fcc'))
f32 = [0.9, 0.1]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/NominalComposition', (len(f32),1), 'f4', f32)
dst.attrs['Unit'] = 'at.-%'
dst = h5w.create_group('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest')
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Shape', data = np.str(''))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Dimensions', data = np.str(''))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Offset', data = np.str(''))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Stride', data = np.str(''))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Experiment/Name', data = np.str('APTFIM-LEAP'))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/Name', data = np.str('DummyComputerName'))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/UUID', data = np.str('DummyComputerUUID'))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/MainMemory', data = np.str('DummyMainMemory'))
#asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
#charlength = 'S' + str(len(max(asciiList, key = len)))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/CPUs/0/Name', data = np.str('Xeon'))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
#dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/Storage/0/Name', data = np.str('DummySSD'))

dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Author/0/Name', data = np.str('Markus K\"uhbach'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Author/0/Affiliation', data = np.str('FHI Berlin'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Author/0/Email', data = np.str('mymail@dummy.de'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Author/1/Name', data = np.str('Nomad Experimentalist'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Author/1/Affiliation', data = np.str('NomadLand'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Author/1/Email', data = np.str('nomadland@dummy.de'))
dtg = datetime.now(timezone.utc)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Experiment/TimeStamp/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Experiment/TimeStamp/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Experiment/TimeStamp/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Experiment/TimeStamp/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))


dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Name', data = np.str('DummyLeapMicroscope'))
####MK::for systems with laser only or hybrid systems
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Laser/Emitter/Name', data = np.str('DummyLaserEmitter'))
f32 = 100.0
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Laser/Emitter/LaserEnergy', (1,1), 'f4', f32)
dst.attrs['Unit'] = 'pJ'
###MK::for systems with HV pulser only or hybrid systems
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/HighVoltagePulser/Name', data = np.str('DummyHVPulser'))
f32 = 250.0
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/HighVoltagePulser/PulseRateTarget', (1,1), 'f4', f32)
dst.attrs['Unit'] = 'kHz'

dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Reflectron/Name', data = np.str('DummyReflectron'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Aperture/0/Name', data = np.str('DummyAperture'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/AnalysisChamber/Name', data = np.str('DummyAnalysisChamber'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/UltraHighVacuumPump/Name', data = np.str('DummyUHVPump'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/SpecimenHolder/Name', data = np.str('DummmySpecimenHolder'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/Name', data = np.str('DelayLineDetector'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/Readout', data = np.str('DelayLine'))
u32 = [1024, 1024]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/Resolution', (len(u32),1), 'u4', u32)
dst.attrs['Unit'] = 'pixel^2'
f32 = [20.0, 20.0]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/Dimensions', (len(f32),1), 'f4', u32)
dst.attrs['Unit'] = 'cm'
f32 = 300.0
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/FlightPathLength', (1,1), 'f4', f32)
dst.attrs['Unit'] = 'mm'
f32 = 0.0025
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/DetectionRateTarget', (1,1), 'f4', f32)
dst.attrs['Unit'] = 'ions/pulse'
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/0/GeometryOpticalEquivalent', data = np.str('DummyEquivalent'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/1/Name', data = np.str('BaseTemperatureDetector'))
f32 = 40.0
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/1/BaseTemperatureTarget', (1,1), 'f4', f32)
dst.attrs['Unit'] = 'K'
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/2/Name', data = np.str('AnalysisChamberPressureDetector'))
f32 = 1.0e-10
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/Component/Detector/2/AnalysisChamberPressure', (1,1), 'f4', f32)
dst.attrs['Unit'] = 'Torr'

f32o = [0.0, 0.0, 0.0]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reference/Origin', (3,1), 'f4', f32o)
f32m = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reference/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/AnalysisChamber/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/AnalysisChamber/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/AnalysisChamber/MapToRefOrigin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/AnalysisChamber/MapToRefMatrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/SpecimenHolder/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/SpecimenHolder/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/SpecimenHolder/MapToRefOrigin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/SpecimenHolder/MapToRefMatrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Specimen/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Specimen/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Specimen/MapToRefOrigin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Specimen/MapToRefMatrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/LaserProbe/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/LaserProbe/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/LaserProbe/MapToRefOrigin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/LaserProbe/MapToRefMatrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Detector/0/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Detector/0/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Detector/0/MapToRefOrigin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Detector/0/MapToRefMatrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/UserGenerated/ProcessStatus/Comment', data = np.str('Successfully created dummy file for testing'))
dst = h5w.create_group('MeasurementID'+str(simid)+'/Metadata/DataHeader')

dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/FlightPath/Spatial', data = np.str('DummyFlightPathSpatial'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/FlightPath/Timing', data = np.str('DummyFlightPathTiming'))
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Laser/Emitter/Current', data = np.float32(0.0))
#dst.attrs['Unit'] = ''
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Laser/Emitter/Wavelength', data = np.float32(0.0))
dst.attrs['Unit'] = 'nm'
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Laser/Emitter/Incidence', data = np.float32(0.0))
#dst.attrs['Unit'] = 'Torr'
dst = h5w.create_group('MeasurementID'+str(simid)+'/Data/HighVoltagePulser')
f32 = np.full( (N,1), 50.0, 'f4')
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/AnalysisChamber/Pressure', (N,1), 'f4', f32)
dst = h5w.create_group('MeasurementID'+str(simid)+'/Data/UltraHighVacuumPump')
f32 = np.array([np.linspace(1,N,N),]*3).transpose()
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/SpecimenHolder/Position', (N,3), 'f4', f32)
dst.attrs['Unit'] = 'cm'
dst = h5w.create_group('MeasurementID'+str(simid)+'/Data/Detector/0')
dst = h5w.create_group('MeasurementID'+str(simid)+'/Data/Detector/1')
f32 = np.full( (N,1), 40.0, 'f4')
dst = h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Detector/1/SpecimenTemperature', (N,1), 'f4', f32)
dst.attrs['Unit'] = 'K'
dst = h5w.create_group('MeasurementID'+str(simid)+'/Data/Images')

#calibration is a pure computational process so we do not have a specimen or sample, only a dataset !
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Dataset/0/Name', data = np.str('My precious RHIT/HITS file for the PtIr sample'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Dataset/0/UUID', data = np.str('DummyDatasetUUID'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Name', data = np.str('APTFIM-Reconstruction'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/Name', data = np.str('DummyComputerName'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/UUID', data = np.str('DummyComputerUUID'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/MainMemory', data = np.str('DummyMainMemory'))
asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
charlength = 'S' + str(len(max(asciiList, key = len)))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/CPUSocket/0/CPU/0/Name', data = np.str('Xeon'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/AcceleratorSocket/0/Accelerator/Name', data = np.str('Nvidia V100 32GB'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/Computer/0/Storage/0/Name', data = np.str('DummySSD'))
dtg = datetime.now(timezone.utc)
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/TimeStamp/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/TimeStamp/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/TimeStamp/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Analysis/TimeStamp/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/Name', data = np.str('IVAS'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/Version', data = np.str('v3.6.4'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/UUID', data = np.str('DummyInstrumentID'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/Component/HitPositionFilter/Name', data = np.str('all'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/Component/TimeOfFlightFilter/Name', data = np.str('all'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/Component/BowlCorrection/Name', data = np.str('DummyBowlCorrectionName'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reference/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reference/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Author/0/Name', data = np.str('IVAS application'))
dst = h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/UserGenerated/ProcessStatus/Comment', data = np.str('Successful calibration inside IVAS'))
dst = h5w.create_group('CalibrationID'+str(simid)+'/Metadata/DataHeader')
dst = h5w.create_group('CalibrationID'+str(simid)+'/Data')

dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Dataset/0/Name', data = np.str('My precious RHIT/HITS file for the PtIr sample'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Dataset/0/UUID', data = np.str('DummyDatasetUUID'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Name', data = np.str('APTFIM-Reconstruction'))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/Name', data = np.str('DummyComputerName'))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/UUID', data = np.str('DummyComputerUUID'))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/MainMemory', data = np.str('DummyMainMemory'))
#asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
#charlength = 'S' + str(len(max(asciiList, key = len)))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/CPUs/0/Name', data = np.str('Xeon'))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
#dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/Computer/0/Storage/0/Name', data = np.str('DummySSD'))
dtg = datetime.now(timezone.utc)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/TimeStamp/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/TimeStamp/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/TimeStamp/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Analysis/TimeStamp/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Name', data = np.str('IVAS'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Version', data = np.str('v3.6.4'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/UUID', data = np.str('DummyInstrumentID'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Component/ReconstructionAlgorithm/Name', data = np.str('DummyReconstructionName'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Component/ReconstructionAlgorithm/Protocol', data = np.str('IVAS (modified Bas et al.)'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Component/ReconstructionAlgorithm/FieldFactor', (1,), 'f4', data = np.float32(3.0))
dst.attrs['Unit'] = '1'
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Component/ReconstructionAlgorithm/ImageCompressionFactor', (1,), 'f4', data = np.float32(1.01))
dst.attrs['Unit'] = '1'
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/Component/ReconstructionAlgorithm/AtomicVolume', (1,), 'f4', data = np.float32(50.0))
dst.attrs['Unit'] = 'nm^3'
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reference/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reference/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reconstruction/Origin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reconstruction/Matrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reconstruction/MapToRefOrigin', (3,1), 'f4', f32o)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Instrument/CoordinateSystem/Reconstruction/MapToRefMatrix', (4,4), 'f4', f32m)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Author/0/Name', data = np.str('IVAS application'))
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/UserGenerated/ProcessStatus/Comment', data = np.str('Successful reconstruction with the IVAS software'))
dst = h5w.create_group('ReconstructionID'+str(simid)+'/Metadata/DataHeader')

u32 = np.linspace(1,N,N)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseNumber', (N, 1), 'u4', data = u32)
dst.attrs['Unit'] = '1'
f32 = np.full( (N,1), 200e3, 'f4')
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseFrequency', (N,1), 'f4', data = f32)
dst.attrs['Unit'] = 'kHz' ###???
f32 = np.array([np.linspace(1,N,N),]*2).transpose()
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/HitPositions', (N, 2), 'f4', data = f32)
dst.attrs['Unit'] = 'cm'
f32 = np.full( (N,1), 0.0, 'f4')
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/LaserEnergy', (N,1), 'f4', data = f32)
dst.attrs['Unit'] = 'pJ' ###???
f32 = np.array([np.full( (N,1), 0.0, 'f4'),]*3).transpose()
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/LaserPosition', (N,3), 'f4', data = f32)
#dst.attrs['Unit'] = '' ###???
f32 = np.array(np.linspace(1,N,N)*1.0e3)
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/StandingVoltage', (N, 1), 'f4', data = f32)
dst.attrs['Unit'] = 'V'
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseVoltage', (N, 1), 'f4', data = f32)
dst.attrs['Unit'] = 'V'
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/ReflectronVoltage', (N, 1), 'f4', data = f32)
dst.attrs['Unit'] = 'V'
f32 = np.array([np.linspace(1,N,N)*0.001,]*3).transpose()
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/SpecimenHolderPosition', (N, 3), 'f4', data = f32)
#dst.attrs['Unit'] = '' ###???
f32 = np.float32( np.linspace(1,N,N)*1.0e-9 )
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/TimeOfFlight', (N, 1), 'f4', data = f32)
dst.attrs['Unit'] = 'ns'
f32 = np.float32( np.linspace(1,N,N)*10.0 )
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/MassToChargeRatio', (N, 1), 'f4', data = f32)
dst.attrs['Unit'] = 'Da'
f32 = np.full( (N,1), 40.0, 'f4' )
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/SpecimenTemperature', (N, 1), 'f4', data = f32)
dst.attrs['Unit'] = 'K'
u32 = np.full( (N,1), 1, 'u4' )
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/Multiplicity', (N, 1), 'u4', data = u32)
dst.attrs['Unit'] = '1'
u32 = np.full( (N,1), 0, 'u4' )
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseSinceLastEventPulse', (N, 1), 'u4', data = u32)
dst.attrs['Unit'] = '1'
u32 = np.full( (N,1), 1, 'u4' )
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/IonsPerPulse', (N, 1), 'u4', data = u32)
dst.attrs['Unit'] = '1'
f32 = np.array([np.linspace(1,N,N),]*3).transpose()
dst = h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/IonPositions', (N, 3), 'f4', data = f32)
dst.attrs['Unit'] = 'nm'


#with APSuite6 typically people combine reconstruction and ranging
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Dataset/0/Name', data = np.str('My precious RHIT/HITS file for the PtIr sample'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Dataset/0/UUID', data = np.str('DummyDatasetUUID'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Analysis/Name', data = np.str('APTFIM-Ranging'))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Analysis/Environment/Computers/0/Name', data = np.str('DummyComputerName'))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/UUID', data = np.str('DummyComputerUUID'))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/MainMemory', data = np.str('DummyMainMemory'))
#asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
#charlength = 'S' + str(len(max(asciiList, key = len)))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/CPUs/0/Name', data = np.str('Xeon'))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/Storage/0/Name', data = np.str('DummySSD'))
dtg = datetime.now(timezone.utc)
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Analysis/TimeStamp/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Analysis/TimeStamp/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Analysis/TimeStamp/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Analysis/TimeStamp/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))

dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Name', data = np.str('IVAS'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Version', data = np.str('v3.6.4'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/UUID', data = np.str('DummyInstrumentID'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/TimeOfFlightToMassToCharge/Comment', data = np.str('m proportional to calibrated tof with proprietary calibration factors'))
#dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/Instrument/Components/SubSampling')
#dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/Instrument/Components/SubSampling/MassToCharge')
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Components/SubSampling/MassToCharge/Type')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/MassToCharge/Name', data = np.str('DummyFilterMassToChargeName'))
f32 = [0.0, 1200.0]
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/MassToCharge/LinearRanges/0/MinMaxMassToCharge', (1,2), 'f4', data = f32)
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/Multiplicity/Name', data = np.str('DummyFilterMultiplicityName'))
dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/Multiplicity/LinearRanges/0/MinMaxMultiplicity')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/IonPosition/Name', data = np.str('DummyFilterIonPositionsName'))
f32 = [[-25.0, 25.0], [-25.0, 25.0], [0.1, 120.0]]
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/IonPosition/AABBEnsemble/0/MinMaxPositions', (3,2), 'f4', data = f32)
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/IonID/Name', data = np.str('DummyFilterIonIDName'))
u32 = [0, 1, N]
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/Filter/IonID/MinIncrMaxLinearSubSampling', (1,3), 'u4', data = u32)
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/BinningAlgorithm/MassToCharge/Type', data = np.str('0.001 Da'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/BackgroundAlgorithm/Name', data = np.str('DummyBackgroundAlgorithmName'))
dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/Instrument/Component/BackgroundAlgorithm/Ranges')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/PeakDeconvolutionAlgorithm/Name', data = np.str('DummyPeakDeconvolutionAlgorithmName'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/PeakDetectionAlgorithm/Name', data = np.str('DummyPeakDetectionAlgorithmName'))
dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/Instrument/Component/PeakDetectionAlgorithm/Ranges')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Instrument/Component/SignalSmoothingAlgorithm/Name', data = np.str('DummySignalSmoothingAlgorithmName'))
dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/Instrument/Component/SignalSmoothingAlgorithm/Ranges')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Author/0/Name', data = np.str('IVAS application'))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Metadata/UserGenerated/ProcessStatus/Comment', data = np.str('Successful ranging using IVAS'))
dst = h5w.create_group('RangingID'+str(simid)+'/Metadata/DataHeader')
#dst = h5w.create_group('RangingID'+str(simid)+'/Data/ExecutionDetails')
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfThreadsPerProcess', (1,), 'u4', data = np.uint32(1))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfGPGPUsPerProcess', (1,), 'u4', data = np.uint32(0))
#dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfProcesses', (1,), 'u4', data = np.uint32(1))
Natoms = 32
dst = h5w.create_group('RangingID'+str(simid)+'/Data/IonSpecies')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/NumberOfDisjointSpecies', data = np.uint32(1))
dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/MaxNumberOfAtomsPerIon', data = np.uint32(Natoms))
dst.attrs['Comment'] = 'specifies the maximum length of the molecular ion isotope vector'
u16 = np.zeros([Natoms], np.uint16)
dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/0/IsotopeVector', data = u16)
dst.attrs['Comment'] = 'vector of hash values which decode hash = Nprotons + 256*Nneutrons'
dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/0/Charge', data = np.int8(0))
dst.attrs['Unit'] = 'eV'
f32 = [0.000, 0.001]
dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/0/MassToChargeRanges', (1,2), 'f4', data = f32)
dst.attrs['Unit'] = 'Da'
u8 = np.zeros([N,1], 'u8')
dst = h5w.create_dataset('RangingID'+str(simid)+'/Data/IonLabels', (N,1), 'u1', u8)

dst = h5w.close()
