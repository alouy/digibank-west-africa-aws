#!/bin/bash
# DigiBank West Africa — Setup VPC
# Région : eu-north-1

VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --query 'Vpc.VpcId' --output text)
aws ec2 create-tags --resources $VPC_ID \
  --tags Key=Name,Value=digibank-vpc
echo "VPC créé : $VPC_ID"
