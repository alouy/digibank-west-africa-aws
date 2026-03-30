import boto3
import json
import os

def lambda_handler(event, context):
    client = boto3.client('redshift-data', region_name='eu-north-1')
    
    cluster_id = 'digibank-redshift'
    database = 'dev'
    db_user = 'adminredshift'
    
    # Créer la table analytics
    create_table = """
    CREATE TABLE IF NOT EXISTS transactions_analytics (
        client_id VARCHAR(50),
        type VARCHAR(20),
        montant DECIMAL(15,2),
        solde_avant DECIMAL(15,2),
        solde_apres DECIMAL(15,2),
        transaction_date DATE,
        statut VARCHAR(20)
    );
    """
    
    # 5 requêtes analytiques
    requetes = {
        "1_volume_par_jour": """
            SELECT transaction_date,
                   COUNT(*) as nb_transactions,
                   SUM(montant) as volume_total
            FROM transactions_analytics
            GROUP BY transaction_date
            ORDER BY transaction_date DESC
            LIMIT 30;
        """,
        "2_top10_clients": """
            SELECT client_id,
                   COUNT(*) as nb_transactions,
                   SUM(montant) as montant_total,
                   AVG(montant) as montant_moyen
            FROM transactions_analytics
            WHERE type = 'DEBIT'
            GROUP BY client_id
            ORDER BY montant_total DESC
            LIMIT 10;
        """,
        "3_taux_fraude": """
            SELECT type,
                   COUNT(*) as total,
                   SUM(CASE WHEN statut='FRAUDE' THEN 1 ELSE 0 END) as nb_fraudes,
                   ROUND(100.0 * SUM(CASE WHEN statut='FRAUDE' THEN 1 ELSE 0 END) / COUNT(*), 2) as taux_fraude_pct
            FROM transactions_analytics
            GROUP BY type
            ORDER BY taux_fraude_pct DESC;
        """,
        "4_montant_moyen_type": """
            SELECT type,
                   COUNT(*) as nb_transactions,
                   AVG(montant) as montant_moyen,
                   MIN(montant) as montant_min,
                   MAX(montant) as montant_max
            FROM transactions_analytics
            GROUP BY type;
        """,
        "5_evolution_hebdomadaire": """
            SELECT DATE_TRUNC('week', transaction_date) as semaine,
                   AVG(solde_apres) as solde_moyen,
                   SUM(CASE WHEN type='CREDIT' THEN montant ELSE 0 END) as total_credits,
                   SUM(CASE WHEN type='DEBIT' THEN montant ELSE 0 END) as total_debits
            FROM transactions_analytics
            GROUP BY DATE_TRUNC('week', transaction_date)
            ORDER BY semaine DESC
            LIMIT 8;
        """
    }
    
    resultats = {}
    
    # Créer la table
    try:
        resp = client.execute_statement(
            ClusterIdentifier=cluster_id,
            Database=database,
            DbUser=db_user,
            Sql=create_table
        )
        resultats['table_creee'] = resp['Id']
    except Exception as e:
        resultats['erreur_creation'] = str(e)
    
    # Exécuter chaque requête
    for nom, sql in requetes.items():
        try:
            resp = client.execute_statement(
                ClusterIdentifier=cluster_id,
                Database=database,
                DbUser=db_user,
                Sql=sql
            )
            resultats[nom] = {'statement_id': resp['Id'], 'statut': 'execute'}
        except Exception as e:
            resultats[nom] = {'erreur': str(e)}
    
    return {"statusCode": 200, "resultats": resultats}
