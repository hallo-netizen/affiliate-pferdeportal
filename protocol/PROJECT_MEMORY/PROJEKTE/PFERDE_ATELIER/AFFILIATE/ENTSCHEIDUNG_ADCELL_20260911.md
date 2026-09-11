# AFFILIATE – WAS/WARUM – ADCELL 2026-09-11

STAND: 2026-09-11
ROLLE: DAUERHAFTER ENTSCHEIDUNGSBELEG FÜR DEN AKTUELLEN ADCELL-AUFTRAG

## WAS

Der aktuelle Affiliate-Arbeitsfokus wurde durch ausdrückliche Nutzerentscheidung auf ADCELL umgestellt.

Verbindlicher Zielweg:
- ADCELL automatisiert über API v2;
- Programme automatisch lesen;
- nur `accepted` + aktiv + explizit freigegebene `programId` verarbeiten;
- Produkt-CSV, Banner und Deeplinks automatisch über dokumentierte API-Wege beziehen;
- kein manueller Import/Export und keine manuell konfigurierte CSV-URL als Normalbetrieb;
- alte/fachfremde accepted Partnerschaften bleiben intern fail-closed ausgeschlossen;
- bestehende zentrale Relevanz-, Creative-, Output-, Veto- und Pause-Logik bleibt erhalten.

Digistore24 bleibt BLOCKED/zurückgestellt. OTTO/Awin bleibt ungelöst und wird für diesen Auftrag pausiert, nicht als erledigt erklärt.

## WARUM

Der Nutzer will einen wartungsarmen, zentralen Affiliate-Betrieb ohne wiederkehrenden Handimport. Die vom Nutzer geöffnete ADCELL-API-v2-Dokumentation belegt eigene Programme-, CSV-, Banner- und Deeplink-Wege, sodass ein manueller Export/Import als Hauptworkflow fachlich nicht erforderlich ist.

Gleichzeitig enthält das ADCELL-Konto ältere, fachfremde angenommene Partnerschaften. Eine explizite `programId`-Allowlist verhindert, dass deren Daten allein wegen des Status `accepted` in das Pferdeportal gelangen.

## FEHLERFOLGE

Die Prüfung des kanonischen Standes zeigte:
- der ADCELL-Automatisierungsbutton fällt derzeit in den Awin-orientierten Automationspfad;
- die bestehende ADCELL-Automation ist auf eine manuell konfigurierte CSV-Export-URL ausgerichtet;
- ein lokaler Scratch nahm die API-Authentifizierung widersprüchlich und ohne autoritativen Beleg an.

Die Fehlerdetails bleiben ausschließlich in der technischen autoritativen Fehlermatrix auf `affiliate-release-current`.

## ENTSCHEIDUNG ZUM SCRATCH

Der lokale 6.72.18-Scratch wird nicht übernommen:
- falsche Basis aus der nicht abgenommenen 6.72.17-Testlinie;
- widersprüchliche, unbestätigte Auth-Annahme;
- kein kanonischer WordPress/MariaDB-E2E.

Neuaufbau ausschließlich aus kanonischem 6.72.8 nach belegtem API-v2-Authentifizierungsvertrag.

## TEST-/ABNAHMEREGEL

Kein Plugin vor:
- kanonischer Positivprüfung;
- kanonischer Negativprüfung;
- Regression gegen bestehenden Gesamtworkflow;
- Fresh-Unpack;
- Source/ZIP-Byte-Identity.

Kein Live-PASS ohne echten ADCELL-Zugang und WordPress/MariaDB-End-to-End.

## NACHHOLSTAND NACH AUTORITATIVER ABSCHLUSSPRÜFUNG

Der Authentifizierungsvertrag ist inzwischen **belegt**: offizieller ADCELL-v2-Tokenweg über `/user/getToken` mit `userName` + `password`, danach Query-Parameter `token`.

Daraufhin wurde kanonisch bereits ein **partieller** Sourcefix in `trait-ppar-network-sync.php` begonnen. Dieser Schritt war sinnvoll, weil er die neue Implementierung an den belegten statt an einen geratenen Auth-Vertrag bindet.

Die Abschlussprüfung zeigte jedoch zwei zwingende Korrekturen des Arbeitsstands:

1. **AF-023 offen:** Die Sourceänderung wurde nicht atomar mit `CURRENT_SOURCE_SHA256.txt` und der Governance-Manifestbindung nachgezogen. Deshalb muss die Source-/Manifest-/Governance-Identität vor jeder weiteren Entwicklungsarbeit wiederhergestellt werden.

2. **AF-062 neu:** Die Provider-Registry ruft weiterhin den alten `test_adcell_connection()` auf; der kanonische Router sendet dort noch Basic Auth. Der belegte Tokenvertrag ist also dokumentarisch geklärt, aber im Runtime-Verbindungstest noch nicht vollständig durchgesetzt.

WARUM diese Reihenfolge jetzt verbindlich ist:
- Ohne korrekte Source-/Manifest-Bindung wäre jeder weitere Test gegen eine nicht eindeutig gebundene Sourcebasis und damit kein belastbarer PASS.
- Erst danach darf der aktive Legacy-Basic-Auth-Pfad entfernt werden.
- Erst anschließend dürfen Routing und Automation (AF-058/059) fertiggestellt und der Gesamtworkflow geprüft werden.

Der Zielvertrag selbst ändert sich dadurch **nicht**. Es ändert sich nur der belastbare aktuelle Reparaturweg.
