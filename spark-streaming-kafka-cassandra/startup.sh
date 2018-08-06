#!/bin/bash

export SPARK_MASTER_URL=spark://${SPARK_MASTER_NAME}:${SPARK_MASTER_PORT}
export SPARK_HOME=/spark
export HADOOP_HOME=/hadoop
export PYSPARK_PYTHON=/usr/bin/python3
export SPARK_DRIVER_PYTHON=/usr/bin/python3

echo "Submit application ${SPARK_APPLICATION_PYTHON_LOCATION} to Spark master ${SPARK_MASTER_URL}"
echo "Passing arguments ${SPARK_APPLICATION_ARGS}"

spark/bin/spark-submit \
    --master ${SPARK_MASTER_URL} \
    --jars spark/jars/spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar \
    --num-executors 1 \
    --driver-memory 2g \
    --executor-memory 1g \
    --executor-cores 1 \
    --verbose \
    ${SPARK_APPLICATION_PYTHON_LOCATION} ${SPARK_APPLICATION_ARGS}  