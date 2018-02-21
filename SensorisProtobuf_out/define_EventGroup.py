import sys
import uuid
import time
import math
import numpy as np
import nvector as nv

import define_Category_Localization as defCatLoc
import define_Category_ObjectDetection as defCatObj

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




def defineSENSORISEventGroup():

    # the event group consists of
    # #1 (origin)
    # #2 (localization category)
    # both is being defined here

    # generating the local container for the content
    localEventGroup = data_pb2.EventGroup()

    # putting it together
    localEventGroup.origin.CopyFrom(defineOrigin())

    #################################################
    # THIS IS THE MAIN ENTRY POINT FOR DETECTION DATA

    # we go external here to define the localization category to stay modular
    localEventGroup.localization_category.CopyFrom(defCatLoc.defineLocalizationCategory())

    localEventGroup.object_detection_category.CopyFrom(defCatObj.defineObjectDetectionCategory())

    #################################################

    return localEventGroup

def defineOrigin():
    # The Origin consists of 4 elements
    # #1.1 timestamp
    # #1.2 absolute spatial reference system
    # #1.3 position
    # #1.4 orientation
    # All these elements are filled here with life
    localOrigin = data_pb2.EventGroup.Origin()

    # hand over the information from sub-functions
    localOrigin.timestamp.CopyFrom(defineTimestamp())
    localOrigin.absolute_spatial_reference_system.CopyFrom(defineAbsoluteSpatialReferenceSystem())
    localOrigin.position.CopyFrom(definePosition("metric", "cov"))
    localOrigin.orientation.CopyFrom(defineRotation("euler", "cov"))
    return localOrigin

def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time_ms.value = getMilliseconds
    # TODO: The fraction is actually the nanoseconds
    localTimestamp.posix_time_micro_s_fraction.value = 678 # QUESTION: HOW?
    return localTimestamp

def defineAbsoluteSpatialReferenceSystem():
    localAbsoluteSpatialReferenceSystem = spatial_pb2.SpatialReferenceSystem.Absolute()

    # #1.2 (absolute spatial reference system)
    localAbsoluteSpatialReferenceSystem = spatial_pb2.SpatialReferenceSystem.Absolute()
    # be sure, the oneOf will make it possible to only define one or the other system. Its not possible to define multiple of them.spatial_pb2
    # Option 1 (going for WGS_84 or another standard)
    localEpsgCodeSystem = spatial_pb2.SpatialReferenceSystem.Absolute.EpsgCodeSystem()
    localEpsgCodeSystem.code_suffix.value = spatial_pb2.SpatialReferenceSystem.Absolute.EpsgCodeSystem.WGS_84
    localAbsoluteSpatialReferenceSystem.epsg_code_system.CopyFrom(localEpsgCodeSystem)

    # Option 2 (being fully free and simply define a text for the reference system of your joice)
    localWellKnownTextSystem = spatial_pb2.SpatialReferenceSystem.Absolute.WellKnownTextSystem()
    localWellKnownTextSystem.wkt.value = "Well Known Text Definition"
    # localAbsoluteSpatialReferenceSystem.wkt_definition.CopyFrom(localWellKnownTextSystem)

    return localAbsoluteSpatialReferenceSystem

# this helper function will convert a GNSS position, provided by long/lat/altitude given in degrees
# to an ECEF location in x, y, z for the WGS84 system
def translateLongLatAlt_to_XYZ(longitude, latitude, altitude):

    wgs84 = nv.FrameE(name='WGS84')
    pointB = wgs84.GeoPoint(longitude, latitude, altitude, degrees=True)
    p_EB_E = pointB.to_ecef_vector()
    myvector = p_EB_E.pvector.ravel() 

    return p_EB_E.pvector.ravel()

