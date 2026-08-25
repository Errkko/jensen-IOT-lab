# Jensen IOT Laboration
Detta repository innehåller ett REST-API för IoT-sensorer som hanterar enheters status och mätdatan. Systemet tar emot simulerad data från tre sensorer som alla skickar temperatur, luftfuktighet och batterinivå. All data valideras och lagras i PostgrieSQL med Redis som agerar cache för den senast gjorda mätningen. Allt körs lokalt med hjälp av Docker Compose och kvalitetssäkras med pytest och en CI-pipeline via GitHub Actions.

## Vad som behövs
  - Docker Desktop
  - Kubectl
  - Minikube 

## Hur allt körs
  - Starta miljön med `docker compose up --build -d`
  - Verifiera att allt körs med `docker compose ps` och att databasen ska visa `healthy`. Om inte så vänta några sekunder och kör kommandot igen.
  - Följ simulatorn med `docker compose logs -f simulator`.
  - Stoppa miljön med `docker compose down`
  - 
## Kontrollera API:t
Kör dessa i en webbläsare för att se till att du får svar, eller lägg till `curl -i` före om du kör från en terminal (`i` bara där för om du vill se statuskoderna som ges):

    - http://localhost:5001 -> enkel startsida
    - http://localhost:5001/health -> ska visa "status": "ok"
    - http://localhost:5001/devices -> ska visa tre sensorer
    - http://localhost:5001/measurements -> ska lista alla mätningar
    - http://localhost:5001/devices/<senosr_id>/latest -> senast gjorda mätningen från vald sensor
    - http://localhost:5001/devices/<senosr_id>/measurements -> alla mätningar från vald sensor
    - http://localhost:5001/statistics -> för att se medeltemperatur, antal mätningar och antal senosrer.

För tester:
- `docker compose exec api pytest`

## Begränsningar
Kubernetes demon täcker endast API-tjänsten och `/` samt `/health` endpointsen. Både databasen och redis-cachen körs i docker compose-miljön och tar därför inte nytta av distribueringen som kubernets tillför.

## SQL Queries
SELECT COUNT(*) FROM measurements;

- Räknar (`COUNT(*)`) alla resultat från (`FROM`) tabellen (`/measurements`) och ger antalet


SELECT AVG(temperature) FROM measurements:

- Tar alla temperaturmätningar från measurements-tabellen och ger medelvärdet 


SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';

- Visar allt från measurements som skapats mellan nu och angivna intervallet 
