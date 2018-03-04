import ConfigParser
import io
import os

def getConfig_Int(strSection, strVariable):

    # Load the configuration file
    with open("SensorDataHandling/SensorisProtobuf_out_python/config.ini") as f:
        sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    f.close()
    
    return int(config.get(strSection, strVariable))

def getConfig_Str(strSelection, strVariable):
    # Load the configuration file
    with open("SensorDataHandling/SensorisProtobuf_out_python/config.ini") as f:
        sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    f.close()
    
    return config.get(strSelection, strVariable)

def getConfig_Float(strSelection, strVariable):
    # Load the configuration file
    with open("SensorDataHandling/SensorisProtobuf_out_python/config.ini") as f:
        sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    f.close()
    
    return float(config.get(strSelection, strVariable))
