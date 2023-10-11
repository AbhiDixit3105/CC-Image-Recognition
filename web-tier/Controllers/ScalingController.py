import boto3

user_data_script = """#!/bin/bash
set -e -x
export PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages/
cd /home/ubuntu/app-tier
python3 AppController.py"""


class ScalingController:
    def __init__(self):
        self.ami = 'ami-0c478986cbb8292d8'
        self.instance_type = 't2.micro'
        self.key_name = 'CC-PROJECT-KEY'
        self.subnet_id = "subnet-09f0728d34cc36e41"
        self.region = 'us-east-1'
        self.max_instances = 20
        self.request_queue_url = (
            "https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue"
        )
        self.response_queue_url = (
            "https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue"
        )
        self.current_instance_count = 1
        self.ec2 = boto3.resource("ec2", region_name=self.region)
        self.min_instances = 1

    def check_backlog(self):
        sqs_client = boto3.client("sqs", region_name="us-east-1")
        response = sqs_client.get_queue_attributes(
            QueueUrl=self.request_queue_url,
            AttributeNames=["ApproximateNumberOfMessages"],
        )
        num_messages = int(response["Attributes"]["ApproximateNumberOfMessages"])
        print(f"Number of messages in the queue: {num_messages}")
        return num_messages

    def get_instance_map(self):
        running_instances = [
            instance.id
            for instance in self.ec2.instances.filter(
                Filters=[{"Name": "instance-state-name", "Values": ["running"]},
                         {"Name": "tag:cc-processing-server", "Values": ["cc-app-tier"]}
                         ]

            )
        ]


        starting_instances = [
            instance.id
            for instance in self.ec2.instances.filter(
                Filters=[
                    {
                        "Name": "instance-state-name",
                        "Values": ["pending"],
                    },
                    {
                        "Name": "tag:cc-processing-server",
                        "Values": ["cc-app-tier"]
                    }
                ]
            )
        ]

        return {"RUNNING": running_instances, "STARTING": starting_instances}

    def create_ec2_instance(self, cc):
        client = boto3.client("ec2", region_name=self.region)
        # user_data = base64.b64encode(user_data_script.encode()).decode()
        instance = client.run_instances(
            ImageId=self.ami,
            InstanceType=self.instance_type,
            KeyName=self.key_name,
            MaxCount=1,
            MinCount=1,
            InstanceInitiatedShutdownBehavior='terminate',
            SecurityGroupIds=['sg-0f94ce2d60babfb06'],
            UserData=user_data_script,
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": "CC-PROCESSING-SERVER-" + str(cc)},
                        {"Key": "cc-processing-server", "Value": "cc-app-tier"},
                    ],
                }
            ]
        )

        instance_id = instance["Instances"][0]["InstanceId"]

        print("Created ec2 instance with id : " + instance_id)

    def destroy_ec2_instance(self, destroy_instance_ids):
        self.ec2.instances.filter(InstanceIds=destroy_instance_ids).terminate()
        print("Destroyed ec2 instance with id : " + destroy_instance_ids)

    def scale_in_function(self):
        instance_id = self.get_instance_map().get("RUNNING").pop()
        self.destroy_ec2_instance([instance_id])
        print("Removed instance with id : ", instance_id)

    def scale_out_function(self, current_instance_count, scale_out_count):
        for i in range(scale_out_count):
            self.create_ec2_instance(current_instance_count)
            current_instance_count += 1

    def monitor_queue_status(self):
        depth = self.check_backlog()
        print("Depth is : ", depth)
        instance_map = self.get_instance_map()
        current_running_instance_count = len(instance_map["RUNNING"])
        print("Current instance count", current_running_instance_count)
        current_starting_instance_count = len(instance_map["STARTING"])
        if current_running_instance_count == 0:
            print("Scaling up")
            self.scale_out_function(0, self.min_instances)
        if depth == 0:
            if current_running_instance_count > self.min_instances:
                print("Scaling down")
                self.scale_in_function()
                current_running_instance_count -= 1
        if current_running_instance_count + current_starting_instance_count == self.max_instances:
            print("Not scaling, max instance count reached")
        elif depth > 1 and current_starting_instance_count == 0:
            print("depth > 1")
            available_capacity = self.max_instances - current_running_instance_count - current_starting_instance_count
            scale_up_count = min(depth - current_starting_instance_count,
                                 available_capacity) if depth > current_running_instance_count else min(
                depth, available_capacity)
            self.scale_out_function(current_running_instance_count, scale_up_count)
            print("Scaling by deficient count")
        elif current_starting_instance_count > 0:
            print("Not scaling as new instances are already starting")
        else:
            print("Not scaling, conditions were not met")
