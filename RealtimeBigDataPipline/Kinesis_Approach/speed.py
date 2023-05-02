import requests
import boto3
import json

# set up the API request to fetch data from Chicago data portal API
url = "https://data.cityofchicago.org/resource/hhkd-xvj4.json"
params = {
    "$limit": 100000,
    "$offset": 0,
    "$where": "violation_date between '2023-01-01T00:00:00' and '2023-04-01T23:59:59'"
}
records = []

while True:
    response = requests.get(url, params=params)
    data = response.json()

    records += data

    print("Fetched", len(data), "records. Total:", len(records))

    if len(data) < 100000:
        break

    params["$offset"] += 100000

# set up the Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')

# send data to Kinesis
for item in records:
    # remove the 'location' key if it exists
    if 'human_address' in item:
        del item['human_address']

    if 'location' in item:
        del item['location']

    if 'camera_id' not in item:
        continue

    # convert the item to JSON format and encode it as bytes
    item_json = json.dumps(item)
    item_bytes = item_json.encode('utf-8')

    # send the data to Kinesis
    response = kinesis_client.put_record(
        StreamName='kinesis_SpeedViolations',
        Data=item_bytes,
        PartitionKey=item['camera_id']
    )

    # check the response status
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Error sending data to Kinesis:", response)
