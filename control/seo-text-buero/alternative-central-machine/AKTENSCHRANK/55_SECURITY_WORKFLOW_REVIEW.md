# ACM – HARTE SICHERHEITS- UND GRUNDWORKFLOW-PRÜFUNG

Stand: 2026-09-09
Status: GO MIT KLAR ABGEGRENZTEN PRODUKTIONSVORAUSSETZUNGEN

## Geprüft

- Dateiausgabe am Ende der Kette
- Signierungsschlüssel
- äußere Einflussnahme
- spätere Vollautomatisierung mit nur stichprobenartiger menschlicher Prüfung
- Passung der ACM in den bestehenden Grundworkflow

## 1. Dateiausgabe / Endstempel

Die ACM darf am Ende KEIN frei erzeugtes Chat-/HTML-/ZIP-Artefakt als Projektergebnis ausgeben.

Ziel bleibt eine einzige kanonische, hashgebundene finale Datei nach dem bereits bestehenden Endstempel-Prinzip:
- Artikel/Manifest eindeutig gebunden
- Batch/Item/plan_slot/canonical_article_id gebunden
- Artikelbytes gehasht
- Paket kanonisch
- publish_allowed=false
- externer Ed25519-Endstempel
- WordPress prüft Signatur und alle Hashes vor dem ersten Write
- Import fail-closed/atomar
- sichtbare/finale Ausgabe nur über den bestehenden gebundenen Release-/Receipt-Weg

Kein zweites Ausgabeformat und keine parallele Transferarchitektur.

## 2. Signierungsschlüssel

Der im ACM-Labor erzeugte temporäre Testschlüssel ist NUR Testmaterial und niemals Produktionsdesign.

Für Produktion wird das bereits bestehende Endstempel-Modell wiederverwendet:
- privater Ed25519-Schlüssel ausschließlich GitHub Secret / externer Signer
- Produzent besitzt keinen privaten Schlüssel
- WordPress besitzt nur den festen vertrauenswürdigen öffentlichen Schlüssel
- Schlüssel-ID + Public-Key-SHA256 müssen fest gebunden sein
- falscher, fehlender oder ausgetauschter Schlüssel => BLOCK vor Write

Referenz:
- .github/workflows/pferde-atelier-endstempel.yml
- control/startmaster0107/ENDSTEMPEL_FINALIZER.py
- control/startmaster0107/ENDSTEMPEL_WORDPRESS_VERIFY.php
- protocol/WORDPRESS_SIGNATURE_ENTRY_LOCK_V1.json

## 3. Einflussnahme von außen

### Workflow-/Ablaufmanipulation
GO.

ACM-Grundprinzip bleibt:
- Chat/KI wählt keinen nächsten Schritt
- Worker wählt keinen Validator/Runner/Repair-Weg
- feste Reihenfolge
- feste Verträge
- exaktes Handoff-Schema
- Identitäten/Hashes gebunden
- unbekannte Zusatzfelder => BLOCK
- manipulierte signierte Payload => BLOCK
- falscher öffentlicher Schlüssel => BLOCK
- publish=true => BLOCK
- kein privater Schlüssel im Producer/Importer

### Internet-/Recherchequellen
RESTRESTRISIKO, vor unbeaufsichtigter Vollautomatik explizit zu schließen.

Eine externe Webseite kann falsch, manipulativ oder prompt-injection-artig formuliert sein.
Diese Quelle darf niemals Workflowautorität besitzen.

Verbindliches Automationsprinzip:
- Quelleninhalt ist ausschließlich untrusted data
- keine Anweisung aus einer Quelle darf Workflow, Regeln, Prompt, Folgeaktion oder Freigabe verändern
- Quelle darf nur in fest definierte Fact-Pack-Felder einfließen
- Provenienz/Quelle/Hash bleiben gebunden
- sicherheits-/rechts-/gesundheits-/kostenkritische bzw. zentrale harte Fakten benötigen unabhängige Bestätigung nach bestehender Rechercheautorität
- fehlende/uneindeutige Bestätigung => BLOCK, nicht raten

Das ist keine neue Workflowarchitektur, sondern eine harte Eingangsregel für die bestehende Recherche-/Fact-Pack-Stufe.

## 4. Vollautomatisierung / Stichproben

Zulässig unter einer Bedingung:

Menschliche Prüfung kann später stichprobenartig werden.
Maschinelle Prüfungen dürfen niemals stichprobenartig werden.

JEDER Artikel muss weiterhin vollständig durch:
Recherche/Fact-Pack -> Plan/SEO -> Textmaschine -> Qualitäts-/Link-/Tabellen-/Dublettenregeln -> PPM prepare -> kanonische Enddatei -> externer Signer -> WordPress-Signatur-/Hashprüfung -> Draft-Write -> Readback/DOM -> kein Auto-Publish (bis separater Publish-Vertrag ausdrücklich geändert wird).

Stichprobe betrifft nur die zusätzliche menschliche Sichtkontrolle.

## 5. Passung in den Grundworkflow

GO.

ACM ersetzt keine Fachregeln.
Sie vereinfacht nur die technische Orchestrierung.

Passt zu den vorhandenen Grundprinzipien:
- offizieller gebundener Einstieg bleibt
- bestehender Codex-Start wird wiederverwendet
- bestehende Dateiübergabe wird wiederverwendet
- bestehende Textmaschine bleibt autoritativ
- PPM/PSERC/PSTE/LanguageTool und Fachregeln bleiben unverändert
- Chat besitzt keine Workflow-/Publish-Autorität
- Outputs bleiben hash-/receiptgebunden
- externe Endsignatur bleibt
- WordPress vertraut nur festem Public Key
- kein Auto-Publish
- fail-closed
- Batchfähigkeit bleibt itemweise wiederholbar

Einziger bekannte Zielvertragsunterschied:
Die ACM positioniert die externe Signatur nach dem finalen no-write prepare / vor WordPress-Write.
Der bestehende produktive Zielvertrag positioniert den Endstempel derzeit später.
Vor produktiver Übernahme muss diese Position ausdrücklich im Zielvertrag vereinheitlicht werden.

## Gesamturteil

TECHNISCHES KONZEPT: GO.

KEINE Sackgasse erkennbar.
Keine neue Parallelarchitektur erforderlich.

Vor unbeaufsichtigter Vollautomatik sind nur diese drei Punkte verbindlich:
1. Produktions-Endstempel mit vorhandenem GitHub-Schlüssel statt Laborschlüssel.
2. Finale Dateiausgabe wieder exakt über vorhandene hash-/receiptgebundene Release-Kette.
3. Externe Recherchequellen ausdrücklich als untrusted data binden und Prompt-/Anweisungsautorität technisch ausschließen.

Bis dahin:
- echter einzelner Draft-Test mit menschlicher Prüfung ist zulässig
- keine Produktionsfreigabe
- kein Auto-Publish
- kein main-Merge
