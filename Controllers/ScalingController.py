import time

import boto3
import schedule


class ScalingController:
    def __init__(self):
        self.AMI = 'ami-09c6ef0459a2ff40e'
        self.INSTANCE_TYPE = 't2.micro'
        self.KEY_NAME = 'CC-PROJECT-KEY'
        self.SUBNET_ID = 'subnet-09f0728d34cc36e41'
        self.REGION = 'US-EAST-1'
        self.max_instances = 10
        self.send_queue_name = 'abc'
        self.current_instance_count = 1
        self.ec2 = boto3.resource('ec2')
        self.monitor_interval_s = 10  # 10 seconds is very aggressive
        self.instance_ids = []

    def check_backlog(self, queue_name):
        queue_resource = boto3.resource('sqs').Queue(queue_name)
        return len(queue_resource.receive_messages(VisibilityTimeout=2, MaxNumberOfMessages=10))

    def get_instance_map(self):
        running_instances = [instance.id for instance in self.ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])]
        starting_instances = [instance.id for instance in self.ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['starting', 'bootstraping']}])]

        return {'RUNNING': running_instances, 'STARTING': starting_instances}

    def create_ec2_instance(self):
        client = boto3.client('ec2')
        instance = client.run_instances(
            ImageId=self.AMI,
            InstanceType=self.INSTANCE_TYPE,
            KeyName=self.KEY_NAME,
            SubnetId=self.SUBNET_ID,
            MaxCount=1,
            MinCount=1,
            InstanceInitiatedShutdownBehavior='terminate'
        )

        instance_id = instance['Instances'][0]['InstanceId']
        self.instance_ids.push(instance_id)

    def destroy_ec2_instance(self):
        pass

    def scale_in_function(self):
        pass

    def scale_out_function(self):
        pass

    def monitor_queue_status(self):
        depth = self.check_backlog(self.send_queue_name)
        instance_map = self.get_instance_map()
        current_instance_count = len(instance_map.get("RUNNING", __default=1))
        backlog_p_i = depth / current_instance_count
        if len(instance_map.get("RUNNING")) + len(instance_map.get("STARTING")) == self.max_instances:
            # max scaling reached:
            pass
        elif backlog_p_i == 0:
            # scale in
            pass
        elif backlog_p_i <= 1:
            # add 1 instance :
            pass
        elif backlog_p_i <= 3:
            # add (max-current)/3 instances
            pass
        elif backlog_p_i <= 6:
            # add (max-current)/2 instances
            pass
        elif backlog_p_i >= 7:
            # add  (max-current) instances
            pass
        time.sleep(3)  # 3 second wait
