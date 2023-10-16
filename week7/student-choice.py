#!/usr/bin/env python3
#lists buckets, their creation date, whether or not they are publicly accessible, and describes their policies
import boto3
import json
import botocore

#creates an s3 client
s3Client = boto3.client("s3")
#creates a list of buckets
buckets = s3Client.list_buckets()["Buckets"]

#loops through the buckets
for bucket in buckets:
    #prints name and creation date
    print(f'{bucket["Name"]} - Created {bucket["CreationDate"]}')
    try:
        #determines whether or not the bucket is publicly accessible
        policyStatus = s3Client.get_bucket_policy_status(Bucket=bucket["Name"])["PolicyStatus"]["IsPublic"]
        #describes the public accessibility of the bucket
        if policyStatus:
            print(" - publicly accessible")
        else:
            print(" - not publicly accessible")
        #gets a list of the bucket policies
        policies = json.loads(s3Client.get_bucket_policy(Bucket=bucket["Name"])["Policy"])["Statement"]
        #describes the policies
        for policy in policies:
            print(f' - {policy["Effect"]}s {policy["Action"]} permissions for {policy["Principal"].replace("*","[anyone]")}')
        print()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == "NoSuchBucketPolicy":
            print(" - This bucket has no policy\n")
        else:
            print(error)
    