def definePosition(positiontype, accuracyType):
    localPosition = spatial_pb2.Position()

    # The position message consists mainly of 2 elements
    # #1 general type of position (geographic or metric)
    # #2 accuracy
    # both elements are being defined here
    # keep in mind, that this position is the reference point for relative meassurements of objects etc. later on

    # #1
    localGeograhicPosition = spatial_pb2.Position.Geographic()
    localMetricPosition = spatial_pb2.Position.Metric()

    # QUESTION: Wie loesen wir hier Kommawerte auf?
    # This is the HERE-Location in Berlin 52.531047, 13.385009 (103m elevation)
    # This is Los Angeles 34.0522  -118.40806 0 (elevation)
    # Lets assume, the GPS-position is exact to 5m radius
    # assuming scalefactor = 5
    localGeograhicPosition.longitude_deg.value = 52531047
    localGeograhicPosition.latitude_deg.value = 13385009
    localGeograhicPosition.altitude_m.value = 100

    metric_x = translateLongLatAlt_to_XYZ(52.531047, 13.385009, 103)

    # metric actually contains float values to be accurate
    # in order to translate this value to an int64, we need to provide a scale factor
    # this scale factor is locally defined here, but needs some general defintion at a centric place
    # TODO
    # the scale factor is 10^2 (=100) to translate meter values in cm values to fit HD requirements
    int64ScaleFactor = 2
    int64ScaleFactor = math.pow(10,int64ScaleFactor)

    localMetricPosition.x_m.value = int(metric_x[0]*int64ScaleFactor)
    localMetricPosition.y_m.value = int(metric_x[1]*int64ScaleFactor)
    localMetricPosition.z_m.value = int(metric_x[2]*int64ScaleFactor)

    if positiontype == "geometric":
        localPosition.geographic.CopyFrom(localGeograhicPosition)
        pass

    if positiontype == "metric":
        localPosition.metric.CopyFrom(localMetricPosition)
        pass

    # these are additions to be compliant to HERE Maplets
    localPosition.satellite_horizon_angle_limit.value = 10
    localPosition.satellite_signal_snr.value = 10
    localPosition.satellite_signal_rinex.value = "RINEX String"

    # the position message comes with multiple accuracies
    # these are all "one of", so, you will have to decide
    # accuracy options are
    # #1 (combined horizontal and vertical)
    # #2 (horizontal and vertical)
    # #3 (horizontal confidence ellipse and vertical accuracy)
    # #4 (covariance matrix)

    # #1
    localCombinedHorizontalAndVerticalAccuracy = spatial_pb2.Position.CombinedHorizontalVerticalAccuracy()
    localCombinedHorizontalAndVerticalAccuracy.horizontal_vertical_m.value = 500000 #representing 5m accuracy in both dimensions

    # #2
    localHorizontalAndVerticalAccuracy = spatial_pb2.Position.HorizontalVerticalAccuracy()
    localHorizontalAndVerticalAccuracy.horizontal_m.value = 500000 # representing 3m in horizontal direction QUESTION: WHAT IS HORIZONTAL?
    localHorizontalAndVerticalAccuracy.vertical_m.value = 500000

    # #3
    localHorizontalConfidenceEllipseVerticalAccuracy = spatial_pb2.Position.HorizontalConfidenceEllipseVerticalAccuracy()
    localHorizontalConfidenceEllipseVerticalAccuracy.horizontal_ellipse_major_m.value = 5
    localHorizontalConfidenceEllipseVerticalAccuracy.horizontal_ellipse_minor_m.value = 3
    localHorizontalConfidenceEllipseVerticalAccuracy.horizontal_ellipse_major_heading_deg.value = 10
    localHorizontalConfidenceEllipseVerticalAccuracy.vertical_m.value = 10
    
    # #4
    localCovarianceMatrix = spatial_pb2.Position.CovarianceMatrix()
    localCovarianceMatrix.covariance_m2.a11.value = 1 # a11 = 0.0012 ... asuming factor 5 ... 120
    localCovarianceMatrix.covariance_m2.a12.value = 2
    localCovarianceMatrix.covariance_m2.a13.value = 3
    localCovarianceMatrix.covariance_m2.a21.value = 4
    localCovarianceMatrix.covariance_m2.a22.value = 5
    localCovarianceMatrix.covariance_m2.a23.value = 6
    localCovarianceMatrix.covariance_m2.a31.value = 7
    localCovarianceMatrix.covariance_m2.a32.value = 8
    localCovarianceMatrix.covariance_m2.a33.value = 9
    # QUESTION: Covariances are usually lower than 1 ... where do I get the scale factor from?

    if accuracyType == "chava":
        localPosition.combined_horizontal_vertical_accuracy.CopyFrom(localCombinedHorizontalAndVerticalAccuracy)
        pass
    if accuracyType == "hav":
        localPosition.horizontal_vertical_accuracy.CopyFrom(localHorizontalAndVerticalAccuracy)
        pass
    if accuracyType == "hcev":
        localPosition.horizontal_confidence_ellipse_vertical_accuracy.CopyFrom(localHorizontalConfidenceEllipseVerticalAccuracy)
        pass

    if accuracyType == "cov":
        localPosition.covariance_matrix.CopyFrom(localCovarianceMatrix)
        pass

    return localPosition

