#  Serverless server Cloud computing project 1 : Image-Recognition using EC2 custom scaling

## Group Members and Tasks:
    1. Bhavesh khubnani
        1. EC2 app tier provisioning
        2. Creating scheduled scaling task based on queue depth
        3.
    2. Aishwariya Ranjan
        1. Provisioned the request and response SQS queues for the app.  
        2. Code to send messages to SQS request queue and receive messages response queues from the web tier side.  
        3. Code to send messages to the response queue and receive them from the request queue from the app tier side. -Code to delete messages from the queues. 
        4. Code to create and destroy EC2 instances in ScalingController.py on the web tier.
    3. Abhijeet Dixit
        1.


## Web-tier URL : 
     http://34.197.236.175/
## SQS Queue Names : 
    1. SQS request queue: cc-proj-1-request-queue
    2. SQS response queue: cc-proj-1-response-queue
## S3 Buckets : 
    1. Input bucket  : cc-ss-input-bucket
    2. Output Bucket : cc-ss-output-bucket

## PEM Key 
    location : data/key/CC-PROJECT-KEY.pem

## Creds :
    1. from console 
    account number : 827983923224 user: Aishwariya password: Aishwariya@1
    2. for cli 
    access_key = 'AKIA4BR5QBAMDUC72SQX' secret_key = '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'
