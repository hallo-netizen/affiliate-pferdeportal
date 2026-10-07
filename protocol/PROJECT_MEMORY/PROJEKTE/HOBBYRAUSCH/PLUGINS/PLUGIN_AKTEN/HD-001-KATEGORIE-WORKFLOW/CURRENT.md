# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-07
STATUS: V1.12.0 ZIELBAUM-BASELINE PASS / V1.12.6 READ-ONLY V2-BEWERTUNG REAL PASS / EXPORT-GATE GESCHLOSSEN / KEIN ZIELBAUM-DEPLOYMENT

## Plugin

ID:
`HD-001-KATEGORIE-WORKFLOW`

Name:
`Affiliate-Portal Kategorie-Workflow`

Art:
Eigenentwicklung / allgemeingültiger Kategorie-Workflow mit Hobby-Depot-Profil.

Fachbüro:
`SEO_KATEGORIEN`

## Letzter autoritativ bestätigter Live-Stand

V1.9.9:
Buchbinden + vier Content-Kategorien + zugeordneter Testartikel real im Frontend bestätigt.

Für V1.12.0 existiert KEIN realer Hobby-Depot-Live-PASS.

## Aktuelle technische Basis

Plugin-Version:
`1.12.0`

Lokales Release-Artefakt:
`HD001_V1.12.0_FIXED_THREE_PILLAR_TARGET_TREE_POSNEG_HARDPASS.zip`

SHA-256:
`f77f676ef4e8df8d44e3cf0d1e61b52883d402924cb8d14033c24dd6645c03d1`

Lokaler Prüfbericht:
`HD001_V1.12.0_FINAL_LOCAL_POSNEG_REPORT.txt`

Der ZIP-Hash wurde am 2026-10-07 erneut aus dem vorhandenen Artefakt geprüft.
Plugin-Header und `APKW_VERSION` = `1.12.0`.

## Was V1.12.0 technisch beweist

- versioniertes 3-Säulen-Zielprofil;
- generischer Target-Tree-Runner;
- Soll/Ist-Sync;
- Add / Rename / Move;
- Merge/Alias-Unterstützung;
- Archive/Inaktiv statt Hard Delete;
- stabile IDs bei gleicher Objektidentität;
- atomare Aktivierung nach Write + Readback;
- Rollback bei Readback-Manipulation;
- Cross-Pillar Keyword-/Intent-Kannibalisierung fail-closed;
- UNKNOWN/NONE-Themen bleiben redaktionell erhalten;
- Treibholz/Treibholz sammeln dedupliziert;
- DataForSEO darf im Target-Tree-Weg Struktur nicht erzeugen/verschieben;
- generisches Nicht-Hobby-Profil lokal validiert.

Lokale Evidence aus dem exakten Release-Artefakt:
- PHP-Lint 55/55 PASS;
- Legacy Regression 270/270 PASS;
- V1.10 Portal-Suiten PASS;
- realer 908/844-Gesamtlauf PASS;
- 420/420 physische Zielobjekte Readback PASS;
- zweiter identischer Lauf: 0 Post-/Term-Writes;
- Add/Rename/Move mit ID-Erhalt PASS;
- Remove→Archive PASS;
- Rollback PASS;
- Buchbinden-Renderer/4 Leafs/stabile IDs PASS;
- Fresh-Unpack/ZIP-Integrität PASS.

## Aktueller V2-Bewertungskandidat

Plugin-Version:
`1.12.6`

Artefakt:
`HD001_V1.12.6_STALE_EXPORT_FAILCLOSED_HARDPASS.zip`

SHA-256:
`788b49529216555cba8cd74aae2a3a469f5f386e7ea2dc3d0449555910d55dca`

