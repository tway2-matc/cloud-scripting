#!/usr/bin/env python3
import boto3

def CreateSNSTopic(name):
    snsClient = boto3.client("sns")
    response = snsClient.create_topic(Name=name)
    return response["TopicArn"]

def SubscribeEmail(arn, email):
    snsClient = boto3.client("sns")
    response = snsClient.subscribe(TopicArn=arn, Protocol='email',Endpoint=email)
    return response["SubscriptionArn"]