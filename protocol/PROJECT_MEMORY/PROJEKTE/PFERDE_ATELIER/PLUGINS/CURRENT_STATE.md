# PLUGINS – CURRENT STATE

## TEXT-/SEO-PLUGIN-DELTA 2026-10-01

Dieser Block ist Inventar-/Betriebsreadback; Fach-/Releaseautorität bleibt im TEXT-Bereich bzw. technischer Originalquelle.

- Portal SEO Redaktionsplan Compiler: im aktuellen Arbeitsstrang wurde **0.28.30** installiert; der zunächst weiter bestehende `PSERC_SEO_CAPABILITY_BINDING_BLOCKED` verschwand erst nach anschließendem PSTE-Austausch. Der spätere reale PSERC-Lauf erreichte `COMPLETE`.
- Portal SEO Themenengine: im aktuellen Arbeitsstrang wurde der neu nummerierte **0.57.17**-Reinstall-Kandidat installiert; danach erreichte der reale PSERC/Snapshot-Weg `COMPLETE`. Diese Aussage stützt sich auf den Nutzer-Installationsschritt + nachfolgenden erfolgreichen Workflow, nicht auf einen separat archivierten Pluginlisten-Screenshot.
- Danach lokal gebaut: **PSTE 0.57.18 – EXISTING POTENTIAL FIRST**. Dieser Kandidat ist **nicht als live installiert belegt** und darf nicht als aktueller Live-Stand ausgegeben werden.
- 0.57.18 ist nur ein Teilfix: sichere `AUTO_REENTRY_ELIGIBLE`-Sandbox-Kandidaten vor Retained Backlog/Provider verwerten. Er ändert die bereits vorhandene Titel-/Familien-/Kategorie-Automatik nicht.
- Der offene Verwertungsfehler liegt fachlich im TEXT-Bereich: zu wenige gespeicherte Kandidaten erreichen trotz vorhandener Auto-Editorialisierung planning-ready/READY. Routing: `../TEXT/CURRENT_STATE.md`.
- Die bereits laufende Recherchewelle wird nicht für einen Pluginwechsel unterbrochen.


STAND: 2026-10-01
STATUS: AFFILIATE 6.72.171 LIVE / 6.72.172 IDEALO-STORAGE-HANDOFF VERIFIZIERT / BACKUPS BEREINIGT / DB-VERSCHLANKUNG OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des PLUGINS-Büros.

- aktueller belastbarer Stand, erster offener Punkt und genau eine NEXT ACTION → diese Datei
- `HOBBYRAUM.md` → nur temporäre Ausführungsfläche, keine eigene Status-/NEXT-ACTION-Autorität
- vollständiger beobachteter Pluginbestand → `PLUGINREGISTER.md`
- Update-Chronik → `UPDATEPROTOKOLL.md`
- Update-/Pflegeregeln → `REGELWERK.md`
- Fach-/Release-/LIVE-Status → zuständiges Fachbüro / technische Originalquelle
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- dauerhaftes WAS/WARUM → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

## REALER WORDPRESS-READBACK 2026-09-30 – AKTUELLER BETRIEBSSTAND

Quelle: vom Nutzer bereitgestellte aktuelle WordPress-Liste „Plugins → Installierte Plugins“. Dieser Block ist Inventar-/Betriebsreadback, keine eigenständige Fach- oder Releasefreigabe.

Aktuell beobachtet:
- Affiliate Portal Template Kit (Pferde-kompatibel): **1.50.578**, aktiv.
- Affiliate-Zentrale (Portal-kompatibel): **6.72.171**, aktiv; Nutzer bestätigt am 01.10.2026 ausdrücklich, dass die Performance-Diagnose 10:30–10:31 UTC unter 6.72.171 lief. Der reale Performance-Readback ist PASS.
- Performance Diagnose Safe: **2.3.0 aktiv**; ältere **2.2.0 inaktiv**.
- Pferde Atelier – Affiliate Design Performance: **3.0.0 inaktiv**.
- Portal Production Machine: **6.7.9**, aktiv.
- Portal SEO Redaktionsplan Compiler: **0.28.27**, aktiv.
- Portal SEO Themenengine: **0.57.13**, aktiv.

Der frühere Kategorie-Stand weiter unten bleibt historische Scope-Dokumentation und darf diese reale Inventarbeobachtung nicht überschreiben.

## AKTIVER ZIELVERTRAG

Autoritative Zielquelle:
`protocol/PROJECT_MEMORY/ZIELVERTRAEGE/ZV-PLUGINS-CLEANUP-001.md`

