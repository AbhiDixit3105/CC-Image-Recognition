import boto3

AMI = 'ami-09c6ef0459a2ff40e'
INSTANCE_TYPE = 't2.micro'
KEY_NAME = 'CC-PROJECT-KEY'
SUBNET_ID = 'subnet-09f0728d34cc36e41'
REGION = 'US-EAST-1'

if __name__ == '__main__':
    pass


def create_ec2_instance():
    client = boto3.client('ec2')
    instance = client.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SubnetId=SUBNET_ID,
        MaxCount=1,
        MinCount=1,
        InstanceInitiatedShutdownBehavior='terminate',
        UserData=init_script
    )

    instance_id = instance['Instances'][0]['InstanceId']

    # store instance_id


def destroy_ec2_instance():
    pass


def send_to_sqs():
    pass


def receive_from_sqs():
    pass


def scale_in_function():
    pass


def scale_out_function():
    pass
