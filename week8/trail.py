#!/usr/bin/env python3

import s3enforce, boto3
import json

def main():
    #gets the account id
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]
    #sets a bucket name for the script
    bucketName = "tway-bucket1-10-16-2023"
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
    CreateTrail("CloudTrail", bucketName)

def CreateTrail(trailName, bucketName):
    CTClient = boto3.client('cloudtrail')
    toReturn = CTClient.create_trail(Name=trailName,S3BucketName=bucketName)
    CTClient.start_logging(Name=trailName)
    return toReturn

if __name__ == "__main__":
    main()