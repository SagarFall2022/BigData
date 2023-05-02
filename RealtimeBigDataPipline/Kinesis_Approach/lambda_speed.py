import json
import boto3

def lambda_handler(event, context):
    # Get the S3 object details from the event
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get the contents of the S3 object
    obj = s3.get_object(Bucket=bucket, Key=key)
    contents = obj['Body'].read().decode('utf-8')

    # Split the contents by '}' to handle multiple JSON objects
    chunks = contents.split('}')
    for chunk in chunks:
        if chunk.strip():
            # Add back the '}' that was removed by the split
            data = json.loads(chunk + '}')

            # Insert the data into the DynamoDB table
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('speed-data')
            table.put_item(Item=data)

    return {
        'statusCode': 200,
        'body': json.dumps('Documents inserted into DynamoDB')
    }
