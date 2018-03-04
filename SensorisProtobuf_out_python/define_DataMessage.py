import sys
import uuid
import time

# first of all, we import some basic compiled protobufs
from sensoris.protobuf.types import base_pb2
from sensoris.protobuf.types import source_pb2
from sensoris.protobuf.types import spatial_pb2
from sensoris.protobuf.messages import data_pb2
from sensoris.protobuf.categories import localization_pb2

import define_Envelope
import define_EventGroup
import define_EventRelation
import define_EventSource
import config

def DefineSENSORISDataMessage():

    # A SENSORIS DataMessage has some main fields, these are
    # #1 (envelope)
    # #2 (event group)
    # #3 (event relation)
    # #4 (event source)
    # these elements will be generated here
    # please check deeper going python files for deeper insights

    # generating the data message container itself
    localDataMessage = data_pb2.DataMessage()

    # putting the local data message together
    # see, that the envelope is a non-repeated value, whereas the others are repeated messages
    localDataMessage.envelope.CopyFrom(define_Envelope.defineSENSORISEnvelope())

    iterator = int(0)
    while iterator < config.getConfig_Int("run_config", "numOfHEREMaplets"):
        localDataMessage.event_group.extend([define_EventGroup.defineSENSORISEventGroup()])
        iterator += 1

    
    #localDataMessage.event_relation.extend([define_EventRelation.defineSENSORISEventRelation()])
    #localDataMessage.event_source.extend([define_EventSource.defineSENSORISEventSource()])

    return localDataMessage