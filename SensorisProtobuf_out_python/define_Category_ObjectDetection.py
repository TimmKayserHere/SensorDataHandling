import sys
import uuid
import time
import math
import numpy as np
import nvector as nv
import random

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

    numOfPLOs = config.getConfig_Int("run_config", "numOfPLOs_perHEREMaplet")
    numOfConesAndBarrels = config.getConfig_Int("run_config", "numOfConesBarrels_perHEREMaplet")

    iterator = int(0)
    while iterator < numOfPLOs:
        localObjectDetection.static_object_detection.extend([definePoleLikeObjects()])
        iterator += 1

    iterator = int(0)
    while iterator < numOfConesAndBarrels:
        localObjectDetection.static_object_detection.extend([defineConesAndBarrels()])
        iterator += 1

    return localObjectDetection

def definePoleLikeObjects():
    localPLO = object_detection_pb2.StaticObjectDetection()

    # Following the HERE Maplet spec, as PLO should come with the following attributes
    # (1) id and timestamp --> provided via the event envelope
    # (2) upper and lower point, covariance and diameter information --> provided via pole_like_object 
    # (3) color, reflectivity --> provided via surface_material_type_and_confidence

    # (1)
    localEventEnvelope = base_pb2.EventEnvelope()
    localEventEnvelope.id.value = random.randrange(1,255)
    localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
    localPLO.envelope.CopyFrom(localEventEnvelope)

    # (2)
    localPLO.pole_like_object.upperPoint.metric.x.value = random.randrange(49700000,49800000)
    localPLO.pole_like_object.upperPoint.metric.y.value = random.randrange(49700000,49800000)
    localPLO.pole_like_object.upperPoint.metric.z.value = random.randrange(49700000,49800000)

    localPLO.pole_like_object.lowerPoint.metric.x.value = random.randrange(49700000,49800000)
    localPLO.pole_like_object.lowerPoint.metric.y.value = random.randrange(49700000,49800000)
    localPLO.pole_like_object.lowerPoint.metric.z.value = random.randrange(49700000,49800000)

    localPLO.pole_like_object.upperDiameter.value = random.randrange(10,2000)
    localPLO.pole_like_object.lowerDiameter.value = random.randrange(10,2000)
    localPLO.pole_like_object.diameterAccuracy.value = random.randrange(0,100)

    localPLO.pole_like_object.covariance.a11.value = 10
    localPLO.pole_like_object.covariance.a12.value = 10
    localPLO.pole_like_object.covariance.a13.value = 10
    localPLO.pole_like_object.covariance.a21.value = 10
    localPLO.pole_like_object.covariance.a22.value = 10
    localPLO.pole_like_object.covariance.a23.value = 10
    localPLO.pole_like_object.covariance.a31.value = 10
    localPLO.pole_like_object.covariance.a32.value = 10
    localPLO.pole_like_object.covariance.a33.value = 10

    # (3)
    localPLO.type_and_confidence.type = object_detection_pb2.StaticObjectDetection.TypeAndConfidence.POLE
    localPLO.surface_material_type_and_confidence.surface_material_type = object_detection_pb2.StaticObjectDetection.SurfaceMaterialTypeAndConfidence.METALLIC
    localPLO.surface_material_type_and_confidence.color = object_detection_pb2.StaticObjectDetection.SurfaceMaterialTypeAndConfidence.RED
    localPLO.surface_material_type_and_confidence.reflectivity.value = random.randrange(0,100)

    return localPLO

def defineConesAndBarrels():
    localConesAndBarrels = object_detection_pb2.StaticObjectDetection()

    # The HERE Maplet defines the following elements for cones/barrels
    # (1) id and timestamp --> provided via envelope
    # (2) anchor point --> provided via position
    # (3) covariance matrix --> provided via positition
    # (4) color and type --> provided via type and confidence

    # (1)
    localEventEnvelope = base_pb2.EventEnvelope()
    localEventEnvelope.id.value = random.randrange(1,255)
    localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
    localConesAndBarrels.envelope.CopyFrom(localEventEnvelope) 

    # (2)
    localConesAndBarrels.position.metric.x.value = random.randrange(49700000,49800000)
    localConesAndBarrels.position.metric.y.value = random.randrange(49700000,49800000)
    localConesAndBarrels.position.metric.z.value = random.randrange(49700000,49800000)

    # (3)
    localConesAndBarrels.position.covariance.a11.value = 1
    localConesAndBarrels.position.covariance.a12.value = 1
    localConesAndBarrels.position.covariance.a13.value = 1
    localConesAndBarrels.position.covariance.a21.value = 1
    localConesAndBarrels.position.covariance.a22.value = 1
    localConesAndBarrels.position.covariance.a23.value = 1
    localConesAndBarrels.position.covariance.a31.value = 1
    localConesAndBarrels.position.covariance.a32.value = 1
    localConesAndBarrels.position.covariance.a33.value = 1

    # (4)
    localConesAndBarrels.surface_material_type_and_confidence.color = object_detection_pb2.StaticObjectDetection.SurfaceMaterialTypeAndConfidence.RED
    localConesAndBarrels.type_and_confidence.type = object_detection_pb2.StaticObjectDetection.TypeAndConfidence.CONE

    return localConesAndBarrels

def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time.value = getMilliseconds
    return localTimestamp