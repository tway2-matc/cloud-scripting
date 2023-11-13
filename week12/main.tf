terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 3.27"
        }
    }
    required_version = ">= 0.14.9"
    cloud {
        organization = "python-scripting-for-cloud"
        workspaces {
            name = "tighearnan-workspace"
        }
    }
}
provider "aws" {
    profile = "default"
    region = "us-east-1"
}
data "aws_iam_role" "lab_role" {
    name = "LabRole"
}
resource "aws_lambda_function" "test_lambda"{
    filename = "stopEC2.zip"
    function_name = "tighearnan_lambda_function"
    role = data.aws_iam_role.lab_role.arn
    runtime = "python3.9"
    handler = "stopEC2.lambda_handler"
}

resource "aws_lambda_function" "start_ec2_lambda"{
    filename = "startEC2/startEC2.zip"
    function_name = "tighearnan_lambda_function_2"
    role = data.aws_iam_role.lab_role.arn
    runtime = "python3.9"
    handler = "startEC2.lambda_handler"
}
