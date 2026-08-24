# Reflektionsdokument

1. Varför ska sensorerna kommunicera med ett API i stället för direkt med PostgreSQL?
Ett API fungerar som en sköld genom att hantera autentisering och validering, samt att sensorer helst inte ska ha direktåtkomst eller nycklar/credentials sparade i sin hårdvara då det ger större risk för intrång och manipulering.

2. Varför ska felaktig sensordata stoppas innan den sparas?
Detta är sköld aspekten av ett API, då inkorrekt/korrupt data såsom orimliga mätningar eller tomma fält inte inkluderas i framtida analys och statistik. Exempelvis hade API:ets '/statistics' endpoint potentiellt kunnat visa helt fel information.

3. Varför passar PostgreSQL för historiska mätvärden?
Det ger en tydlig struktur till datan och har ger en goda verktyg för att få fram tydlig rapportering och analys (som vi använde oss av när vi gjorde '/statistics' endpointen), vilket är är ett bra supplement till sensorer som mäter data konstant över längre tider.

4. Vad händer med lösningen om Redis försvinner?
Systemet kommer fortfarande att köras utan problem tack vare att det körs på Redis-Aside och kommer därför läsa direkt från PostgreSQL vid en cache-miss. Dock så kommer  detta med en liten prestanda-minskning och svaren kommer ta lite längre tid.

5. Vad händer med lösningen om PostgreSQL försvinner?
Eftersom PostgreSQL är den beständiga datakällan så kommer alla 'POST /measurements' sluta att fungera och de enda mätningarna som finns kvar är de som fortfarande ligger i cachen.

6. Varför används Docker Compose lokalt?
Systemet kan startas enkelt med ett enda kommando och säkerställer att alla volymer och services skapas på rätt sätt varje gång.

7. Vad automatiserar din CI-pipeline?
Den kör pytest vid git push/pull för att se till att felaktig kod inte når main-branchen.

8. Vad observerade du när du tog bort en Kubernetes Pod?
Med hjälp av self-healing så återskapades den snabbt när kubectl märkte att antalet önskade replicas inte matchade antalet som fanns. 

9. Varför kan flera repliker ge högre tillgänglighet?
Fler pods ger bättre beöastningsutjämning, så om en pod får för mycket att göra så kan de andra poddarna ta över.

10. När hade Kubernetes varit overkill för en lösning?
Kubernetes tillför en högre komplexitet och större krav på övervakning som kan vara onödig för mindre system (som inte kommer behöva skalas) där man vet att trafiken och antalet anvöndare kommer vara minimalt.
