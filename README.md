# Real-Time Data Analysis and Prediction: Chicago Traffic Violations and Crashes
This project focuses on analyzing and predicting various factors and consequences associated with traffic violations and crashes in the city of Chicago. The project utilizes a real-time dataset provided by the City of Chicago, which includes information on traffic congestion estimates, red light camera violations, speed violations, traffic crashes, and towed vehicles. The dataset contains multiple features that are crucial for drawing conclusions about the violations and their effects, whether they are financial or health-related.

## Objective
The main objective of this project is to build an end-to-end big data pipeline that extracts real-time data, loads it into a database, and performs analytics services such as visualization and prediction. To achieve this objective, we employ tools such as Kafka or AWS Kinesis for data streaming, AWS DynamoDB or EMR for data storage and processing, and Machine Learning models (Logistic Regression and Random Forests) for prediction.


## Project Goals
1. Data Cleansing: Implement data cleansing techniques using Lambda functions to ensure data quality and consistency.
2. Data Processing: Upload the necessary files to an S3 bucket for further processing.
3. Real-time Data Loading: Utilize Lambda functions to upload the cleansed data into DynamoDB for real-time storage.
4. Data Streaming: Enable Kinesis or Kafka data streaming for DynamoDB to process and analyze real-time data.
5. Data Visualization: Leverage Tableau 2023.1 to create visualizations for various factors associated with the dataset.
6. Prediction with Machine Learning: Develop Machine Learning models using Logistic Regression and Random Forests to predict relevant outcomes.

## Specific Questions
Alongside the primary problem statement, we have addressed the following specific questions:

1. When do most car crashes occur?
2. What is the financial damage per incident?
3. Are all car crashes fatal?
4. How does road conditions affect car crashes?

## Conclusion
This big data pipeline project demonstrates the successful utilization of various tools and systems to process and analyze large volumes of data efficiently. We have built a real-time data pipeline using AWS Kinesis/Kafka, S3, Lambda functions, DynamoDB, Tableau, and Sagemaker. Two approaches, AWS Kinesis and Kafka, were employed for the data streaming part. A Lambda function was used to process the data triggered by changes in S3 and store it in DynamoDB, a NoSQL database. The dataset was effectively visualized, and Machine Learning models using Sagemaker, including Logistic Regression and Random Forests, were created. All the questions posed at the beginning of the project were successfully answered through the analysis and predictions conducted.
