-- Requête 1 : Volume par jour
SELECT transaction_date, COUNT(*) as nb_transactions, SUM(montant) as volume_total
FROM transactions_analytics
GROUP BY transaction_date ORDER BY transaction_date DESC LIMIT 30;

-- Requête 2 : Top 10 clients
SELECT client_id, COUNT(*) as nb_transactions,
       SUM(montant) as montant_total, AVG(montant) as montant_moyen
FROM transactions_analytics WHERE type='DEBIT'
GROUP BY client_id ORDER BY montant_total DESC LIMIT 10;

-- Requête 3 : Taux de fraude
SELECT type, COUNT(*) as total,
       SUM(CASE WHEN statut='FRAUDE' THEN 1 ELSE 0 END) as nb_fraudes,
       ROUND(100.0*SUM(CASE WHEN statut='FRAUDE' THEN 1 ELSE 0 END)/COUNT(*),2) as taux_pct
FROM transactions_analytics GROUP BY type ORDER BY taux_pct DESC;

-- Requête 4 : Montant moyen par type
SELECT type, COUNT(*) as nb, AVG(montant) as moy,
       MIN(montant) as min_montant, MAX(montant) as max_montant
FROM transactions_analytics GROUP BY type;

-- Requête 5 : Evolution hebdomadaire
SELECT DATE_TRUNC('week', transaction_date) as semaine,
       AVG(solde_apres) as solde_moyen,
       SUM(CASE WHEN type='CREDIT' THEN montant ELSE 0 END) as credits,
       SUM(CASE WHEN type='DEBIT' THEN montant ELSE 0 END) as debits
FROM transactions_analytics
GROUP BY DATE_TRUNC('week', transaction_date)
ORDER BY semaine DESC LIMIT 8;
