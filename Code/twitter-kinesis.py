from TwitterAPI import TwitterAPI
import boto3, json
import twitterCreds
import threading, time
from threading import Thread
import sys, urllib3, http
from random import *
import os
from global_variables import *

MAX_BUFF_LEN = 15000
tweet_buffer = []
hashkey = (340282366920938463463374607431768211455/shard_count)*(int(sys.argv[2])) + 1
sleep_time = 0

class TwitterDataProducer (threading.Thread):
    def __init__(self, api, kinesis):
        threading.Thread.__init__(self)
        self.count = 0
        self.tweets = []
        self.api = api
        self.kinesis = kinesis

    def run(self):
        global tweet_buffer
        print("Producer started...")
        while (1):
            try:
                r = self.api.request('statuses/filter', {'locations':'-180,-90,180,90'})
                self.tweets = []
                self.count = 0
                for item in r:
                    jsonItem = json.dumps(item)
                    #self.tweets.append({'Data':jsonItem, 'PartitionKey':"filler"})
                    tweet_buffer.append({'Data':jsonItem, 'PartitionKey':str(sys.argv[2]), 'ExplicitHashKey':str(hashkey)})
                    self.count += 1
                    # place the data into a global buffer shared among producer and all consumers
                    if len(tweet_buffer) >= MAX_BUFF_LEN:
                        del tweet_buffer[0]
            except (urllib3.exceptions.ProtocolError, http.client.IncompleteRead) as e:
                print(e)
                continue


class TwitterDataConsumer (threading.Thread):
    def __init__(self, api, kinesis):
        threading.Thread.__init__(self)
        # self.tweet_record = []
        self.api = api
        self.kinesis = kinesis

    def run(self):
        global tweet_buffer
        tweet_record = []
        print("Consumer started...")
        i=0
        while (1):
            # check if the buffer has atleast one tweet to read
            if len(tweet_buffer) != 0 and len(tweet_buffer) > i:
                # tweet_record = []
                # read the tweet and remove from the buffer
                tweet_record.append(tweet_buffer[i])
                #del tweet_buffer[0]
                # push the tweet into aws kinesis
                #print "consumer reading data from buffer and pushing into kinesis..."
                '''
                try:
                    self.kinesis.put_records(StreamName="twitter", Records=tweet_record)
                except Exception as e:
                    print(e)
                    continue
                del tweet_record[0]
                '''
                i=i+1
                #time.sleep(random())
            # add more tweets until half the buffer is full then push to kinesis
            if i==100:
                try:
                    self.kinesis.put_records(StreamName="twitter", Records=tweet_record)
                    time.sleep(0.11)
                except Exception as e:
                    print(e)
                    continue
                tweet_record = []
                i=0
            # if len(tweet_buffer)==0:
            #     time.sleep(1)




def main():

    ## twitter credentials
    consumer_key = twitterCreds.consumer_key
    consumer_secret = twitterCreds.consumer_secret
    access_token_key = twitterCreds.access_token_key
    access_token_secret = twitterCreds.access_token_secret

    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    kinesis = boto3.client('kinesis')
    producer = TwitterDataProducer(api, kinesis)
    producer.start()
    num_consumers = int(sys.argv[1])
    for i in range(num_consumers):
        consumer = TwitterDataConsumer(api, kinesis)
        consumer.start()


if __name__ == "__main__":
    main()
