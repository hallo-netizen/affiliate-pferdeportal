# P6 – MAKRO-GEGENPRÜFUNG GEGEN HISTORISCHE FEHLER M01–M33

Datum: 2026-09-08
Status: GO MIT KLARER GRENZE

## Ziel

Nicht weiter in Detailentwicklung gehen.

Prüfen, ob die Zentralmaschinen-Architektur reale historische Fehlerklassen
- wirklich reduziert,
- nur verschiebt,
- oder unverändert weiter absichern muss.

## Grundsatz

Eine historische Fehlernummer darf NICHT einfach gelöscht werden.

Es wird unterschieden zwischen:

A. FACH-/SICHERHEITSINVARIANTE MUSS BLEIBEN
Die Schutzwirkung bleibt zwingend, auch wenn ihre technische Umsetzung später anders aussieht.

B. IMPLEMENTIERUNGSARTEFAKT DES ALTEN RAUM-/HANDOFF-WEGS
Die konkrete alte Datei/Gate/Handoff-Form kann entfallen, WENN dieselbe Schutzwirkung in der Zentralmaschine nachweislich einfacher und fail-closed erreicht wird.

C. NOCH OFFEN
Im Prototyp bisher nicht ausreichend geprüft.

## Makro-Mapping

### M01 – verteilte State-/Bundle-Hash-Chain
B = Kandidat für strukturelle Vereinfachung.
Schutzwirkung bleibt: aktueller Auftrag/Zustand muss unverwechselbar gebunden sein.
Neu: ein kanonischer Jobzustand statt mehrfacher ROOT/State/Bundle-Neubindung.
Noch nicht final bewiesen: Persistenz/Restart.

### M02 – eindeutige Artikeldateien
A.
Muss bleiben.
Zentralmaschine besitzt item_id je Artikel; reale Dateiausgabe noch später zu testen.

### M03 – PREPARED Persist/Restore
B/C.
Alte PREPARED-Übergabe kann durch einen einzigen kanonischen Checkpoint ersetzt werden.
Persistenz/Restart ist noch nicht im aktuellen KISS-Kern bewiesen.

### M04/M05 – Finalize + dauerhafte Release/Receipt
C.
Releasephase wurde bewusst noch nicht gebaut.
Schutzwirkung bleibt zwingend.

### M06/M07 – Fake-Produktion / Recovery darf nicht automatisch final sein
A.
Muss vollständig erhalten bleiben.

### M08/M09 – PPM-/PSERC-Originalpakete
A, bereits P3 real bewiesen.
Exakte Paket-SHAs PASS.

### M10 – Preflight fail-closed bei falschem Paket
A, P3 negativ bewiesen.
Paketdrift -> BLOCKED.

### M11 – realer PPM-Aufruf
A.
Reale Eintrittsstelle P3 nachgewiesen; P4 reale PPM-Pipeline ausgeführt.

### M12 – Fake PPM blockieren
A.
Muss bleiben.
P3/P4 beweisen Paket-/Pipeline-Echtheit, aber ein vollständiger Fake-Report-Angriff gehört später in die echte Integrationsregression.

### M13 – finaler Content-Hash = PPM-Content-Hash
A.
Muss bleiben.
Im vorhandenen realen PPM/Fachworkflow bereits vorgesehen; in der Alternativmaschine noch nicht als echter Artikel-Handoff integriert.

### M14/M15 – Current Action / 107007 Handoff
B.
Dies sind starke Kandidaten dafür, als eigene Übergabemechanik zu entfallen.
Schutzwirkung bleibt: der exakt nächste erlaubte Mikroschritt muss gebunden sein.
In der Zentralmaschine besitzt ausschließlich der Kern den next_step.

### M16 – Signer Boundary
A.
Muss bleiben.
Externe Signatur; keine Signer-Credentials beim Worker.
Noch nicht als finaler P7-Perimeter geprüft.

### M17–M20 – Finalisierung / ENDSTEMPEL / Delivery
C.
Noch nicht Bestandteil des Prototyps.
Müssen vor Produktionsreife separat erhalten/vereinfacht werden.

### M21 – No Auto Publish
A.
Muss bleiben.
P3/P4 real: publish_allowed=false; kein WordPress-Schreiben.

### M22–M24 – signierter Produktionsvertrag / H8 / kein Rollback
A/B, noch autoritativ zu auditieren.
Die Schutzwirkung „nur autorisierter, unveränderter Auftrag darf produzieren“ bleibt zwingend.
Ob die konkrete H8-Mehrschichtarchitektur nötig bleibt, ist eine Implementierungsfrage und darf nicht ohne separaten Audit entfernt werden.
Keine neue interne Signierung.

### M25 – keine freie Neuplanung / Fachworkflow autoritativ
A, Kernziel der Zentralmaschine.
P0–P2: keine freie Folgeschritt-/Validator-/Enginewahl.
Bestehender Fachworkflow/Textmaschine bleibt unverändert.

### M26 – gebundener aktueller Fachkontext
A, aber strukturell stark vereinfachbar.
Fact-Pack/Plan/Item müssen weiterhin exakt aktuell und konsistent sein.
Neu: ein kanonischer Jobzustand soll diesen Kontext einmal besitzen statt ihn an Raumgrenzen neu zu konstruieren.
Das beseitigt die Anforderung nicht, reduziert aber die Verluststelle.

