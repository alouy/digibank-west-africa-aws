import pymysql
import json
import os

def lambda_handler(event, context):
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user='admin',
        password='DigiBankPass2026!',
        database='digibank',
        connect_timeout=10
    )
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id VARCHAR(50) PRIMARY KEY,
                    nom VARCHAR(100),
                    solde DECIMAL(15,2) DEFAULT 0.00,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    client_id VARCHAR(50) NOT NULL,
                    type VARCHAR(20) NOT NULL,
                    montant DECIMAL(15,2) NOT NULL,
                    solde_avant DECIMAL(15,2),
                    solde_apres DECIMAL(15,2),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    statut VARCHAR(20) DEFAULT 'COMPLETED',
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            """)
            cur.execute("SHOW TABLES")
            tables = [t[0] for t in cur.fetchall()]
        conn.commit()
        return {"statusCode": 200, "tables": tables, "message": "Tables créées !"}
    finally:
        conn.close()
