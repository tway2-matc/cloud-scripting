#!/usr/bin/env python3
import boto3
import csv

def main():
    response = Get_Instances("instance-type", "t2.micro")
    headerRow = ["InstanceId", "InstanceType", "State", "PublicIpAddress", "Monitoring"]
    content = Get_Content(response)
    
    CSV_Writer(headerRow, content)



def Get_Instances(Name, Values):
    ec2Client = boto3.client("ec2")
    paginator = ec2Client.get_paginator("describe_instances")
    page_list = paginator.paginate(Filters=[
        {
            'Name': 'instance-state-name',
            'Values':[
                'running',
            
            ]
        },{
            'Name': Name,
            'Values':[
                Values,
            ]
        }])
    response = []
    for page in page_list:
        for reservation in page["Reservations"]:
            response.append(reservation)

    return response

def CSV_Writer(header, content):
    with open("export.csv", "w") as export:
        writer = csv.DictWriter(export, fieldnames=header)
        writer.writeheader()
        for row in content:
            writer.writerow(row)

def Get_Content(response):
    content = []
    for instance in response:
        for ec2 in instance["Instances"]:
            content.append(
                {
                    "InstanceId":ec2["InstanceId"],
                    "InstanceType":ec2["InstanceType"],
                    "State":ec2["State"]["Name"], 
                    "PublicIpAddress":ec2.get("PublicIpAddress", "N/A"),
                    "Monitoring":ec2["Monitoring"]["State"]
                }

            )
    return content

if __name__ == "__main__":
    main()