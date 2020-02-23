import boto3
import os
 
def lambda_handler(event, context):
    cluster = event['Clusters']
    rds = boto3.client('rds')
    # instance = rds.Instance(instances)
    if event['Action'] == 'START':
        try:
            rds.start_db_cluster(DBClusterIdentifier=cluster)
        except Exception as error:
            call_sns(str(error), event['Action'])
            return 2
    elif event['Action'] == 'STOP':
        try:
            rds.stop_db_cluster(DBClusterIdentifier=cluster)
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
