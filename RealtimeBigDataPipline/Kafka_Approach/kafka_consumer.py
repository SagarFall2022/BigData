
import json
import boto3
from kafka import KafkaConsumer
import sys
import time

topic = sys.argv[1]

# Set the AWS region and S3 bucket name
region_name = 'us-east-1'
#bucket_name = 'csp554-project-towed'
start_date = "2023-01-01"
end_date = "2023-04-30"
date_str = start_date + "-to-" + end_date
MAX_PAYLOAD_SIZE = 5000  # maximum total size of payloads to accumulate before uploading to S3
total_size = 0  # variable to keep track of total payload size
payloads = []  # list to accumulate payloads
total_payloads = 63
total_payloads_ = 0

bucket_dict = {
                "TowedVehicles": 'csp554-project-towed',
                "RedLightViolations": 'csp554-project-redlightviolations',
                "SpeedViolations" : 'csp554-project-speedviolations',
                "Crashes": 'csp554-project-crashes'
                }

print("Connecting to S3")
# Set up the AWS S3 client
s3 = boto3.client('s3', region_name=region_name)

print("Setting up Consumer")
print("Bucket to be used:", bucket_dict[topic])

#print("Consuming Messages:")


# Set up the Kafka consumer
print("Starting ", topic)
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    fetch_max_bytes =52428800*10,
    max_partition_fetch_bytes = 1048576*10,
    max_poll_records = 500*20)

# Consume Kafka messages and write to S3
for message in consumer:
    bucket_name = bucket_dict[topic]
    print(f"Retrieving {message.topic} in {date_str} from Producer")
    try:
        # Decode the message payload
        payload = json.loads(message.value)
        
        payloads.extend(payload)  # append payload to list
        total_size += len(payload)  # add payload size to total
        total_payloads_ += 1
        if total_size >= MAX_PAYLOAD_SIZE or total_payloads == total_payloads_:
            # if we have accumulated enough payloads, upload them to S3
            json_array = json.dumps(payloads)
            s3.put_object(
                Bucket=bucket_name,
                Key=f'{message.topic}/{message.partition}/{message.offset}.json',
                Body=json_array,
                ContentType='application/json'
            )
            print("Payload put in S3:", total_size)
            # reset variables for next batch of payloads
            payloads = []
            total_size = 0
            time.sleep(60*20)
    except (ValueError, KeyError) as e:
        # Handle any exceptions and continue consuming
        print(f'Error occured', e)
        continue


print("Consumer Done!!")