Prüfbericht:
`HD001_V1.12.6_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`c9442f08b722e93a24fee697cec09d77e67f1ad9cd23cda9067a5185e90b042e`

Zweck:
stale gespeicherte V1.12.3-Ergebnisse beim Export selbst fail-closed auf die KISS-Regel 1.4 neu berechnen.

Realer Readback vor Fix:
- hochgeladene Datei trägt weiterhin plugin_version 1.12.3;
- SHA-256 = `086456f70d8896c51a97a27f7dcdc29906ad90534f9322aa6f1f5a7b519d69ae`;
- damit kein V1.12.5-Recalc-Result, sondern der alte gespeicherte Stand.

Root Cause:
V1.12.5 recalculierte nur beim Rendern der Adminseite; der Download-Handler exportierte ungeprüft `last_result()`.

V1.12.6:
- Download-Gate recalculiert bei altem Ergebnis selbst;
- speichert das korrigierte Ergebnis;
- exportiert erst danach;
- bei Recalc-Fehler BLOCKED statt stale JSON;
- 0 Provider-Aufrufe;
- 0 neue Kosten;
- 0 Strukturwrites.

Lokaler direkter Download-Replay mit exakt der realen stale Datei:
- plugin_version 1.12.6;
- 34 ideale Leafs;
- 1 HOBBY_HUB_CANDIDATE;
- 1 EDITORIAL_TOPIC_CANDIDATE;
- 5 AGGREGATION_REVIEW;
- 3 MACRO_REVIEW;
- 6 EVIDENCE_REQUIRED;
- 0 Zielbaum-Writes.

Tests:
- PHP 31/31 PASS;
- ZIP-Integrität PASS;
- realer stale-Result-Download-Replay PASS;
- idempotenter zweiter Download PASS;
- kein Ergebnis → BLOCKED PASS.

V1.12.6 bleibt read-only Bewertungskandidat, kein Zielbaum-Deployment.

## Fachliche Fortschreibung NACH V1.12.0

Die V1.12.0-Technik bleibt Basis, aber das gebündelte Hobby-Depot-Zielprofil ist NICHT der endgültige neue Installationsbaum.

Nach V1.12.0 wurde verbindlich vorgeschaltet:
`HOBBY_MASTER V2`.

Neue fachliche Regeln:
- große bekannte Hobbys als wirtschaftliche Anker integrieren;
- mittlere Hobbys als Rückgrat;
- Nischen als SEO-/Longtail-Stärke;
- großer interner Bestand, kleine sichtbare Navigation;
- Rollen ORIENTATION_UNIVERSE / HOBBY_HUB / EDITORIAL_TOPIC / ARTICLE_ONLY / FINDER_ONLY / OUT_OF_SCOPE;
- Größenprüfung vor Zielbaum;
- Monetarisierung beeinflusst CORE-Priorität, nicht Erhalt;
- DataForSEO ist SEO-Evidenz, keine Strukturautorität;
- acht Hauptwelten sind oberste fachliche CORE-Ebene.

## Bekannter V1.12-Profilfehler gegenüber der neuen Fachregel

Das V1.12-Hobby-Profil modelliert:
`core:hub (Hobbywelten) → core:world:gestalten/fertigen/...`

Das ist fachlich inzwischen verworfen.

Verbindlich:
Die acht Welten sind CORE-Ebene 1.
`Hobbywelten` ist nur Übersicht/View/Einstieg und kein Parent.

Dieser Fehler wird NICHT durch manuelles Patchen des alten Livebaums gelöst, sondern im späteren V2-Zielbaum-Delta.

## ERSTER OFFENER BLOCKER

Kein technischer Plugin-Blocker für Batch 001.

V1.12.6 ist real bestätigt:
- Recalc COMPLETE;
- 0 neue Provider-Aufrufe;
- 0 neue Kosten;
- 0 Strukturwrites;
- Export liefert den korrigierten Stand.

Der offene Punkt liegt jetzt fachlich außerhalb des Plugin-Gates:
`HD001_V2_BATCH001_SCOPE_IDENTITY_OWNERSHIP_REVIEW_PENDING`.

## EXAKT EINE NEXT ACTION

Keine weitere Plugin-Änderung.

Fachprüfung der sechs EVIDENCE_REQUIRED-Hubfälle fortsetzen.

## Release-/Artefaktgrenze

V1.12.0 bleibt lokale technische Zielbaum-Baseline. V1.12.6 ist der aktuelle read-only Bewertungskandidat für genau einen realen Export-Readback. Er ist kein Zielbaum-Deploymentkandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Der exakte V1.12-ZIP-Hash ist verifiziert, aber `CURRENT.zip` wurde in diesem Abschlusslauf NICHT ersetzt, weil der aktive GitHub-Toolpfad keinen direkten Binärtransfer aus dem lokalen Container bereitstellt. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten.
Kein altes V1.12-Profil installieren, bevor das V2-Zielbaum-Delta freigegeben und erneut vollständig getestet ist.
