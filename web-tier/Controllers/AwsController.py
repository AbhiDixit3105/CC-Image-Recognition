import boto3


class AwsController:
    def __int__(self):
        self.kms_key_id = 'b9279eb0-0de3-4f49-96df-5d7467abdd5e'
        self.encryption_key = 'cc-serverless-server'
        self.sqs_client = boto3.client('sqs')
        self.request_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue'
        self.response_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue'
        self.sqs_client = boto3.client('sqs', region_name="us-east-1")
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.s3_bucket_in = 'cc-ss-input-bucket'
        self.s3_bucket_o = 'cc-ss-output-bucket'

    def upload_to_s3(self, file):
        s3= boto3.client('s3', region_name='us-east-1')
        print("Uploading S3 object with SSE-KMS")
        s3.upload_fileobj(file,'cc-ss-input-bucket',file.filename)
        print("Done")

        pass

    def send_to_sqs(self, message):

        response = self.sqs_client.send_message(
            QueueUrl=self.request_queue_url,
            MessageBody=message
        )
        return response

    def delete_message(self, message):
        delete_response = self.sqs_client.delete_message(
            QueueURL=self.response_queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )

    def receive_from_sqs(self, message_id):
        # get msg from reponse queue, check message body for message id and match to message_id.
        # If exists, delete form queue, else ignore

        response = self.sqs_client.receive_message(
            QueueUrl=self.response_queue_url,
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=10,
            WaitTimeSeconds=0
        )

        messages = response['Messages']
        for message in messages:
            if message_id in message['Body']:
                output_val = message['Body'].split('-')[2]
                self.delete_message(message)
                return output_val
