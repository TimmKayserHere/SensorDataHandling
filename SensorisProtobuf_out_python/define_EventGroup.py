import sys
import uuid
import time
import math
import numpy as np
import nvector as nv

import define_Category_Localization as defCatLoc
import define_Category_ObjectDetection as defCatObj
import define_Category_SignFaces as defCatSigns
import define_Category_RoadAttribution as defCatRoadAttribution
import define_Category_Intersection_Attribution as defCatInterSecAttribution

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

import config


def defineSENSORISEventGroup():

    # the event group consists of
    # #1 (origin)
    # #2 (localization category)
    # #n (... all different categories)
    # both is being defined here

    # generating the local container for the content
    localEventGroup = data_pb2.EventGroup()

    # putting it together

    # here we transmit the relevant point for the whole HERE Maplet
    localEventGroup.envelope.origin.CopyFrom(defineOrigin())

    #################################################
    # THIS IS THE MAIN ENTRY POINT FOR DETECTION DATA

    # we go external here to define the localization category to stay modular
    # here we transmit the pose points inside the HERE Maplet
    # eaach pose point is identified via an id
    # with that id, you can later relate information to pose points
    # e.g. "at pose point id 123, i've collected traffic sign with id = 234"
    localEventGroup.localization_category.CopyFrom(defCatLoc.defineLocalizationCategory())

    # now we add some traffic signs to our HERE Maplet
    localEventGroup.traffic_regulation_category.CopyFrom(defCatSigns.defineSignFacesCategory())

    # now we add some road surface markings to our HERE Maplet
    # now we add some lane marking observations to our HERE Maplet
    # we need to process both, as definitions will otherwise be overwritten.
    localEventGroup.road_attribution_category.CopyFrom(defCatRoadAttribution.defineRoadAttribution())

    # now we add some pole-like objects (PLOs) and Cones and Barrels to our HERE Maplet
    localEventGroup.object_detection_category.CopyFrom(defCatObj.defineObjectDetectionCategory())

    # now we add some traffic signals to our HERE Maplet
    localEventGroup.intersection_attribution_category.CopyFrom(defCatInterSecAttribution.defineIntersectionAttribution())

    # now we add some lane marking observations to our HERE Maplet
    #localEventGroup.road_attribution_category.CopyFrom(defCatRoadAttribution.defineLaneMarking())



    #################################################

    return localEventGroup

def defineOrigin():
    # The Origin consists of 4 elements
    # #1.1 timestamp
    # #1.2 absolute spatial reference system
    # #1.3 position
    # #1.4 orientation
    # #1.5 drift
    # All these elements are filled here with life
    localOrigin = data_pb2.EventGroup.Envelope.Origin()

    # hand over the information from sub-functions
    localOrigin.timestamp.CopyFrom(defineTimestamp())
    localOrigin.absolute_spatial_reference_system.CopyFrom(defineAbsoluteSpatialReferenceSystem())
    localOrigin.position.CopyFrom(definePosition("metric", "COV"))
    localOrigin.orientation.CopyFrom(defineRotation("euler", "COV"))
    localOrigin.drift.CopyFrom(defineDrift("COV"))
    
    return localOrigin

def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time.value = getMilliseconds
    return localTimestamp

def defineAbsoluteSpatialReferenceSystem():

    # define a local copy of that
    localSpatialReferenceSystem = spatial_pb2.ReferenceSystem.Absolute()

    if config.getConfig_Str("HERE_MAPLET_ORIGIN", "used_satellite_coordinate_system") == "WGS84":
        localSpatialReferenceSystem.EpsgCodeSystem.WGS_84
        pass
    
    localSpatialReferenceSystem.mask_angle.value = config.getConfig_Int("HERE_MAPLET_ORIGIN", "mask_angle_deg")
    localSpatialReferenceSystem.snr.value = config.getConfig_Int("HERE_MAPLET_ORIGIN", "snr_dB")
    localSpatialReferenceSystem.rinex_string.value = config.getConfig_Str("HERE_MAPLET_ORIGIN", "rinex_string")

    return localSpatialReferenceSystem

