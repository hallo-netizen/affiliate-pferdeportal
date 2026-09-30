# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN OWNERSHIP LOKAL PASS / HD-001 V1.9.1 + EIGENES HD-002 V0.1.0 VERKETTBAR / PROBLEME + FAQ DATENLÜCKE / LIVE-ABNAHME OFFEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_KONZEPT`.

## Aktueller belastbarer Stand

Aktueller Markenname: **Hobby Depot**.

Hauptwelten:
**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln**

Harte Tiefe:
**SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE**

Buchbinden-Pilot:
**Fertigen → Buch & Papier → Buchbinden**

Owner-Regel:
**Ein Beitrag = ein primärer Intent = ein eindeutiger Kategorie-Owner.**

Bereiche:
- Einstieg;
- Ausrüstung;
- Material;
- Techniken/Praxis;
- Fragen/Probleme;
- FAQ nur für belegte Restintents.

**Eine Frageform erzeugt niemals automatisch FAQ-Ownership.**

## Technische Umsetzung

### HD-001
Kategorie-Workflow V1.9.1 liefert den allgemeinen Editorial-Ownership-Handoff.

### HD-002
Eigenes Hobby-Depot Text-/SEO-Plugin:
`Hobby Depot SEO Themenengine V0.1.0`

Keine Abhängigkeit vom Pferdeatelier-PSTE.

HD-002:
- eigener Namespace/Speicher;
- liest V1.9.1-Handoff;
- bindet `owner_concept_id`;
- verlangt `semantic_intent_key`;
- blockiert semantische Dubletten/Owner-Sprünge fail-closed;
- erlaubt neue eigenständige Intents;
- Frageform besitzt keine FAQ-Autorität.

Lokale Prüfung:
- Ownership 11/11 PASS;
- Frage≠FAQ 12/12 PASS;
- Family 8/8 PASS;
- Projektgrenze PASS;
- paralleler Boot neben PSTE ohne Kollision PASS.

## Buchbinden-Datenstand

Vorhandene DataForSEO-Evidenz:
- Einstieg: vorhanden;
- Ausrüstung: vorhanden;
- Material: Mindestbreite vorhanden;
- Techniken/Praxis: vorhanden;
- Fragen/Probleme: DATA GAP;
- FAQ: DATA GAP.

FAQ darf nicht künstlich aufgefüllt werden.

## Erster offener Blocker

Kein lokaler Architektur- oder Ownership-Blocker.

Offen:
1. Live-Abnahme HD-001 → HD-002;
2. gezielte Nachrecherche für Fragen/Probleme und echte FAQ-Restintents.

## NEXT ACTION

Keine weitere Pluginarchitektur bauen.

Vor Installation HD-002 nur noch aktuellen Storage-/Performance-Referenzdelta prüfen.

Danach:
HD-001 live abnehmen → HD-002 installieren → Handoff importieren → Buchbinden E2E → fehlende Research-Räume gezielt nachrecherchieren.
