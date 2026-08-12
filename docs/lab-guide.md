# Praktiska instruktioner – Jensen IoT Platform

## Så används guiden

Tre simulerade sensorer skickar temperatur, luftfuktighet och batterinivå till ett REST API. Du ska färdigställa API:t så att data valideras, lagras i PostgreSQL och den senaste mätningen kan hämtas via Redis-cache.

Markeringarna betyder:

- **Obligatoriskt** – grunduppgift som ska genomföras.
- **Reflektion** – besvaras i `docs/reflection.md`.
- **Frivillig fördjupning** – behövs inte för godkänt.
- **Kontroll** – ett konkret sätt att verifiera resultatet.

Gör milstolparna i ordning. Commit och push regelbundet till din egen fork.

### Tidsåtgång och förkunskaper

Räkna med ungefär **18–24 timmars arbete** om du har begränsad erfarenhet av Python. Tiden kan variera beroende på erfarenhet av SQL, Docker och installationen av Minikube.

Du behöver inte kunna bygga en Flask-applikation från grunden. Innan du börjar bör du däremot känna igen:

- Python-funktioner, dictionaries, listor, `None` och imports
- hur JSON tas emot och returneras i ett REST API
- grundläggande `SELECT`, `INSERT`, `WHERE` och `ORDER BY` i SQL
- hur ett enkelt test med `pytest` är uppbyggt

Om något av detta är nytt, använd kursmaterialet eller be om handledning innan du försöker felsöka Docker eller Kubernetes. Börja med `validation.py` och de befintliga testerna; de är de minsta och enklaste exemplen i kodbasen.

### Arbetscykel när du ändrar kod

Källkoden kopieras in i Docker-imagen och uppdateras därför inte automatiskt. Efter en kodändring bygger och startar du om berörda tjänster:

```text
docker compose up --build -d
```

Kontrollera sedan status och loggar:

```text
docker compose ps
docker compose logs --tail=50 api simulator
```

Ett Python-fel syns normalt i API-loggen. Ett misslyckat anrop från simulatorn syns i simulatorloggen.

## Milstolpe 1 – IoT Data API

### 1. Bekanta dig med startläget

**Obligatoriskt:** Starta miljön enligt [`README.md`](../README.md). Läs sedan:

- `database/init.sql` för tabeller och startdata
- `api/app.py` för endpoints
- `api/db.py` för databasfunktionerna
- `api/validation.py` och `api/tests/test_validation.py` för validering och tester

Filerna innehåller `TODO M1` där kod saknas. Följande endpoints ska fungera när milstolpen är klar:

| Metod och sökväg | Uppgift | Förväntad status |
|---|---|---|
| `POST /measurements` | validera och lagra en mätning | `201` vid skapad, `400` vid ogiltig data eller okänd sensor |
| `GET /measurements` | lista de senaste mätningarna | `200` |
| `GET /devices` | lista sensorer | `200` |
| `GET /devices/{id}/measurements` | visa en sensors historik | `200` (även för en tom lista), `404` om sensorn saknas |
| `GET /devices/{id}/latest` | visa senaste mätningen | `200`, `404` om sensorn eller en mätning saknas |

### Kodstöd för Python och PostgreSQL

Du behöver inte skapa databasstrukturen från grunden. Använd `get_devices()` och `get_measurements()` i `api/db.py` som mönster för anslutning, cursor och konvertering till JSON.

Skicka alltid värden som parametrar i stället för att bygga SQL med strängar:

```python
cur.execute(
    "SELECT ... FROM ... WHERE device_id = %s",
    (device_id,),
)
row = cur.fetchone()
```

`fetchone()` ger en rad eller `None`. `fetchall()` ger en lista, som kan vara tom. Använd `RETURNING` tillsammans med `INSERT` om du behöver få tillbaka den skapade raden. Du ska ersätta `...` med rätt tabell, kolumner och SQL; exemplet är inte en färdig lösning.

### 2. Implementera lagringen

**Obligatoriskt:**

1. Implementera `device_exists(device_id)` i `api/db.py` så att den avgör om sensorn finns i tabellen `devices`.
2. Implementera `insert_measurement(data)` i `api/db.py` med en parametriserad `INSERT`-fråga. Returnera den skapade raden.
3. Anropa funktionerna från `POST /measurements` i `api/app.py`.
4. Ändra startersvaret `202` till `201` först när mätningen faktiskt sparas.
5. Behåll valideringen före databaslagringen. Ogiltiga mätningar ska ge `400` och får inte sparas.
6. Kontrollera att `deviceId` finns i tabellen `devices` innan mätningen sparas. Ett okänt id, exempelvis `sensor-999`, ska ge `400` med ett tydligt JSON-fel i stället för ett databasfel.

**Kontroll:** Bygg om efter kodändringar och följ simulatorn:

```text
docker compose up --build -d
docker compose logs -f simulator
```

Giltiga rader ska nu få `201`; avsiktligt felaktiga rader från `sensor-003` ska få `400`. Öppna `/measurements` och kontrollera att listan fylls på. Avsluta loggvisningen med `Ctrl+C`.

### 3. Implementera historik och senaste mätning

