# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-07
STATUS: V1.12.0 ZIELBAUM-BASELINE PASS / V1.12.3 REALER DEPTH-LAUF KOMPLETT / FREMDTREFFER-ZÄHLFEHLER ERKANNT / V1.12.4 ZERO-COST-RECALC LOKAL HARD PASS / KEIN ZIELBAUM-DEPLOYMENT

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
`1.12.4`

Artefakt:
`HD001_V1.12.4_V2_RELEVANCE_RECALC_ZERO_COST_HARDPASS.zip`

SHA-256:
`5ceffaa03eda90b45a235cf844ff2ddae3bef553f2a61f4ec32ea38eefcf75f6`

Prüfbericht:
`HD001_V1.12.4_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`6b8938a5a5b46b1876a564f69f26f60048963e1fc1e5edbd879b7531bc643bb3`

Zweck:
bereits bezahltes V1.12.3-Ergebnis korrekt neu auswerten.

KISS-Regel:
- Artikelintents kommen aus der Fachlogik;
- DataForSEO bestätigt/vereinigt/dedupliziert;
- Keyword-Ideas-Rohzeilen erzeugen keine zusätzlichen Artikel;
- nur passende Depth-Treffer dürfen einen bereits vorhandenen PENDING-Intent bestätigen;
- keine neuen Provider-Aufrufe;
- keine neuen Kosten;
- keine Strukturwrites.

Realer Result-Replay:
- 541 gespeicherte Depth-Gruppen;
- 2 echte Matches auf bisher PENDING fachliche Artikelintents;
- 539 Rohgruppen zählen NICHT als neue Artikel;
- DataForSEO-Calls bleiben 39;
- Kosten bleiben ca. 0.9738 USD;
- Zielbaum-Writes bleiben 0.

Fresh-Unpack:
- PHP 66/66 PASS;
- Legacy 270/270 PASS;
- Relevanz-/Fremdkeywordtest PASS;
- realer V1.12.3-Result-Replay PASS;
- 0 neue Calls PASS;
- 0 neue Kosten PASS;
- 0 Strukturwrites PASS.

V1.12.4 ist weiterhin nur Bewertungskandidat.

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

`HD001_V2_BATCH001_V124_ZERO_COST_RECALC_PENDING`

Die DataForSEO-Recherche ist komplett.
Offen ist nur die korrigierte Neuberechnung derselben gespeicherten Evidence.

## EXAKT EINE NEXT ACTION

V1.12.4 in Hobby Depot installieren und einmal `Kategorien → V2-Hobbybewertung` öffnen.

Die Seite korrigiert das gespeicherte COMPLETE-Ergebnis automatisch:
0 Calls / 0 neue Kosten / 0 Strukturwrites.

Danach neues Ergebnis-JSON herunterladen und fachlich prüfen.

## Release-/Artefaktgrenze

V1.12.0 bleibt lokale technische Zielbaum-Baseline. V1.12.1 ist der aktuelle read-only Bewertungskandidat und darf installiert werden, um Batch 001 real mit DataForSEO zu prüfen; er ist kein Zielbaum-Deploymentkandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Der exakte V1.12-ZIP-Hash ist verifiziert, aber `CURRENT.zip` wurde in diesem Abschlusslauf NICHT ersetzt, weil der aktive GitHub-Toolpfad keinen direkten Binärtransfer aus dem lokalen Container bereitstellt. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten.
Kein altes V1.12-Profil installieren, bevor das V2-Zielbaum-Delta freigegeben und erneut vollständig getestet ist.
