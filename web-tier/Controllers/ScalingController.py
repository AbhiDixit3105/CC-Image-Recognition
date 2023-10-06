import time

import boto3


class ScalingController:
    def __init__(self):
        self.ami = "ami-08c91ab714ebe5c98"
        self.instance_type = "t2.micro"
        self.key_name = "CC-PROJECT-KEY"
        self.subnet_id = "subnet-09f0728d34cc36e41"
        self.region = "us-east-1"
        self.max_instances = 20
        self.request_queue_url = (
            "https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-request-queue"
        )
        self.response_queue_url = (
            "https://sqs.us-east-1.amazonaws.com/827983923224/cc-proj-1-response-queue"
        )
        self.current_instance_count = 1
        self.ec2 = boto3.resource("ec2", region_name=self.region)
        self.monitor_interval_s = 10  # 10 seconds is very aggressive
        self.instance_ids = []

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
                Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
            )
        ]
        starting_instances = [
            instance.id
            for instance in self.ec2.instances.filter(
                Filters=[
                    {
                        "Name": "instance-state-name",
                        "Values": ["starting", "bootstraping"],
                    }
                ]
            )
        ]

        return {"RUNNING": running_instances, "STARTING": starting_instances}

    def create_ec2_instance(self,count):
        client = boto3.client("ec2", region_name=self.region)
        user_data_script = """#!/bin/bash
python3 /home/ubuntu/sqs-tier/SqsController.py
"""
        instance = client.run_instances(
            ImageId=self.ami,
            InstanceType=self.instance_type,
            KeyName=self.key_name,
            SubnetId=self.subnet_id,
            MaxCount=1,
            MinCount=1,
            InstanceInitiatedShutdownBehavior="terminate",
            UserData=user_data_script,
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": "CC-PROCESSING-SERVER-"+str(count)},
                        {"Key": "cc-processing-server", "Value": "cc-app-tier"},
                    ],
                }
            ]
        )

        instance_id = instance["Instances"][0]["InstanceId"]

        self.instance_ids.append(instance_id)
        print("Created ec2 instance with id : " + instance_id)

    def destroy_ec2_instance(self, destroy_instance_ids):
        self.ec2.instances.filter(InstanceIds=destroy_instance_ids).terminate()
        print("Destroyed ec2 instance with id : " + destroy_instance_ids)

    def scale_in_function(self):
        self.destroy_ec2_instance([self.instance_ids.pop()])

    def scale_out_function(self, count):
        # for i in range(count):
        #     self.create_ec2_instance()
        self.create_ec2_instance(count)
        pass

    def monitor_queue_status(self):
        depth = self.check_backlog()
        print("Depth is : ", depth)
        instance_map = self.get_instance_map()
        print("Depth is : ", depth)
        current_instance_count = len(instance_map["RUNNING"])
        print("Current instance count", current_instance_count)
        # backlog_p_i =  depth / current_instance_count - 1
        # print("Backlog per instance is : ", backlog_p_i)

        # Scale up logic
        if depth > 1 and current_instance_count + len(instance_map["STARTING"]) < 20:
            print("Scaling UP ...")
            self.scale_out_function(current_instance_count)

        # Scale down logic
        elif depth <= 2 and current_instance_count + len(instance_map["STARTING"]) > 1:
            print("Scaling down ....")
            self.scale_in_function()


        # if current_instance_count + len(instance_map["STARTING"]) == self.max_instances:
        #     # max scaling reached:
        #     print("Not scaling, max instance count reached")
        #     pass
        # elif backlog_p_i == 0:
        #     print("Scaling down")
        #     self.scale_in_function()
        #     pass
        # elif backlog_p_i <= 1:
        #     print("Scaling up by 1")
        #     self.scale_out_function(1)
        #     # add 1 instance :
        #     pass
        # elif backlog_p_i <= 3:
        #     print("Scaling up")
        #     self.scale_out_function(max(1, int((self.max_instances - current_instance_count) / 3)))
        #     # add (max-current)/3 instances
        #     pass
        # elif backlog_p_i <= 6:
        #     print("Scaling up ")
        #     # add (max-current)/2 instances
        #     self.scale_out_function(max(1, int((self.max_instances - current_instance_count) / 2)))
        #     pass
        # elif backlog_p_i >= 7:
        #     print("Scaling up ")
        #     self.scale_out_function(max(1, int((self.max_instances - current_instance_count))))
        #     # add  (max-current) instances
        #     pass
        time.sleep(3)  # 3 second wait
