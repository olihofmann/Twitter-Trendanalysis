import sys
import os
import glob
import json

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext 
from pyspark.streaming.kafka import KafkaUtils 

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

schema = StructType([                                                                                          
    StructField("text", StringType(), True)
])

def getSqlContextInstance(sparkContext):
    if ("sqlContextSingletonInstance" not in globals()):
        globals()["sqlContextSingletonInstance"] = SQLContext(sparkContext)
    return globals()["sqlContextSingletonInstance"]

def processTweets(time, rdd):
    print("========= %s =========" % str(time))
    try:
        sql_context = getSqlContextInstance(rdd.context)
        json_RDD = sql_context.read.schema(schema).json(rdd)
        json_RDD.show()
        #json_RDD.registerTempTable("tweets")
        print("process tweet")
    except:
        print("Error process tweet")
        pass

spark_context = SparkContext(appName="TwitterTrendAnalyses") 
stream_context = StreamingContext(spark_context, 2) 
 
kafka_stream = KafkaUtils.createDirectStream(stream_context, ["Tweets"], {"metadata.broker.list": "192.168.1.106:9092"}) 
kafka_stream.map(lambda rawTweet: rawTweet[1]).foreachRDD(processTweets)
# parsed_stream = kafka_stream.map(lambda rawTweet: json.loads(rawTweet[1]))
# parsed_stream.pprint()
#parsed_stream.foreachRDD(processTweets)
 
stream_context.start() 
stream_context.awaitTermination()


# # Load Spark NLP
# sys.path.extend(glob.glob(os.path.join(os.path.expanduser("~"), "spark/jars/*.jar")))
# from sparknlp.base import *
# from sparknlp.annotator import *
# #from sparknlp.pretrained.pipeline.en import BasicPipeline

# schema = StructType([                                                                                          
#     StructField("text", StringType(), True) 
# ])

# def extract_noun(text):
#     #BasicPipeline().annotate(text)
#     return text

# def saveToCassandra(tweet):
#     print(tweet.nouns)

# # Create the Spark Session and the Application
# spark_session = SparkSession.builder.appName("TwitterTrendAnalyses").getOrCreate()

# # Read the Kafka Stream
# twitter_data_stream = spark_session.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "192.168.1.106:9092") \
#     .option("subscribe", "Tweets") \
#     .option("startingOffsets", "latest") \
#     .load()

# data_stream_transformed = twitter_data_stream.withWatermark("timestamp", "1 day")

# # Extact the Json from the Kafka Stream
# data_stream_string = data_stream_transformed.selectExpr("CAST(value AS STRING) as json")
# tweets_table = data_stream_string.select(from_json(col("json"), schema).alias("tweet"))

# # Get the tweet data
# tweet_text_table = tweets_table.select("tweet.text")

# # udf = USER DEFINED FUNCTION
# text_to_pos = udf(extract_noun, StringType())

# # Get the Text from the Tweet Table
# noun_table = tweet_text_table.withColumn("nouns", text_to_pos("text"))
# #noun_table = tweets_table.selectExpr(text_to_pos("tweet.text")).alias("pos_tags")

# #new_dataFrame = tweet_text_table.withColumn("nlp_text", "tweet_text")

# query = noun_table.writeStream.trigger(processingTime='10 seconds').format("console").start()
# query.awaitTermination()
