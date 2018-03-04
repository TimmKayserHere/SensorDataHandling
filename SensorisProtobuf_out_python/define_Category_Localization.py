import sys
import uuid
import time
import math
import numpy as np
import nvector as nv
import random

import define_DataMessage as defDataMessage
import define_EventGroup as defEventGroup
import config

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

    # the localization category consists of mainly 4 items
    # #1 (envelope)
    # #2 (vehicle position and orientation)
    # #3 (vehicle odometry)
    # #4 (vehicle dynamics)
    # 3 elements are defined as "repeated", that means, you can link multiple of them together   
    localLocalizationCategory = localization_pb2.LocalizationCategory()

    # here we define the mandatory event envelope for the localization
    # There is a little bug in the Sensoris spec, as no content is defined in the category envelope
    # but we define it, to comply
    localizationCategoryEnvelope = base_pb2.CategoryEnvelope()
    localLocalizationCategory.envelope.CopyFrom(localizationCategoryEnvelope)

    ##########################################
    # Here is the place to put in all the pose points we want to have in our HERE Maplet
    # for the example, we assume to collect 5 different pose points
    # these 5 pose points define the pose path
    # all information that are not directly given in the pose point definition are "overarching" and will be given in the
    # origin-evelop of the HERE Maplet (e.g. the drift of the vehicle throughout the whole maplet)

    # As I do not want to manually code 5 localisations, I will use some random generators for the attributes
    # But I will simply copy paste the next lines. Each line makes a pose point
    # each of these pose points will come with an event envelope that contains a time stamp
    # if you want to relate them to each other (or even the later generated fields, you can easily relate them by the timestamp)
    numOfPosePointsInMessage = config.getConfig_Int("run_config", "numOfPosePoints_perHEREMaplet")

    iterator = int(0)
    while iterator < numOfPosePointsInMessage:
        localLocalizationCategory.vehicle_position_and_orientation.extend([defineVehiclePositionAndOrientation()])
        iterator += 1

    return localLocalizationCategory

def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time.value = getMilliseconds
    return localTimestamp

def defineVehiclePositionAndOrientation():

    localVehiclePositionAndOrientation = localization_pb2.VehiclePositionAndOrientation()
    # In this section, we basically generate a HERE Maplet Pose Point
    # per definition, the pose point should contain the following information
    # (1) timestamp: given via the event envelope
    # (2) pose point itself: given in ecef coordinates
    # (3) orientation information: meaning yaw, pitch, roll without any accuracy information

    # Keep in mind, the standard definition of SENSORIS could attach even more. But we will not utilize the standard
    # to fit our needs.

    # DEFNINITION of (1) EVENT ENVELOPE
    localEventEnvelope = base_pb2.EventEnvelope()
    localEventEnvelope.id.value = random.randrange(1,255)
    localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
    localVehiclePositionAndOrientation.envelope.CopyFrom(localEventEnvelope)

    # DEFNINITION of (2) POSITION
    localPosition = spatial_pb2.PositionAndAccuracy()

    # "faking" ECEF values in a precise and meaningful way is a bit more tricky. Here is the approach:
    # First, we take the ECEF xyz-values for the HERE Berlin office to have a meaningful first step
    # x = 4973.941km, y = 2757.1km, z=-2878.261km
    # but ecef values should be provided in meters, but with an accuracy for 1 cm
    # for that reason, we convert the native km-values to cm precision
    # wherever I have not enough precision provided in the above Berlin example, i add some tailing "9"
    # x = 497394199 cm, y = 275710099 cm, z = -287826199 cm
    # now we check, in which range these values might change
    # x is in +/- 8000 m variance, basically, going from 4970km to + 4980km
    # y is in +/- 8000 m variance, basically, going from 4970km to + 4980km
    # y is in +/- 8000 m variance, basically, going from 4970km to + 4980km
    # so, we basically generate a random int generator, working as follow
 
    localPosition.metric.x.value = random.randrange(49700000,49800000)
    localPosition.metric.y.value = random.randrange(49700000,49800000)
    localPosition.metric.z.value = random.randrange(-49800000,-49700000)

    localVehiclePositionAndOrientation.position.CopyFrom(localPosition)

    # DEFNINITION of (3) 

    localOrientation = spatial_pb2.RotationAndAccuracy()

    # a roatation around the vehicle coordinate system usually turns in +180 degree or -180 degree in all directions
    # we want to cover this with regards to the requested accuracy for 0.01 digits
    # this means, we generate random values for -18000 to +18000 for all the angles
    localOrientation.euler.yaw.value = random.randrange(-18000,18000)
    localOrientation.euler.pitch.value = random.randrange(-18000,18000)
    localOrientation.euler.roll.value = random.randrange(-18000,18000)

    localVehiclePositionAndOrientation.orientation.CopyFrom(localOrientation)

    return localVehiclePositionAndOrientation

    