Dauerhafte Arbeitsentscheidung/Warum:
`protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md` → `PLUGINS-001`.

Diese Current-Datei kopiert den Zielinhalt nicht; sie bindet nur aktuellen Stand, ersten offenen Punkt und NEXT ACTION.

## FRISCHE STORAGE-BASELINE 2026-10-01 11:13–11:15 UTC

Quelle: realer WordPress-Export `wordpress-speicheranalyse-20261001-111515.json`, vollständig `done=true`.

- gescannte Dateien gesamt: **16.879.899.578 Bytes**
- `wp-content/ai1wm-backups`: **13.295.750.128 Bytes**, 7 Dateien; darin zwei große `.wpress`-Backups:
  - 01.10.2026: **7.264.453.820 Bytes**
  - 29.09.2026: **6.031.295.633 Bytes**
- `wp-content/wpvividbackups`: **2.109.325.928 Bytes**, 100 Dateien
- `wp-content/uploads`: **1.042.403.409 Bytes**
- darin fünf `ppar-idealo-feed-*.tmp`: zusammen **749.350.091 Bytes**
- vier dieser idealo-TMP-Dateien waren bereits im 29.09.-Baselinebericht mit identischem Namen/Größe vorhanden; damit sind liegengebliebene Tempdateien real belegt.
- Affiliate 6.72.171 löscht den jeweils normalen idealo-Downloadpfad bei Erfolg/HTTP-Fehlern, aber der zentrale Housekeeping-Disk-Pass räumt aktuell nur `ppar-affiliate-product-images` auf und erfasst verwaiste `ppar-idealo-feed-*.tmp` im Upload-Root nicht. Das ist ein belegter Zukunftsschutz-Gap, kein Grund für pauschale Dateilöschung.
- Datenbank gesamt: **1.561.968.640 Bytes** gegenüber 1.576.435.712 Bytes am 29.09. (**-14.467.072 Bytes / ca. -0,9 %**)
- `slfo_options`: **410.746.880 Bytes** (vorher 421.232.640)
- `slfo_pste_candidates`: **409.108.480 Bytes** (unverändert)
- `slfo_pste_runs`: **366.510.080 Bytes** (unverändert)
- `slfo_pste_topic_pool`: **114.311.168 Bytes** (leicht kleiner)
- `slfo_ppar_ebay_items`: **103.219.200 Bytes** (unverändert)
- Autoload: **260.941 Bytes**; kein Autoload-Großproblem.
- TEXT-Autorität meldet laufenden PSTE-Kontextabgleich. Deshalb aktuell **keine PSTE-Themen-/Sandbox-/Run-Daten löschen oder umklassifizieren**.

Aktuell größter sicher trennbarer Hebel ist lokaler Backupbestand. Das alte All-in-One-Backup vom 29.09. plus der verbleibende WPvivid-Bestand belegen bereits **8,14 GB** potentiell entfernbaren lokalen Backup-Speicher, aber irreversible Löschung erst nach extern gesichertem aktuellen Rollback.

ERSTER OFFENER PUNKT:
**Aktuelles 01.10.-All-in-One-Backup extern sichern/verifizieren; erst dann alte lokale Backupbestände löschen. PSTE-Daten bleiben bis zum laufenden Kontext-Refresh-COMPLETE unberührt.**

GENAU EINE NEXT ACTION:
`SECURE_CURRENT_AIO_BACKUP_OFFSERVER_THEN_PURGE_OLD_LOCAL_BACKUPS`.

Danach als gebundener Folgepunkt: genau einen Affiliate-Zentrale-Storagefix für verwaiste `ppar-idealo-feed-*.tmp` bauen/hart positiv-negativ-regressiv testen und erst danach die belegten Alt-TMPs bereinigen. Keine Plugin-Orgie und kein separater Hilfsrunner.

## STORAGE-READBACK NACH BACKUP-LÖSCHUNG 2026-10-01 11:24–11:25 UTC

Quelle: realer WordPress-Export `wordpress-speicheranalyse-20261001-112548.json`, vollständig `done=true`.

- Gesamtscan: **3.584.150.125 Bytes** statt 16.879.899.578 Bytes vorher.
- Differenz: **-13.295.749.453 Bytes**.
- `wp-content/ai1wm-backups`: nur noch **675 Bytes / 5 Kleinstdateien** statt 13.295.750.128 Bytes.
- Damit wurden die großen All-in-One-`.wpress`-Backups vollständig aus dem lokalen Serverbestand entfernt.
- `wp-content/wpvividbackups`: weiterhin **2.109.325.928 Bytes / 100 Dateien**, unverändert.
- `wp-content/uploads`: weiterhin **1.042.403.409 Bytes**, unverändert.
- fünf `ppar-idealo-feed-*.tmp`: weiterhin **749.350.091 Bytes**, unverändert.
- Datenbank: weiterhin **1.561.968.640 Bytes**, unverändert.
- Schlussfolgerung: bisherige Einsparung stammt praktisch vollständig aus der All-in-One-Backup-Löschung; WPvivid, Idealo-TMP und DB sind noch offen.

