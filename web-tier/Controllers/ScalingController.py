import time

import boto3


class ScalingController:
    def __init__(self):
        self.ami = 'ami-09c6ef0459a2ff40e'
        self.instance_type = 't2.micro'
        self.key_name = 'CC-PROJECT-KEY'
        self.subnet_id = 'subnet-09f0728d34cc36e41'
        self.region = 'us-east-1'
        self.max_instances = 10
        self.send_queue_name = 'abc'
        self.current_instance_count = 1
        self.ec2 = boto3.resource('ec2', region_name=self.region)
        self.monitor_interval_s = 10  # 10 seconds is very aggressive
        self.instance_ids = []

    def check_backlog(self, queue_name):
        queue_resource = boto3.resource('sqs',region_name=self.region).Queue(queue_name)
        return len(queue_resource.receive_messages(VisibilityTimeout=2, MaxNumberOfMessages=10))

    def get_instance_map(self):
        running_instances = [instance.id for instance in self.ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])]
        starting_instances = [instance.id for instance in self.ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['starting', 'bootstraping']}])]

        return {'RUNNING': running_instances, 'STARTING': starting_instances}

    def create_ec2_instance(self):
        client = boto3.client('ec2',region_name=self.region)
        instance = client.run_instances(
            ImageId=self.ami,
            InstanceType=self.instance_type,
            KeyName=self.key_name,
            SubnetId=self.subnet_id,
            MaxCount=1,
            MinCount=1,
            InstanceInitiatedShutdownBehavior='terminate'
        )

        instance_id = instance['Instances'][0]['InstanceId']
        self.instance_ids.append(instance_id)

    def destroy_ec2_instance(self, destroy_instance_ids):
        self.ec2.instances.filter(InstanceIds=destroy_instance_ids).terminate()

    def scale_in_function(self):
        self.destroy_ec2_instance([self.instance_ids.pop()])


    def scale_out_function(self, count):
        for i in range(count):
            self.create_ec2_instance()
        pass

    def monitor_queue_status(self):
        depth = self.check_backlog(self.send_queue_name)
        instance_map = self.get_instance_map()
        current_instance_count = len(instance_map.get("RUNNING", __default=1))
        backlog_p_i = depth / current_instance_count

        if current_instance_count + len(instance_map.get("STARTING")) == self.max_instances:
            # max scaling reached:
            pass
        elif backlog_p_i == 0:
            self.scale_in_function()
            pass
        elif backlog_p_i <= 1:
            self.scale_out_function(1)
            # add 1 instance :
            pass
        elif backlog_p_i <= 3:
            self.scale_out_function(max(1, int((self.max_instances - current_instance_count) / 3)))
            # add (max-current)/3 instances
            pass
        elif backlog_p_i <= 6:
            # add (max-current)/2 instances
            self.scale_out_function(max(1, int((self.max_instances - current_instance_count) / 2)))
            pass
        elif backlog_p_i >= 7:
            self.scale_out_function(max(1, int((self.max_instances - current_instance_count))))
            # add  (max-current) instances
            pass
        time.sleep(3)  # 3 second wait
