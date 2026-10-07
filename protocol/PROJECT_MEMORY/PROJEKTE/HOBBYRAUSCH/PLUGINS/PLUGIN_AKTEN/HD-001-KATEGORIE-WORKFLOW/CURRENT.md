# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-07
STATUS: V1.12.0 ZIELBAUM-BASELINE PASS / V1.12.1 INITIALER REALER BATCH PASS / V1.12.2 READ-ONLY TIEFENPRÜFUNG LOKAL HARD PASS / REALER DEPTH-LAUF OFFEN / KEIN ZIELBAUM-DEPLOYMENT

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

### Reale V1.12.1-Ausführung

V1.12.1 wurde in Hobby Depot real ausgeführt.

Ergebnis:
- Batch 001;
- 16 Hobbys;
- 34 fachlich vorgeschlagene Leafs;
- 263 vorgeschlagene Artikelintents;
- 1 realer DataForSEO Keyword-Overview;
- 106 / 263 exakte Keywords returned;
- 157 exakte Seeds PENDING;
- Kosten 0.02472 USD;
- 0 WordPress-/HivePress-Strukturwrites;
- Result SHA-256 `5857319ea29c2477159c9eddefe691e7a6e5fdb0d0c8161314f75b1474b51fe9`.

Befund:
Der erste Overview reicht für die vollständige V2-Content-Capacity nicht aus.
`0 Hub-Kandidaten` ist deshalb kein endgültiger Negativbefund.

### V1.12.2 – fehlende Tiefenprüfung

Plugin-Version:
`1.12.2`

Artefakt:
`HD001_V1.12.2_V2_DATAFORSEO_DEPTH_READONLY_HARDPASS.zip`

SHA-256:
`233f3b5a71f6080d98e8748795cedb0b684c5e1a16407ec509919fa3d1f7e17f`

Prüfbericht:
`HD001_V1.12.2_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`1e7197feb74e9b3a070a4201f79a0416f46dfef960fdab556d59f21c4cb55048`

Funktion:
- erkennt das gespeicherte V1.12.1-Ergebnis;
- wiederholt den bereits bezahlten Gesamt-Overview NICHT;
- ermittelt exakt 37 noch offene, bereits fachlich definierte Depth-Cluster;
- plant exakt 37 Keyword-Ideas-Aufrufe;
- danach exakt 1 gebündelten Keyword-Overview;
- insgesamt exakt 38 zusätzliche DataForSEO-Aufrufe;
- übernimmt je Cluster höchstens 15 distinct Intent/Core-Keyword-Gruppen, weil ab etwa 15 ohnehin Split-Review erreicht ist;
- kombiniert alte und neue Evidence;
- dedupliziert erneut per Core Keyword;
- berechnet Batch-Ownership-Überschneidungen erneut;
- schreibt 0 Kategorien und 0 Zielbaumobjekte.

Fresh-Unpack-Test:
- PHP 62/62 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Lauf PASS;
- V1.12.1 Assessment Regression PASS;
- echter hochgeladener Batch-001-Result-Readback PASS;
- Follow-up-Plan exakt 38 Calls PASS;
- DataForSEO-Failure fail-closed PASS;
- 0 Strukturwrites PASS.

V1.12.2 ist weiterhin nur Bewertungskandidat, kein Zielbaum-Deployment.

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

`HD001_V2_BATCH001_DEPTH_DATAFORSEO_RUN_PENDING`

Der reale Initiallauf ist abgeschlossen.
Der noch fehlende Teil ist die laut Regelvertrag 1.2 notwendige Tiefenprüfung der 37 unvollständig belegten, bereits definierten Cluster.

## EXAKT EINE NEXT ACTION

V1.12.2 in Hobby Depot installieren und unter `Kategorien → V2-Hobbybewertung` die zusätzliche Tiefenprüfung ausführen.

Vor dem Paid Run muss das Plugin exakt anzeigen:
- 37 Keyword-Ideas-Aufrufe;
- 1 gebündelten Keyword-Overview;
- 38 zusätzliche DataForSEO-Aufrufe insgesamt.

Danach neues Ergebnis-JSON herunterladen und fachlich prüfen.

Kein Zielbaum-Write.
Keine WordPress-/HivePress-Kategorieänderung.

## Release-/Artefaktgrenze

V1.12.0 bleibt lokale technische Zielbaum-Baseline. V1.12.1 ist der aktuelle read-only Bewertungskandidat und darf installiert werden, um Batch 001 real mit DataForSEO zu prüfen; er ist kein Zielbaum-Deploymentkandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Der exakte V1.12-ZIP-Hash ist verifiziert, aber `CURRENT.zip` wurde in diesem Abschlusslauf NICHT ersetzt, weil der aktive GitHub-Toolpfad keinen direkten Binärtransfer aus dem lokalen Container bereitstellt. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten.
Kein altes V1.12-Profil installieren, bevor das V2-Zielbaum-Delta freigegeben und erneut vollständig getestet ist.
