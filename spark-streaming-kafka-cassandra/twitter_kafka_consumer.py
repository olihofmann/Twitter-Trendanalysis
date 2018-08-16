import sys
import os
import glob

from pyspark import SparkContext, SparkFiles
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

sys.path.extend(glob.glob(os.path.join(os.path.expanduser("~"), "spark/jars/*.jar")))
from sparknlp.base import *
from sparknlp.annotator import *

schema = StructType([                                                                                          
    StructField("text", StringType(), True) 
])

def extract_noun(text):
    return "Ice"
    # is_noun = lambda pos: pos[:2] == "NN"
    # tokens = nltk.word_tokenize(text)
    # return [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)]

# Create the Spark Session and the Application
spark_session = SparkSession.builder.appName("TwitterTrendAnalyses").getOrCreate()

# Read the Kafka Stream
twitter_data_stream = spark_session.readStream.format("kafka").option("kafka.bootstrap.servers", "192.168.1.106:9092").option("subscribe", "Tweets").option("startingOffsets", "latest").load()
data_stream_transformed = twitter_data_stream.withWatermark("timestamp", "1 day")

# Extact the Json from the Kafka Stream
data_stream_string = data_stream_transformed.selectExpr("CAST(value AS STRING) as json")
tweets_table = data_stream_string.select(from_json(col("json"), schema).alias("tweet"))

# Get the tweet data
tweet_text_table = tweets_table.select("tweet.text")

# udf = USER DEFINED FUNCTION
text_to_pos = udf(extract_noun, StringType())

# Get the Text from the Tweet Table
noun_table = tweet_text_table.withColumn("nouns", text_to_pos("text"))
#noun_table = tweets_table.selectExpr(text_to_pos("tweet.text")).alias("pos_tags")

#new_dataFrame = tweet_text_table.withColumn("nlp_text", "tweet_text")
query = noun_table.writeStream.trigger(processingTime='10 seconds').format("console").start()
query.awaitTermination()
