import boto3

# get client
# region_name='us-east-1',aws_access_key_id="ACCESS_KEY_HERE",
client = boto3.client('sqs')
#   aws_secret_access_key="SECRET_KEY_HERE")

# SQS Queue URL
request_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue'


# get first available message in recieve queue
def get_queue_data():
    request = client.receive_message(
        QueueUrl=request_queue_url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=10,
        WaitTimeSeconds=0
    )

    message = request['Messages'][0]
    receipt_handle = message['ReceiptHandle']

# send output data to response queue


def send_data_to_queue(image_ouput):
    response = client.send_message(
        QueueUrl=response_queue_url,
        MessageBody=image_output
    )


def delete_message(message):
    message.delete()
