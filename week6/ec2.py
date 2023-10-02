#!/usr/bin/env python3
import boto3
import botocore
DRYRUN = False

def main():
    ec2Client = boto3.client('ec2')
    #gets the ami
    image = Get_Image(ec2Client)

    #creates the WebSG group if it doesn't already exist
    Create_SG(ec2Client,"WebSG")

    #creates an instance
    instance = Create_EC2(image, ec2Client, DRYRUN)
    print("Creating instance")
    #waits until the instance is running
    instance.wait_until_running()
    print("instance running")
    #prints the public IP address
    print(Get_IP(instance))
    #adds a new tag
    Add_Tag(instance,"Name","Tighearnan")
    #prints the tags again
    print(Get_Tags(instance))

    #terminates the instance
    #Terminate_EC2(instance)

def Get_Image(ec2Client):
    #gets the images
    images = ec2Client.describe_images(
        Filters=[{
            'Name': 'description',
            'Values': ['Amazon Linux 2 AMI*']
        },{
            'Name': 'architecture',
            'Values': ['x86_64']
        },{
            'Name': 'owner-alias',
            'Values': ['amazon']
        }])
    return images["Images"][0]["ImageId"]

def Create_SG(ec2Client, name):
    #gets a list of existing security groups
    groups = []
    for sg in ec2Client.describe_security_groups()["SecurityGroups"]:
        groups.append(sg["GroupName"])
    #checks if the named security group exists
    if not(name in groups):
        #creates the security group
        print(f"Group {name} does not exist, creating security group")
        ec2Client.create_security_group(Description="Allows http access", GroupName=name)
        ec2Client.authorize_security_group_ingress(GroupName=name, 
                                                   FromPort=80,
                                                   ToPort=80, 
                                                   IpProtocol="tcp",
                                                   CidrIp="0.0.0.0/0")
    


def Create_EC2(AMI, ec2Client, DRYRUN):
    ec2 = boto3.resource('ec2')
    #creates an instance with the latest linux 2 ami
    response = ec2Client.run_instances(
        ImageId = AMI,
        InstanceType = 't2.micro',
        MinCount = 1,
        MaxCount = 1,
        DryRun = DRYRUN,
        SecurityGroups = ['WebSG'],
        UserData='''#!/bin/bash -ex
            # Updated to use Amazon Linux 2
            yum -y update
            yum -y install httpd php mysql php-mysql
            /usr/bin/systemctl enable httpd
            /usr/bin/systemctl start httpd
            cd /var/www/html
            wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-100-ACCLFO-2/lab6-scaling/lab-app.zip
            unzip lab-app.zip -d /var/www/html/
            chown apache:root /var/www/html/rds.conf
            '''
    )
    #gets and returns the instance
    instance = ec2.Instance(response["Instances"][0]["InstanceId"])
    return instance

def Get_IP(instance):
    publicIP = instance.public_ip_address
    return publicIP

def Get_Tags(instance):
    tags = instance.tags
    return tags

def Add_Tag(instance, key, value):
    response = instance.create_tags(
        Tags = [{
            "Key" : key,
            "Value" : value
        }]
    )
    return response

def Terminate_EC2(instance):
    #terminates the instance
    instance.terminate()
    #waits until the instance is terminated
    instance.wait_until_terminated()
    print(f"instance is {instance.state['Name']}")

try:
    if __name__ == "__main__":
        main()
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == "UnauthorizedOperation":
        print("Please check your region configuration")
    else:
        print(error)