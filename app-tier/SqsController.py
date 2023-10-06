import subprocess
import time
import boto3

request_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue'

access_key = 'AKIA4BR5QBAMDUC72SQX'
secret_key = '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'
s3_bucket_in = 'cc-ss-input-bucket'
s3_bucket_o = 'cc-ss-output-bucket'

sqs_client = boto3.client('sqs', region_name="us-east-1", aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)


def get_queue_data():
    request = sqs_client.receive_message(
        QueueUrl=request_queue_url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=10,
        WaitTimeSeconds=0
    )

    return request['Messages'][0]


def send_data_to_queue(image_output):
    response = sqs_client.send_message(
        QueueUrl=response_queue_url,
        MessageBody=image_output
    )


def download_image(image_name):
    session = boto3.client("s3",aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    file_name = '/home/ubuntu/inputImages/' + image_name + '.jpg'
    session.download_file(s3_bucket_in, image_name, file_name)


def classify_image(image_name):
    path = '/home/ubuntu/inputImages/' + image_name
    filename = '/home/ubuntu/outputImages/' + image_name + '.txt'
    subprocess.run(['touch', filename])
    output_file = open(filename, "w")
    subprocess.run(('python3', './image_classification.py', path), stdout=output_file)
    return output_file


if __name__ == '__main__':
    while True:
        try:
            message = get_queue_data()
            image_name = message['Body']
            download_image(image_name)
            message_id = message['MessageId']
            output_val = classify_image(image_name)
            send_data_to_queue(str(message_id) + '-' + str(image_name) + '-')
            print("proceedind to delete message")
            delete_response = sqs_client.delete_message(
                QueueUrl=request_queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
        except Exception as e:
            print(e)
            print(f"Checking queue ....")
            time.sleep(5)
        else:
            print(f"Operation executed")
        time.sleep(10)



