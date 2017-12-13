CREATE EXTERNAL TABLE twitter_dynamodb(country string, country_code string, favorites_count bigint, friends_count bigint, full_name string, id bigint, it_atr string, lang string, name string, place_type string, screen_name string,SequenceNumber string, source string, statuses_count bigint, text string, time_zone string)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name" = "Twitter", "dynamodb.column.mapping" = "country:country,country_code:country_code,favorites_count:favorites_count,friends_count:friends_count,full_name:full_name,id:id,it_atr:it_atr,lang:lang,name:name,place_type:place_type,screen_name:screen_name,SequenceNumber:SequenceNumber,source:source,statuses_count:statuses_count,text:text,time_zone:time_zone");

create external table twitter_hdfs ( country string, country_code string, favorites_count bigint, friends_count bigint, full_name string, id bigint, it_atr string, lang string, name string, place_type string, screen_name string,SequenceNumber string, source string, statuses_count bigint, text string, time_zone string) STORED AS SEQUENCEFILE location 'hdfs:///twitter/';

INSERT OVERWRITE TABLE twitter_hdfs SELECT * from twitter_dynamodb;
INSERT INTO TABLE twitter_hdfs SELECT * from twitter_hdfs;

