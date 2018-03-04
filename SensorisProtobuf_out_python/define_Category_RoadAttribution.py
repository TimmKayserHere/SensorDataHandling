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
from sensoris.protobuf.categories import traffic_regulation_pb2
from sensoris.protobuf.categories import road_attribution_pb2

def defineRoadAttribution():
  localRoadAttribution = road_attribution_pb2.RoadAttributionCategory()

  # We need to cover 2 HERE Maplet aspects here:
  # 1. Road Surface Markings
  # 2. Lane Marking Observations

  # for that reason, we only generate the category envelope and the two frames for the 2 topics here
  # and we dig deeper in separate functions.

  localCategoryEnvelope = base_pb2.CategoryEnvelope()
  localRoadAttribution.envelope.CopyFrom(localCategoryEnvelope)

  # now we add the lanes
  numOfLaneBoundaryDefinitionsPerHEREMaplet = config.getConfig_Int("run_config", "numOfLaneMarkingObservations_perHEREMaplet")

  iterator = int(0)
  while iterator < numOfLaneBoundaryDefinitionsPerHEREMaplet:
      localRoadAttribution.lane_boundary.extend([defineAnIndividualLaneBoundary()])
      iterator += 1

  # now we add the road surface markings
  numOfRoadSurfaceMarkings = config.getConfig_Int("run_config", "numOfSurfaceMarkings_perHEREMaplet")

  iterator = int(0)
  while iterator < numOfRoadSurfaceMarkings:
      localRoadAttribution.surface_marking.extend([defineAnIndividualSurfaceMarking()])
      iterator += 1

  return localRoadAttribution


def defineAnIndividualSurfaceMarking():
  localSurfaceMarking = road_attribution_pb2.SurfaceMarking()

  # DEFNINITION of (1) EVENT ENVELOPE and timestamp
  localEventEnvelope = base_pb2.EventEnvelope()
  localEventEnvelope.id.value = random.randrange(1,255)
  localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
  localSurfaceMarking.envelope.CopyFrom(localEventEnvelope)

  # Definition of (2) bounding box rectangle
  # The HERE Maplet spec has one attribute for the rectangle. 
  # The SENSORIS spec decomposes the definition in FIRST: define the position of the boundingbox in GNSS coordinates
  # SEDOND: define the dimensions (3D) relative to that point
  # the reference point of the bounding box is the middle of it. This is, what is referenced with the position.

  # FIRST: definition of the position
  localPosition = spatial_pb2.PositionAndAccuracy()
  localPosition.metric.x.value = random.randrange(49700000,49800000)
  localPosition.metric.y.value = random.randrange(49700000,49800000)
  localPosition.metric.z.value = random.randrange(-49800000,-49700000)
  localSurfaceMarking.position.CopyFrom(localPosition)

  # SECOND: definition of the bounding box
  # keep in mind, that the relative coordinates provided, are relative to the abolute point and are given in meters by scaling factor 0.01
  # that means, a 5x5m road surface comes with all elements at + or - 2500
  localVector = spatial_pb2.BoundingBoxAndAccuracy()
  localVector.lowerLeftPoint.x.value = -2500
  localVector.lowerLeftPoint.y.value = -2500
  localVector.lowerLeftPoint.z.value = -2500
  localVector.upperRightPoint.x.value = 2500
  localVector.upperRightPoint.y.value = 2500
  localVector.upperRightPoint.z.value = 2500

  # The HERE Maplet spec asks for a covariance matrix for the bounding box
  # this is done by providing covariance values for the lowerleft and upper right points
  localVector.lowerLeftPoint.covariance.a11.value = 1
  localVector.lowerLeftPoint.covariance.a12.value = 1
  localVector.lowerLeftPoint.covariance.a13.value = 1
  localVector.lowerLeftPoint.covariance.a21.value = 1
  localVector.lowerLeftPoint.covariance.a22.value = 1
  localVector.lowerLeftPoint.covariance.a23.value = 1
  localVector.lowerLeftPoint.covariance.a31.value = 1
  localVector.lowerLeftPoint.covariance.a32.value = 1
  localVector.lowerLeftPoint.covariance.a33.value = 1

  localVector.upperRightPoint.covariance.a11.value = 1
  localVector.upperRightPoint.covariance.a12.value = 1
  localVector.upperRightPoint.covariance.a13.value = 1
  localVector.upperRightPoint.covariance.a21.value = 1
  localVector.upperRightPoint.covariance.a22.value = 1
  localVector.upperRightPoint.covariance.a23.value = 1
  localVector.upperRightPoint.covariance.a31.value = 1
  localVector.upperRightPoint.covariance.a32.value = 1
  localVector.upperRightPoint.covariance.a33.value = 1

  localSurfaceMarking.marking_bounding_box_vector.CopyFrom(localVector)

  localTypeAndConfidence = road_attribution_pb2.SurfaceMarking.TypeAndConfidence()
  localTypeAndConfidence.color = road_attribution_pb2.SurfaceMarking.TypeAndConfidence.WHITE
  localTypeAndConfidence.type = road_attribution_pb2.SurfaceMarking.TypeAndConfidence.ARROW_LEFT
  
  localSurfaceMarking.type_and_confidence.CopyFrom(localTypeAndConfidence)

  return localSurfaceMarking

