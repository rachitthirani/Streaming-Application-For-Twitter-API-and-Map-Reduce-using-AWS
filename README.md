# RedOctopusProject

## Architecture

![alt text](https://github.ncsu.edu/CSC591-DIC/RedOctopusProject/blob/master/Documents/RedOctopus%20Architecture.png)
### Streaming Data from Twitter using Kinesis
AWS Kinesis is used to stream the data from the Twitter servers using the TwitterAPI. TwitterAPI helps in fetching data from Twitter REST API and helps in streaming data easily. However, the data volume generated and received by the TwitterAPI is not large enough. Therefore, a multi-threaded program helps to generate large volumes of data by replicating the data received from Twitter. A thread retrieves the streaming data from Twitter and places that data in a shared buffer, while the other remaining threads read from the shared buffer and continuously push that data into the AWS Kinesis shards. For interacting with Kinesis boto3 library of Python is used just because of easy semantics it provides.

To feed the data into a shard, a hash is automatically calculated from the PartitionKey which results in a low success rate because of collisions. To overcome it, each process on different machines determined their unique shard using ExplicitHashKey to ingest data into that particular shard. This hash is being calculated using the command line parameter as the process number (not to be confused with process ID). The process number is the specific shard ID where the process the want to sends the data.

### Storing the Streamed data in DynamoDB
By default, the data is stored in Kinesis shards for a maximum of 24 hours. The default value can be changed to say 7 days but it cannot be infinitely large. Thus, the data need to be transferred into some persistent storage. Therefore, AWS DynamoDB is chosen as a persistent store. Firstly, a table is created with key as Sequence Number. The Sequence Number is the unique record number in the Kinesis stream. The Sequence Number is being chosen to make every record unique to avoid over-writing of records with same key.

Since the write capacity of writing units in DynamoDB is quite less. A multi-threaded program is required to read data continuously from all the shards. Processing is being done on the data to make the it quite homogeneous by discarding the records that does not fit to some required structure, i.e. filtering out the tweets which have missing values for the required attributes.

### Moving data form DynamoDB to HDFS to apply Map Reduce Task
Performing operations on DynamoDB directly is costly if one has to perform it multiple times. Also storing large amount of data in DynamoDB can also be costly. Therefore, the data is moved to HDFS from DynamoDB in batches whenever required.

Before moving the data, a cluster is needs to be setup. A total of four nodes of type m1.xlarge were chosen to setup the cluster with large SSD storage of 1680 GB at each node.

Amazon recommends using Hive to transfer the data from DynamoDB to HDFS. As one can select the required attributes only and Hive query engine automatically manages the transfer of data according to the number of specified reading units of the DynamoDB so that requests does not throttle. Therefore, an external table is created using hive which is mapped to the data in the DynamoDB table. Another external table was created in HDFS to store the data that will be copied from DynamoDB to HDFS. Thus, Hive knows the structure of the data and it will be very easy to copy only the required data. Finally, using INSERT, data was inserted into the table in HDFS from DynamoDB using Hive.

### Analysis of data
After transferring the data from DynamoDB to HDFS, data is replicated to increase the size as lot of data is being filtered out while storing the data in DynamoDB and transferring it from DynamoDB to HDFS. This is being to see the affect of large amount of data to the processing in a cluster environment.

The application developed was restricted to perform only simple analysis on data. The application searches for the most common name that is found among all the users who tweets. This analysis ultimately lands on the word count problem on the names. Firstly, all other attributes are filtered and only name is chosen. Name can be comprised of more than one word. Therefore, they are split to get all worse within a name and then to perform the main analysis. After splitting, words are grouped uniquely and the number of occurrence of each word is saved along the name in the output file or is printed on the screen.

## Code Structure
All the required code and configurations are present in the folder. Configurations folder consists of the script which automatically installs al the packages. There is an additional file which lists down the packages required.  
Code folder of the repository consists of all the files which contain the code and the Twitter Credentials.  

How to proceed:
1. Clone this git repository in all the machines which will be used for analysis.  
```git clone https://github.ncsu.edu/CSC591-DIC/RedOctopusProject```  
2. Install all the requirements.  
  + Boto3  
  + Twitter API  
  + HTTP  
  + Twitter  
  + awscli  
These can be installed using setup script which is in the Configuration folder. The setup script also makes sure to install python and pip and sets up the environment parameters.  
3. Update your AWS credentials using aws configure command. Use same AWS credentials on all the machines chosen to move the data to the same DynamoDB location. This can be done by entering “aws configure” command in terminal of the machine and updating the required fields.  
4. Create Twitter API. One access key can be used used for for two simultaneously connections. Store the Twitter credentials in the “twitterCreds.py” file which is in the Code folder.  
5. To create Kinesis stream run Code/create-stream.py using "python Code/create-stream.py" command in the terminal.  
6. Run Twitter Kinesis to generate data through command line  
    ```python Code/twitter-kinesis.py <num_threads> <shard_id>```  
7. If table doesn’t exists in DynamoDB create the table by running create-dynamodb.py by using "python Code/create-dynamodb.py" command in terminal.  
8. To start reading data from Kinesis and storing them persistently by running shard-dynmodb.py by using "python Code/shard-dynmodb.py" comman in terminal.  
9. Create EMR Cluster as per the need.  
10. Transfer data from DynamoDB to hadoop in EMR shell by running  
      ```hive -f Code/fetch_data.hql```  
11. To run the sample analysis again run it using  
      ```hive -f Code/hive.hql```


