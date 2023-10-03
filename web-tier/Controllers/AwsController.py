import boto3


class AwsController:
    def __int__(self):
        self.kms_key_id = 'b9279eb0-0de3-4f49-96df-5d7467abdd5e'
        self.encryption_key = 'cc-serverless-server'
        self.sqs_client = boto3.client('sqs')
        self.request_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue'
        self.response_queue_url = 'https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue'


    def upload_to_s3(self, file, bucket_name):
        s3 = boto3.client('s3')
        print("Uploading S3 object with SSE-KMS")
        s3.put_object(Bucket=bucket_name,
                      Key=self.encryption_key,
                      Body=file,
                      ServerSideEncryption='aws:kms',
                      SSEKMSKeyId=self.kms_key_id)
        print("Done")

        pass

    def send_to_sqs(self, message):
        sqs_client = boto3.client('sqs', region_name="us-east-1")
        response = sqs_client.send_message(
            QueueUrl=self.request_queue_url,
            MessageBody=message
        )
        return response



