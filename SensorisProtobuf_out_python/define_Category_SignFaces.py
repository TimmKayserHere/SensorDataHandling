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


def defineSignFacesCategory():

  localSignFaces = traffic_regulation_pb2.TrafficRegulationCategory()

  # The HERE Maplet spec says, that you want to collect the following items:
  # (1) Sign ID
  # (2) timestamp
  # (3) Center Point of detected traffic sign
  # (4) covariance matrix for the position reported
  # (5) orientation
  # (6) height, width and shape of the traffic sign

  # (1) will be defined via the event envelope
  # (2) will be defined via the event envelope
  # (3) will be given via the message "sign recognition" in position and accuracy
  # (4) will be given via the message "sign recognition" in position and accuracy
  # (5) will be given via the message "sign recognition" in the "rotation and accuracy"
  # (6) will be given via the message "size and accuracy" ... shape will be an enum in there as well

  # again, we generate these items several times (configurable) and set some meaningful random fake values

  # here we define the mandatory event envelope for the localization
  # There is a little bug in the Sensoris spec, as no content is defined in the category envelope
  # but we define it, to comply
  signfacesCategoryEnvelope = base_pb2.CategoryEnvelope()
  localSignFaces.envelope.CopyFrom(signfacesCategoryEnvelope)

  NumOfTrafficSignsInSensorisMessage = config.getConfig_Int("run_config", "numOfSignFaces_perHEREMaplet")
  
  iterator = int(0)
  while iterator < NumOfTrafficSignsInSensorisMessage:
      localSignFaces.sign_recognition.extend([defineTrafficSign()])
      iterator += 1

  return localSignFaces

def defineTrafficSign():

  localTrafficSign = traffic_regulation_pb2.SignRecognition()

  # (1) Event Envelope ... whereas the sign id is defined
  localEventEnvelope = base_pb2.EventEnvelope()
  localEventEnvelope.id.value = random.randrange(1,255)
  localEventEnvelope.timestamp.CopyFrom(defineTimestamp())
  localTrafficSign.envelope.CopyFrom(localEventEnvelope)

  localSignFacePosition = spatial_pb2.PositionAndAccuracy()

  localSignFacePosition.metric.x.value = random.randrange(49700000,49800000)
  localSignFacePosition.metric.y.value = random.randrange(49700000,49800000)
  localSignFacePosition.metric.z.value = random.randrange(-49800000,-49700000)

  # for HERE Maplets, we want to have some covariances defined
  localCovarianceSignFace = base_pb2.Int64Matrix3x3()
  localCovarianceSignFace.a11.value = 1
  localCovarianceSignFace.a12.value = 1
  localCovarianceSignFace.a13.value = 1
  localCovarianceSignFace.a21.value = 1
  localCovarianceSignFace.a22.value = 1
  localCovarianceSignFace.a23.value = 1
  localCovarianceSignFace.a31.value = 1
  localCovarianceSignFace.a32.value = 1
  localCovarianceSignFace.a33.value = 1

  localSignFacePosition.covariance.CopyFrom(localCovarianceSignFace)

  localTrafficSign.position_and_accuracy.CopyFrom(localSignFacePosition)

  # DEFNINITION of (3) 

  localOrientation = spatial_pb2.RotationAndAccuracy()

  # a roatation around the vehicle coordinate system usually turns in +180 degree or -180 degree in all directions
  # we want to cover this with regards to the requested accuracy for 0.01 digits
  # this means, we generate random values for -18000 to +18000 for all the angles
  localOrientation.euler.yaw.value = random.randrange(-18000,18000)
  localOrientation.euler.pitch.value = random.randrange(-18000,18000)
  localOrientation.euler.roll.value = random.randrange(-18000,18000)

  localTrafficSign.rotation_and_accuracy.CopyFrom(localOrientation)

  # now we define height, width and shape

  # if we assume square traffic sign with 70cm width and 90 cm height
  # and an accuracy to 0.01m, we get:
  localTrafficSign.size_and_confidence.width.value = 70
  localTrafficSign.size_and_confidence.height.value = 90
  localTrafficSign.shape_and_confidence.type = traffic_regulation_pb2.SignRecognition.ShapeAndConfidence.RECTANGLE
  

  return localTrafficSign

def defineTimestamp():
    localTimestamp = base_pb2.Timestamp()
    getMilliseconds = int(round(time.time() * 1000))
    localTimestamp.posix_time.value = getMilliseconds
    return localTimestamp