# this helper function will convert a GNSS position, provided by long/lat/altitude given in degrees
# to an ECEF location in x, y, z for the WGS84 system
def translateLongLatAlt_to_XYZ(longitude, latitude, altitude):

    wgs84 = nv.FrameE(name='WGS84')
    pointB = wgs84.GeoPoint(longitude, latitude, altitude, degrees=True)
    p_EB_E = pointB.to_ecef_vector()
    myvector = p_EB_E.pvector.ravel() 

    return p_EB_E.pvector.ravel()

def definePosition(positiontype, accuracyType):
    localPosition = spatial_pb2.PositionAndAccuracy()

    # The position message consists mainly of 2 elements
    # #1 general type of position (geographic or metric)
    # #2 accuracy
    # both elements are being defined here
    # keep in mind, that this position is the reference point for relative meassurements of objects etc. later on

    # #1
    localGeograhicPosition = spatial_pb2.PositionAndAccuracy.Geographic()
    localMetricPosition = spatial_pb2.PositionAndAccuracy.Metric()

    # QUESTION: Wie loesen wir hier Kommawerte auf?
    # This is the HERE-Location in Berlin 52.531047, 13.385009 (103m elevation)
    # This is Los Angeles 34.0522  -118.40806 0 (elevation)
    # Lets assume, the GPS-position is exact to 5m radius
    # assuming scalefactor = 5
    localGeograhicPosition.longitude.value = 52531047
    localGeograhicPosition.latitude.value = 13385009
    localGeograhicPosition.altitude.value = 100

    metric = translateLongLatAlt_to_XYZ(52.531047, 13.385009, 103)

    # metric actually contains float values to be accurate
    # in order to translate this value to an int64, we need to provide a scale factor
    # this scale factor is locally defined here, but needs some general defintion at a centric place
    # TODO
    # the scale factor is 10^2 (=100) to translate meter values in cm values to fit HD requirements
    int64ScaleFactor = 2
    int64ScaleFactor = math.pow(10,int64ScaleFactor)

    localMetricPosition.x.value = int(metric[0]*int64ScaleFactor)
    localMetricPosition.y.value = int(metric[1]*int64ScaleFactor)
    localMetricPosition.z.value = int(metric[2]*int64ScaleFactor)

    if positiontype == "geometric":
        localPosition.geographic.CopyFrom(localGeograhicPosition)
        pass

    if positiontype == "metric":
        localPosition.metric.CopyFrom(localMetricPosition)
        pass



    # the position message comes with multiple accuracies
    # these are all "one of", so, you will have to decide
    # accuracy options are
    # (1) combined standard deviation
    # (2) standard deviation
    # (3) horizontal confidence elipsoid vertical standard deviation
    # (4) covariance matrix

    # #2
    localHorizontalVerticalStdDev = spatial_pb2.PositionAndAccuracy.HorizontalVerticalStdDev()
    localHorizontalVerticalStdDev.horizontal.value = 1000
    localHorizontalVerticalStdDev.vertical.value = 2000
    

    # #3
    localHorConfElipVertStdDev = spatial_pb2.PositionAndAccuracy.HorizontalConfidenceEllipseVerticalStdDev()
    localHorConfElipVertStdDev.horizontal_ellipse_major.value = 10
    localHorConfElipVertStdDev.horizontal_ellipse_minor.value = 10
    localHorConfElipVertStdDev.horizontal_ellipse_major_heading.value = 10
    localHorConfElipVertStdDev.vertical.value = 5

    
    # #4
    localCovarianceMatrix = base_pb2.Int64Matrix3x3()
    localCovarianceMatrix.a11.value = 1 # a11 = 0.0012 ... asuming factor 5 ... 120
    localCovarianceMatrix.a12.value = 2
    localCovarianceMatrix.a13.value = 3
    localCovarianceMatrix.a21.value = 4
    localCovarianceMatrix.a22.value = 5
    localCovarianceMatrix.a23.value = 6
    localCovarianceMatrix.a31.value = 7
    localCovarianceMatrix.a32.value = 8
    localCovarianceMatrix.a33.value = 9
    # QUESTION: Covariances are usually lower than 1 ... where do I get the scale factor from?

    if accuracyType == "combStdDev":
        localPosition.combined_std_dev.value = 5000
        pass
    if accuracyType == "StdDev":
        localPosition.std_dev.CopyFrom(localHorizontalVerticalStdDev)
        pass
    if accuracyType == "HorConvElipVertStdDev":
        localPosition.horizontal_confidence_ellipse_vertical_std_dev.CopyFrom(localHorConfElipVertStdDev)
        pass

    if accuracyType == "COV":
        localPosition.covariance.CopyFrom(localCovarianceMatrix)
        pass

    # HERE MAPLET position do not require a precision accuracy for the GNSS point
    # therefore we introduce this option here.
    if accuracyType == "":
        pass

    return localPosition

