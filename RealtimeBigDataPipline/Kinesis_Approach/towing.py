import requests
import boto3
import json

# set up the API request to fetch data from Chicago data portal API
url = "https://data.cityofchicago.org/resource/ygr5-vcbg.json"
params = {
    "$limit": 1000,
    "$offset": 0
}
records = []

while True:
    response = requests.get(url, params=params)
    data = response.json()
    records += data

    if len(data) < 1000:
        break

    params["$offset"] += 1000

# set up the Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')

# send data to Kinesis
for item in records:
    # convert the item to JSON format and encode it as bytes
    item_json = json.dumps(item)
    item_bytes = item_json.encode('utf-8')

    # send the data to Kinesis
    response = kinesis_client.put_record(
        StreamName='kinesis',
        Data=item_bytes,
        PartitionKey=item['inventory_number']
    )

    # check the response status
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Error sending data to Kinesis:", response)
