import boto3


class AwsController:


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

        # Credentials for all the boto clients are picked up from env when running on amazon linux EC2 (web server)
    if __name__ == '__main__':
            ssm_client = boto3.client('ssm')
            commands = ['echo "hello world"']
            instance_ids = ['i-013adb440154a55d0']
            # i-02d039e7f2ee6aa41
            execute_cmd_on_ec2(ssm_client, commands, instance_ids)
