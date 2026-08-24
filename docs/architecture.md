# Arkitekturdiagram

<img width="3408" height="1768" alt="image" src="/docs/iot-diagram.png" />

## Beskrivning

### Lokal Miljö
Detta är det kompletta flödet där de tre sensorerna skickar sin simulerade mätdata samtidigt som användaren hämtar status och statistik via REST API:t. Med hjälp av caching så läses och skrivs mätvärden till Redis för en snabbare åtkomst medans resterande historik sparas i PostgreSQL.

### Kubernetes Demo
Visar skalning och tillgänglighet i Minikube. Trafik mot `/` och `health` går genom en kubernetes service som distribuerar anrop över tre pods.

### CI Pipeline
De automatiserade testerna som sker vid varje push/pull och körs av Github Actions. Här körs testerna och docker imagen byggs för att säkerställa att trasig kod flaggas.

## Arkitekturval

### Redis Cache
Detta avlastar databasen vid anrop på senaste mätvärden, medan PostgreSQL fortfarande kan agera som databas och backup ifall Redis kraschar.

### Kubernetes Self-Healing
Om en pod slutar fungerar tar self-healing över och startar en ny pod utan att systemets funktion påverkas, då det fördelar lasten automatiskt mellan de pods som är aktiva och fungerar.

