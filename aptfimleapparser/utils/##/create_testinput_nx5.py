#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 12:48:12 2021
@author: kuehbach
"""

import os, sys, glob
from pathlib import Path
import numpy as np
#basePath = '/home/kuehbach/GITHUB/FRWR3_KOCH_GROUP/code/frwr/build'
#sys.path.append(basePath)
import h5py
from datetime import datetime, timezone

h5fn = 'example.nx5'
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

#create the NeXuS/HDF5 tree for
simid = 1
#dummy assumed number of atoms
N = 10
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Method/Name', data = np.str('APTFIM-LEAP'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Name', data = np.str('My precious PtIr specimen'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/UUID', data = np.str('DummySampleUUID'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/TrivialName', data = np.str('PtIr'))
asciiList = [n.encode("ascii", "ignore") for n in ['Pt', 'Ir']]
charlength = 'S' + str(len(max(asciiList, key = len)))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Elements', (len(asciiList),1), charlength, asciiList)
f32 = [0.9, 0.1]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/NominalComposition', (len(f32),1), 'f4', f32)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Shape', data = np.str('tip'))
f32 = [24.0, 24.0, 100.0]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Dimensions', (len(f32),1), 'f4', f32)
###MK::the following should be an array of element names! variable length string array
asciiList = [n.encode("ascii", "ignore") for n in ['Platinum', 'Ir']]
charlength = 'S' + str(len(max(asciiList, key = len)))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/Elements', (len(asciiList),1), charlength, asciiList)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/Description', data = np.str('solid solution'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/CrystalStructure', data = np.str('fcc'))
f32 = [0.9, 0.1]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/Constituents/0/NominalComposition', (len(f32),1), 'f4', f32)
h5w.create_group('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest')
#h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Shape', data = np.str(''))
#h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Dimensions', data = np.str(''))
#h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Offset', data = np.str(''))
#h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Sample/Material/RegionOfInterest/Stride', data = np.str(''))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/Name', data = np.str('DummyComputerName'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/UUID', data = np.str('DummyComputerUUID'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/MainMemory', data = np.str('DummyMainMemory'))
asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
charlength = 'S' + str(len(max(asciiList, key = len)))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/CPUs/0/Name', data = np.str('Xeon'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Environment/Computers/0/Storage/0/Name', data = np.str('DummySSD'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Name', data = np.str('DummyLeapMicroscope'))
###MK::for systems with laser only or hybrid systems
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Laser/Emitter/Name', data = np.str('DummyLaserEmitter'))
###MK::for systems with HV pulser only or hybrid systems
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/HighVoltagePulser/Name', data = np.str('DummyHVPulser'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Reflectron/Name', data = np.str('DummyReflectron'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Aperture/0/Name', data = np.str('DummyAperture'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/SpecimenChamber/Name', data = np.str('DummySpecimenChamber'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/UltraHighVacuumPump/Name', data = np.str('DummyUHVPump'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/SpecimenHolder/Name', data = np.str('DummmySpecimenHolder'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Detectors/0/Name', data = np.str('DummyDelayLineDetector'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Detectors/0/Readout', data = np.str('DelayLine'))
u32 = [1024, 1024]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Detectors/0/Resolution', (len(u32),1), 'u4', u32)
f32 = [20.0, 20.0]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Detectors/0/Dimensions', (len(f32),1), 'f4', u32)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Detectors/0/GeometryOpticalEquivalent', data = np.str('DummyEquivalent'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/Components/Detectors/1/Name', data = np.str('DummyTemperatureDetector'))
f32o = [0.0, 0.0, 0.0]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Origin', (3,1), 'f4', f32o)
f32m = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/MapToRefOrigin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenChamber/MapToRefMatrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/MapToRefOrigin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/SpecimenHolder/MapToRefMatrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/MapToRefOrigin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Specimen/MapToRefMatrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/MapToRefOrigin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/LaserProbe/MapToRefMatrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/MapToRefOrigin', (3,1), 'f4', f32o)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Detectors/0/MapToRefMatrix', (4,4), 'f4', f32m)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Operators/0/Name', data = np.str('Markus K\"uhbach'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Operators/1/Name', data = np.str('Nomad Experimentalist'))
dtg = datetime.now(timezone.utc)
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Timestamps/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Timestamps/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Timestamps/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/Timestamps/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('MeasurementID'+str(simid)+'/Metadata/ProcessStatus/Comment', data = np.str('Successfully created dummy file for testing'))

h5w.create_dataset('MeasurementID'+str(simid)+'/Data/FlightPath/Spatial', data = np.str('DummyFlightPathSpatial'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/FlightPath/Timing', data = np.str('DummyFlightPathTiming'))
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Laser/Emitter/Current', data = np.float32(0.0))
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Laser/Emitter/Wavelength', data = np.float32(0.0))
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Laser/Emitter/Incidence', data = np.float32(0.0))
h5w.create_group('MeasurementID'+str(simid)+'/Data/HighVoltagePulser')
f32 = np.full( (N,1), 50.0, 'f4')
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/SpecimenChamber/Pressure', (N,1), 'f4', f32)
h5w.create_group('MeasurementID'+str(simid)+'/Data/UltraHighVacuumPump')
f32 = np.array([np.linspace(1,N,N),]*3).transpose()
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/SpecimenHolder/Position', (N,3), 'f4', f32)
h5w.create_group('MeasurementID'+str(simid)+'/Data/Detectors/0')
h5w.create_group('MeasurementID'+str(simid)+'/Data/Detectors/1')
f32 = np.full( (N,1), 40.0, 'f4')
h5w.create_dataset('MeasurementID'+str(simid)+'/Data/Detectors/1/SpecimenTemperature', (N,1), 'f4', f32)


h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Method/Name', data = np.str('APTFIM-Reconstruction'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Dataset/Name', data = np.str('My precious RHIT/HITS file for the PtIr sample'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Dataset/UUID', data = np.str('DummyDatasetUUID'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/Name', data = np.str('DummyComputerName'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/UUID', data = np.str('DummyComputerUUID'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/MainMemory', data = np.str('DummyMainMemory'))
asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
charlength = 'S' + str(len(max(asciiList, key = len)))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/CPUs/0/Name', data = np.str('Xeon'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Environment/Computers/0/Storage/0/Name', data = np.str('DummySSD'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/Name', data = np.str('IVAS'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/Version', data = np.str('v3.6.4'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/UUID', data = np.str('DummyToolID'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/Workflow/HitPositionFilter/Name', data = np.str('all'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/Workflow/TimeOfFlightFilter/Name', data = np.str('all'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Tool/Workflow/BowlCorrection/Name', data = np.str('DummyBowlCorrectionName'))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Operators/0/Name', data = np.str('IVAS application'))
dtg = datetime.now(timezone.utc)
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Timestamps/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Timestamps/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Timestamps/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/Timestamps/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('CalibrationID'+str(simid)+'/Metadata/ProcessStatus/Comment', data = np.str('Successful calibration inside IVAS'))
h5w.create_group('CalibrationID'+str(simid)+'/Data')


h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Method/Name', data = np.str('APTFIM-Reconstruction'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Dataset/Name', data = np.str('My precious RHIT/HITS file for the PtIr sample'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Dataset/UUID', data = np.str('DummyDatasetUUID'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/Name', data = np.str('DummyComputerName'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/UUID', data = np.str('DummyComputerUUID'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/MainMemory', data = np.str('DummyMainMemory'))
asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
charlength = 'S' + str(len(max(asciiList, key = len)))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/CPUs/0/Name', data = np.str('Xeon'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Environment/Computers/0/Storage/0/Name', data = np.str('DummySSD'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Name', data = np.str('IVAS'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Version', data = np.str('v3.6.4'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/UUID', data = np.str('DummyToolID'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reference/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/Origin', (3,1), 'f4', f32o)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/Matrix', (4,4), 'f4', f32m)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/MapToRefOrigin', (3,1), 'f4', f32o)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/CoordinateSystems/Reconstruction/MapToRefMatrix', (4,4), 'f4', f32m)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/Name', data = np.str('DummyReconstructionName'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/Protocol', data = np.str('IVAS (modified Bas et al.)'))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/FieldFactor', (1,), 'f4', data = np.float32(3.0))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/ImageCompressionFactor', (1,), 'f4', data = np.float32(1.01))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Tool/Components/ReconstructionAlgorithm/AtomicVolume', (1,), 'f4', data = np.float32(50.0))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Operators/0/Name', data = np.str('IVAS application'))
dtg = datetime.now(timezone.utc)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Timestamps/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Timestamps/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Timestamps/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/Timestamps/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('ReconstructionID'+str(simid)+'/Metadata/ProcessStatus/Comment', data = np.str('Successful reconstruction inside IVAS'))

u32 = np.linspace(1,N,N)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseNumber', (N, 1), 'u4', data = u32)
f32 = np.full( (N,1), 200e3, 'f4')
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseFrequency', (N,1), 'f4', data = f32)
f32 = np.array([np.linspace(1,N,N),]*2).transpose()
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/HitPositions', (N, 2), 'f4', data = f32)
f32 = np.full( (N,1), 0.0, 'f4')
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/LaserEnergy', (N,1), 'f4', data = f32)
f32 = np.array([np.full( (N,1), 0.0, 'f4'),]*3).transpose()
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/LaserPosition', (N,3), 'f4', data = f32)
f32 = np.array(np.linspace(1,N,N)*1.0e3)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/StandingVoltage', (N, 1), 'f4', data = f32)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseVoltage', (N, 1), 'f4', data = f32)
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/ReflectronVoltage', (N, 1), 'f4', data = f32)
f32 = np.array([np.linspace(1,N,N)*0.001,]*3).transpose()
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/SpecimenHolderPosition', (N, 3), 'f4', data = f32)
f32 = np.float32( np.linspace(1,N,N)*1.0e-9 )
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/TimeOfFlight', (N, 1), 'f4', data = f32)
f32 = np.float32( np.linspace(1,N,N)*10.0 )
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/MassToChargeRatio', (N, 1), 'f4', data = f32)
f32 = np.full( (N,1), 40.0, 'f4' )
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/SpecimenTemperature', (N, 1), 'f4', data = f32)
u32 = np.full( (N,1), 1, 'u4' )
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/Multiplicity', (N, 1), 'u4', data = u32)
u32 = np.full( (N,1), 0, 'u4' )
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/PulseSinceLastEventPulse', (N, 1), 'u4', data = u32)
u32 = np.full( (N,1), 1, 'u4' )
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/IonsPerPulse', (N, 1), 'u4', data = u32)
f32 = np.array([np.linspace(1,N,N),]*3).transpose()
h5w.create_dataset('ReconstructionID'+str(simid)+'/Data/IonPositions', (N, 3), 'f4', data = f32)


#with APSuite6 typically people combine reconstruction and ranging
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Method/Name', data = np.str('APTFIM-Ranging'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Dataset/Name', data = np.str('My precious RHIT/HITS file for the PtIr sample'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Dataset/UUID', data = np.str('DummyDatasetUUID'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/Name', data = np.str('DummyComputerName'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/UUID', data = np.str('DummyComputerUUID'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/OperatingSystem', data = np.str('Win10 DummyVersion'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/MainMemory', data = np.str('DummyMainMemory'))
asciiList = [n.encode("ascii", "ignore") for n in ['Xeon', 'Xeon']]
charlength = 'S' + str(len(max(asciiList, key = len)))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/CPUs/0/Name', data = np.str('Xeon'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/GPGPUs/0/Name', data = np.str('Nvidia V100 32GB'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Environment/Computers/0/Storage/0/Name', data = np.str('DummySSD'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Name', data = np.str('IVAS'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Version', data = np.str('v3.6.4'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/UUID', data = np.str('DummyToolID'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/TimeOfFlightToMassToCharge/Comment', data = np.str('m proportional to calibrated tof with proprietary calibration factors'))
#h5w.create_group('RangingID'+str(simid)+'/Metadata/Tool/Components/SubSampling')
#h5w.create_group('RangingID'+str(simid)+'/Metadata/Tool/Components/SubSampling/MassToCharge')
#h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/SubSampling/MassToCharge/Type')
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/MassToCharge/Name', data = np.str('DummyFilterMassToChargeName'))
f32 = [0.0, 1200.0]
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/MassToCharge/LinearRanges/0/MinMaxMassToCharge', (1,2), 'f4', data = f32)
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/Multiplicity/Name', data = np.str('DummyFilterMultiplicityName'))
h5w.create_group('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/Multiplicity/LinearRanges/0/MinMaxMultiplicity')
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonPosition/Name', data = np.str('DummyFilterIonPositionsName'))
f32 = [[-25.0, 25.0], [-25.0, 25.0], [0.1, 120.0]]
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonPosition/AABBEnsemble/0/MinMaxPositions', (3,2), 'f4', data = f32)
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonID/Name', data = np.str('DummyFilterIonIDName'))
u32 = [0, 1, N]
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/Filters/IonID/MinIncrMaxLinearSubSampling', (1,3), 'u4', data = u32)
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/BinningAlgorithm/MassToCharge/Type', data = np.str('0.001 Da'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/BackgroundAlgorithm/Name', data = np.str('DummyBackgroundAlgorithmName'))
h5w.create_group('RangingID'+str(simid)+'/Metadata/Tool/Components/BackgroundAlgorithm/Ranges')
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDeconvolutionAlgorithm/Name', data = np.str('DummyPeakDeconvolutionAlgorithmName'))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDetectionAlgorithm/Name', data = np.str('DummyPeakDetectionAlgorithmName'))
h5w.create_group('RangingID'+str(simid)+'/Metadata/Tool/Components/PeakDetectionAlgorithm/Ranges')
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Tool/Components/SignalSmoothingAlgorithm/Name', data = np.str('DummySignalSmoothingAlgorithmName'))
h5w.create_group('RangingID'+str(simid)+'/Metadata/Tool/Components/SignalSmoothingAlgorithm/Ranges')
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Operators/0/Name', data = np.str('IVAS application'))
dtg = datetime.now(timezone.utc)
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Timestamps/StartUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Timestamps/EndUtc', data = np.str(dtg)) #np.str(datetime.now(timezone.utc).strftime("%Y-%m-%d")+'-'+datetime.now(timezone.utc).strftime("%H:%M:%S"))
dtl = datetime.now()
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Timestamps/StartLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/Timestamps/EndLocal', data = np.str(dtl)) #datetime.now().strftime("%Y-%m-%d")+'-'+datetime.now().strftime("%H:%M:%S"))
h5w.create_dataset('RangingID'+str(simid)+'/Metadata/ProcessStatus/Comment', data = np.str('Successful ranging using IVAS'))

h5w.create_group('RangingID'+str(simid)+'/Data')
h5w.create_group('RangingID'+str(simid)+'/Data/ExecutionDetails')
h5w.create_dataset('RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfThreadsPerProcess', (1,), 'u4', data = np.uint32(1))
h5w.create_dataset('RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfGPGPUsPerProcess', (1,), 'u4', data = np.uint32(0))
h5w.create_dataset('RangingID'+str(simid)+'/Data/ExecutionDetails/MaxNumberOfProcesses', (1,), 'u4', data = np.uint32(1))
Natoms = 32
u16 = np.zeros([Natoms], np.uint16)
h5w.create_group('RangingID'+str(simid)+'/Data/IonSpecies')
h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/NumberOfDisjointSpecies', data = np.uint32(1))
h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/MaxNumberOfAtomsPerIon', data = np.uint32(Natoms))
h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/0/IsotopeVector', data = u16)
h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/0/ChargeState', data = np.uint8(0))
f32 = [0.000, 0.001]
h5w.create_dataset('RangingID'+str(simid)+'/Data/IonSpecies/0/MassToChargeRanges', (1,2), 'f4', data = f32)
u8 = np.zeros([N,1], 'u8')
h5w.create_dataset('RangingID'+str(simid)+'/Data/IonLabels', (N,1), 'u1', u8)

h5w.close()