ERSTER OFFENER PUNKT:
**WPvivid-Altbestand 2,109 GB ist noch vollständig vorhanden.**

GENAU EINE NEXT ACTION:
`PURGE_WPVIVID_LOCAL_BACKUPS`.

Danach: Affiliate-Temp-Zukunftsschutz + Alt-TMP-Bereinigung, Bildoptimierungsblock, anschließend DB-Retention/DB-Verschlankung und physische Reorganisation.

## STORAGE-READBACK NACH WPVIVID-BEREINIGUNG + IDEALO-ZUKUNFTSSCHUTZ 2026-10-01

Realer WordPress-Speicherexport `wordpress-speicheranalyse-20261001-114840.json`, vollständig `done=true`:
- Gesamtscan: **1.475.744.045 Bytes**;
- `wp-content/ai1wm-backups`: **675 Bytes**;
- `wp-content/wpvividbackups`: **919.848 Bytes / 77 Dateien**, überwiegend verbleibende Logdateien; die alten Backup-Payloads sind physisch entfernt;
- `wp-content/uploads`: **1.042.403.409 Bytes**;
- fünf `ppar-idealo-feed-*.tmp`: weiterhin **749.350.091 Bytes**;
- Datenbank weiterhin **1.561.968.640 Bytes**; Datenbank-Verschlankung ist noch nicht ausgeführt.

Affiliate-Zentrale:
- Live bleibt **6.72.171** bis zu neuem WordPress-Readback.
- Kandidat **6.72.172** schließt ausschließlich den belegten Idealo-Temp-Retention-Gap im bestehenden Housekeeping.
- lokaler Positiv-/Negativtest: PASS;
- kompletter Housekeeping-Disk-Durchlauf: PASS;
- exakter Handoff-Installer `AFFILIATE_ZENTRALE_6.72.172.zip`;
- Handoff-SHA-256: `c9fd44b97793422890a46b87dcdcbc88ce52ae26437b77173a64c9d976b73a25`;
- 27/27 Source-Identität PASS; Fresh-Unpack 27/27 PASS; PHP-Lint 21/21 PASS; Header/Runtime 6.72.172 PASS;
- technische Autorität: `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`;
- Repository-Binärsync bleibt wegen fehlendem bytegenauem Binär-Uploadweg formal offen; der geprüfte Handoff-Installer ist davon getrennt.
- alte hardcodierte 6.72.170/171-CI-Jobs sind kein 6.72.172-Fehler: Governance/Source/Tree/Start PASS; Abbruch erst an fest verdrahtetem Versions-`grep`. Workflows wurden nicht umgebaut.

Datenbank:
- PSTE bleibt bis `PSTE_CONTEXT_REFRESH_COMPLETE` strikt unangetastet;
- aktueller TEXT-Blocker ist weiterhin `PSTE_CONTEXT_REFRESH_NOT_COMPLETE`;
- PSERC besitzt bereits Generation-Retention/Storage-Maintenance; keine neue Architektur erforderlich;
- Affiliate-Housekeeping besitzt bereits bounded DB-Retention und eBay-Payload-Kompaktion; diese Pfade werden nach Idealo-Live-Readback im DB-Block gezielt verwendet/vermessen.

ERSTER OFFENER PUNKT:
**Den exakt geprüften Affiliate-Zentrale-6.72.172-Handoff installieren und den aktiven Versionsstand in WordPress zurücklesen.**

GENAU EINE NEXT ACTION:
`INSTALL_AND_READBACK_AFFILIATE_6_72_172`.

Erst danach: zentralen Housekeeping-Lauf ausführen, Storage erneut messen und belegen, dass die fünf Idealo-TMPs verschwunden sind. Anschließend DB-Verschlankung: PSERC/Affiliate bereits mögliche Retention zuerst; PSTE erst nach Context-Refresh-COMPLETE; danach physische Tabellenreorganisation und erneute Speicher-/Performance-Messung.

## HARDLOCK – KEIN PERFORMANCE-RÜCKBAU 2026-10-01

Für jede kommende Affiliate-Funktionsreparatur (eBay-Ausspielung, Portalabdeckung, Banner-Zuordnung, Tarifcheck/CHECK24) gilt verbindlich:

