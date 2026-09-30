# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: V1.9.1 LIVE-STAGE-TEST PASS / BUCHBINDEN PRODUKTIONS-DRAFT POSITIV+NEGATIV SIMULIERT / PRODUKTIVIMPORT NÄCHSTES

## Aktueller belastbarer Stand

### V1.9.1 Kategorie-Workflow

Lokale Vollprüfung:
- 248/248 PASS;
- Fresh-Unpack PASS;
- PHP-Lint Source/Installer PASS;
- Runtime-Parität PASS.

Live-Test:
- alten Deployment-Testlauf vollständig zurückgerollt;
- READ_ONLY_PREVIEW erneut übernommen;
- finale Struktur freigegeben;
- WordPress-Vorschau erstellt;
- Testdeployment durchgeführt;
- vollständiger Rollback PASS.

Damit ist der frühere Stage-/Stale-Deployment-Fehler live nicht erneut aufgetreten.

### Harte Abnahmeregel

Ab jetzt gilt für diesen Scope:

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

Nur Syntax-/Schema-PASS genügt nicht.

## Buchbinden Produktions-Pilot

Datei:
`HOBBY_DEPOT_BUCHBINDEN_PRODUKTIONS_PILOT_RESEARCH_DRAFT_POSNEG_PASS.json`

SHA-256:
`0458b11769e17af1214e0adcd10f50e1eff5604bd50e6b78334795279bec88d1`

Korrigierter Source-Binding-Wert:
`https://www.hobby-depot.de`

Der vorherige Kandidat mit `https://hobby-depot.de` war falsch und wurde live mit `SOURCE_SITE_MISMATCH` blockiert.

### Positivsimulation

Exakter Produktiv-Draft gegen denselben V1.9.1-Import-/Preflight-Code:
- VALID;
- 0 Errors;
- 0 Warnings.

### Negativsimulation

Alle erwartungsgemäß BLOCKED:
- falsche Site → `SOURCE_SITE_MISMATCH`;
- doppelter Intent-Key → `INTENT_KEY_DUPLICATE`;
- fehlender Parent → `PARENT_NOT_FOUND`;
- ungültiger Target-Adapter → `TARGET_ADAPTER_INVALID`;
- falscher Modus → `PREFLIGHT_MODE_INVALID`.

Evidence:
`BUCHBINDEN_PRODUKTIONS_PILOT_POS_NEG_EVIDENCE.json`

Zusätzlicher kompletter V1.9.1-Regressionslauf:
**248/248 PASS**

Evidence:
`V191_FULL_SUITE_RECHECK_248_PASS.txt`

## Beleggrenze

Der korrigierte Buchbinden-Draft ist lokal positiv/negativ simuliert, aber noch nicht live importiert.

## NEXT ACTION

Genau den korrigierten Buchbinden-Produktions-Draft in `Kategorien` übernehmen.

Danach den normalen Workflow weiterführen.

Bei irgendeinem BLOCKED/Fehler:
keine Abnahme, sondern Fehler lokal reproduzieren → Positiv-/Negativsimulation → erst danach neuer Kandidat.
