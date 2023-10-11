#  Serverless server Cloud computing project 1 : Image-Recognition using EC2 custom scaling

## Group Members and Tasks:
    1. Bhavesh khubnani
        1. Provisioned an EC2 instance for the web tier using the AWS console.
        2. Designed a web controller to handle specific image file uploads from web tier users.
        3.Uploaded user image files to the S3 input bucket and sent files to the SQS request queue for processing.
        4.Developed scaling logic in the scaling controller, monitoring the SQS queue depth every 30 seconds, and dynamically creating or terminating EC2 instances in the app tier, with a limit of 20 instances.
        5.Provided assistance and support to other team members as needed.

    2. Aishwariya Ranjan
        1. Provisioned the request and response SQS queues for the app.  
        2. Code to send messages to SQS request queue and receive messages response queues from the web tier side.  
        3. Code to send messages to the response queue and receive them from the request queue from the app tier side. -Code to delete messages from the queues. 
        4. Code to create and destroy EC2 instances in ScalingController.py on the web tier.
    3. Abhijeet Dixit
        1. 1.Provisioned the EC2 instances for the app tier for the app.
        2.Created the web app for users to interact with the application and upload images in the web tier. 
        3. Configured the EC2 instances to interact with each other and the internet by setting up the gunicorn (WSGI server) and the NGINX server to proxy requests from the user to the Web Tier. 
        4. Responsible for setting up the SQS queues and creation and configuration of AMI’s for the app tier.
        5. Configured the App Tier instances to run a custom python script along with the image recognition py script.


## Web-tier URL for  : 
     http://34.197.236.175/
## SQS Queue Names : 
    1. SQS request queue: cc-proj-1-request-queue
    2. SQS response queue: cc-proj-1-response-queue
## S3 Buckets : 
    1. Input bucket  : cc-ss-input-bucket
    2. Output Bucket : cc-ss-output-bucket

## PEM Key 
    location : data/key/CC-PROJECT-KEY.pem
    https://github.com/AbhiDixit3105/CC-Image-Recognition/blob/ICC-13-edited-code/data/key/CC-PROJECT-KEY.pem
## Creds :
    1. from console 
    account number : 827983923224 user: Aishwariya password: Aishwariya@1
    2. for cli 
    access_key = 'AKIA4BR5QBAMDUC72SQX' secret_key = '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'

## Custom AMI Image ID :
ami-0c478986cbb8292d8

*Use the web-tier folder code and upload it to the web-tier instance (This is already pre-configured on the AWS account)
*App tier will automatically be provisioned and scaled by the web-tier depending on the SQS queue.
