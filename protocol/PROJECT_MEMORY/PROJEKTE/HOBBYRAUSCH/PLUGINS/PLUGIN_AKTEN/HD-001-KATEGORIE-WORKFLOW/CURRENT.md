# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-07
STATUS: V1.12.0 LOKAL FULL POS/NEG PASS ALS TECHNISCHE BASIS / NICHT LIVE ABGENOMMEN / V2-REGELN 1.1 PRO LEAF + ZUSAMMENFASSUNG GEBUNDEN / DATAFORSEO-BATCHABGLEICH OFFEN / KEIN DEPLOYMENTAUFTRAG

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

`HD001_V2_BATCH001_HD001_ASSESSMENT_RUN_NOT_BOUND`

Die V2-Fachregeln wurden gegen das vollständige Konzept nachgeschärft:
- 5–12 distinct Artikelintents müssen pro unterster Kategorie belegt sein;
- kleine valide Hobbys dürfen fachlich sinnvoll zusammengefasst werden, ihre Identität bleibt getrennt;
- DataForSEO bleibt reine SEO-/Intent-Evidenz.

Batch 001 ist fachlich vorbereitet.
Ein exakter DataForSEO-Request ist gebunden.

Der vorhandene reale Buchbinden-DataForSEO-Befund ergibt aktuell 4 / 5 / 3 / 4 distinct Gruppen in den vier aktiven Leafs.
Damit bleibt Buchbinden als bestehender Live-/Technikpilot unangetastet, ist aber nach V2 noch kein finaler Hub-PASS.

Für die übrigen Batch-Fälle fehlt der reale DataForSEO-Abgleich.

## EXAKT EINE NEXT ACTION

Keine Pluginänderung und kein Deployment starten.

Zuerst im Scope `SEO_KATEGORIEN` den vorbereiteten Batch-001-DataForSEO-Request im HD-001-WordPress-Plugin als read-only V2-Bewertungslauf ausführen und danach Leaf-Kapazität, Ownership und mögliche Zusammenfassung erneut bewerten.

Erst nach abgeschlossener Masterbewertung und Zielbaum-Delta wird V1.12.0 technisch gegen das neue Zielprofil fortgeschrieben und erneut vollständig POS/NEG getestet.

## Release-/Artefaktgrenze

V1.12.0 ist lokale technische Baseline, kein aktueller Hobby-Depot-Deploymentkandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Der exakte V1.12-ZIP-Hash ist verifiziert, aber `CURRENT.zip` wurde in diesem Abschlusslauf NICHT ersetzt, weil der aktive GitHub-Toolpfad keinen direkten Binärtransfer aus dem lokalen Container bereitstellt. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten.
Kein altes V1.12-Profil installieren, bevor das V2-Zielbaum-Delta freigegeben und erneut vollständig getestet ist.
