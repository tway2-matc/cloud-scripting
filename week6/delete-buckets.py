#!/usr/bin/env python3

import boto3

s3Client = boto3.client("s3")
buckets = s3Client.list_buckets()

for bucket in buckets["Buckets"]:
    objects = s3Client.list_objects_v2(Bucket=str(bucket["Name"]))
    for object in objects["Contents"]:
        s3Client.delete_object(Bucket=bucket["Name"], Key=object["Key"])
    s3Client.delete_bucket(Bucket=bucket["Name"])
    
