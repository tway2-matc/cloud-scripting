#!/usr/bin/env python3
import boto3
import datetime
import pytz

#creates iam client
iamClient = boto3.client("iam")
#gets a list of all the iam roles
iamRoles = iamClient.list_roles()["Roles"]
#creates a list that contains all of the roles created in the last 90 days
recentIamRoles = []
for role in iamRoles:
    if role["CreateDate"] > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
        recentIamRoles.append(role)

#loops through the roles and prints out their policies
for role in recentIamRoles:
    #prints the role and creation date
    print(f"Role {role['RoleName']} - Created {role['CreateDate']}")
    #prints the unmanaged policies
    try:
        policies = iamClient.list_role_policies(RoleName=role["RoleName"])["PolicyNames"]
        for policy in policies:
            print(f" - unmanaged policy: {policy}")
    except:
        print("[permissions needed to view unmanaged policies]")
    #prints the managed policies
    try:
        policies = iamClient.list_attached_role_policies(RoleName=role["RoleName"])["AttachedPolicies"]
        for policy in policies:
            print(f" - managed policy:   {policy['PolicyName']}")
    except:
        print("[permissions needed to view managed policies]")
    print()