def defineAnIndividualLaneBoundary():
  localIndividualLaneBoundary = road_attribution_pb2.LaneBoundary()

  # The HERE Maplet spec wants to get the following items
  # (1) id and timestamp --> via envelope
  # (2) sample point --> via position
  # (3) marking width --> via width directly
  # (4) marking separation --> this is not explicitly modeled, as, e.g., a double lane is modelled in 2 different lane boundaries
  # (5) style, type and color --> via "type, material and color"

  # DEFNINITION of (1) EVENT ENVELOPE and timestamp
  localEventEnvelope = base_pb2.EventEnvelope()
  localEventEnvelope.id.value = random.randrange(1,255)
  localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
  localIndividualLaneBoundary.envelope.CopyFrom(localEventEnvelope)

  localIndividualLaneBoundary.position.metric.x.value = random.randrange(49700000,49800000)
  localIndividualLaneBoundary.position.metric.y.value = random.randrange(49700000,49800000)
  localIndividualLaneBoundary.position.metric.z.value = random.randrange(49700000,49800000)

  localIndividualLaneBoundary.width.value_and_accuracy.value = random.randrange(10,1000)
  localIndividualLaneBoundary.color_and_confidence.type = road_attribution_pb2.LaneBoundary.ColorAndConfidence.WHITE
  localIndividualLaneBoundary.type_and_confidence.type = road_attribution_pb2.LaneBoundary.TypeAndConfidence.SINGLE_SOLID



  return localIndividualLaneBoundary


# def defineLaneMarking():

#   localRoadAttribution = road_attribution_pb2.RoadAttributionCategory()

#   # putting lanes to our HERE Maplet is a little bit tricky, as the lanes are (definition-wise) part of the road attribution
#   # where also the road surface marking lie in.
#   # For that reason, we now generate a few more road attribution items, that just constain the lane marking information
#   # lane markings, as HERE undstands them, are related to "lane boundaries" in the SENSORIS specification
#   # for SENSORIS, a lane always consists of lane boundaries on each side. Thats the significant detail to know, in order to properly define the details.return

  # The HERE Maplet spec wants to get the following items
  # (1) id and timestamp --> via envelope
  # (2) sample point --> via position
  # (3) marking width --> via width directly
  # (4) marking separation --> this is not explicitly modeled, as, e.g., a double lane is modelled in 2 different lane boundaries
  # (5) style, type and color --> via "type, material and color"

#   # the category envelope does not make sense right now, but is at least defined
#   LaneMarkingCategoryEnvelope = base_pb2.CategoryEnvelope()
#   localRoadAttribution.envelope.CopyFrom(LaneMarkingCategoryEnvelope)

#   numOfLaneBoundaryDefinitionsPerHEREMaplet = config.getConfig_Int("run_config", "numOfLaneMarkingObservations_perHEREMaplet")

#   iterator = int(0)
#   while iterator < numOfLaneBoundaryDefinitionsPerHEREMaplet:
#       localRoadAttribution.lane_boundary.extend([defineAnIndividualLaneBoundary()])
#       iterator += 1


#   return localRoadAttribution

# def defineAnIndividualLaneBoundary():
#   localIndividualLaneBoundary = road_attribution_pb2.LaneBoundary()

#   # DEFNINITION of (1) EVENT ENVELOPE and timestamp
#   localEventEnvelope = base_pb2.EventEnvelope()
#   localEventEnvelope.id.value = random.randrange(1,255)
#   localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
#   localIndividualLaneBoundary.envelope.CopyFrom(localEventEnvelope)

#   return localIndividualLaneBoundary

# def defineRoadSurfaceMarkings():

#   localRoadAttribution = road_attribution_pb2.RoadAttributionCategory()

#   # the category envelope does not make sense right now, but is at least defined
#   localizationCategoryEnvelope = base_pb2.CategoryEnvelope()
#   localRoadAttribution.envelope.CopyFrom(localizationCategoryEnvelope)

#   localSurfaceMarking = road_attribution_pb2.SurfaceMarking()

#   # The HERE Maplet spec wants to collect the following items
#   # (1) ID and timestamp --> done via event envelope
#   # (2) Bounding box rectangle --> done via "marking_counding_box_vector" and "position"
#   # (3) Covariance martrix --> done via "type_and_confidence"
#   # (4) color --> done via "type_and_confidence"
#   # (5) class --> done via "type and confidence"



#   localSurfaceMarking.type_and_confidence.CopyFrom(localTypeAndConfidence)

#   numOfRoadSurfaceMarkings = config.getConfig_Int("run_config", "numOfSurfaceMarkings_perHEREMaplet")

#   iterator = int(0)
#   while iterator < numOfRoadSurfaceMarkings:
#       localRoadAttribution.surface_marking.extend([localSurfaceMarking])
#       iterator += 1

#   return localRoadAttribution


def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time.value = getMilliseconds
    return localTimestamp