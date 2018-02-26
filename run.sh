#!/bin/bash
clear
echo Starting Compilation of the local sample files for protobuf.

echo
echo Used Protobuf Version:
protoc --version
echo
echo ------------------------------------------------------------
echo Compiling SENSORIS protobuf for PYTHON...
cd ..
cd specification

echo Compile "data.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/messages/data.proto
echo Done.

echo Compile "base.proto"
protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/types/base.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,base.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./base.proto
echo Done.

echo Compile "source.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/types/source.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,source.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./source.proto
echo Done.

echo Compile "spatial.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/types/spatial.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,spatial.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./spatial.proto
echo Done.

echo Compile "brake.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/brake.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,brake.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./brake.proto
echo Done.

echo Compile "driving_behavior.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/driving_behavior.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,driving_behavior.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./driving_behavior.proto
echo Done.

echo Compile "intersection_attribution.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/intersection_attribution.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,intersection_attribution.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./intersection_attribution.proto
echo Done.

echo Compile "localization.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/localization.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,localization.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./localization.proto
echo Done.

echo Compile "map.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/map.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,map.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./map.proto
echo Done.

echo Compile "object_detection.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/object_detection.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,map.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./map.proto
echo Done.

echo Compile "powertrain.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/powertrain.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,object_detection.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./object_detection.proto
echo Done.

echo Compile "road_attribution.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/road_attribution.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,road_attribution.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./road_attribution.proto
echo Done.

echo Compile "traffic_events.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/traffic_events.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,traffic_events.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./traffic_events.proto
echo Done.

echo Compile "traffic_maneuver.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/traffic_maneuver.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,traffic_maneuver.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./traffic_maneuver.proto
echo Done.

echo Compile "traffic_regulation.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/traffic_regulation.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,traffic_regulation.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./traffic_regulation.proto
echo Done.

echo Compile "weather.proto"
#protoc -I=./src/ --python_out=../SensorDataHandling/SensorisProtobuf_out/ ./src/sensoris/protobuf/categories/weather.proto
#protoc --doc_out=../../../../doc/ --doc_opt=html,weather.html -I=. --python_out=../../../../../SensorDataHandling/SensorisProtobuf_out/ ./weather.proto
echo Done.

echo Successfully compiled all SENSORIS protobuf files for PYTHON
echo ------------------------------------------------------------
