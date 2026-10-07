# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-07
STATUS: V1.12.0 ZIELBAUM-BASELINE PASS / V1.12.3 ECHTE DATAFORSEO-EVIDENCE VORHANDEN / V1.12.5 KISS-GESAMTPFAD LOKAL HARD PASS / EINMALIGER LIVE-READBACK OFFEN / KEIN ZIELBAUM-DEPLOYMENT

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
`1.12.5`

Artefakt:
`HD001_V1.12.5_KISS_CONTENT_CAPACITY_ZERO_DEPTH_HARDPASS.zip`

SHA-256:
`68d521a9835bcbf2b2658dd0bd8d0a5163e6e1d656bf51855e20f830958a7af9`

Prüfbericht:
`HD001_V1.12.5_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`8a6768b4222dd086f3ff124579684feeed6f11f45f268d5596631de326002075`

### Was V1.12.5 fachlich korrigiert

Content Capacity ist wieder KISS:

- Fachlogik definiert die eigenständigen Artikelintents.
- Diese Intents werden pro unterster Kategorie gezählt.
- DataForSEO dient als SEO-Abgleich.
- Exaktes Core-Keyword-/Synonym-Evidence darf Dubletten zusammenführen.
- Eine fehlende exakte Longtail-Zeile löscht keinen fachlich eigenständigen Artikelintent.
- Keyword-Ideas-/Suggestions-Rohzeilen erzeugen niemals zusätzliche Artikel.
- der automatische 38-Call-Depth-Weg ist deaktiviert.

### Realer Evidence-Stand

Die echte V1.12.3-Datei enthält:
- 39 historische DataForSEO-Aufrufe;
- Kosten ca. 0.9738 USD;
- 0 Strukturwrites.

V1.12.5 benutzt diese vorhandene Evidence nur noch korrekt und startet beim Recalc keine neuen Provider-Aufrufe.

### Lokaler Replay des echten Ergebnisses

- Kandidaten: 16
- ideale Leafs: 34
- HOBBY_HUB_CANDIDATE: 1
- EDITORIAL_TOPIC_CANDIDATE: 1
- AGGREGATION_REVIEW: 5
- MACRO_REVIEW: 3
- EVIDENCE_REQUIRED: 6
- Zielbaum-Writes: 0

Kapazitätsseitig typischer Hubbereich:
- Airbrush: 5 ideale Leafs
- Bean-to-Bar-Schokolade: 6
- Aeroponik: 4
- Ameisenhaltung: 6
- 3D-Bogenschießen: 5
- Wabikusa: 4

Diese sechs bleiben wegen Scope-/Identitätsprüfung noch EVIDENCE_REQUIRED.

Buchbinden:
- 4 ideale Leafs;
- 5 / 6 / 6 / 6 fachlich eigenständige Intents;
- HOBBY_HUB_CANDIDATE.

### Hardtest

- PHP Source 68/68 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Lauf PASS;
- V1.12.1 Assessment Regression PASS;
- echter V1.12.3-Result-Replay PASS;
- fehlende exakte Provider-Zeilen blockieren fachlich tragfähige Leafs nicht PASS;
- exact core_keyword Dedupe PASS;
- Provider-Rohzeilen erzeugen 0 Artikel PASS;
- automatische Depth-Recherche = 0 Calls PASS;
- 0 neue Provider-Kosten PASS;
- 0 Strukturwrites PASS;
- Recalc idempotent PASS;
- Fresh Release PHP 31/31 PASS.

V1.12.5 ist weiterhin read-only Bewertungskandidat, kein Zielbaum-Deployment.

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

`HD001_V2_BATCH001_V125_SINGLE_LIVE_READBACK_PENDING`

Kein DataForSEO-Research-Schritt ist mehr offen.

Der gesamte Batch-001-Weg wurde mit der echten gespeicherten Evidence lokal bis zum Endzustand geprüft.

## EXAKT EINE NEXT ACTION

Einmal V1.12.5 in Hobby Depot installieren und `Kategorien → V2-Hobbybewertung` öffnen.

Das vorhandene Ergebnis muss automatisch und kostenlos nach Regelvertrag 1.4 neu berechnet werden.

Erwarteter Readback:
- 0 neue DataForSEO-Aufrufe;
- 0 neue Kosten;
- 0 Strukturwrites;
- Plugin 1.12.5;
- korrigierte Batch-Summary wie im lokalen Replay.

Danach Ergebnis-JSON einmal prüfen.

## Release-/Artefaktgrenze

V1.12.0 bleibt lokale technische Zielbaum-Baseline. V1.12.5 ist der aktuelle read-only Bewertungskandidat für genau einen realen Readback. Er ist kein Zielbaum-Deploymentkandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Der exakte V1.12-ZIP-Hash ist verifiziert, aber `CURRENT.zip` wurde in diesem Abschlusslauf NICHT ersetzt, weil der aktive GitHub-Toolpfad keinen direkten Binärtransfer aus dem lokalen Container bereitstellt. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten.
Kein altes V1.12-Profil installieren, bevor das V2-Zielbaum-Delta freigegeben und erneut vollständig getestet ist.
