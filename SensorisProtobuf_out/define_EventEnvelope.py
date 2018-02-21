import sys
import uuid
import time

# first of all, we import some basic compiled protobufs
from sensoris.protobuf.types import base_pb2
from sensoris.protobuf.types import source_pb2
from sensoris.protobuf.types import spatial_pb2
from sensoris.protobuf.messages import data_pb2
from sensoris.protobuf.categories import localization_pb2

import config

def defineEventEnvelope(intID):
  localEventEnvelope = base_pb2.EventEnvelope()

  localTimestamp = base_pb2.Timestamp()
  getMilliseconds = int(round(time.time() * 1000))
  localTimestamp.posix_time_ms.value = getMilliseconds
  # TODO: The fraction is actually the nanoseconds
  #localTimestamp.posix_time_micro_s_fraction.value = 678 # QUESTION: HOW?

  localEventEnvelope.timestamp.CopyFrom(localTimestamp)
  localEventEnvelope.id.value = intID
  return localEventEnvelope