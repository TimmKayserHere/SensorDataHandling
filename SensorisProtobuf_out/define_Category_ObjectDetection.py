import sys
import uuid
import time
import math
import numpy as np
import nvector as nv

import define_DataMessage as defDataMessage
import define_EventGroup as defEventGroup
import define_Envelope
import define_EventEnvelope

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

def defineObjectDetectionCategory():

    localObjectDetection = object_detection_pb2.ObjectDetectionCategory()

    # the object detecion category has 2 main messages

    # main message generation
    localMovingObject = object_detection_pb2.MovableObjectDetection()
    localStaticObject = object_detection_pb2.StaticObjectDetection()

    # a static object comes with the following attributes to be filled by this script: Lets see, what is happening, if 
    # 1 - envelope
    # 2 - type and confidence
    # 4 - position
    # 5 - rotation
    # 6 - size vector
    # 7 - surface type
    # 8 - surface material type
    
    localStaticObject.envelope.CopyFrom(define_EventEnvelope.defineEventEnvelope(config.getConfig_Int("HERE_MAPLET_CONE_BARREL", "construction_zone_marker_id_int")))

    if config.getConfig_Str("HERE_MAPLET_CONE_BARREL", "construction_zone_cone_type_enum") == "CONE":
        localStaticObject.type_and_confidence.type = object_detection_pb2.StaticObjectDetection.TypeAndConfidence.CONE
        pass

    # THIS IS NOT REQUESTED BY HERE MAPLET
    #localStaticObject.type_and_confidence.confidence_percent.value = 67

    localStaticObject.type_and_confidence.color = base_pb2.GCE_RED

    # generation of the necessary elements

    # handover of the necessary elements

    # main message hand over to the local Object detecion
    # please note, that the static and moveable objects are repeated elements
    # this means, you can add as many objects as you need.
    localObjectDetection.static_object_detection.extend([localStaticObject])
    localObjectDetection.movable_object_detection.extend([localMovingObject])

    return localObjectDetection