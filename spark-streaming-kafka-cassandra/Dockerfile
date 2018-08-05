FROM bde2020/spark-submit:2.3.1-hadoop2.7

# Environment
ENV SPARK_VERSION 2.3.1
ENV HADOOP_VERSION 2.7
ENV SCALA_VERSION 2.11
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/twitter_kafka_consumer.py
ENV SPARK_APPLICATION_ARGS ""

# Spark Kafka Streaming
RUN cd /tmp && \
    wget http://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_${SCALA_VERSION}/${SPARK_VERSION}/spark-streaming-kafka-0-8-assembly_${SCALA_VERSION}-${SPARK_VERSION}.jar && \
    mv spark-streaming-kafka-0-8-assembly_${SCALA_VERSION}-${SPARK_VERSION}.jar /spark/jars

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/
RUN cd /app \
    && pip3 install -r requirements.txt

# Copy the source code
COPY twitter_kafka_consumer.py /app

# Copy Startup Script
COPY startup.sh .
CMD ["/bin/bash", "/startup.sh"]