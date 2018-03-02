#!/bin/bash
clear
echo Starting Compilation of the local sample files for protobuf.

echo
echo Used Protobuf Version:
protoc --version
echo
echo ---------------------------------------------------------------------------------
echo Compiling SENSORIS protobuf for PYTHON ...
cd ..
cd specification

echo Compile "data.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/messages/data.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/messages/data.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/messages/data.proto
echo Done.

echo Compile "base.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/types/base.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/types/base.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/types/base.proto
echo Done.

echo Compile "source.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/types/source.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/types/source.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/types/source.proto
echo Done.

echo Compile "spatial.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/types/spatial.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/types/spatial.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/types/spatial.proto
echo Done.

echo Compile "brake.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/brake.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/brake.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/brake.proto
echo Done.

echo Compile "driving_behavior.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/driving_behavior.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/driving_behavior.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/driving_behavior.proto
echo Done.

echo Compile "intersection_attribution.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/intersection_attribution.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/intersection_attribution.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/intersection_attribution.proto
echo Done.

echo Compile "localization.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/localization.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/localization.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/localization.proto
echo Done.

echo Compile "map.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/map.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/map.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/map.proto
echo Done.

echo Compile "object_detection.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/object_detection.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/object_detection.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/object_detection.proto
echo Done.

echo Compile "powertrain.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/powertrain.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/powertrain.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/powertrain.proto
echo Done.

echo Compile "road_attribution.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/road_attribution.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,road_attribution.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out_python/ ./road_attribution.proto
echo Done.

echo Compile "traffic_events.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/traffic_events.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/traffic_events.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/traffic_events.proto
echo Done.

echo Compile "traffic_maneuver.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/traffic_maneuver.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/traffic_maneuver.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/traffic_maneuver.proto
echo Done.

echo Compile "traffic_regulation.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/traffic_regulation.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/traffic_regulation.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/traffic_regulation.proto
echo Done.

echo Compile "weather.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out_python/ ./src/sensoris/protobuf/categories/weather.proto
protoc -I=./src/ --java_out=../SensorDataHandling/SensorisProtobuf_out_java/ ./src/sensoris/protobuf/categories/weather.proto
protoc -I=./src/ --cpp_out=../SensorDataHandling/SensorisProtobuf_out_cpp/ ./src/sensoris/protobuf/categories/weather.proto
echo Done.

cd src
echo Generating the SENSORIS documentation ...
protoc --plugin=../../SensorDataHandling/bin/ --doc_out=../doc/ --doc_opt=html,index.html sensoris/protobuf/messages/data.proto sensoris/protobuf/types/base.proto sensoris/protobuf/types/source.proto sensoris/protobuf/types/spatial.proto sensoris/protobuf/categories/brake.proto sensoris/protobuf/categories/driving_behavior.proto sensoris/protobuf/categories/intersection_attribution.proto sensoris/protobuf/categories/localization.proto sensoris/protobuf/categories/map.proto sensoris/protobuf/categories/object_detection.proto sensoris/protobuf/categories/powertrain.proto sensoris/protobuf/categories/traffic_events.proto sensoris/protobuf/categories/traffic_maneuver.proto sensoris/protobuf/categories/traffic_regulation.proto sensoris/protobuf/categories/weather.proto
echo Done.

echo Successfully compiled all SENSORIS protobuf files for PYTHON incl. documentation
echo ---------------------------------------------------------------------------------
