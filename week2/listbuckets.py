#!/usr/bin/env python3

import boto3
import json

s3Client = boto3.client('s3')
buckets = s3Client.list_buckets()
bucketsFile = open("mybuckets.txt", "w")
for bucket in buckets["Buckets"]:
    print(bucket["Name"])
    bucketsFile.write(bucket["Name"])
    objects = s3Client.list_objects(Bucket=bucket["Name"])
    for item in objects["Contents"]:
        print(f"     {item['Key']}")
        bucketsFile.write(f"     {item['Key']}")

bucketsFile.close()
