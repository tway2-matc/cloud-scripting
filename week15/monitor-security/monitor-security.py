#!/usr/bin/env python3
import boto3

def main():
    #creates a set of security group names
    securityGroups = getSecurityGroups()
    
    #secures SSH access for each security group in the set
    for securityGroup in securityGroups:
        secureSSH(securityGroup)

    print("script completed")

def getSecurityGroups():
    print("Getting set of security groups used by ec2 instances")
    #creates an empty set
    toReturn = set()
    #creates an ec2 client
    ec2Client = boto3.client("ec2")
    reservations = ec2Client.describe_instances()["Reservations"]
    #loops through the reservations to get each instance
    for reservation in reservations:
        instances = reservation["Instances"]
        #loops through each instance to get all the security groups it uses
        for instance in instances:
            securityGroups = instance["SecurityGroups"]
            #adds each security group to the set
            for securityGroup in securityGroups:
                toReturn.add(securityGroup["GroupId"])
    #returns the set
    return toReturn

def secureSSH(securityGroup):
    #creates an ec2 client
    ec2Client = boto3.client("ec2")
    #gets the security group
    sg = ec2Client.describe_security_groups(GroupIds=[securityGroup])["SecurityGroups"][0]
    print(f"checking security group {sg['GroupName']}")
    #gets the list of rules
    sgRules = sg["IpPermissions"]
    #creates a boolean to remember if any access has been revoked
    accessRevoked = False
    #loops through the rules
    for sgRule in sgRules:
        #prints information about the rule
        print(f"\nallows access to ports {sgRule['FromPort']} to {sgRule['ToPort']} from")
        for ipRange in sgRule["IpRanges"]:
            print(f"     {ipRange['CidrIp']}")
        #checks if the rule allows ssh access
        sshOpen = (22 in range(sgRule["FromPort"],sgRule["ToPort"]+1))
        #checks if the rule allows access from anywhere
        accessAnywhere = False
        for ipRange in sgRule["IpRanges"]:
            if ipRange["CidrIp"] == "0.0.0.0/0":
                accessAnywhere = True
        #if both are true, removes the rule
        if sshOpen and accessAnywhere:
            print("rule allows ssh access from anywhere")
            ec2Client.revoke_security_group_ingress(
                GroupId=securityGroup,
                IpPermissions=[sgRule])
            print("ssh access revoked")
            accessRevoked = True
    if not accessRevoked:
        print("No access needed to be revoked")
    print()
    
if __name__ == "__main__":
    main()
