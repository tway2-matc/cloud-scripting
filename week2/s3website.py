#!/usr/bin/env python3

import boto3
import json

s3Client = boto3.client('s3')

bucketName = "tway2-week2-bucket"
s3Client.create_bucket(Bucket=bucketName)

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

s3Client.put_bucket_policy(Bucket=bucketName, Policy=json.dumps(bucket_policy))

put_bucket_response = s3Client.put_bucket_website(Bucket=bucketName, WebsiteConfiguration={ 'ErrorDocument': {'Key': 'error.html'}, 'IndexDocument': {'Suffix': 'index.html'}, } )

with open("mybuckets.txt", "w") as bucketsFile:
    bucketsFile.write(json.dumps(put_bucket_response, indent=4))

with open("index.html", "rb") as indexFile:
    s3Client.put_object(Body=indexFile, Bucket=bucketName, Key="index.html", ContentType='text/html' )
with open("error.html", "rb") as errorFile:
    s3Client.put_object(Body=errorFile, Bucket=bucketName, Key="error.html", ContentType='text/html' )