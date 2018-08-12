import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import nltk

schema = StructType([                                                                                          
    StructField("text", StringType(), True) 
])

def extract_noun(text):
    is_noun = lambda pos: pos[:2] == "NN"
    tokens = nltk.word_tokenize(text)
    return [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)]

# Create the Spark Session and the Application
spark_session = SparkSession.builder.appName("TwitterTrendAnalyses").getOrCreate()

# Read the Kafka Stream
twitter_data_stream = spark_session.readStream.format("kafka").option("kafka.bootstrap.servers", "192.168.1.106:9092").option("subscribe", "Tweets").option("startingOffsets", "latest").load()
data_stream_transformed = twitter_data_stream.withWatermark("timestamp", "1 day")

# Extact the Json from the Kafka Stream
data_stream_string = data_stream_transformed.selectExpr("CAST(value AS STRING) as json")
tweets_table = data_stream_string.select(from_json(col("json"), schema).alias("tweet"))

# Get the Text from the Tweet Table
pos_tags_table = tweets_table.selectExpr(extract_verbs("tweet.text")).alias("pos_tags")

#new_dataFrame = tweet_text_table.withColumn("nlp_text", "tweet_text")
query = pos_tags_table.writeStream.trigger(processingTime='10 seconds').format("console").start()
query.awaitTermination()
