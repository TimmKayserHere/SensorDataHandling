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

def DefineSENSORISVersion():
    ############### 1 ###############
    # we locally define our own version message and append it to the SENSORIS message
    # the way, the version message is valid for non-repeated messages
    localVersion = base_pb2.Version()

    localVersion.major.value = config.getConfig_Int("general", "major_version")
    localVersion.minor.value = config.getConfig_Int("general", "minor_version")
    localVersion.patch.value = config.getConfig_Int("general", "patch_version")
    localVersion.name.value = config.getConfig_Str("general", "version_name")

    return localVersion


def DefineMapVersion():

    localVersion = base_pb2.Version()

    localVersion.major.value = config.getConfig_Int("map_identification", "map_source_version_major")
    localVersion.minor.value = config.getConfig_Int("map_identification", "map_source_version_minor")
    localVersion.patch.value = config.getConfig_Int("map_identification", "map_source_version_patch")

    return localVersion

def DefineCompilerVersion():

    localVersion = base_pb2.Version()

    localVersion.major.value = config.getConfig_Int("map_identification", "map_compiler_version_major")
    localVersion.minor.value = config.getConfig_Int("map_identification", "map_compiler_version_minor")
    localVersion.patch.value = config.getConfig_Int("map_identification", "map_compiler_version_patch")

    return localVersion