# script to read data from Kinesis, extract dat and store into dynamoDB

import boto3, time, json, decimal, threading
from threading import Thread
from global_variables import *
# aws creds are stored in ~/.boto
# Connent to the kinesis stream
kinesis = boto3.client("kinesis")
#print kinesis.describe_stream(StreamName="twitter")




class ReadDataFromShard (threading.Thread):
    def __init__(self, shard_no):
        threading.Thread.__init__(self)
	if shard_no  <= 9:
            shard_id = 'shardId-00000000000' + str(shard_no)
	else:
            shard_id = 'shardId-0000000000' + str(shard_no)
        self.shard_it = kinesis.get_shard_iterator(StreamName="twitter", ShardId=shard_id, ShardIteratorType="LATEST")["ShardIterator"]
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('Twitter')

    def run(self):
        while True:
            out = kinesis.get_records(ShardIterator=self.shard_it, Limit=100)
            # print(out['Records'])
            for record in out['Records']:
                tweet_record = json.loads(record['Data'].decode('utf-8'))
                # print(record['Data'])
                if 'id_str' in tweet_record.keys() and 'lang' in tweet_record.keys() \
                and 'text' in tweet_record.keys() and 'source' in tweet_record.keys():
                    if 'user' in tweet_record.keys() and tweet_record['id_str'] is not None\
                    and tweet_record['lang'] is not None and tweet_record['text'] is not None\
                    and tweet_record['source'] is not None:
                        tweet_user = tweet_record['user']
                        """
                            id, friends_count, statuses_count, favourites_count - int
                            rest all attributes are string
                        """
                        #print(tweet_user['time_zone'])
                        if 'id' in tweet_user.keys() and 'name' in tweet_user.keys() \
                        and 'time_zone' in tweet_user.keys() and 'friends_count' in tweet_user.keys() \
                        and 'screen_name' in tweet_user.keys() and 'statuses_count' in tweet_user.keys() \
                        and 'favourites_count' in tweet_user.keys() and 'description' in tweet_user.keys():
                            if tweet_user['id'] is not None and tweet_user['name'] is not None \
                            and tweet_user['time_zone'] is not None and tweet_user['friends_count'] is not None \
                            and tweet_user['screen_name'] is not None and tweet_user['statuses_count'] is not None \
                            and tweet_user['favourites_count'] is not None and tweet_user['description'] is not None:
                                if 'place' in tweet_record.keys():
                                    tweet_place = tweet_record['place']
                                    if tweet_place is not None and 'country' in tweet_place.keys() and 'country_code' in tweet_place.keys() \
                                    and 'full_name' in tweet_place.keys() and 'place_type' in tweet_place.keys():
                                        #print(tweet_place['country'] .encode('utf8'))
                                        if tweet_place['country'] is not None and tweet_place['country_code'] is not None \
                                        and tweet_place['full_name'] is not None and tweet_place['place_type'] is not None:
                                            try:
                                                self.table.put_item(
                                                    Item={
                                                        'SequenceNumber': record['SequenceNumber'],
                                                        'id_str': tweet_record['id_str'],
                                                        'text': tweet_record['text'],
                                                        'lang': tweet_record['lang'],
                                                        'source': tweet_record['source'],
                                                        'id': tweet_user['id'],
                                                        'name': tweet_user['name'],
                                                        'time_zone': tweet_user['time_zone'],
                                                        'friends_count': tweet_user['friends_count'],
                                                        'screen_name': tweet_user['screen_name'],
                                                        'statuses_count': tweet_user['statuses_count'],
                                                        'favourites_count': tweet_user['favourites_count'],
                                                        'description': tweet_user['description'],
                                                        'country': tweet_place['country'],
                                                        'country_code': tweet_place['country_code'],
                                                        'full_name': tweet_place['full_name'],
                                                        'place_type': tweet_place['place_type'],
                                                    })
                                                print(tweet_place['place_type'] .encode('utf8'))
                                            except Exception as e:
                                                    print(e)
            # Refer http://boto3.readthedocs.io/en/latest/guide/dynamodb.html for pushing data in DynamoDB
            # print("Working fine...")
            self.shard_it = out["NextShardIterator"]
            time.sleep(0.10)

for i in range(shard_count):
    obj = ReadDataFromShard(i)
    obj.start()
