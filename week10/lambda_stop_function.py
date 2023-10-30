#!/usr/bin/env python3

import json
import boto3

ec2Client = boto3.client("ec2")

def lambda_handler(event,context):
    # TODO Implement
    response = Stop_EC2()
    print(List_EC2())
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from lambda")
    }

def List_EC2():
    instanceList = []
    reservations = ec2Client.describe_instances()["Reservations"]
    for reservation in reservations:
        instances = reservation["Instances"]
        for instance in instances:
            instanceList.append(instance["InstanceId"])
    return instanceList

def Stop_EC2():
    instanceList = List_EC2()
    return ec2Client.stop_instances(InstanceIds=instanceList)