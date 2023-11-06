#!/usr/bin/env python3

import boto3

ec2Client = boto3.client("ec2")
def main():
    Filter = [{'Name': 'tag:env',
               'Values':['dev']}]
    Start_EC2(Filter)

def List_EC2(Filter):
    instanceList = []
    reservations = ec2Client.describe_instances(Filters=Filter)["Reservations"]
    for reservation in reservations:
        instances = reservation["Instances"]
        for instance in instances:
            instanceList.append(instance["InstanceId"])
    return instanceList

def Stop_EC2(Filter):
    instanceList = List_EC2(Filter)
    return ec2Client.stop_instances(InstanceIds=instanceList)

def Start_EC2(Filter):
    instanceList = List_EC2(Filter)
    return ec2Client.start_instances(InstanceIds=instanceList)

if __name__ == "__main__":
    main()