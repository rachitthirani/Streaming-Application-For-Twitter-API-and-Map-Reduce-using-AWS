import boto3
from global_variables import *

client = boto3.client('kinesis')
response = client.create_stream(StreamName='twitter', ShardCount=shard_count)
