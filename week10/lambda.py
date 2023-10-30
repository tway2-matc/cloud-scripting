#!/usr/bin/env python3

import boto3

iamClient = boto3.client('iam')
lamClient = boto3.client('lambda')

def main():
    functionName = "start_ec2"
    if not Function_Exists(functionName):
        Create_Lambda(functionName)
    Invoke_Lambda(functionName)

def Create_Lambda(function):
    labRole = iamClient.get_role(RoleName="LabRole")
    with open("lambda_start_function.zip","rb") as codeZip:

        lamClient.create_function(FunctionName = function,
                                  Role = labRole['Role']['Arn'],
                                  Publish = True,
                                  PackageType = 'Zip',
                                  Runtime = 'python3.9',
                                  Code = { 'ZipFile': codeZip.read() },
                                  Handler = 'lambda_start_function.lambda_handler')

def Function_Exists(functionName):
    functionList = lamClient.list_functions()["Functions"]
    for function in functionList:
        if function["FunctionName"] == functionName:
            return True
    return False

def Invoke_Lambda(function):
    return lamClient.invoke(FunctionName=function)

if __name__ == "__main__":
    main()