- Ausgangsbasis ist ausschließlich der **frisch gelesene kanonische Current-Sourcebaum** auf `affiliate-release-current`.
- Aktuellster Kandidat: **6.72.172**, aufgebaut auf dem freigegebenen Performance-Stand **6.72.171**.
- Die 6.72.171-Performanceoptimierungen in `pferdeportal-affiliate-router.php`, `includes/trait-ppar-automation-suite.php` und `includes/trait-ppar-ebay.php` dürfen nicht entfernt, überschrieben oder durch Altcode ersetzt werden.
- Die 6.72.172-Storageänderung in `includes/trait-ppar-housekeeping.php` bleibt ebenfalls erhalten.
- Kein Cherry-Pick/Copy aus 6.72.170 oder älter, kein Alt-ZIP als Basis, keine Rekonstruktion.
- Vor jedem Source-Write erneut Current, Branch-HEAD, Manifest und betroffene Datei-Hashes lesen.
- Funktionsfix nur als **kleinstes Delta auf dem aktuellen Baum**.
- Regression muss neben dem Fach-PASS zwingend die 6.72.171-Performance-Semantik prüfen: identische Slot-Auswahl/HTML/Kandidatenreihenfolge, request-lokale Caches weiter aktiv, Admin/Worker uncached wie bisher.
- Bei Performanceverschlechterung oder Verlust eines belegten Cachepfads: FAIL, kein Installer.

## NEUER REALER AFFILIATE-AUSGABEFEHLER 2026-10-01

Nutzer-Readback:
- eBay-Produktanzeigen werden im Frontend erneut nicht sichtbar ausgespielt;
- vorhandene Banner werden nicht zuverlässig automatisch dem fachlich passenden Ziel zugeordnet;
- konkreter reproduzierbarer Fall: vorhandener Banner „Schabrackendesigner“ erscheint nicht auf der Produktseite/Kategorie „Schabracken“.

Read-only technische Einordnung:
- der historische reale WordPress-Bestand belegt für „Schabracken“ eine aktive eBay-BUSINESS-Kampagne mit exakter Zielbindung `page:schabracken` und den drei `category_product_1..3`-Placements; der Grundfehler ist daher nicht „Schabracken existiert nicht“ oder „nie zugeordnet“;
- die aktuelle Banner-Automatik besitzt vor dem Zielranking ein Fachdomain-Gate. Ein Creative wie „Schabrackendesigner“ kann dort bereits auf REVIEW enden, wenn die Creative-Evidence keinen generischen Pferdebegriff enthält, obwohl „Schabracken“ selbst ein exaktes reales Portalziel ist. Dieser Pfad ist im aktuellen Sourcecode belegt und muss nach Live-Readback eng regressiv geprüft werden;
- eBay besitzt zusätzlich einen Safe-Public-Checkpoint. Bei vorhandenem sicheren Checkpoint dürfen nur die dort enthaltenen BUSINESS-Campaign-IDs öffentlich erscheinen. Der aktuelle produktive Checkpoint-Inhalt ist noch nicht read-only belegt; deshalb wird die eBay-Ursache nicht geraten.

HARD RULE:
- Affiliate 6.72.172 bleibt der aktuelle Storage-only Kandidat; keine Banner-/eBay-Fachänderung in dieses Paket mischen.
- Nach Installation/Readback von 6.72.172 wird VOR weiterer Storage-Housekeeping-Arbeit zuerst der reale read-only `Portalabdeckung`-Snapshot für „Schabracken“ ausgewertet und der tatsächliche Banner-Datensatz „Schabrackendesigner“ geprüft.
- Erst den ersten exakt belegten eBay-Gatefehler fixen; keine Ranking-/Provider-/Checkpoint-Neukonstruktion auf Verdacht.
- Bannerfix nur eng: exakte reale Produktthemen müssen als fachliche Evidence zählen können, ohne negative Fachsignale oder Veto/Safety zu lockern.
- Positiv-/Negativ-/Realrouter-Regression zwingend vor neuem Installer.

Gebundener Folgepunkt nach `INSTALL_AND_READBACK_AFFILIATE_6_72_172`:
`READ_ONLY_DIAGNOSE_SCHABRACKEN_EBAY_AND_SCHABRACKENDESIGNER_THEN_FIX_FIRST_PROVEN_OUTPUT_GATE`.

## NEUER REALER EBAY-PRIVATE/HIVEPRESS-FEHLER 2026-10-01

Nutzer-Readback:
- Im HivePress-Bereich „Private Anzeigen“ werden eBay-Privatanzeigen gezählt, aber es sind keine eBay-Anzeigen sichtbar.

