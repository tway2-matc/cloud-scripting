#!/usr/bin/env python3
import boto3
DRYRUN = False

def main():
    ec2Client = boto3.client('ec2')
    #gets the ami
    image = Get_Image(ec2Client)
    #creates an instance
    instance = Create_EC2(image, ec2Client)

    #waits until the instance is running
    instance.wait_until_running()
    #prints the public IP address
    print(Get_IP(instance))
    #prints the tags
    print(Get_Tags(instance))
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

def Create_EC2(AMI, ec2Client):
    ec2 = boto3.resource('ec2')
    #creates an instance with the latest linux 2 ami
    response = ec2Client.run_instances(
        ImageId = AMI,
        InstanceType = 't2.micro',
        MinCount = 1,
        MaxCount = 1,
        DryRun = DRYRUN
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

if __name__ == "__main__":
    main()