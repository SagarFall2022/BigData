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
    print(contents)
    contents = json.loads(contents)
    for chunk in contents:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('trail2')
        table.put_item(Item=chunk)

    return {
        'statusCode': 200,
        'body': json.dumps('Documents inserted into DynamoDB')
    }