FROM bde2020/spark-submit:2.3.1-hadoop2.7

# Environment
ENV SPARK_VERSION 2.3.1
ENV HADOOP_VERSION 2.7
ENV SCALA_VERSION 2.11
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/twitter_kafka_consumer.py
ENV SPARK_APPLICATION_ARGS ""

# Spark SQL
RUN cd /tmp && \
    wget http://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar && \
    mv spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar /spark/jars

# Kafka Client
RUN cd /tmp && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/0.10.0.0/kafka-clients-0.10.0.0.jar && \
    mv kafka-clients-0.10.0.0.jar /spark/jars

# Spark NLP
COPY spark-nlp-assembly-1.6.1.jar /spark/jars/
RUN pip3 install --index-url https://test.pypi.org/simple/ spark-nlp==1.6.1

# Install Numpy
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y build-essential
RUN apt-get install -y python3-numpy

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/
RUN cd /app \
    && pip3 install -U -r requirements.txt

# Copy the source code
COPY twitter_kafka_consumer.py /app

# Copy Startup Script
COPY startup.sh .
CMD ["/bin/bash", "/startup.sh"]