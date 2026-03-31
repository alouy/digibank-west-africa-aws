# 🏦 DigiBank West Africa — Architecture Haute Disponibilité AWS

> **Projet P-07 — AWS Academy Cloud Foundations**
> ISI Dakar | 2025-2026 | **Aloyse Faye** | Superviseur : M. LAM Baye Sabarane

---

## 📋 Contexte
Banque digitale fictive traitant **500 000+ transactions/jour** au Sénégal, Côte d'Ivoire et Ghana.

## 🏗️ Architecture AWS
| Service | Configuration | Module |
|---|---|---|
| VPC | 10.0.0.0/16 — 6 sous-réseaux — 2 AZ | M5 |
| EC2 Auto Scaling | t3.micro — min:1 max:3 CPU:60% | M6 |
| ALB | Application Load Balancer internet-facing | M10 |
| Aurora MySQL | db.t3.medium — Single-AZ — KMS chiffré | M8 |
| DynamoDB | Sessions TTL 1h — PAY_PER_REQUEST | M8 |
| Redshift | ra3.xlplus — 5 requêtes analytiques | M8 |
| S3 | Lifecycle Standard→IA→Glacier — SSE-AES256 | M7 |
| Lambda | 5 fonctions Python 3.11 — batch 02h00 UTC | M6 |
| CloudWatch | Dashboard unifié — 5 alarmes actives | M10 |
| CloudTrail | Multi-région — Logs → S3 | M4 |
| IAM | 4 groupes — Politiques least-privilege — MFA | M4 |
| EBS | gp3 20GB chiffré attaché EC2 | M7 |

## 🌐 Endpoints
```
API ALB  : http://digibank-alb-1985318916.eu-north-1.elb.amazonaws.com
Aurora   : digibank-aurora.cluster-c5m2owwwikua.eu-north-1.rds.amazonaws.com
Redshift : digibank-redshift.crs3k2rakdhw.eu-north-1.redshift.amazonaws.com
```

## 🖼️ Diagramme Architecture
![Architecture AWS](docs/architecture_aws.png)

## 📊 Dataset PaySim
- Source : [Kaggle — Synthetic Financial Datasets For Fraud Detection](https://www.kaggle.com/datasets/ealaxi/paysim1)
- **6.3 millions** de lignes disponibles
- **100 000** transactions chargées dans Aurora MySQL
- **116 fraudes** détectées ($62.8M)

## 🔌 API Flask — 3 Endpoints
```bash
# Health check
GET  /health
→ {"status": "healthy", "service": "DigiBank API"}

# Enregistrer une transaction
POST /transaction
Body: {"client_id": "C1231006815", "type": "CREDIT", "montant": 5000}
→ {"message": "Transaction enregistree", "solde_apres": 5000}

# Consulter le solde
GET  /client/{client_id}/solde
→ {"client_id": "C1231006815", "solde": 34008736.98}

# Statistiques journalières
GET  /stats/journalier
→ {"date": "2026-03-31", "stats": {...}}
```

## 🧪 Tester avec Postman
1. Ouvrir Postman
2. **Import** → glisser-déposer `docs/postman_collection.json`
3. La variable `BASE_URL` est déjà configurée
4. Lancer les 9 requêtes dans l'ordre

| # | Requête | Méthode | Description |
|---|---|---|---|
| 1 | /health | GET | Santé de l'API |
| 2 | /transaction CREDIT | POST | Créditer un client |
| 3 | /transaction DEBIT | POST | Débiter un client |
| 4 | /transaction FRAUDE | POST | Client frauduleux PaySim |
| 5 | /client/{id}/solde | GET | Consulter le solde |
| 6 | /client/top1/solde | GET | Client le plus riche ($34M) |
| 7 | /stats/journalier | GET | Stats du jour |
| 8 | /client/inexistant | GET | Test erreur 404 |
| 9 | /transaction insuffisant | POST | Test erreur 400 |

## 💰 Analyse TCO
| Infrastructure | Coût mensuel | Coût annuel |
|---|---|---|
| **AWS Cloud** | **$268.62** | **$3 223** |
| On-Premise | $1 600.00 | $19 200 |
| **Économies** | **$1 331/mois** | **$15 977/an** |
| **Réduction** | **83.2%** | |

## 🔒 Sécurité
- ✅ IAM 4 groupes avec politiques least-privilege
- ✅ MFA activé sur compte root
- ✅ Chiffrement S3 SSE-AES256
- ✅ Chiffrement RDS KMS at-rest
- ✅ CloudTrail multi-région actif
- ✅ Security Groups : ALB(80/443) → EC2(5000) → RDS(3306)
- ✅ Aucun credential hardcodé dans le code

## 📈 Well-Architected Framework
| Pilier | Score | Action prioritaire |
|---|---|---|
| Excellence Opérationnelle | ★★★★☆ | CI/CD pipeline |
| Sécurité | ★★★★☆ | AWS WAF + Secrets Manager |
| Fiabilité | ★★★☆☆ | Aurora Multi-AZ (CRITIQUE) |
| Performance | ★★★★☆ | Provisioned Concurrency Lambda |
| Optimisation Coûts | ★★★☆☆ | Redshift pause + Reserved Instances |

## 📁 Structure du projet
```
digibank-west-africa-aws/
├── api/
│   ├── app.py                         # API Flask 3 endpoints
│   └── requirements.txt               # Dépendances Python
├── lambdas/
│   ├── digibank-batch-aggregation/    # Agrégation quotidienne Aurora→S3
│   ├── digibank-charger-donnees/      # Chargement PaySim dans Aurora
│   ├── digibank-redshift-analytics/   # 5 requêtes analytiques Redshift
│   ├── digibank-init-db/              # Initialisation tables Aurora
│   └── digibank-verif-db/             # Vérification données
├── database/
│   ├── init_schema.sql                # Schema Aurora MySQL
│   └── redshift/
│       └── requetes_analytiques.sql   # 5 requêtes analytiques
├── infrastructure/
│   ├── deploy_complet.sh              # Script déploiement VPC complet
│   ├── setup_monitoring.sh            # 5 alarmes CloudWatch
│   └── ressources.md                  # IDs ressources AWS déployées
├── docs/
│   ├── architecture_aws.png           # Diagramme architecture complet
│   ├── DigiBank_Soutenance.pptx       # Slides soutenance 10 slides
│   ├── WellArchitected_DigiBank.docx  # Rapport Well-Architected 5 piliers
│   ├── postman_collection.json        # Collection Postman 9 requêtes
│   ├── tco_analyse.md                 # Analyse TCO détaillée
│   └── well_architected.md            # Résumé Well-Architected
└── README.md
```

## 🚀 Déploiement
Région AWS : `eu-north-1` (Stockholm)
2 Availability Zones : `eu-north-1a` · `eu-north-1b`

## 📚 Ressources
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected)
- [Dataset PaySim Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)
- [AWS Academy Cloud Foundations](https://aws.amazon.com/training/awsacademy/)