def defineRotation(rotationsystem, accuracy):
    localRotation = spatial_pb2.RotationAndAccuracy()

    # The rotation matrix mainly consists of 2 elements
    # #1 Which Quaternion is used?
    # #2 Accuracy
    # both elements are of type "one of", so there is a clear decision to take here

    # #1
    localEuler = spatial_pb2.RotationAndAccuracy.Euler()
    localEuler.yaw.value = 10
    localEuler.pitch.value = 11
    localEuler.roll.value = 12

    localQuaternion = spatial_pb2.RotationAndAccuracy.Quaternion()
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
    # #2.2 standard deviation for all different angles
    # #2.3 covariance matrice

    # #2.1
    #localCombinedYawPitchRollAccuracy = spatial_pb2.RotationAndAccuracy.CombinedYawPitchRollAccuracy()
    #localRotation.combined_std_dev.value = 10

    # #2.2
    localYawPitchRollAccuracy = spatial_pb2.RotationAndAccuracy.YawPitchRollStdDev()
    localYawPitchRollAccuracy.yaw.value = 10
    localYawPitchRollAccuracy.pitch.value = 11
    localYawPitchRollAccuracy.roll.value = 12
    
    # #2.3
    localRollCovarianceMatrix = base_pb2.Int64Matrix3x3()
    localRollCovarianceMatrix.a11.value = 1
    localRollCovarianceMatrix.a12.value = 2
    localRollCovarianceMatrix.a13.value = 3
    localRollCovarianceMatrix.a21.value = 4
    localRollCovarianceMatrix.a22.value = 5
    localRollCovarianceMatrix.a23.value = 6
    localRollCovarianceMatrix.a31.value = 7
    localRollCovarianceMatrix.a32.value = 8
    localRollCovarianceMatrix.a33.value = 9

    if accuracy == "cypr":
        localRotation.combined_std_dev.value = 10
        pass
    if accuracy == "ypr":
        localRotation.std_dev.CopyFrom(localYawPitchRollAccuracy)
        pass
    if accuracy == "COV":
        localRotation.covariance.CopyFrom(localRollCovarianceMatrix)
        pass
    
    if accuracy == "":
        pass

    return localRotation

def defineDrift(accuracy):

    localDriftVector = spatial_pb2.XyzVectorAndAccuracy()

    localDriftVector.x.value = 10
    localDriftVector.y.value = 20
    localDriftVector.z.value = 30

    # there are three versions to define the accuracy of the drift
    # 1. combined standard deviation in all dimensions
    # 2. standard deviation for each direction
    # 3. 3x3 covariance matrice

    if accuracy == "combined":
        localDriftVector.combined_std_dev.value = 10
        pass

    if accuracy == "stddev":
        localDriftVector.XyzAccuracy.x.value = 10
        localDriftVector.XyzAccuracy.y.value = 20
        localDriftVector.XyzAccuracy.z.value = 30
        pass

    if accuracy == "COV":
        localCovariance = base_pb2.Int64Matrix3x3()
        localCovariance.a11.value = 1
        localCovariance.a12.value = 2
        localCovariance.a13.value = 3
        localCovariance.a21.value = 4
        localCovariance.a22.value = 5
        localCovariance.a23.value = 6
        localCovariance.a31.value = 7
        localCovariance.a32.value = 8
        localCovariance.a33.value = 9
        localDriftVector.covariance.CopyFrom(localCovariance)
        pass

    if accuracy == "":
        pass

    return localDriftVector