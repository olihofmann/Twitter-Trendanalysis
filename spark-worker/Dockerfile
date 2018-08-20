FROM bde2020/spark-base:2.3.1-hadoop2.7

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

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

COPY worker.sh /

ENV SPARK_WORKER_WEBUI_PORT 8081
ENV SPARK_WORKER_LOG /spark/logs
ENV SPARK_MASTER "spark://spark-master:7077"

EXPOSE 8081

CMD ["/bin/bash", "/worker.sh"]