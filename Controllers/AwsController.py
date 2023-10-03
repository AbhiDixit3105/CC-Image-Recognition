import boto3


class AwsController:
    def upload_to_s3(self,file):
        pass
    def send_to_sqs(self):
        pass

    def receive_from_sqs(self):
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



