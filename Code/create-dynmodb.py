
## create a table to store twitter hashtags in DynamoDB
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='Twitter',
    KeySchema=[
        {
            'AttributeName': 'SequenceNumber',
            'KeyType': 'HASH',
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'SequenceNumber',
            'AttributeType': 'S',
        }
    ],
    # pricing determined by ProvisionedThroughput
    ProvisionedThroughput={
        'ReadCapacityUnits': 25,
        'WriteCapacityUnits': 25
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='Twitter')
