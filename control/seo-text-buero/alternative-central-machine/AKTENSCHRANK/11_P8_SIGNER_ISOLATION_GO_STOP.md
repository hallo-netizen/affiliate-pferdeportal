# P8 – EXTERNE SIGNER-PROZESSISOLATION

Datum: 2026-09-08
Status: GO

## Ziel

Beweisen, dass der Produktionsworker den privaten Signierschlüssel technisch nicht besitzt.

## Isolierter Laboraufbau

Drei getrennte GitHub-Jobs:

1. PRODUCER
- checkt ausschließlich den Kandidaten aus
- erzeugt nur das unsigned Release
- besitzt keinen privaten Schlüssel
- kann nicht signieren

2. EXTERNAL SIGNER
- startet erst nach erfolgreichem Producer
- checkt keinen Produktionscode aus
- erhält nur das fertige unsigned Release
- erzeugt den privaten Ed25519-Schlüssel ausschließlich in seinem eigenen temporären Job
- signiert
- löscht den privaten Schlüssel
- exportiert nur Release + Signatur + öffentlichen Schlüssel

3. IMPORTER
- startet erst nach Signer-PASS
- erhält Release + Signatur + öffentlichen Schlüssel
- erhält keinen privaten Schlüssel
- prüft über P7 fail-closed
- Ergebnis nur IMPORT_VERIFIED_NO_PUBLISH oder BLOCKED

## Echter Laborlauf

Workflow: `Alternative SEO Text P8 Signer Isolation Lab`
Ergebnis: SUCCESS.

Beweise:
- `P8_PRODUCER_NO_SIGNING_CAPABILITY_PASS`
- `P8_EXTERNAL_SIGNER_PRIVATE_KEY_EPHEMERAL_PASS`
- `P8_IMPORTER_PUBLIC_KEY_ONLY_PASS`
- `P8_SIGNER_PROCESS_ISOLATION_PASS`

## Gegenprüfung

### 0,0 Freiheit
PASS.
Producer kann nicht signieren.
Signer produziert keinen Text und trifft keine Workflowentscheidung.
Importer kann nur verifizieren.

### Signer-Credentials beim Worker
PASS.
Der private Schlüssel entsteht erst in einem späteren separaten Job und wird nicht an Producer oder Importer exportiert.

### Einfluss nach Dateiausgabe
PASS zusammen mit P7.
Änderung nach Signatur wird blockiert.

### KISS
PASS für das Produktionskonzept.
Es gibt genau eine externe Signierstufe.
Die drei GitHub-Jobs sind ausschließlich Testinfrastruktur zum Beweis der Trennung und kein vorgeschlagener Produktions-Controller-Zoo.

### interne Signierung
NICHT eingeführt.

### WordPress
Noch kein realer WordPress-Schreibtest.
Importprinzip und Credential-/Signaturgrenze sind bewiesen.
No-Publish bleibt hart.

## Grenze des P8-Prototyps

Der Test verwendet einen ephemeren Testschlüssel.
In einer realen Installation müsste WordPress einen festen vertrauenswürdigen öffentlichen Schlüssel bzw. dessen unveränderlichen Trust-Anker besitzen.
Das ist eine Deploymentfrage und keine zusätzliche Workflowentscheidung.

## GO/STOP

GO.

Damit sind sowohl
- Kernsteuerung
als auch
- äußere Signaturgrenze
im Prototypprinzip ohne freie KI-/Workerentscheidung darstellbar.

Nächster sinnvoller Schritt ist keine weitere technische Detailstufe, sondern ein abschließendes Prototyp-Gesamturteil gegen alle unverhandelbaren Anforderungen.
