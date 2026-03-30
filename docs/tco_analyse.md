# Analyse TCO — DigiBank West Africa

## Couts AWS mensuels
| Service | Configuration | Cout/mois |
|---|---|---|
| EC2 t3.micro | ASG min:1 max:3 CPU:60% | $8.50 |
| Aurora MySQL | db.t3.medium Single-AZ | $25.00 |
| DynamoDB | PAY_PER_REQUEST | $0.00 |
| S3 | 490MB + lifecycle | $0.12 |
| Lambda | 5 fonctions Python 3.11 | $0.00 |
| NAT Gateway | 730h + 10GB | $32.00 |
| ALB | 730h + 1 LCU | $18.00 |
| Redshift | ra3.xlplus Single node | $180.00 |
| CloudTrail | Multi-region | $2.00 |
| CloudWatch | Dashboard + 5 alarmes | $3.00 |
| **TOTAL AWS** | | **$268.62/mois** |

## Couts On-Premise equivalents
| Composant | Cout/mois |
|---|---|
| Serveur physique | $300.00 |
| Reseau + firewall | $150.00 |
| Electricite | $200.00 |
| Administration systeme | $500.00 |
| Licences logicielles | $200.00 |
| Maintenance | $100.00 |
| Datacenter | $150.00 |
| **TOTAL** | **$1 600.00/mois** |

## ROI
- Economies mensuelles : $1 331/mois
- Economies annuelles : $15 977/an
- Reduction des couts : **83.2%**

## Plan optimisation 12 mois
- M1-M3 : Supprimer NAT Gateway hors prod (-$32/mois)
- M3-M6 : Redshift pause nuit/weekend (-$90/mois)
- M6-M9 : Reserved Instances EC2 (-$3.40/mois)
- M9-M12 : S3 Intelligent-Tiering
