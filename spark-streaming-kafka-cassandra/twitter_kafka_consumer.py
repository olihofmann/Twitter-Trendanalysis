import sys
import json
import nltk
import datetime

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext 
from pyspark.streaming.kafka import KafkaUtils 

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "tweet_keyspace"
schema = StructType([                                                                                          
    StructField("text", StringType(), True),
    StructField("retweet_count", IntegerType(), True),
    StructField("favorite_count", IntegerType(), True)
])

def createKeySpace():
    print("Start creating keyspace")
    cluster = Cluster(["cassandra"])
    session = cluster.connect()

    try:
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)

        session.set_keyspace(KEYSPACE)

        session.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                noun text,
                timestamp date,
                count counter,
                retweets counter,
                likes counter,
                PRIMARY KEY (noun, timestamp)
            )
            """)
    except Exception as e:
        print(e)
        pass

def updateData(noun, date, count, retweets, likes):
    print("Start persist")
    cluster = Cluster(["cassandra"])
    session = cluster.connect()

    session.set_keyspace(KEYSPACE)
    
    prepared = session.prepare("""UPDATE tweets SET count=count + ?, retweets=retweets + ?, likes=likes + ?
    WHERE noun=? AND timestamp=?""")
    
    session.execute(prepared, [count, retweets, likes, noun, date])

def getSqlContextInstance(sparkContext):
    if ("sqlContextSingletonInstance" not in globals()):
        globals()["sqlContextSingletonInstance"] = SQLContext(sparkContext)
    return globals()["sqlContextSingletonInstance"]

def extract_noun(text):
    is_noun = lambda pos: pos[:2] == "NN" 

    tweet_tokenizer = nltk.tokenize.TweetTokenizer()
    tokens = tweet_tokenizer.tokenize(text)
    return [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)] 

def processTweets(time, rdd):
    print("========= %s =========" % str(time))
    try:
        sql_context = getSqlContextInstance(rdd.context)

        # Parse the Tweet Json
        tweet_dataframe = sql_context.read.schema(schema).json(rdd)

        # Extract the relevant properties
        extract_dataframe = tweet_dataframe.select("text", "retweet_count", "favorite_count")

        # Define the user defined function
        text_to_pos = udf(extract_noun, ArrayType(StringType()))

        # Extract the data from the text
        text_noun_dataframe = extract_dataframe.withColumn("nouns", text_to_pos("text"))

        # Preparing the persist dataset
        persist_dataframe = text_noun_dataframe.select(explode("nouns"), "retweet_count", "favorite_count")
        persist_dataframe.show()

        # Collect and persist to cassandra
        for p in persist_dataframe.collect():
            print("Persist noun: " + p[0] + " Date: " + datetime.datetime.now().date().isoformat())
            updateData(p[0], datetime.datetime.now().date().isoformat(), 1, p[1], p[2])

    except Exception as e:
        print("Error process tweet: " + e)
        pass

# Create Spark Context
spark_context = SparkContext(appName="TwitterTrendAnalyses") 
stream_context = StreamingContext(spark_context, 10) 
 
# Connect to Kafka
kafka_stream = KafkaUtils.createDirectStream(stream_context, ["Tweets"], {"metadata.broker.list": "192.168.1.106:9092"}) 
kafka_stream.map(lambda rawTweet: rawTweet[1]).foreachRDD(processTweets)

# Create Cassandra Keyspace
createKeySpace()

# Start Streaming
stream_context.start() 
stream_context.awaitTermination()
