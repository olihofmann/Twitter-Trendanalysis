import os
from kafka import KafkaProducer, KafkaClient, SimpleProducer
from time import sleep

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Define the Keyword List
KEYWORDS = "burtonsnowboard"  

# Variables for the Twitter API
ACCESS_TOKEN = "2343354570-t4LW7hmh0ek8TrKRpWYFEarTYvBjmGI3KxR2T2t"
ACCESS_TOKEN_SECRET = "pS1WuTyWBladQI8c7m5Pv6fEl4rWJkUhxLJirrHvHJz3b"
CONSUMER_KEY = "MlRJiTxncDFzVqRz8v8bup2tZ"
CONSUMER_SECRET = "5lxi2JNpg5s28OfZidTUS6LL1HRPVaTDUyQOAP5N970xzZFOFB"

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=["192.168.1.106:9092"])

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print("message sent to Kafka")
        producer.send("Tweets", data.encode('utf-8'))
        return True

    def on_error(self, status):
        print(status)


class Producer(object):

    def run(self, filters):
        #This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener()
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, l)
        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=filters)

def main():
    twitter_producer = Producer()
    twitter_producer.run(KEYWORDS)

if __name__ == "__main__":
    main()


