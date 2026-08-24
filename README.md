# Jensen IOT Laboration
Detta repository innehåller ett REST-API för IoT-sensorer som hanterar enheters status och mätdatan. Systemet tar emot simulerad data från tre sensorer som alla skickar temperatur, luftfuktighet och batterinivå. All data valideras och lagras i PostgrieSQL med Redis som agerar cache för den senast gjorda mätningen. Allt körs lokalt med hjälp av Docker Compose och kvalitetssäkras med pytest och en CI-pipeline via GitHub Actions.

## Vad som behövs

  - Docker Desktop
  - Kubectl
  - Minikube 

## Hur allt körs

  - Starta miljön med 'docker compose up --build -d'
  - Verifiera att allt körs med 'docker compose ps'

För tester:

- 'docker compose exec api pytest'


## SQL Queries

SELECT COUNT(*) FROM measurements;

- Räknar (COUNT(*)) alla resultat från (FROM) tabellen (measurements) och ger antalet


SELECT AVG(temperature) FROM measurements:

- Tar alla temperaturmätningar från measurements-tabellen och ger medelvärdet 


SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';

- visar allt från measurements som skapats mellan nu och angivna intervallet 
