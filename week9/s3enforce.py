#!/usr/bin/env python3

import boto3

def CreateBucket(bucketName):
    s3Client = boto3.client('s3')
    toReturn = s3Client.create_bucket(Bucket=bucketName)
    #s3Client.delete_public_access_block(Bucket=bucketName)
    return toReturn

def DeleteBucket(bucketName):
    s3Client = boto3.client('s3')
    return s3Client.delete_bucket(Bucket=bucketName)

def EnforceVersioning(bucketName):
    s3Client = boto3.client('s3')
    return s3Client.put_bucket_versioning(Bucket=bucketName, VersioningConfiguration = {
        "MFADelete" : "Disabled",
        "Status" : "Enabled"
    })

def SetBucketPolicy(bucketName, policyString):
    s3Client = boto3.client('s3')
    return s3Client.put_bucket_policy(Bucket=bucketName,Policy=policyString)

def main():
    bucketName = "tway-10-16-2023"
    CreateBucket(bucketName)
    EnforceVersioning(bucketName)

if __name__ == "__main__":
    main()