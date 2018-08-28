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
    StructField("text", StringType(), True)
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

def getSqlContextInstance(sparkContext):
    if ("sqlContextSingletonInstance" not in globals()):
        globals()["sqlContextSingletonInstance"] = SQLContext(sparkContext)
    return globals()["sqlContextSingletonInstance"]

def extract_noun(text):
    is_noun = lambda pos: pos[:2] == "NN" 
    tokens = nltk.word_tokenize(text) 
    return [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)] 

def processTweets(time, rdd):
    print("========= %s =========" % str(time))
    try:
        sql_context = getSqlContextInstance(rdd.context)

        # Parse the Tweet Json
        tweet_dataframe = sql_context.read.schema(schema).json(rdd)

        # Extract the relevant properties
        extract_dataframe = tweet_dataframe.select("text")

        # Define the user defined function
        text_to_pos = udf(extract_noun, ArrayType(StringType()))

        # Extract the nouns from the text
        text_noun_dataframe = extract_dataframe.withColumn("nouns", text_to_pos("text"))

        # Preparing the persist dataset
        persist_dataframe = text_noun_dataframe.select(explode("nouns"))
        persist_dataframe.show()

        # rdd = rdd.context.parallelize([{
	    #     "key": t[0],
	    #     "timestamp": datetime.datetime.now().date(),
	    #     "count": 1,
	    #     "retweets": 10,
	    #     "likes": 0
        # } for t in persist_dataframe.collect()])

        # rdd.saveToCassandra(
	    #     "nouns",
	    #     "tweets")
    except:
        print("Error process tweet")
        pass

spark_context = SparkContext(appName="TwitterTrendAnalyses") 
stream_context = StreamingContext(spark_context, 10) 
 
kafka_stream = KafkaUtils.createDirectStream(stream_context, ["Tweets"], {"metadata.broker.list": "192.168.1.106:9092"}) 
kafka_stream.map(lambda rawTweet: rawTweet[1]).foreachRDD(processTweets)
# parsed_stream = kafka_stream.map(lambda rawTweet: json.loads(rawTweet[1]))
# parsed_stream.pprint()
#parsed_stream.foreachRDD(processTweets)

createKeySpace()
stream_context.start() 
stream_context.awaitTermination()
