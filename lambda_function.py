import boto3
import os
 
def lambda_handler(event, context):
    instance = event['instances']
    rds = boto3.client('rds')
    if event['Action'] == 'START':
        try:
            rds.start_db_instance(DBInstanceIdentifier = instance)
        except Exception as error:
            call_sns(str(error), event['Action'])
            return 2
    elif event['Action'] == 'STOP':
        try:
            rds.stop_db_instance(DBInstanceIdentifier = dbinstance)
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
