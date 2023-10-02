import boto3

def create_ec2_instance():
    pass
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

def execute_cmd_on_ec2(client, commands, instance_ids):
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


# Credentials for all the boto clients are picked up from env when running on amazon linux EC2 (web server)
if __name__ == '__main__':
    ssm_client = boto3.client('ssm')
    commands = ['echo "hello world"']
    instance_ids = ['an_instance_id_string']
    execute_cmd_on_ec2(ssm_client, commands, instance_ids)

