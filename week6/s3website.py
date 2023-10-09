#!/usr/bin/env python3

import boto3
import json
import argparse
import random
import string
import botocore

s3Client = boto3.client('s3')

parser = argparse.ArgumentParser(description="arguments for bucket name for s3 website")
parser.add_argument("-s","--sitename", default="".join(random.choices(string.ascii_lowercase, k=10)),type=str)
args = parser.parse_args()

bucketName = args.sitename
print(f'creating a bucket with the name "{bucketName}"')

try:
    #creates an s3 bucket
    s3Client.create_bucket(Bucket=bucketName)

    #removes the public access block
    s3Client.delete_public_access_block(Bucket=bucketName)

    #creates a bucket policy
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucketName
        }]
    }
    #adds the policy to the bucket
    policyString = json.dumps(bucket_policy)
    s3Client.put_bucket_policy(Bucket=bucketName, Policy=policyString)
    #adds the website configuration to the bucket

    put_bucket_response = s3Client.put_bucket_website(Bucket=bucketName, WebsiteConfiguration={ 'ErrorDocument': {'Key': 'error.html'}, 'IndexDocument': {'Suffix': 'index.html'}, } )

    #writes the list of s3 buckets to the mybuckets.txt file
    with open("mybuckets.txt", "w") as bucketsFile:
        bucketsFile.write(json.dumps(put_bucket_response, indent=4))

    #adds index and error files to s3 bucket
    with open("index.html", "rb") as indexFile:
        s3Client.put_object(Body=indexFile, Bucket=bucketName, Key="index.html", ContentType='text/html' )
    with open("error.html", "rb") as errorFile:
        s3Client.put_object(Body=errorFile, Bucket=bucketName, Key="error.html", ContentType='text/html' )
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == "InvalidToken":
        print("please update your AWS credentials with a valid token")
    else:
        print(f"some other error occured {error}")
except s3Client.exceptions.BucketAlreadyExists as err:
    print("Bucket {} already exists".format(err.response["Error"]["BucketName"]))
