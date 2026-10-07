# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-07
STATUS: V1.12.0 ZIELBAUM-BASELINE PASS / V1.12.1 READ-ONLY V2-BEWERTUNG LOKAL HARD PASS / NICHT LIVE ABGENOMMEN / REALER WORDPRESS-DATAFORSEO-BATCHLAUF OFFEN / KEIN ZIELBAUM-DEPLOYMENT

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
`1.12.1`

Artefakt:
`HD001_V1.12.1_HOBBY_MASTER_V2_READONLY_ASSESSMENT_HARDPASS.zip`

SHA-256:
`959bc80217aac9b90ac107e6b315908b084704d09777ae9be990c2825245d33d`

Prüfbericht:
`HD001_V1.12.1_FINAL_LOCAL_POSNEG_REPORT.txt`

Zweck:
ausschließlich HOBBY_MASTER-V2-Bewertung im echten WordPress mit dem vorhandenen DataForSEO-Zugang.

Neu:
- eigener Backendpunkt `Kategorien → V2-Hobbybewertung`;
- gebündelter kontrollierter Batch 001;
- 16 Hobbys / 34 vorgeschlagene Leafs / 263 Artikelintents;
- exakt 1 DataForSEO Keyword-Overview-Aufruf;
- DataForSEO-Dedupe über `core_keyword`;
- Batch-übergreifende Intent-/Ownership-Overlap-Markierung;
- Konzeptgrenzen exakt: <4 zusammenlegen, 5–12 ideal, ab etwa 15 Teilung prüfen;
- kleine valide Hobbys bleiben Identitäten und können gemeinsam dargestellt werden;
- Target-Tree-Autorun deaktiviert;
- manueller Target-Tree-Refresh blockiert;
- 0 WordPress-/HivePress-Strukturwrites im Bewertungslauf.

Fresh-Unpack-Test:
- PHP-Lint 59/59 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Bestand PASS;
- V1.12.1 V2-Grenz-/Negativsuite PASS.

V1.12.1 ist ausdrücklich KEIN neuer Zielbaum und kein Live-PASS.

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

`HD001_V2_BATCH001_WORDPRESS_DATAFORSEO_RUN_PENDING`

Der read-only V2-Bewertungslauf ist technisch fertig und lokal hart geprüft.

Es fehlt nur noch die echte Ausführung in Hobby Depot:
V1.12.1 installieren → `Kategorien → V2-Hobbybewertung` → Batch 001 vorprüfen → exakt 1 DataForSEO-Aufruf bestätigen → Ergebnis-JSON herunterladen.

Keine Kategorien werden geschrieben.
Der alte V1.12-Zielbaum-Runner ist in V1.12.1 absichtlich deaktiviert.

## EXAKT EINE NEXT ACTION

Das exakte V1.12.1-Artefakt in Hobby Depot installieren und den gebündelten Batch 001 real über den vorhandenen WordPress-/DataForSEO-Zugang ausführen.

Danach Ergebnis fachlich gegen Regelvertrag 1.2 auswerten.
Erst danach weitere Masterbewertung und später Zielbaum-Delta.

## Release-/Artefaktgrenze

V1.12.0 bleibt lokale technische Zielbaum-Baseline. V1.12.1 ist der aktuelle read-only Bewertungskandidat und darf installiert werden, um Batch 001 real mit DataForSEO zu prüfen; er ist kein Zielbaum-Deploymentkandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Der exakte V1.12-ZIP-Hash ist verifiziert, aber `CURRENT.zip` wurde in diesem Abschlusslauf NICHT ersetzt, weil der aktive GitHub-Toolpfad keinen direkten Binärtransfer aus dem lokalen Container bereitstellt. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten.
Kein altes V1.12-Profil installieren, bevor das V2-Zielbaum-Delta freigegeben und erneut vollständig getestet ist.
