# Arkitekturdiagram – obligatorisk leverabel

Skapa ett enkelt diagram över **din färdiga lösning**. Det ska visa komponenterna och hur de kommunicerar; du behöver inte använda UML eller någon annan avancerad standard.

Diagrammet ska minst visa:

- en klient eller användare som anropar lösningen
- de tre simulerade IoT-sensorerna
- REST API:t
- PostgreSQL för beständig historik
- Redis för cache av senaste mätning
- Docker Compose som lokal körmiljö
- CI-pipelinen
- Kubernetes-demon med Deployment, Pod-repliker och Service

Använd namngivna pilar som visar viktiga anrop och dataflöden, exempelvis `HTTP POST /measurements`, `SQL` och `cache read/write`. Det ska gå att se vilket flöde som är skrivintensivt (**write-heavy**), vad som cacheas och vad som måste vara persistent.

Ett enkelt exempel på detaljnivå:

```text
[3 sensorer] -- HTTP POST /measurements --> [REST API]
                                              |  \
                               SQL, historik  |   \ senaste värde
                                              v    v
                                        [PostgreSQL] [Redis cache]

[GitHub push] --> [CI: tester + image build]
[Användare] --> [Kubernetes Service] --> [Deployment: 3 Pod-repliker]
```

Exemplet är vägledning, inte en mall som måste kopieras. Du kan göra ett sammanhängande diagram eller två tydligt märkta vyer (lokal Docker Compose-miljö och Kubernetes-demo). Gör inte diagrammet mer detaljerat än vad som behövs för att förklara lösningen.

## Så lämnas det i repositoryt

1. Skapa diagrammet i valfritt verktyg, exempelvis diagrams.net, Excalidraw, Visio, PowerPoint eller Figma.
2. Exportera det som PNG eller PDF till `docs/`.
3. Länka eller bädda in filen här.
4. Ersätt denna instruktion med en kort beskrivning av diagrammet och dina viktigaste arkitekturval.

Kontrollera före inlämning att text och pilar går att läsa direkt från GitHub och att diagrammet stämmer med den kod du faktiskt lämnar in.
