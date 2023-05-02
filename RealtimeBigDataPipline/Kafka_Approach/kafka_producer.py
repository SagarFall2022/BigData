
import requests
from kafka import KafkaProducer
import json
from datetime import datetime
import sys

topic_p = sys.argv[1]

start_date = "2023-01-01"
end_date = "2023-04-30"


# Set up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def get_producer_dict(start_date=None, end_date=None):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    date_dict = {"TowedVehicles":"tow_date",
                "RedLightViolations": 'violation_date',
                "SpeedViolations" : 'violation_date',
                "Crashes": 'crash_date'
                }
    producer_dict = {
                "TowedVehicles": 'https://data.cityofchicago.org/resource/ygr5-vcbg.json',
                "RedLightViolations": 'https://data.cityofchicago.org/resource/spqx-js37.json',
                "SpeedViolations" : 'https://data.cityofchicago.org/resource/hhkd-xvj4.json',
                "Crashes": 'https://data.cityofchicago.org/resource/85ca-t3if.json'
                }
    if start_date==None:
        return(producer_dict)
    else:        
        for dataset in list(producer_dict.keys()):
            condition_add = "?$where=" + date_dict[dataset] + " >= '" + start_date + "' and " + date_dict[dataset] + " <= '" + end_date + "'" + " &$limit=500000"
            producer_dict[dataset] = producer_dict[dataset] + condition_add
    return(producer_dict)
            


def producer_send(topic, api_url):
    # Set up the API endpoint and request parameters
    record_size = 500
    print("Starting send for ", topic)
    
    print(api_url)
    response = requests.get(api_url)
    # Make a GET request to the API and     publish the response to Kafka
    #if topic_p == topic:
    if response.status_code == 200:
        data = response.json() 
        for item in data:
            # remove the 'location' key if it exists
            if 'location' in item:
                del item['location']
        print("Size of response ", len(data))
        if len(data)>0:
            for i in range(0, len(data), record_size):
                producer.send(topic, data[i:i+record_size])
                producer.flush()
                print('Sending ', i+record_size)
        else:
            print("No data for in specified date range for ", topic)
    else:
        print(f'Error retrieving data from API: {response.status_code}')

producer_dict = get_producer_dict(start_date, end_date)
producer_send(topic_p, producer_dict[topic_p])



