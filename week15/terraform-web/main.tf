terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
        }
    }
    required_version = ">= 0.14.9"
}
provider "aws" {
    profile = "default"
    region = var.region
}
data "aws_availability_zones" "available" {
    state = "available"
}
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.2.0"

  name = "tway2-fall-2023-cloud-scripting-vpc"
  cidr = var.cidr
  azs = data.aws_availability_zones.available.names
  private_subnets = var.private_subnets
  public_subnets = var.public_subnets
  enable_nat_gateway = false
  enable_vpn_gateway = false
}
module "web-sg"{
  source = "terraform-aws-modules/security-group/aws//modules/http-80"
  version = "5.1.0"

  name        = "web-sg"
  description = "Security group for web-server with HTTP ports open within VPC"
  vpc_id      = module.vpc.vpc_id
  ingress_cidr_blocks = ["0.0.0.0/0"]
}
data "aws_ami" "web-server-ami" {
    filter{
        name = "name"
        values = ["amzn2-ami-hvm-*-x86_64-gp2"]
    }
    most_recent = true
    owners = ["amazon"]
}
module "web-server"{
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.5.0"

  name = "tighearnan-web-server"

  ami = data.aws_ami.web-server-ami.image_id
  instance_type          = "t2.micro"
  key_name               = "vockey"
  vpc_security_group_ids = [module.web-sg.security_group_id]
  subnet_id              = module.vpc.public_subnets[0]
  user_data = templatefile("${path.module}/init-script.sh", {file_content = "INSERT YOUR TIGHEARNAN AND WAY HERE"})
  associate_public_ip_address = true
}
output "web-server-ip" {
  value = module.web-server.public_ip
}