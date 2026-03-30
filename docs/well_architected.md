# Well-Architected Framework — DigiBank West Africa

## Pilier 1 — Excellence Operationnelle
- CloudTrail multi-region actif (IsLogging: True)
- CloudWatch Dashboard unifie : DigiBank-Dashboard (5 widgets)
- 5 alarmes proactives configurees
- Lambda batch automatisee cron(0 2 * * ? *)
- EventBridge planifie : 02h00 UTC chaque nuit

## Pilier 2 — Securite
- IAM 4 groupes : Admins, DevOps, Analysts, ReadOnly
- MFA active sur compte root
- Chiffrement S3 SSE-AES256
- Chiffrement RDS KMS at-rest
- EBS gp3 20GB chiffre
- Security Groups least-privilege (ALB:80/443, EC2:5000, RDS:3306, Redshift:5439)

## Pilier 3 — Fiabilite
- Auto Scaling Group min:1 max:3 CPU cible:60%
- Multi-AZ VPC : eu-north-1a + eu-north-1b
- ALB Health Checks /health toutes 30 secondes
- Aurora backups automatiques retention 1 jour
- DynamoDB TTL sessions 1 heure

## Pilier 4 — Performance
- EC2 t3.micro Target Tracking CPU 60%
- Aurora MySQL OLTP optimise
- DynamoDB PAY_PER_REQUEST latence milliseconde
- Redshift ra3.xlplus OLAP analytics 5 requetes

## Pilier 5 — Optimisation des Couts
- AWS : $268.62/mois vs On-Premise : $1 600/mois
- Economies : 83.2% soit $15 977/an
- Plan : NAT GW pause + Redshift schedule + Reserved Instances

## 3 Risques et Mitigations
1. Aurora Single-AZ (CRITIQUE) -> Upgrade Multi-AZ en production
2. Absence WAF -> Deployer AWS WAF sur ALB
3. Pas de backup cross-region -> S3 Cross-Region Replication