**Obligatoriskt:**

1. Implementera `get_measurements_for_device(device_id)` och `get_latest_measurement(device_id)` i `api/db.py`.
2. Använd funktionerna i motsvarande endpoints i `api/app.py`.
3. Skilj mellan en känd sensor utan mätningar och en okänd sensor. Historik för en känd sensor utan mätningar ska ge `200` och `[]`; ett okänt sensor-id ska ge `404`.
4. Returnera JSON och relevanta statuskoder enligt tabellen ovan.
5. Lägg till minst tre valideringstester utöver starttesterna: saknat `deviceId`, fel datatyp för `humidity` och fel datatyp för `battery`. Databas-, cache- och endpointflöden verifieras med guidens manuella kontroller. Automatiserade integrationstester är frivillig fördjupning.

**Kontroll:** Ersätt `{id}` med exempelvis `sensor-001` och öppna båda adresserna. Testa även ett okänt id, exempelvis `sensor-999`, och kontrollera att felhanteringen är tydlig.

```text
http://localhost:5001/devices/sensor-001/measurements
http://localhost:5001/devices/sensor-001/latest
```

Kör testerna i API-containern:

```text
docker compose exec api python -m pytest -q
```

**Vanlig fallgrop:** JSON använder `deviceId`, medan databaskolumnen heter `device_id`. Översätt namnet på ett konsekvent ställe i koden.

### 4. Grundläggande SQL-uppgifter

**Obligatoriskt:** Skriv och prova tre SQL-frågor som visar:

- totalt antal mätningar med `COUNT`
- medeltemperatur med `AVG`
- mätningar från de senaste 24 timmarna

Följande visar syntaxen. Anpassa själv tabell, kolumn och villkor till labbens schema:

```sql
SELECT COUNT(*) FROM tabell;
SELECT AVG(kolumn) FROM tabell;
SELECT * FROM tabell
WHERE tidskolumn >= NOW() - INTERVAL '24 hours';
```

Öppna PostgreSQL-klienten med:

```text
docker compose exec db psql -U student -d jensen_iot
```

**Kontroll:** Varje fråga ska kunna köras utan fel och ge ett rimligt resultat utifrån datan i tabellen `measurements`. Avsluta `psql` med `\q`. Spara de tre frågorna och en kort förklaring i projektets README eller i en separat `.sql`-fil som länkas från README.

**Frivillig fördjupning:** Implementera `/statistics`, Online/Offline-status eller beräkningar för högsta medeltemperatur och mest aktiva sensor.

## Milstolpe 2 – Docker och cache

### 1. Förstå miljön och verifiera persistence

**Obligatoriskt:** Läs `docker-compose.yml` och identifiera tjänsterna `api`, `simulator`, `db` och `redis`, deras beroenden samt vilka portar som exponeras till datorn.

**Kontroll av persistence:**

1. Notera en mätning via `/measurements`.
2. Kör `docker compose down` och sedan `docker compose up -d`.
3. Kontrollera att mätningen finns kvar. PostgreSQL använder volymen `postgres_data`.

### 2. Implementera latest-cache

**Obligatoriskt:**

1. Implementera `get_latest_from_cache` och `set_latest_in_cache` i `api/cache.py`.
2. Använd ett tydligt nyckelformat, exempelvis `latest:sensor-001`, och JSON för värdet.
3. I endpointen för senaste mätning: läs först från Redis. Vid cache miss, läs från PostgreSQL och lägg resultatet i cache innan det returneras.
4. Uppdatera cache när en ny mätning sparas.
5. PostgreSQL ska även fortsättningsvis vara den beständiga källan; ett tomt Redis får inte innebära att historiken försvinner.

Redis lagrar text. Använd `json.dumps(measurement)` när värdet sparas och `json.loads(value)` när det läses tillbaka. Importen `json` och Redis-klienten är redan förberedda i `api/cache.py`.

**Kontroll:** Hämta senaste värdet och kontrollera därefter nycklarna:

```text
docker compose exec redis redis-cli KEYS "latest:*"
```

Du ska se minst en nyckel efter att en senaste mätning har hämtats eller sparats. Testa en cache miss genom att tömma endast labbens Redis med `docker compose exec redis redis-cli FLUSHDB`; nästa GET ska fortfarande kunna läsa värdet från PostgreSQL och återskapa cacheposten.

**Reflektion:** Förklara varför historik lagras i PostgreSQL medan senaste mätningen lämpar sig för cache, och vad som händer om respektive tjänst försvinner.

## Milstolpe 3 – CI och introduktion till Kubernetes

### 1. Skapa en enkel CI-pipeline

**Obligatoriskt:** Skapa `.github/workflows/ci.yml` i din fork. Pipelinen ska köras vid push och pull request och minst:

1. checka ut koden
2. installera `api/requirements.txt`
3. köra testerna med `python -m pytest`
4. bygga API:ts Docker image

Detta är ett minimalt exempel som du kan använda och förklara:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r api/requirements.txt
      - run: python -m pytest tests -q
        working-directory: api
      - run: docker build -t jensen-iot-api:ci ./api
