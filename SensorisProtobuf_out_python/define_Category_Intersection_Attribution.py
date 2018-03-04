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

def defineIntersectionAttribution():

  localTrafficSignal = intersection_attribution_pb2.IntersectionAttributionCategory()

  # here we define the mandatory event envelope for the localization
  # There is a little bug in the Sensoris spec, as no content is defined in the category envelope
  # but we define it, to comply
  TrafficSignalCategoryEnvelope = base_pb2.CategoryEnvelope()
  localTrafficSignal.envelope.CopyFrom(TrafficSignalCategoryEnvelope)

  NumOfTrafficSignalsInSensorisMessage = config.getConfig_Int("run_config", "numOfTrafficSignals_perHEREMaplet")
  
  iterator = int(0)
  while iterator < NumOfTrafficSignalsInSensorisMessage:
      localTrafficSignal.traffic_light_status.extend([defineTrafficSignal()])
      iterator += 1

  return localTrafficSignal

def defineTrafficSignal():

  localTrafficSignal = intersection_attribution_pb2.TrafficLightStatus()

  # HERE Maplet spec wants to get the following:
  # (1) ID and timestamp --> via envelope
  # (2) Bounding box --> ???
  # (3) covariance --> ??
  # (4) active color and orientation of the light --> ???
  # (5) tier count --> ???

  # (1)
  localEventEnvelope = base_pb2.EventEnvelope()
  localEventEnvelope.id.value = random.randrange(1,255)
  localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
  localTrafficSignal.envelope.CopyFrom(localEventEnvelope)

  # (2)
  # spatial position
  localTrafficSignal.position.metric.x.value = random.randrange(49700000,49800000)
  localTrafficSignal.position.metric.y.value = random.randrange(49700000,49800000)
  localTrafficSignal.position.metric.z.value = random.randrange(49700000,49800000)

  # covariance
  localTrafficSignal.position.covariance.a11.value = 3
  localTrafficSignal.position.covariance.a12.value = 3
  localTrafficSignal.position.covariance.a13.value = 3
  localTrafficSignal.position.covariance.a21.value = 3
  localTrafficSignal.position.covariance.a22.value = 3
  localTrafficSignal.position.covariance.a23.value = 3
  localTrafficSignal.position.covariance.a31.value = 3
  localTrafficSignal.position.covariance.a32.value = 3
  localTrafficSignal.position.covariance.a33.value = 3

  # 3D bounding box, relative to absolute position
  localTrafficSignal.bounding_box.lowerLeftPoint.x.value = -10
  localTrafficSignal.bounding_box.lowerLeftPoint.y.value = -10
  localTrafficSignal.bounding_box.lowerLeftPoint.z.value = -10
  localTrafficSignal.bounding_box.upperRightPoint.x.value = 20
  localTrafficSignal.bounding_box.upperRightPoint.y.value = 20
  localTrafficSignal.bounding_box.upperRightPoint.z.value = 20

  # indicating, that the traffic signal is working, currently GREEN, circular shaped in a vertical setup
  localTrafficSignal.status_and_confidence.status = intersection_attribution_pb2.TrafficLightStatus.StatusAndConfidence.ON
  localTrafficSignal.colour_and_confidence.colour = intersection_attribution_pb2.TrafficLightStatus.ColourAndConfidence.GREEN
  localTrafficSignal.shape_and_confidence.shape = intersection_attribution_pb2.TrafficLightStatus.ShapeAndConfidence.CIRCLE
  localTrafficSignal.shape_and_confidence.orientation = intersection_attribution_pb2.TrafficLightStatus.ShapeAndConfidence.VERTICAL

  # (5)
  localTrafficSignal.tier_count.traffic_signal_horizontal_count.value = 10
  localTrafficSignal.tier_count.traffic_signal_vertical_count.value = 3
  localTrafficSignal.tier_count.traffic_signal_horizontal_light_count.value = 5
  localTrafficSignal.tier_count.traffic_signal_vertical_light_count.value = 2

  return localTrafficSignal


def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time.value = getMilliseconds
    return localTimestamp