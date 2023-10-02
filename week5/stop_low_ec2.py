#!/usr/bin/env python3
import boto3
import ec2
import sns

DRYRUN = False

sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]

#creates an ec2 instance and stores the instance id
ec2Client = boto3.client('ec2')
image = ec2.Get_Image(ec2Client)
instance = ec2.Create_EC2(image, ec2Client, DRYRUN)
instance_id = instance.instance_id

#sets up email notifications
email = "tway2@madisoncollege.edu"
topicArn = sns.CreateSNSTopic("WayTopic")
sns.SubscribeEmail(topicArn,email)

#creates a cloudwatch client
cwClient = boto3.client("cloudwatch")
#creates a cloudwatch alarm that stops the instance on low cpu use
response = cwClient.put_metric_alarm(
    AlarmName='Web_Server_LOW_CPU_Utilization',
    ComparisonOperator='LessThanOrEqualToThreshold',
    EvaluationPeriods=1,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=10.0,
    ActionsEnabled=True,
    AlarmActions=[
        f'arn:aws:swf:us-east-1:{account_id}:action/actions/AWS_EC2.InstanceId.Stop/1.0',
        f'arn:aws:sns:us-east-1:{account_id}:WayTopic'
    ],
    AlarmDescription='Alarm when server CPU is lower than 10%',
    Dimensions=[{
        'Name': 'InstanceId',
        'Value': instance_id
    },])
