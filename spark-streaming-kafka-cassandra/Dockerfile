FROM bde2020/spark-submit:2.3.1-hadoop2.7

# Environment
ENV SPARK_VERSION 2.3.1
ENV HADOOP_VERSION 2.7
ENV SCALA_VERSION 2.11
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/twitter_kafka_consumer.py
ENV SPARK_APPLICATION_ARGS ""

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

#Install Anaconda
RUN curl -s https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh -o anaconda.sh && \
    chmod a+x anaconda.sh && \
    ./anaconda.sh -b -p $CONDA_DIR && \
    rm ./anaconda.sh && \
    $CONDA_DIR/bin/conda install -y -q jupyter notebook && \
    $CONDA_DIR/bin/conda clean -tipsy

#Environment vaiables for Spark to use Anaconda Python and Jupyter notebook
ENV PYSPARK_PYTHON $CONDA_DIR/bin/python3
ENV PYSPARK_DRIVER_PYTHON $CONDA_DIR/bin/python3

# Install NLTK
RUN conda install -c anaconda nltk
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader averaged_perceptron_tagger

# Spark Kafka Streaming 
RUN cd /tmp && \ 
    wget http://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_${SCALA_VERSION}/${SPARK_VERSION}/spark-streaming-kafka-0-8-assembly_${SCALA_VERSION}-${SPARK_VERSION}.jar && \ 
    mv spark-streaming-kafka-0-8-assembly_${SCALA_VERSION}-${SPARK_VERSION}.jar /spark/jars 

# Spark SQL
RUN cd /tmp && \
    wget http://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar && \
    mv spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar /spark/jars

# Kafka Client
RUN cd /tmp && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/0.10.0.0/kafka-clients-0.10.0.0.jar && \
    mv kafka-clients-0.10.0.0.jar /spark/jars

# PySpark Cassandra Connector
RUN cd /tmp && \
    wget http://dl.bintray.com/spark-packages/maven/anguenot/pyspark-cassandra/0.9.0/pyspark-cassandra-0.9.0.jar && \
    mv pyspark-cassandra-0.9.0.jar /spark/jars

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/
RUN cd /app \
    && pip3 install -U -r requirements.txt

# Copy the source code
COPY twitter_kafka_consumer.py /app

# Copy Startup Script
COPY startup.sh .
CMD ["/bin/bash", "/startup.sh"]