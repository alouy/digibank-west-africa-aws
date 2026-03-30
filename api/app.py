from flask import Flask, request, jsonify
import pymysql
import os
from datetime import date

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user='admin',
        password=os.environ.get('DB_PASS'),
        database='digibank',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "DigiBank API"})

@app.route('/transaction', methods=['POST'])
def post_transaction():
    data = request.get_json()
    if not all(k in data for k in ['client_id','type','montant']):
        return jsonify({"error": "Champs manquants"}), 400
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT solde FROM clients WHERE id=%s", (data['client_id'],))
            client = cur.fetchone()
            solde_avant = float(client['solde']) if client else 0.0
            if data['type'] == 'DEBIT' and solde_avant < data['montant']:
                return jsonify({"error": "Solde insuffisant"}), 400
            solde_apres = solde_avant + data['montant'] if data['type'] == 'CREDIT' else solde_avant - data['montant']
            cur.execute(
                "INSERT INTO transactions (client_id, type, montant, solde_avant, solde_apres) VALUES (%s,%s,%s,%s,%s)",
                (data['client_id'], data['type'], data['montant'], solde_avant, solde_apres)
            )
            cur.execute(
                "INSERT INTO clients (id, solde) VALUES (%s,%s) ON DUPLICATE KEY UPDATE solde=%s",
                (data['client_id'], solde_apres, solde_apres)
            )
        conn.commit()
        return jsonify({"message": "Transaction enregistrée", "solde_apres": solde_apres}), 201
    finally:
        conn.close()

@app.route('/client/<client_id>/solde')
def get_solde(client_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT solde FROM clients WHERE id=%s", (client_id,))
            client = cur.fetchone()
            if not client:
                return jsonify({"error": "Client non trouvé"}), 404
            return jsonify({"client_id": client_id, "solde": float(client['solde'])})
    finally:
        conn.close()

@app.route('/stats/journalier')
def stats_journalier():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) as total_transactions,
                    SUM(CASE WHEN type='CREDIT' THEN montant ELSE 0 END) as total_credits,
                    SUM(CASE WHEN type='DEBIT' THEN montant ELSE 0 END) as total_debits,
                    AVG(montant) as montant_moyen,
                    COUNT(DISTINCT client_id) as clients_actifs
                FROM transactions WHERE DATE(timestamp)=%s
            """, (date.today().isoformat(),))
            stats = cur.fetchone()
            return jsonify({"date": date.today().isoformat(),
                "stats": {k: float(v) if v else 0 for k,v in stats.items()}})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