Read-only Codebefund im aktuellen kanonischen 6.72.172-Baum:
- HivePress kann Kategorie-/Nachfahrenzahlen bereits aus der Taxonomie ermitteln.
- Die eigentliche sichtbare Ergebnisliste wird danach zusätzlich durch `ebay_filter_stale_posts()` gefiltert.
- Für eBay-PRIVATE prüft dieser Finalfilter u. a. den sicheren Public-Checkpoint (`private_listing_ids`), Source-Row, Seller-Typ INDIVIDUAL, Source-/Policy-State, Inhalts-Policy, Lifecycle, Control-Gate und Endzeit.
- Dadurch ist der beobachtete Zustand „gezählt, aber 0 sichtbar“ technisch möglich, wenn der Rohbestand existiert, aber der finale Sichtbarkeitsvertrag alle eBay-Posts verwirft.
- Die konkrete live blockierende Bedingung ist noch nicht read-only belegt; nicht raten.

Nachhaltiger Zielvertrag:
1. Gültige eBay-PRIVATE-Listings im Teilbaum „Private Anzeigen“ müssen sichtbar sein.
2. Ungültige/stale/blocked Listings bleiben fail-closed unsichtbar.
3. Kategorie-/Trefferzahlen dürfen nicht dauerhaft einen anderen Sichtbarkeitszustand behaupten als der finale Listing-Loop.
4. Native HivePress-Anzeigen bleiben vollständig unverändert.
5. Keine Öffnung von eBay-PRIVATE außerhalb des erlaubten „Private Anzeigen“-Teilbaums.
6. Keine Rücknahme der 6.72.171-Performance-Caches.
7. Positiv/Negativ/Performance-Test muss mindestens abdecken:
   - parent „Private Anzeigen“ mit sichtbaren gültigen eBay-INDIVIDUAL-Listings;
   - direkte Unterkategorie mit sichtbaren gültigen eBay-Listings;
   - allgemeiner Anzeigenmarkt zeigt keine eBay-PRIVATE-Listings;
   - native HivePress-Anzeige bleibt sichtbar;
   - stale/ended/blocked/checkpoint-nicht-freigegeben bleibt unsichtbar;
   - Count/Loop-Konsistenz für den geprüften sichtbaren Bestand;
   - keine zusätzliche ungebremste DB-/Term-Auflösung auf normalen Portalrequests.

Reihenfolge:
- 6.72.172 unverändert installieren/readbacken; kein Mischfix in das geprüfte Storage-Paket.
- Danach read-only den ersten live blockierenden PRIVATE-Gatepfad belegen.
- Genau diesen ersten belegten Fehler als kleinstes Delta auf dem dann aktuellen Sourcebaum reparieren.
- Danach kompletter eBay-PRIVATE Positiv-/Negativ-/Performance-Regressionslauf.

## BILDOPTIMIERUNG ALS GEBUNDENER AUFRÄUMBLOCK 2026-10-01

Aus der frischen Speicheranalyse:
- 375 Attachments;
- 2.992 WebP-Dateien mit zusammen ca. 142,1 MB;
- 737 PNG-Dateien mit zusammen ca. 135,6 MB;
- 427 JPG-Dateien mit zusammen ca. 25,6 MB.
Damit ist WebP bereits breit im Einsatz; eine pauschale Neu-Konvertierung ist nicht begründet.
- Die WordPress-Medienmetadaten belegen bei typischen Artikelbildern Original + mehrere abgeleitete Größen (u.a. 300, 768, 1024 sowie HivePress-spezifische Größen). Deshalb liegt das relevante Optimierungspotenzial eher in unnötigen Original-/Dublettenbeständen, überflüssigen Größen und korrekter Frontend-Auslieferung als in einem neuen Bildformat-Plugin.
- Der aktuelle Speicherreport zeigt mindestens drei exakte Bild-Dubletten-Gruppen mit ca. 8,5 MB unmittelbar belegtem Einsparpotenzial; keine pauschale Löschung ohne Referenzprüfung.
- Historische Performance-Evidence zeigt Artikel-LCP mehrfach auf dem Featured Image; Bildauslieferung bleibt deshalb eigener Performance-Prüfpunkt.
- Kein neues Bildoptimierungsplugin installieren. Erst bestehende Bildzentrale/WordPress-Größen, Referenzen und Auslieferung prüfen.
- Bildoptimierung wird vor der finalen Performance-Abnahme erledigt, aber nach Backup-/Tempbereinigung und parallel zur DB-Verschlankung.

