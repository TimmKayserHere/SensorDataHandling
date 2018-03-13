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
import define_Version

def defineSENSORISEnvelope():

    # the Envelope consists for three elements
    # #1 (identifiers)
    # #2 (vehicle dimensions)
    # #3 (field resolution override) // not needed for HERE Maplet
    # #4 (map identification)

    # generating a local container for the content
    localEnvelope = data_pb2.DataMessage.Envelope()


    localIdentifyer = base_pb2.MessageEnvelopeIds()
    localIdentifyer.session_id.value = str(uuid.uuid4())
    localIdentifyer.message_id.value = config.getConfig_Int("general_message_config", "message_id")
    localIdentifyer.vehicle_fleet_id.value = str(uuid.uuid4())
    localIdentifyer.vehicle_id.value = str(uuid.uuid4())
    localIdentifyer.driver_id.value = str(uuid.uuid4())
    
    localIdentifyer.job_request_id.append(str(uuid.uuid4()))
    localIdentifyer.job_submitter_id.value = str(uuid.uuid4())

    localEnvelope.ids.CopyFrom(localIdentifyer)

    localVehicleDimensions = data_pb2.DataMessage.Envelope.VehicleDimensions()
    localVehicleDimensions.length_to_front.value = config.getConfig_Int("vehicle_dimensions", "vehicle_dimension_x_forward")
    localVehicleDimensions.length_to_back.value = config.getConfig_Int("vehicle_dimensions", "vehicle_dimension_x_backward")
    localVehicleDimensions.length_to_left.value = config.getConfig_Int("vehicle_dimensions", "vehicle_dimension_y_left")
    localVehicleDimensions.length_to_right.value = config.getConfig_Int("vehicle_dimensions", "vehicle_dimension_y_right")
    localVehicleDimensions.length_to_top.value = config.getConfig_Int("vehicle_dimensions", "vehicle_dimension_z_up")
    localVehicleDimensions.length_to_ground.value = config.getConfig_Int("vehicle_dimensions", "vehicle_dimension_z_down")
    localEnvelope.vehicle_dimensions.CopyFrom(localVehicleDimensions)

    # this implementation is highly inefficient. I cannot recoomend to use it
    # you can simply avoid this, if you take the resolutions defined in the comments above your attributes
    #localFieldResolutionOverride = data_pb2.DataMessage.Envelope.FieldResolutionOverride()
    #localFieldResolutionOverride.path.value = "nice/path/to/attribute/with/different/scale/factor/than/defined/in/comment"
    #localFieldResolutionOverride.factor.value = 3 #translates into mulitplicator by 10-times-3 = 1,000
    #localEnvelope.field_resolution_override.extend([localFieldResolutionOverride])

    # provinding some information on used map
    localMapIdentification = data_pb2.DataMessage.Envelope.MapIdentification()
    localMapIdentification.map_source_identification.map_source_name.value = config.getConfig_Str("map_identification", "map_source_name")
    localMapIdentification.map_source_identification.map_source_version.CopyFrom(define_Version.DefineMapVersion())
    localMapIdentification.map_compiler_identification.map_compiler_name.value = config.getConfig_Str("map_identification", "map_compiler_name")
    localMapIdentification.map_compiler_identification.map_compiler_version.CopyFrom(define_Version.DefineCompilerVersion())
    localMapIdentification.map_format = data_pb2.DataMessage.Envelope.MapIdentification.NDS
    localEnvelope.map_identification.CopyFrom(localMapIdentification)
    
    return localEnvelope