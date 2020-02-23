import boto3
import os
 
def lambda_handler(event, context):
    instances = event['Instances']
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instances)
    if event['Action'] == 'START':
        try:
            instance.start()
            instance.wait_until_running()
        except Exception as error:
            call_sns(str(error), event['Action'])
            return 2
    elif event['Action'] == 'STOP':
        try:
            instance.stop()
            instance.wait_until_stopped()
        except Exception as error:
            call_sns(str(error), event['Action'])
            return 2

def call_sns(msg, action):
    """
    Nortify via E-mail if Exception arised.
    """
    topic_arn = os.environ["TOPIC_ARN"]
    subject = os.environ[action + "_SUBJECT"]
    client = boto3.client("sns")
    request = {
        'TopicArn': topic_arn,
        'Message': msg,
        'Subject': subject
        }

    client.publish(**request)
