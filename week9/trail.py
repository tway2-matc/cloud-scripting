#!/usr/bin/env python3

import s3enforce, boto3, botocore
import json

def main():
    #gets the account id
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]
    #sets a bucket name for the script
    bucketName = "tway-bucket1-10-16-2023"
    #sets a trailname for the script
    trailName = "Cloudtrail"
    #creates a bucket
    s3enforce.CreateBucket(bucketName)

    #creates a policy string for the bucket
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:GetBucketAcl",
            "Resource": f"arn:aws:s3:::{bucketName}"
        },{
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:PutObject",
            "Resource": f"arn:aws:s3:::{bucketName}/AWSLogs/{account_id}/*",
            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
    }]}
    policyString = json.dumps(policy)
    #adds the policy to the bucket
    s3enforce.SetBucketPolicy(bucketName,policyString)
    #create a cloudtrail
    CreateTrail(trailName, bucketName)
    StopLogging(trailName)

    trailStatus = GetTrailStatus(trailName)
    if not trailStatus:
        StartLogging(trailName)

def CreateTrail(trailName, bucketName):
    CTClient = boto3.client('cloudtrail')
    #checks if the trail exists
    trail = CTClient.describe_trails(trailNameList=[trailName])['trailList']
    if(trail == []):
        toReturn = CTClient.create_trail(Name=trailName,S3BucketName=bucketName)
        CTClient.start_logging(Name=trailName)
    else:
        print(f"trail {trailName} already exists")
        toReturn = trail
    return toReturn

def StartLogging(trailName):
    CTClient = boto3.client("cloudtrail")
    return CTClient.start_logging(Name=trailName)

def StopLogging(trailName):
    CTClient = boto3.client("cloudtrail")
    return CTClient.stop_logging(Name=trailName)

def GetTrailStatus(trailName):
    CTClient = boto3.client("cloudtrail")
    try:
        return CTClient.get_trail_status(Name=trailName)["IsLogging"]
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == "TrailNotFoundException":
            raise NameError("That Cloudtrail Trail was not found.")

if __name__ == "__main__":
    main()