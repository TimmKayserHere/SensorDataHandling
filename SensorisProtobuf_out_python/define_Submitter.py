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


def DefineSENSORISSubmitter():
    # we locally define our own submitter message and append it to the SENSORIS message
    # the way we do that, is valid for repeated messages
    localsubmitter = base_pb2.Submitter()

    localsubmitter.name.value = config.getConfig_Str("submitter", "OEM_brand")
    localsubmitter.type.value = config.getConfig_Str("submitter", "OEM_vehicle_type")
    localsubmitter.software_version.value = config.getConfig_Str("submitter", "OEM_ecu_sw_version")
    localsubmitter.hardware_version.value = config.getConfig_Str("submitter", "OEM_ecu_hw_version")

    return localsubmitter