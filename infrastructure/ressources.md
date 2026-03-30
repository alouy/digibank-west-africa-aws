# Ressources AWS — DigiBank West Africa

## Endpoints
- **API ALB** : http://digibank-alb-1985318916.eu-north-1.elb.amazonaws.com
- **Aurora** : digibank-aurora.cluster-c5m2owwwikua.eu-north-1.rds.amazonaws.com
- **Redshift** : digibank-redshift.crs3k2rakdhw.eu-north-1.redshift.amazonaws.com

## IDs AWS
- **VPC** : vpc-09c5a24abb9ff36d0
- **S3** : digibank-transactions-1774659318
- **Région** : eu-north-1 (Stockholm)

## EC2
- **Instance** : i-005f69903bfd5ae57
- **Type** : t3.micro
- **IP privée** : 10.0.11.225
- **AZ** : eu-north-1b

## Security Groups
- SG-ALB : sg-0e88373163a310ca8
- SG-EC2 : sg-0586e88806f145829
- SG-RDS : sg-04a5b578c701d231c
- SG-Redshift : sg-0ebe63975b7069dfb

## Sous-réseaux
- PUB_1A : subnet-04e35cf59fde91438 (10.0.1.0/24)
- PUB_1B : subnet-01287c7b09a94662c (10.0.2.0/24)
- PRIV_1A : subnet-0c3b3ce7cffaaa403 (10.0.10.0/24)
- PRIV_1B : subnet-0807b868079bda4c3 (10.0.11.0/24)
- DATA_1A : subnet-016cb095dd7797c10 (10.0.20.0/24)
- DATA_1B : subnet-0d1b602f3f2ff8db8 (10.0.21.0/24)
