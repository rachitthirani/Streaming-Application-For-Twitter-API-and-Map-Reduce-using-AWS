#emr

# first  add this to  bashrc fiel and change the source export PATH="$PATH:$HIVE_HOME/bin"

#create an external table for the data in dynamodb which has to be mapped to the hive to copy data form dynamodb to hdfs
#CREATE EXTERNAL TABLE twitter_dynamodb(hash string, count bigint) STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' TBLPROPERTIES ("dynamodb.table.name" = "hashtags", "dynamodb.column.mapping" = "hash:hashtag,count:htCount");

#create a table in hdfs where the data has to be copied.
#create external table hdfs_twitter (hash string, coutn bigint) STORED AS SEQUENCEFILE location 'hdfs:///rachittwittertest/'
#do add the way we want the data ot be stored in the file

#copy data from dynamodb to hdfs
#INSERT OVERWRITE TABLE hdfs_twitte_1r SELECT * from twitter_dynamodb;

import sys
from random import random
from operator import add

from pyspark import SparkContext
import time
start_time=time.time()

if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    sc = SparkContext(appName="PythonPi")
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    # Ref: https://stackoverflow.com/questions/30787635/takeordered-descending-pyspark
    output = sc.textFile('hdfs:///twitter/000000_0').flatMap(',').map(lambda x:x[9]).flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add).takeOrdered(100, key = lambda x: -x[1])
    # output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word.encode('utf-8'), count))
    sc.stop()
end_time=time.time()
print ("---%s seconds --- "%(end_time-start_time))
