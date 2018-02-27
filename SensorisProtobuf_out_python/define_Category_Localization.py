import sys
import uuid
import time
import math
import numpy as np
import nvector as nv

import define_DataMessage as defDataMessage
import define_EventGroup as defEventGroup

# first of all, we import some basic compiled protobufs
from sensoris.protobuf.types import base_pb2
from sensoris.protobuf.types import source_pb2
from sensoris.protobuf.types import spatial_pb2
from sensoris.protobuf.messages import data_pb2

from sensoris.protobuf.categories import localization_pb2
from sensoris.protobuf.categories import brake_pb2
from sensoris.protobuf.categories import driving_behavior_pb2
from sensoris.protobuf.categories import intersection_attribution_pb2
from sensoris.protobuf.categories import map_pb2
from sensoris.protobuf.categories import object_detection_pb2
from sensoris.protobuf.categories import powertrain_pb2
from sensoris.protobuf.categories import road_attribution_pb2
from sensoris.protobuf.categories import traffic_events_pb2
from sensoris.protobuf.categories import traffic_maneuver_pb2
from sensoris.protobuf.categories import traffic_regulation_pb2
from sensoris.protobuf.categories import weather_pb2

def defineLocalizationCategory():

    # the localization category consists of mainly 3 items
    # #1 (vehicle position and orientation)
    # #2 (vehicle odometry)
    # #3 (vehicle dynamics)
    # all elements are defined as "repeated", that means, you can link multiple of them together   
    localLocalizationCategory = localization_pb2.LocalizationCategory()

    # hand over the information from sub-functions
    localLocalizationCategory.vehicle_position_and_orientation.extend([defineVehiclePositionAndOrientation()])
    localLocalizationCategory.vehicle_odometry.extend([defineVehicleOdometry()])
    localLocalizationCategory.vehicle_dynamics.extend([defineVehicleDynamics()])

    return localLocalizationCategory

def defineVehiclePositionAndOrientation():
    
    localVehiclePositionAndOrientation = localization_pb2.VehiclePositionAndOrientation()

    localEnvelope = base_pb2.EventEnvelope()
    localPosition = spatial_pb2.Position()
    localOrientation = spatial_pb2.Rotation()
    localNavigationSatelliteSystem = localization_pb2.VehiclePositionAndOrientation.NavigationSatelliteSystem()

    # ENVELOPE
    localEnvelope.id.value = 123
    localEnvelope.timestamp.CopyFrom(defEventGroup.defineTimestamp())

    # POSITION
    localPosition.CopyFrom(defEventGroup.definePosition("metric", "cov"))

    # ORIENTATION
    localOrientation.CopyFrom(defEventGroup.defineRotation("euler", "cov"))

    # SATELLITE SYSTEM
    localNavigationSatelliteSystem = localization_pb2.VehiclePositionAndOrientation.NavigationSatelliteSystem()

    # SATELLITE SYSTEM -- Satellites by System
    localSatellitesBySystem = localization_pb2.VehiclePositionAndOrientation.NavigationSatelliteSystem.SatellitesBySystem()
    localSatellitesBySystem.system = source_pb2.Sensor.NavigationSatelliteSystem.GPS # IMPROVE HERE
    localSatellitesBySystem.total.value = 2 # IMPROVE HERE
    localNavigationSatelliteSystem.satellites_by_system.extend([localSatellitesBySystem])   

    # SATELLITE SYSTEM - fix_type - hvpt dop
    localNavigationSatelliteSystem.fix_type = localization_pb2.VehiclePositionAndOrientation.NavigationSatelliteSystem.TWO_D_SATELLITE_BASED_AUGMENTATION
    localNavigationSatelliteSystem.hdop.value = 123
    localNavigationSatelliteSystem.vdop.value = 456
    localNavigationSatelliteSystem.pdop.value = 789
    localNavigationSatelliteSystem.tdop.value = 369

    localVehiclePositionAndOrientation.envelope.CopyFrom(localEnvelope)
    localVehiclePositionAndOrientation.position.CopyFrom(localPosition)
    localVehiclePositionAndOrientation.orientation.CopyFrom(localOrientation)
    localVehiclePositionAndOrientation.navigation_satellite_system.CopyFrom(localNavigationSatelliteSystem)

    return localVehiclePositionAndOrientation

def defineVehicleOdometry():
    localVehicleOdometry = localization_pb2.VehicleOdometry()

    localVehicleOdometry_Envelope = base_pb2.EventEnvelope()
    localVehicleOdometry_Translation = spatial_pb2.Position()
    localVehicleOdometry_Rotation = spatial_pb2.Rotation()

    localVehicleOdometry_Envelope.id.value = 123
    localVehicleOdometry_Envelope.timestamp.CopyFrom(defEventGroup.defineTimestamp())

    localVehicleOdometry_Translation.CopyFrom(defEventGroup.definePosition("metric", "cov"))

    localVehicleOdometry_Rotation.CopyFrom(defEventGroup.defineRotation("euler", "cov"))

    localVehicleOdometry.envelope.CopyFrom(localVehicleOdometry_Envelope)
    localVehicleOdometry.translation.CopyFrom(localVehicleOdometry_Translation)
    localVehicleOdometry.rotation.CopyFrom(localVehicleOdometry_Rotation)

    return localVehicleOdometry