def defineRotation(rotationsystem, accuracy):
    localRotation = spatial_pb2.Rotation()

    # The rotation matrix mainly consists of 2 elements
    # #1 Which Quaternion is used?
    # #2 Accuracy
    # both elements are of type "one of", so there is a clear decision to take here

    # #1
    localEuler = spatial_pb2.Rotation.Euler()
    localEuler.yaw_deg.value = 10
    localEuler.pitch_deg.value = 11
    localEuler.roll_deg.value = 12

    localQuaternion = spatial_pb2.Rotation.Quaternion()
    localQuaternion.x.value = 100
    localQuaternion.y.value = 110
    localQuaternion.z.value = 120

    if rotationsystem == "euler":
        localRotation.euler.CopyFrom(localEuler)
        pass

    if rotationsystem == "quaternion":
        localRotation.quaternion.CopyFrom(localQuaternion)
        pass

    #2
    # there are 6 versions to define the accuracy of rotations
    # #2.1 combined yaw/pitch/roll accuracy
    # #2.2 yaw/pitch/roll accuracy
    # #2.3 covariance matrice

    # #2.1
    localCombinedYawPitchRollAccuracy = spatial_pb2.Rotation.CombinedYawPitchRollAccuracy()
    localCombinedYawPitchRollAccuracy.yaw_pitch_roll_deg.value = 10

    # #2.2
    localYawPitchRollAccuracy = spatial_pb2.Rotation.YawPitchRollAccuracy()
    localYawPitchRollAccuracy.yaw_deg.value = 10
    localYawPitchRollAccuracy.pitch_deg.value = 11
    localYawPitchRollAccuracy.roll_deg.value = 12
    
    # #2.3
    localRollCovarianceMatrix = spatial_pb2.Rotation.CovarianceMatrix()
    localRollCovarianceMatrix.covariance_deg2.a11.value = 1
    localRollCovarianceMatrix.covariance_deg2.a12.value = 2
    localRollCovarianceMatrix.covariance_deg2.a13.value = 3
    localRollCovarianceMatrix.covariance_deg2.a21.value = 4
    localRollCovarianceMatrix.covariance_deg2.a22.value = 5
    localRollCovarianceMatrix.covariance_deg2.a23.value = 6
    localRollCovarianceMatrix.covariance_deg2.a31.value = 7
    localRollCovarianceMatrix.covariance_deg2.a32.value = 8
    localRollCovarianceMatrix.covariance_deg2.a33.value = 9

    if accuracy == "cypr":
        localRotation.combined_yaw_pitch_roll_accuracy.CopyFrom(localCombinedYawPitchRollAccuracy)
        pass
    if accuracy == "ypr":
        localRotation.yaw_pitch_roll_accuracy.CopyFrom(localYawPitchRollAccuracy)
        pass
    if accuracy == "cov":
        localRotation.covariance_matrix.CopyFrom(localRollCovarianceMatrix)
        pass

    return localRotation