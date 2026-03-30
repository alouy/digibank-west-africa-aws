# 🏦 DigiBank West Africa — Architecture Haute Disponibilité AWS

## Projet P-07 — AWS Academy Cloud Foundations
**ISI Dakar | 2025-2026 | Aloyse Faye | M. LAM Baye Sabarane**

## Contexte
Banque digitale fictive traitant 500 000+ transactions/jour au Sénégal, Côte d'Ivoire et Ghana.

## Architecture AWS
- **Région** : eu-north-1 (Stockholm)
- **VPC** : 10.0.0.0/16 — 6 sous-réseaux sur 2 AZ
- **Compute** : EC2 Auto Scaling Group (min:1, max:3, CPU:60%)
- **API** : Flask — POST /transaction, GET /client/{id}/solde, GET /stats/journalier
- **Bases de données** : Aurora MySQL + DynamoDB + Redshift
- **Stockage** : S3 + lifecycle + EBS gp3 20GB
- **Sécurité** : IAM 4 groupes + MFA + CloudTrail + Chiffrement KMS/AES256
- **Monitoring** : CloudWatch Dashboard + 5 alarmes

## Dataset
PaySim — Synthetic Financial Datasets For Fraud Detection (Kaggle)
- 100 000 transactions chargées
- 116 fraudes détectées ($62.8M)

## TCO
| Infrastructure | Coût mensuel |
|---|---|
| AWS Cloud | $268.62 |
| On-Premise | $1 600.00 |
| **Économies** | **83.2%** |

## Services AWS utilisés
M2 · M4 · M5 · M6 · M7 · M8 · M9 · M10

## Structure du projet
```
digibank-west-africa-aws/
├── api/
│   └── app.py              # API Flask
├── lambda/
│   ├── batch_aggregation.py
│   ├── redshift_analytics.py
│   └── charger_donnees.py
├── infrastructure/
│   ├── setup_vpc.sh
│   ├── setup_security.sh
│   └── setup_monitoring.sh
├── docs/
│   ├── architecture.png
│   └── well_architected.md
└── README.md
```
