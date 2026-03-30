import pymysql
import os
from datetime import datetime
from decimal import Decimal

def convertir(obj):
    if isinstance(obj, datetime):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)

def nettoyer(data):
    if isinstance(data, list):
        return [nettoyer(i) for i in data]
    if isinstance(data, dict):
        return {k: nettoyer(v) for k, v in data.items()}
    return convertir(data) if isinstance(data, (datetime, Decimal)) else data

def lambda_handler(event, context):
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user='admin',
        password='DigiBankPass2026!',
        database='digibank',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        resultats = {}
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM clients")
            resultats['total_clients'] = cur.fetchone()['total']
            cur.execute("SELECT COUNT(*) as total FROM transactions")
            resultats['total_transactions'] = cur.fetchone()['total']
            cur.execute("SELECT * FROM transactions LIMIT 5")
            resultats['exemples_transactions'] = nettoyer(cur.fetchall())
            cur.execute("""
                SELECT type, COUNT(*) as nb,
                       SUM(montant) as total_montant,
                       AVG(montant) as montant_moyen
                FROM transactions GROUP BY type
            """)
            resultats['stats_par_type'] = nettoyer(cur.fetchall())
            cur.execute("""
                SELECT statut, COUNT(*) as nb, SUM(montant) as montant_total
                FROM transactions GROUP BY statut ORDER BY nb DESC
            """)
            resultats['stats_fraudes'] = nettoyer(cur.fetchall())
            cur.execute("SELECT id, solde FROM clients ORDER BY solde DESC LIMIT 5")
            resultats['top5_clients'] = nettoyer(cur.fetchall())
            cur.execute("""
                SELECT client_id, montant, timestamp
                FROM transactions WHERE statut='FRAUDE' LIMIT 5
            """)
            resultats['exemples_fraudes'] = nettoyer(cur.fetchall())
        return {"statusCode": 200, "resultats": resultats}
    finally:
        conn.close()
