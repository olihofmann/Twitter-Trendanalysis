import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "main":
    spark_context = SparkContext(appName="TwitterTrendAnalyses")
    stream_context = StreamingContext(spark_context, 2)
    
    kafka_stream = KafkaUtils.createDirectStream(stream_context, ["Tweets"], {"metadata.broker.list": "192.168.1.106:9092"})
    lines = kafka_stream.map(lambda x: x[1])
