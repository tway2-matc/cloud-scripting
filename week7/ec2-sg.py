#!/usr/bin/env python3
import boto3
import argparse

#gets the sg the user is looking for
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--security-group",default="")
search = parser.parse_args().security_group

#creates an ec2 client
ec2Client = boto3.client("ec2")
#gets the list of security groups
securityGroups = ec2Client.describe_security_groups()["SecurityGroups"]

#loops through the security groups
for sg in securityGroups:
    #checks if the sg's name has what the user was looking for
    if(search.lower() in sg["GroupName"].lower()):
        #prints the name and description
        print(f'{sg["GroupName"]} - {sg["Description"]}')
        #loops through the sg's rules
        sgIpPerms = sg["IpPermissions"]
        for rule in sgIpPerms:
            if(rule["IpProtocol"] != "-1"):
                #prints the port range
                print(f" - Ports: {rule['FromPort']}-{rule['ToPort']}")
                #prints the ipv4 ranges
                for address in rule['IpRanges']:
                    print(f"    - Cidr: {address['CidrIp']}")
                    if address["CidrIp"] == "0.0.0.0/0":
                        print("   WARNING: open to the public internet")
        print()