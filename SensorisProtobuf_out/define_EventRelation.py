import sys
import uuid
import time

# first of all, we import some basic compiled protobufs
from sensoris.protobuf.types import base_pb2
from sensoris.protobuf.types import source_pb2
from sensoris.protobuf.types import spatial_pb2
from sensoris.protobuf.messages import data_pb2
from sensoris.protobuf.categories import localization_pb2




def defineSENSORISEventRelation():
    localEventRelation = data_pb2.DataMessage.EventRelation()

    # message basically has 3 components
    # #1 (from id)
    # #2 (type)
    # #3 (to id)

    # COMPILER ERROR FOR append()
    #localEventRelation.from_id.append(123)
    #localEventRelation.to_id.append(124)
    
    localEventRelation.type = data_pb2.DataMessage.EventRelation.GROUP

    return localEventRelation