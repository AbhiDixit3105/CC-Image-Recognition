import boto3


class AwsController:
    def __int__(self):
        self.kms_key_id = 'b9279eb0-0de3-4f49-96df-5d7467abdd5e'
        self.encryption_key = 'cc-serverless-server'
        self.sqs_client = boto3.client('sqs')
        self.request_queue_url = ''
        self.response_queue_url = ''

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
        pass

    def receive_from_sqs(self):
        self.sqs_client.receive_message(
            QueueUrl=self.request_queue_url,
            AttributeNames=[
                'All' ],
            MessageAttributeNames=[
                'string',
            ],
            MaxNumberOfMessages=10,
            VisibilityTimeout=3,
            WaitTimeSeconds=3
        )
        pass

    def execute_cmd_on_ec2(self, client, commands, instance_ids):
        """Runs commands on remote linux instances
        :param client: a boto/boto3 ssm client
        :param commands: a list of strings, each one a command to execute on the instances
        :param instance_ids: a list of instance_id strings, of the instances on which to execute the command
        :return: the response from the send_command function (check the boto3 docs for ssm client.send_command() )
        """

        resp = client.send_command(
            DocumentName="AWS-RunShellScript",  # One of AWS' preconfigured documents
            Parameters={'commands': commands},
            InstanceIds=instance_ids,
        )
        return resp
