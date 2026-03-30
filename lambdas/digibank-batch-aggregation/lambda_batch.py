import boto3
import pymysql
import json
import os
from datetime import date, timedelta

def lambda_handler(event, context):
    hier = (date.today() - timedelta(days=1)).isoformat()
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user='admin',
        password='DigiBankPass2026!',
        database='digibank',
        cursorclass=pymysql.cursors.DictCursor
    )
    s3 = boto3.client('s3')
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT client_id, type,
                    COUNT(*) as nb_transactions,
                    SUM(montant) as total_montant,
                    AVG(montant) as montant_moyen,
                    MIN(montant) as montant_min,
                    MAX(montant) as montant_max,
                    DATE(timestamp) as date_transaction
                FROM transactions
                WHERE DATE(timestamp) = %s
                GROUP BY client_id, type, DATE(timestamp)
            """, (hier,))
            rows = cur.fetchall()
        cle = f"aggregations/{hier}/resume_journalier.json"
        s3.put_object(
            Bucket=os.environ['BUCKET_NAME'],
            Key=cle,
            Body=json.dumps(rows, default=str),
            ContentType='application/json'
        )
        print(f"Agrégation {hier} : {len(rows)} lignes sauvegardées")
        return {"statusCode": 200, "lignes_traitees": len(rows)}
    finally:
        conn.close()
