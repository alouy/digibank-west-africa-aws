#!/bin/bash
# DigiBank West Africa — Setup CloudWatch 5 alarmes

aws cloudwatch put-metric-alarm \
  --alarm-name "DigiBank-CPU-Eleve" \
  --metric-name CPUUtilization --namespace AWS/EC2 \
  --statistic Average --period 300 --threshold 80 \
  --comparison-operator GreaterThanThreshold --evaluation-periods 2

aws cloudwatch put-metric-alarm \
  --alarm-name "DigiBank-Aurora-Connexions" \
  --metric-name DatabaseConnections --namespace AWS/RDS \
  --dimensions Name=DBClusterIdentifier,Value=digibank-aurora \
  --statistic Average --period 60 --threshold 100 \
  --comparison-operator GreaterThanThreshold --evaluation-periods 1

aws cloudwatch put-metric-alarm \
  --alarm-name "DigiBank-Lambda-Erreurs" \
  --metric-name Errors --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=digibank-batch-aggregation \
  --statistic Sum --period 60 --threshold 5 \
  --comparison-operator GreaterThanThreshold --evaluation-periods 1

aws cloudwatch put-metric-alarm \
  --alarm-name "DigiBank-ALB-Erreurs-5XX" \
  --metric-name HTTPCode_ELB_5XX_Count \
  --namespace AWS/ApplicationELB \
  --statistic Sum --period 60 --threshold 10 \
  --comparison-operator GreaterThanThreshold --evaluation-periods 1

aws cloudwatch put-metric-alarm \
  --alarm-name "DigiBank-S3-Requetes" \
  --metric-name NumberOfObjects --namespace AWS/S3 \
  --statistic Average --period 86400 --threshold 10000 \
  --comparison-operator GreaterThanThreshold --evaluation-periods 1

echo "5 alarmes CloudWatch configurees !"