## AUFRÄUM-/PERFORMANCE-PRÜFSTAND 2026-10-01

Technische Affiliate-Releasewahrheit:
`affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.

Belastbarer Stand für PA-E-003:
- letzter ausdrücklich versionsbezogener WordPress-Readback: Affiliate-Zentrale **6.72.170 aktiv** (01.10.2026, WordPress-Uploadvergleich);
- danach wurden 6.72.168–6.72.170 im laufenden Performance-/Storage-Strang technisch weiterentwickelt und reale Performance-Diagnosen geliefert; die Diagnose-Datei selbst enthält keine Plugin-Versionsnummer und wird deshalb nicht als separater Versions-Readback ausgegeben;
- realer Performancebefund vor 6.72.171: Top-Kategorie `/ausruestung/` ca. **1,65 s**, während tiefere Kategorieprodukt-Seiten wie Trensen/Pferdesättel weiter bei ca. **8,6–9,1 s** lagen;
- Ursache: die drei öffentlichen `category_product_1..3`-Slots wiederholten große Teile desselben slot-unabhängigen Kontext-Rankings und mehrerer reiner Gates/Providerprüfungen;
- **6.72.171** teilt dieses slot-unabhängige Ranking pro Seite und cached nur request-lokal reine, identische Prüfungen; Slot-Placement, Control/Veto, Provider-Mix und finale Auswahl bleiben pro Slot erhalten;
- Source-Head des getesteten Runtime-Baums: `ad4db0c34552667a9d398d4b74cb7d8b7130f03a`;
- Source-Manifest SHA-256: `5094f6df73c172b01819294d3dd455002fa244aa9676da0ebbbb4b058530dda4`;
- Exact Local A-B Run `36839006440`: SUCCESS, funktionale 1:1-Gleichheit + Positiv/Negativ PASS, Median **393,694 ms → 365,895 ms**;
- 2012er Snapshot Exact Local A-B Run `36839006513`: SUCCESS, identische Auswahl/HTML/Kandidatenzahlen, Gesamt **1248,595 ms → 249,597 ms (-80,01 %)**, Hub **-71,20 %**, Leaf/Unterkategorie **-89,87 %**;
- final lokal frisch gebauter Installer: `AFFILIATE_ZENTRALE_6.72.171.zip`;
- Installer SHA-256: `dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba`;
- 27/27 Source-Dateien byteidentisch zum getesteten GitHub-Baum; PHP-Lint 21/21 PASS; Fresh-Unpack erneut PASS;
- Exact-A/B-Evidence: `release/affiliate-zentrale/evidence/affiliate_router_v672171_category_product_performance_rootfix_20261001.md`;
- finaler Full-Gate Run `36842612555`: **SUCCESS**;
- finale Release-Evidence: `release/affiliate-zentrale/evidence/affiliate_router_v672171_full_release_gate_20261001.md`;
- technische Release-Autorität: **6.72.171 RELEASED / release_allowed=true**;
- neue reale Performance-Diagnose Safe 2.3.0 vom **01.10.2026 10:30–10:31 UTC** liegt vor; Messmodus `PASSIVE_NO_FILTERS`;
- die Diagnose führt `affiliate-portal-router/pferdeportal-affiliate-router.php` als **aktiv** auf, enthält aber selbst **keine Plugin-Versionsnummer**;
- reale Zeiten dieser Diagnose: `/ausruestung/` **1,560219 s**, `/ausruestung/ausruestung-sattel/` **2,308272 s**, `.../pferdesaettel/` **4,634054 s**, `.../trensen/` **4,537820 s**;
- gegen den zuvor dokumentierten 6.72.170-Befund (~1,65 s / ~8,85 s / ~9,09 s / ~8,62 s) sind alle vier Vergleichsseiten schneller; die drei tiefen Kategorieproduktseiten verbessern sich um ca. **73,9 % / 49,0 % / 47,4 %**;
- alle vier Vergleichsrequests liefern **HTTP 200** und `last_php_error = null`;
- diese Messung belegt die reale Performanceverbesserung und den aktiven Affiliate-Router, darf aber ohne separaten Versions-Readback nicht allein als exakter **6.72.171-Versionbeleg** ausgegeben werden;
- isolierter Repository-`CURRENT.zip`-Sync bleibt separat BLOCKED, solange der verfügbare Dokumentationsweg keinen bytegenauen Binärtransfer belegt; keine Ersatz-ZIP erfinden.

Der frühere NEXT `FRESH_STORAGE_BASELINE_THEN_RETENTION_CLASSIFICATION` ist durch die frische Baseline oben erledigt und supersediert.

### PSTE-KANDIDATENDELTA NACH ABSCHLUSSPRÜFUNG 2026-09-30

Bei der Abschlussprüfung wurde in einem früheren 0.57.13-Paket eine ungewollte Backup-Datei `includes/class-pste-sandbox-record-store.php.orig` entdeckt. Dieser Kandidat wurde **vor Installation verworfen**.

Final neu gebaut und frisch geprüft:
- ZIP SHA-256: `bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`
- Version: `0.57.13`
- Fresh PHP-Lint: `78/78 PASS`
- Storage Core: `22/22 PASS`
- Maintenance + Active-Work Guards: `10/10 PASS`
- Public Storage API: `8/8 PASS`
- Rollback Restore: `17/17 PASS`
- Restore Mode: `7/7 PASS`
- Atomic Lock: `3/3 PASS`
- PSERC-0.28.27-Bindung: `PASS`
- Stray-Backup-Dateien `*.orig/*.bak/*~`: `0`
- Diff gegen 0.57.12: 2 neue Storage-Dateien, 6 geänderte Runtime/Admin-Dateien, 1 entfernte ungenutzte `.orig`-Datei; Contracts/Fixtures unverändert.

Der Nutzer bestätigt die Installation; der WordPress-Readback zeigt **Portal SEO Themenengine 0.57.13 aktiv**. Die Pluginliste beweist Version/Aktivstatus, aber nicht unabhängig den exakten Live-Bytebestand.

## ABSCHLUSS-/ARTEFAKTSTATUS

Die nach Abschlussregel geforderten isolierten `CURRENT.zip`-Binärartefakte konnten über den in diesem Chat verfügbaren GitHub-Schreibweg nicht bytegenau ins Repository übertragen werden. Es wurden deshalb keine ZIPs rekonstruiert.

Dauerhafte Blockerbelege:
- `ISOLIERTE_PLUGINS/PA-E-003/MANIFEST.md`
- `ISOLIERTE_PLUGINS/PA-E-019/MANIFEST.md`

Dies ändert die technische NEXT ACTION nicht. Der formale Plugin-Artefakt-Sync bleibt jedoch BLOCKED, bis ein autorisierter Binär-Uploadweg verfügbar ist.

## KATEGORIE-CLOSEOUT-SYNC 2026-09-24

Reine Dokumentations-Nachführung aus der technischen Current-Autorität `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`. Keine Pluginänderung und kein WordPress-Write durch diese Bürosynchronisierung.

Kategorie-/Strukturscope: **PASS / CLOSED**.
Finale Nachweise:
- `Category Integration Final Closeout` Run `36005442270` = SUCCESS
- `Category Integration Hard Baseline` Run `36005442188` = SUCCESS

Aktuell gebundene Kategorie-relevante Pluginstände:
- Affiliate Portal Template Kit: **1.50.559** – 1149er Kategorie-/Breadcrumb-Readback PASS
- Affiliate-Zentrale: **6.72.152** – Portalstruktur/Katalog 1149 PASS
- Allgemeine Bildzentrale: **2.7.6** – keine statische Vollkopie, kein Kategorie-Delta erforderlich
- Portal Link Policy Runtime Verifier: **1.0.0** – kein statisches Vollkopie-Delta erforderlich
- Portal Production Center: **1.1.1** – 1149 / 9 / 5790 + Build-Integrity PASS
- Portal Production Link Policy Gate: **1.0.1** – dynamischer/source-getriebener Kategoriepfad
- Portal Production Machine: **6.7.9** – Kategorieintegration 25/25 + 125/125 Slots PASS
- Portal SEO Redaktionsplan Compiler: **0.28.23** – vollständiger 1149-Strukturgate PASS
- Portal SEO Themenengine: **0.57.12** – LIVE_READBACK_PASS_CLOSED; `pferde putztasche` Readback PASS
- Portal Category Structure Repair Guard: **1.0.1** – kein statisches Vollkopie-Delta erforderlich

HARD RULE: Keine Kategorie-/Strukturarbeit erneut öffnen, solange keine neue harte Evidenz eines echten Kategorie-/Strukturdefekts vorliegt.

## BEOBACHTETER WORDPRESS-BESTAND 2026-09-12

Quelle: sechs vom Nutzer bereitgestellte Screenshots der WordPress-Seite `Plugins → Installierte Plugins`.

- **55 Pluginzeilen** sichtbar.
- **28 Zeilen Eigenentwicklungen/Projektentwicklungen**, entsprechend **27 unterschiedlichen Plugins**.
- Grund für die Abweichung: `Portal SEO Redaktionsplan Compiler` ist zweimal vorhanden (`0.28.20` aktiv, `0.28.16` inaktiv).
- **4 sichtbar inaktive Pluginzeilen**: HivePress Geolocation, HivePress Messages, Minimal Coming Soon & Maintenance Mode, Portal SEO Redaktionsplan Compiler 0.28.16.
- Es wurde in diesem Inventarlauf **kein Plugin aktualisiert, deaktiviert, aktiviert oder gelöscht**.

## INVENTARDELTA 2026-09-23 – NUR KATEGORIE-SCOPE

Quelle: Nutzer-Readback der real installierten WordPress-Plugins am 23.09.2026. Dieses Delta aktualisiert **nur** die für die Pferdeportal-Kategorieintegration relevanten beobachteten Versionen. Es ist keine Release-/LIVE-Freigabe.

Beobachtet:
- Affiliate Portal Template Kit (Pferde-kompatibel): **1.50.559**
- Affiliate-Zentrale (Portal-kompatibel): **6.72.152**
- Allgemeine Bildzentrale: **2.7.6**
- Portal Link Policy Runtime Verifier: **1.0.0**
- Portal Production Center: **1.1.1**
- Portal Production Link Policy Gate: **1.0.1**
- Portal Production Machine: **6.7.9**
- Portal SEO Redaktionsplan Compiler: **0.28.23**
- Portal SEO Themenengine: **0.57.12**
- Portal Category Structure Repair Guard: **1.0.1**

Für Fach-/Release-/LIVE-Status weiterhin zwingend zum zuständigen Fachbüro bzw. zur technischen Hauptquelle routen. Die Kategorieintegration selbst hat ihre technische Current-Autorität auf `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.

## SICHTBARE UPDATE-HINWEISE IM SNAPSHOT

Nur als Beobachtung, **keine Update-Freigabe**:

- HivePress Authentication: installiert 1.1.4 → Hinweis auf 1.1.5.
- Kubio: installiert 2.9.0 (build 517) → Hinweis auf 2.9.1.
- Relevanssi: installiert 4.28.2 → Hinweis auf 4.28.3.
- Site Kit by Google: installiert 1.185.0 → Hinweis auf 1.187.0.
- WordPress Importer: installiert 0.9.5 → Hinweis auf 0.9.6.
- WPvivid Backup Plugin: installiert 0.9.132 → Hinweis auf 0.9.135.

## HISTORISCHER ABGLEICH AUS SNAPSHOT 2026-09-12 – DURCH DELTA OBEN TEILWEISE ÜBERHOLT

Der WordPress-Snapshot zeigt bei mehreren Eigenentwicklungen neuere installierte Versionen als ältere Campus-/Artefaktbelege. Dieses Büro überschreibt die Fachwahrheit deshalb **nicht automatisch**.

Offene Abgleiche:

- Affiliate-Zentrale: historischer 12.09.-Drift ist für den Kategorie-Scope durch den 24.09.-Closeout überholt; aktueller gebundener Stand **6.72.152**.
- Portal SEO Redaktionsplan Compiler: Kategorie-Scope aktuell **0.28.23**; der separat beobachtete inaktive Altstand 0.28.16 bleibt nur als möglicher Aufräumpunkt bestehen.
- Universal Product Comparison: WordPress beobachtet `0.8.5-prototype`; PRODUKTVERGLEICH-CURRENT_STATE enthält älteren Testkandidaten → Fachbüro frisch abgleichen.
- Universal Product Knowledge: WordPress beobachtet `0.5.1-prototype`; frühere Produktvergleichsbelege referenzieren 0.5.0 → Fachbüro frisch abgleichen.

Diese Punkte sind **Inventardrift**, nicht automatisch Fehler und nicht automatisch Release-PASS.

## AUFRÄUMLOGIK

Aktuell eindeutigster Eigenentwicklungs-Altbestand: inaktiver `Portal SEO Redaktionsplan Compiler 0.28.16` neben aktivem 0.28.20. **Entfernung trotzdem erst nach TEXT-Abhängigkeits-/Rollbackprüfung.**

Weitere Audit-/Diagnose-/Exporter-Plugins sind im `PLUGINREGISTER.md` als Prüf-/Aufräumkandidaten gekennzeichnet. Bewertung allein berechtigt niemals zur Löschung.

## EINE-WAHRHEIT-GRENZE

PLUGINS verwaltet Inventar, betriebliche Zuordnung, Bewertung und Update-Ereignis-ID.  
Es wird **keine zweite Fach-, Release-, LIVE-, Fehler- oder Modulwahrheit** geführt.