### M27 – Produktionsumgebungsidentität
A/C.
Muss als äußere Deployment-/Versionsbindung bleiben.
P3 beweist Paketidentität, aber nicht den späteren kompletten Produktions-Deploymentweg.

### M28 – materiell ausführbarer Fachworkflow-Handoff
B.
Die konkrete Handoff-Request ist Kandidat zum Entfallen.
Alle Fachinformationen bleiben zwingend; sie liegen im kanonischen Jobobjekt und werden nicht als neue Worker-zu-Worker-Anweisung materialisiert.

### M29/M30 – Batch-/Finalkontext-Identität
A, strukturell vereinfachbar.
Batch-ID/Itemzahl/Output müssen identisch bleiben.
Ein zentraler Zustand vermeidet Neubindung zwischen 107007/107008/Handoff.
Noch reale Batch-/Releaseprüfung offen.

### M31 – synthetischer zweiter Executor
B, im P0–P2-Prinzip bereits vermieden.
Kein Capability-Suchen und kein zweiter Workflow-Executor.
Zentralmaschine ruft den festen Mikroschritt selbst auf.

### M32 – gebundener PPM-Pfad ohne Environment-Abhängigkeit
A, P3 im Prototypprinzip PASS.
Fester Pfad + SHA; keine Runtime-Enginewahl.

### M33 – finaler GitHub-/ENDSTEMPEL-Weg ohne Codex-Push-Abhängigkeit
A/C.
Bleibt zwingend.
Noch nicht in der Alternativarchitektur umgesetzt.

## Historische Hauptfehler M26–M33 – Wirkung der neuen Architektur

M26 Kontext fehlt:
REDUZIERT, nicht automatisch erledigt.
Ein Zustandseigentümer statt Handoff-Rekonstruktion.

M27 falsche Produktionsumgebung:
BLEIBT äußere Pflicht.

M28 Handoff Request fehlt/ungültig:
DIE KONKRETE FEHLERKLASSE KANN ENTFALLEN,
wenn keine Handoff-Request mehr existiert.
Fachkontextpflicht bleibt.

M29 Release-Metadaten falsch:
REDUZIERT durch eine zentrale Batchidentität; Releaseprüfung bleibt.

M30 Finalkontext wechselt:
STARK REDUZIERT, weil derselbe Jobzustand bis zur Ausgabe fortgeführt wird.

M31 zweiter Executor fehlt:
STRUKTURELL ENTFERNT im Prototyp.
Keine zweite Executor-Capability vorgesehen.

M32 PPM-Pfad fehlt:
P3 PASS mit fest gebundenem Pfad/Hash.

M33 finaler Push/Endstempel:
BLEIBT offen und muss außen gelöst werden.

## Gegenprüfung gegen unverhandelbare Anforderungen

### 0,0 Freiheit
GO.
Architekturprinzip weiterhin erfüllt.
Keine neue freie Stelle aus P6 notwendig.

### Kein Einfluss von außen
GO für Kern; AUSSENRAND NOCH OFFEN.
Finale Signatur/WordPress-Importgrenze muss noch separat beweisen, dass fertige Bytes nach Ausgabe nicht manipuliert werden können.

### Textmaschine unverändert
GO.
P3/P4 reale Pakete unangetastet.

### Textregeln zwingend
GO als Architekturprinzip, NOCH KEIN GESAMTBEWEIS.
P4 beweist den echten PPM-Kern inklusive realem negativen Content/Link-Test.
Alle weiteren bestehenden Fachgates müssen später als unveränderte Komponenten gemappt werden, nicht neu interpretiert.

### KISS
GO.
Die größten Chancen liegen ausdrücklich darin, alte Handoff-/State-Artefakte NICHT 1:1 nachzubauen.

### Nachhaltigkeit
GO.
Ein kanonischer Jobzustand + feste Komponenten ist allgemeiner als raumspezifische Handoff-Dateien.

### Themenunabhängigkeit
GO.
Steuerkern ist fachblind; Fachregeln bleiben in den vorhandenen Komponenten.

### Automatisierung
GO.
Keine manuelle Navigation im Kern.

### theoretisch beliebig viele Artikel
GO als Architekturprinzip.
Keine fest kodierte Artikelobergrenze; unabhängige Itemzustände.
Reale Ressourcen bleiben natürlich endlich.

## P6-Gesamtentscheidung

GO.

Die neue Architektur zeigt auf Makroebene einen echten Unterschied zur bisherigen:
Sie reduziert NICHT Prüfungen und NICHT Schutzregeln.
Sie reduziert die Zahl der Stellen, an denen derselbe Zustand neu materialisiert, neu erklärt oder neu gebunden werden muss.

Das ist eine reale Vereinfachung und keine reine Umbenennung.

## Nächste Prüfstufe

P7 soll NICHT weitere Fachdetails integrieren.

P7 = minimaler äußerer Hochsicherheitstrakt:
- genau ein autorisierter Eingang
- genau ein finaler Ausgang
- externe Signatur/Hash-Bindung
- WordPress akzeptiert später nur exakt dieses unveränderte Ausgabepaket
- keine interne Signatur
- keine neue Raum-/Handoff-Kaskade

Nur als isolierter Prototyp.
Wenn hierfür wieder mehrere Signier-/Handoff-/Release-Schichten nötig werden:
STOP.
