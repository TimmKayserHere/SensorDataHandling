import sys
import uuid
import time

# first of all, we import some basic compiled protobufs
from sensoris.protobuf.types import base_pb2
from sensoris.protobuf.types import source_pb2
from sensoris.protobuf.types import spatial_pb2
from sensoris.protobuf.messages import data_pb2
from sensoris.protobuf.categories import localization_pb2

def DefineSENSORISVersion(major, minor, patch):
    ############### 1 ###############
    # we locally define our own version message and append it to the SENSORIS message
    # the way, the version message is valid for non-repeated messages
    localVersion = base_pb2.Version()

    localVersion.major.value = major
    localVersion.minor.value = minor
    localVersion.patch.value = patch

    return localVersion