```

Samma tester kan köras lokalt med `docker compose exec api python -m pytest -q`. Pusha workflow-filen och kontrollera fliken **Actions** på GitHub. En grön körning är den förväntade verifieringen.

### 2. Starta Minikube och bygg imagen

Kubernetes-delen är en kort, introducerande men praktiskt genomförd demo av API:t. Du ska alltså starta Minikube, distribuera API:t och genomföra momenten nedan. PostgreSQL, Redis och simulatorn ska inte distribueras i Kubernetes. Därför används startsidan och `/health` i övningen; databasberoende endpoints ingår inte i denna demo.

**Obligatoriskt:** Kontrollera först att Docker, Minikube och `kubectl` fungerar. Starta sedan klustret och bygg imagen direkt i Minikube:

```text
minikube start --driver=docker
minikube status
minikube image build -t jensen-iot-api:lab ./api
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
```

Vänta tills alla tre Pod-statusar är `Running` och `READY` visar `1/1`. Vid problem, använd `kubectl describe pod <podnamn>` och `kubectl logs <podnamn>`.

### 3. Nå tjänsten

**Obligatoriskt:** Kör följande och låt terminalfönstret vara öppet medan du testar sidan:

```text
minikube service jensen-iot-api
```

Minikube visar eller öppnar rätt URL. Utgå inte från `localhost:30080`; adressen varierar mellan operativsystem och Minikube-driver.

Om webbläsaren inte öppnas automatiskt kan du få adressen med `minikube service jensen-iot-api --url`. Som tillfälligt alternativ kan du köra `kubectl port-forward service/jensen-iot-api 8080:80` och öppna <http://localhost:8080>. Avsluta en pågående service-tunnel eller port-forward med `Ctrl+C`.

### 4. Observera self-healing och scaling

**Obligatoriskt:**

1. Kör `kubectl get pods` och kopiera namnet på en Pod.
2. Radera just den Poden med `kubectl delete pod <podnamn>`.
3. Kör `kubectl get pods -w`. Deploymenten ska skapa en ersättare så att antalet återgår till tre. Avsluta bevakningen med `Ctrl+C`.
4. Skala upp och sedan tillbaka:

```text
kubectl scale deployment jensen-iot-api --replicas=5
kubectl get pods
kubectl scale deployment jensen-iot-api --replicas=3
kubectl get pods
```

Detta demonstrerar **self-healing** och **scaling**. Manifestet innehåller en Deployment som hanterar Pod-repliker och en Service som ger dem en gemensam ingång. Avancerad klusterkonfiguration, rolling update och rollback är inte obligatoriska moment.

När övningen är klar:

```text
minikube stop
```

**Reflektion:** Beskriv vad du observerade när en Pod raderades, varför flera repliker kan öka tillgängligheten och när Kubernetes skulle vara onödigt stort för en lösning.

## Milstolpe 4 – dokumentation och inlämningsfiler

**Obligatoriskt:** Färdigställ följande i din fork:

- projektets `README.md`: beskriv din lösning, förutsättningar, hur den byggs/startas, hur tester körs och eventuella kända begränsningar; anpassa startertexten så att den speglar ditt slutresultat
- `docs/architecture.md` samt ett länkat/exporterat diagram enligt instruktionen i filen
- `docs/reflection.md`: korta men motiverade svar på samtliga frågor
- kod och tester samt en grön CI-körning

Formen för inlämning, åtkomst, deadline och de formella bedömningskriterierna finns i uppgiftsunderlaget.

## Koppling till bedömningskriterierna

| Krav i uppgiftsunderlaget | Praktiskt stöd i repositoryt |
|---|---|
| fungerande REST API | milstolpe 1, endpoints och verifieringar |
| API, PostgreSQL och Docker Compose | milstolpe 1–2 samt `docker-compose.yml` |
| validering och HTTP-statuskoder | milstolpe 1, `validation.py` och tester |
| SQL-uppgifter | milstolpe 1, avsnitt 4 |
| Kubernetes: scaling och self-healing | milstolpe 3, avsnitt 2–4 |
| cache och CI | milstolpe 2–3 |
| README, arkitekturdiagram och reflektion | milstolpe 4 och mallarna i `docs/` |

Grunduppgifterna märkta **Obligatoriskt** stödjer kraven för godkänt. De tre grundläggande SQL-frågorna (`COUNT`, `AVG` och senaste 24 timmarna) är obligatoriska; mer avancerade analyser och `/statistics` är frivillig fördjupning.

## Slutkontroll före inlämning

Kontrollera att:

- `docker compose up --build -d` startar alla fyra tjänster utan fel
- simulatorn får `201` för giltiga mätningar och `400` för ogiltiga
- samtliga obligatoriska endpoints ger förväntad JSON och statuskod
- mätningar finns kvar efter `docker compose down` och en ny start
- senaste mätningen kan återskapas från PostgreSQL efter att Redis har tömts
- `docker compose exec api python -m pytest -q` är grön
- den senaste CI-körningen på GitHub är grön
- Kubernetes-demon har genomförts med tre repliker, self-healing och scaling
- README, arkitekturdiagram och reflektionsdokument är färdiga och pushade
