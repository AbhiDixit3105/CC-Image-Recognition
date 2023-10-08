import subprocess
import time
import boto3

# AWS credentials and queue URLs

request_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue'
access_key = 'AKIA4BR5QBAMDUC72SQX'
secret_key = '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'
s3_bucket_in = 'cc-ss-input-bucket'
s3_bucket_o = 'cc-ss-output-bucket'

# Initialize AWS clients
sqs_client = boto3.client('sqs', region_name="us-east-1", aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)


def get_queue_data():
    try:
        request = sqs_client.receive_message(
            QueueUrl=request_queue_url,
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=10,
            WaitTimeSeconds=0
        )

        if 'Messages' in request:
            return request['Messages'][0]
        else:
            return None
    except Exception as e:
        print("Error while receiving messages:", e)
        return None


def send_data_to_queue(image_output):
    try:
        response = sqs_client.send_message(
            QueueUrl=response_queue_url,
            MessageBody=image_output
        )
        print("Message sent to response queue:", response['MessageId'])
    except Exception as e:
        print("Error while sending message:", e)


def download_image(image_name):
    try:
        s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        file_name = '/home/ubuntu/inputImages/' + image_name
        s3.download_file(s3_bucket_in, image_name, file_name)
    except Exception as e:
        print("Error while downloading image:", e)


def upload_to_s3(file, filename):
    try:
        s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        print("Uploading S3 object with SSE-KMS")
        s3.upload_file(file, s3_bucket_o, filename)
        print("Done")
    except Exception as e:
        print("Error while uploading to S3:", e)


def classify_image(image_name):
    try:
        path = '/home/ubuntu/inputImages/' + image_name
        filename = '/home/ubuntu/outputImages/' + image_name + '.txt'
        subprocess.run(['touch', filename])
        output_file = open(filename, "w")
        p = subprocess.Popen(['python3', './image_classification.py', path],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        output_file.write("Output: {}\n".format(out.decode()))
        output_file.write("Error: {}\n".format(err.decode()))
        upload_to_s3(output_file.name, image_name + '.txt')
        return out.decode()
    except Exception as e:
        print("Error during image classification:", e)
        return str(e)


if __name__ == '__main__':
    while True:
        try:
            message = get_queue_data()
            if message:
                image_name = message['Body']
                download_image(image_name)
                message_id = message['MessageId']
                output_val = classify_image(image_name)
                send_data_to_queue(str(message_id) + '-' + str(image_name) + '-')
                print("Proceeding to delete message")
                delete_response = sqs_client.delete_message(
                    QueueUrl=request_queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        except Exception as e:
            print(e)
        finally:
            print("Checking queue ....")
            time.sleep(5)
