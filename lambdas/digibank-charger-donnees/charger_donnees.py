import pymysql
import boto3
import json
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    obj = s3.get_object(
        Bucket=os.environ['BUCKET_NAME'],
        Key='data/transactions.json'
    )
    data = json.loads(obj['Body'].read())
    
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user='admin',
        password='DigiBankPass2026!',
        database='digibank',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cur:
            clients_inseres = 0
            for client_id, solde in data['clients'].items():
                cur.execute("""
                    INSERT INTO clients (id, nom, solde)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE solde=%s
                """, (client_id, f"Client {client_id}", solde, solde))
                clients_inseres += 1

            transactions = data['transactions']
            total = 0
            lot = []
            for tx in transactions:
                lot.append((
                    tx['client_id'], tx['type'],
                    tx['montant'], tx['solde_avant'],
                    tx['solde_apres'], tx['timestamp'],
                    tx['statut']
                ))
                if len(lot) == 1000:
                    cur.executemany("""
                        INSERT INTO transactions
                        (client_id, type, montant, solde_avant, solde_apres, timestamp, statut)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """, lot)
                    total += len(lot)
                    lot = []
            if lot:
                cur.executemany("""
                    INSERT INTO transactions
                    (client_id, type, montant, solde_avant, solde_apres, timestamp, statut)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, lot)
                total += len(lot)
        conn.commit()
        return {
            "statusCode": 200,
            "clients_inseres": clients_inseres,
            "transactions_inserees": total
        }
    finally:
        conn.close()
