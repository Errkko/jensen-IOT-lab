## SQL Queries

SELECT COUNT(*) FROM measurements;

- Räknar (COUNT(*)) alla resultat från (FROM) tabellen (measurements) och ger antalet


SELECT AVG(temperature) FROM measurements:

- Tar alla temperaturmätningar från measurements-tabellen och ger medelvärdet 


SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';

- visar allt från measurements som skapats mellan nu och angivna intervallet 