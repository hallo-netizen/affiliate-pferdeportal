# TEXTSYSTEM 4A – ZIELVERTRAG

STAND: 2026-09-13
STATUS: VERBINDLICH FÜR DEN ISOLIERTEN 4A-PROTOTYP

## Ziel

Konzept 4a soll denselben fachlichen Qualitätsstandard wie die bestehende Pferde-Atelier-Produktion mit einer universellen, möglichst kleinen Laufzeitarchitektur ausführen.

## Unveränderlich

- Inhaltliche Regeln bleiben unverändert.
- Design bleibt unverändert.
- Qualitätsprüfer bleiben unverändert und alleinige PASS-Autorität.
- Kein Auto-Publish.
- Kein Einfluss von außen auf Route, Regeln, nächsten Schritt oder Toolchain.
- Kein zweiter Workflow-Besitzer neben dem 4a-Controller.

## Architekturziel

`1 Controller + N unabhängige Artikelkapseln + bestehende reale Prüfer als reine Aufrufe + 1 finaler Ausgang`

Eine Kapsel enthält dauerhaft die Identität und den belegten Zustand genau eines Artikels. Prüfer dürfen Ergebnisse liefern, aber weder Kapselzustand noch Route selbst verändern.

## Flexibilitätsziel

Der Controller darf weder konkrete Artikelzahl noch Beitragsart hardcoden. Neue freigegebene Beitragsarten werden ausschließlich durch bestehende autoritative Beitragsart-/PPM-/Textregeln erkannt. Fehlt eine autoritative Freigabe, wird fail-closed blockiert.

## Automatisierungsziel

Nach gültigem Produktionsanstoß läuft die Kette ohne manuelle Chatnavigation bis entweder:
- konkretes fail-closed BLOCK/FAIL mit erster Ursache, oder
- finale geprüfte WordPress-Importdatei.

Reparaturen bleiben innerhalb derselben Artikelkapsel. Kein Neustart des Gesamtworkflows wegen eines reparierbaren Einzelartikelfehlers.

## Skalierungsziel

Architektonisch identischer Weg für 1, 3, 25, 1000 und darüber hinaus. Batch ist nur eine Sammlung unabhängiger Kapseln, keine gemeinsame fachliche Zustandsmaschine.

## Finaler Dateivertrag

Die finale Datei muss mindestens enthalten bzw. nachweisbar binden:
- Batch-/Snapshot-Identität;
- `publish_allowed=false`;
- WordPress-Direct-Import-Ziel und verifizierte Importer-Version;
- pro Artikel: `title`, `target_keyword`, `category`, `article_type`, `plan_slot`, finaler Body, Body-Hash, Revision, gebundener Produktionskontext/Fact-Pack und echte Prüfnachweise;
- artikelübergreifende Freigabe;
- exakt dieselben final geprüften Artikelbytes.

Kein fester Artikelcount und keine feste Beitragsart im Schema.

## Abbruchkriterium

4a wird verworfen, wenn es gegenüber dem aktuellen System 4 keine nachweisbare Reduktion echter Laufzeitgrenzen bringt oder dafür vorhandene Fach-/Design-/Qualitätsautoritäten duplizieren müsste.
