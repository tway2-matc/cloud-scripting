#!/usr/bin/env python3

import json
import boto3

ec2Client = boto3.client("ec2")

def lambda_handler(event,context):
    # TODO Implement
    Filter = [{'Name': 'tag:env',
               'Values':['dev']}]
    print(Start_EC2(Filter))
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from lambda")
    }

def List_EC2(Filter):
    instanceList = []
    reservations = ec2Client.describe_instances(Filters=Filter)["Reservations"]
    for reservation in reservations:
        instances = reservation["Instances"]
        for instance in instances:
            instanceList.append(instance["InstanceId"])
    return instanceList

def Start_EC2(Filter):
    instanceList = List_EC2(Filter)
    ec2Client.start_instances(InstanceIds=instanceList)
    return instanceList