#!/bin/bash
sudo yum update -y
sudo yum install httpd -y
sudo systemctl enable httpd
sudo systemctl start httpd
echo "TIGHEARNAN - Week 15 complete!" > /var/www/html/index.html