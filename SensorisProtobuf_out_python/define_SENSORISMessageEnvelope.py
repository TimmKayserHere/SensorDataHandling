import sys
import uuid
import time

# first of all, we import some basic compiled protobufs
from sensoris.protobuf.types import base_pb2
from sensoris.protobuf.messages import data_pb2

import define_Version
import define_Submitter
import define_Version
import define_Submitter
import config


def DefineSENSORISMessageEnvelope():

    localSensorisMessageEnvelope = data_pb2.DataMessages.Envelope()

    # set the version
    localSensorisMessageEnvelope.version.CopyFrom(define_Version.DefineSENSORISVersion())

    # set the submitter
    localSensorisMessageEnvelope.submitter.extend([define_Submitter.DefineSENSORISSubmitter()])

    return localSensorisMessageEnvelope