def defineVehicleDynamics():
    localVehicleDynamics = localization_pb2.VehicleDynamics()
    
    # taking care on the envelope
    localVehicleDynamics_Envelope = base_pb2.EventEnvelope()
    localVehicleDynamics_Envelope.id.value = 123
    localVehicleDynamics_Envelope.timestamp.CopyFrom(defEventGroup.defineTimestamp())

    localVehicleDynamics.envelope.CopyFrom(localVehicleDynamics_Envelope)
    localVehicleDynamics.speed.CopyFrom(defineVehicleSpeed("xyz"))
    localVehicleDynamics.acceleration.CopyFrom(defineVehicleAcceleration("xyz"))
    localVehicleDynamics.rotation_rate.CopyFrom(defineVehicleRotationRate("cov"))

    return localVehicleDynamics

def defineVehicleSpeed(strAccuracy):
    localSpeed = spatial_pb2.Speed()

    localSpeed.x_m_p_s.value = 16666 # representing 16.666 m/s with scale factor = 3
    localSpeed.y_m_p_s.value = 20
    localSpeed.z_m_p_s.value = 30

    if strAccuracy == "cxyz":
        localSpeed.combined_x_y_z_accuracy.x_y_z_m_p_s.value = 2
        pass
    
    if strAccuracy == "xyz":
        localSpeed.x_y_z_accuracy.x_m_p_s.value = 2
        localSpeed.x_y_z_accuracy.y_m_p_s.value = 2
        localSpeed.x_y_z_accuracy.z_m_p_s.value = 2

    if strAccuracy == "cov":
        localSpeed.covariance_matrix.a11.value = 1
        localSpeed.covariance_matrix.a12.value = 1
        localSpeed.covariance_matrix.a13.value = 1
        localSpeed.covariance_matrix.a21.value = 1
        localSpeed.covariance_matrix.a22.value = 1
        localSpeed.covariance_matrix.a23.value = 1
        localSpeed.covariance_matrix.a31.value = 1
        localSpeed.covariance_matrix.a32.value = 1
        localSpeed.covariance_matrix.a33.value = 1

    return localSpeed

def defineVehicleAcceleration(strAccuracy):
    localAcceleration = spatial_pb2.Acceleration()

    localAcceleration.x_m_p_s2.value = 10
    localAcceleration.y_m_p_s2.value = 20
    localAcceleration.z_m_p_s2.value = 30

    if strAccuracy == "cxyz":
        localAcceleration.combined_x_y_z_accuracy.x_y_z_m_p_s2.value = 2
        pass
    
    if strAccuracy == "xyz":
        localAcceleration.x_y_z_accuracy.x_m_p_s2.value = 2
        localAcceleration.x_y_z_accuracy.y_m_p_s2.value = 2
        localAcceleration.x_y_z_accuracy.z_m_p_s2.value = 2

    if strAccuracy == "cov":
        localAcceleration.covariance_m2_p_s4.a11.value = 1
        localAcceleration.covariance_m2_p_s4.a12.value = 1
        localAcceleration.covariance_m2_p_s4.a13.value = 1
        localAcceleration.covariance_m2_p_s4.a21.value = 1
        localAcceleration.covariance_m2_p_s4.a22.value = 1
        localAcceleration.covariance_m2_p_s4.a23.value = 1
        localAcceleration.covariance_m2_p_s4.a31.value = 1
        localAcceleration.covariance_m2_p_s4.a32.value = 1
        localAcceleration.covariance_m2_p_s4.a33.value = 1

    return localAcceleration

def defineVehicleRotationRate(strAccuracy):
    localVehicleDynamics_RotationRate = spatial_pb2.RotationRate()

    localVehicleDynamics_RotationRate.yaw_deg_p_s.value = 20
    localVehicleDynamics_RotationRate.pitch_deg_p_s.value = 40
    localVehicleDynamics_RotationRate.roll_deg_p_s.value = 60

    if strAccuracy == "cypr":
        localVehicleDynamics_RotationRate.combined_yaw_pitch_roll_accuracy.yaw_pitch_roll_deg_p_s.value = 70
        pass

    if strAccuracy == "ypr":
        localVehicleDynamics_RotationRate.yaw_deg_p_s.value = 80
        localVehicleDynamics_RotationRate.pitch_deg_p_s.value = 90
        localVehicleDynamics_RotationRate.roll_deg_p_s.value = 100
        pass
    
    if strAccuracy == "cov":
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a11.value = 5
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a12.value = 10
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a13.value = 15
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a21.value = 20
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a22.value = 25
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a23.value = 30
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a31.value = 35
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a32.value = 40
        localVehicleDynamics_RotationRate.covariance_matrix.covariance_deg2_p_s2.a33.value = 45
        pass

    return localVehicleDynamics_RotationRate
