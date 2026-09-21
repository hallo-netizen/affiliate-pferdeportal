# AFFILIATE-ZENTRALE — NOTFALL-ZIELVERTRAG: Wiederherstellung des letzten belastbaren 6.72.108-Verhaltens

Stand: 2026-09-20T10:53:34+02:00
Status: `ACTIVE_RECOVERY_TARGET / NO_RELEASE_PASS`

Dieses Dokument ist **Zielquelle**, keine CURRENT-/Status-/NEXT-ACTION-Autorität. Die einzige aktuelle Statuswahrheit bleibt `control/release-governance/CURRENT_RELEASE.json`.

## Langfristiges Ziel

Der bestehende Zielvertrag `protocol/AFFILIATE_RELEASE_AUTOMATIC_CREATIVE_LIFECYCLE_SCOPE_20260918.md` bleibt fachlich bestehen. Er wird **nicht** geändert. Bis zur Wiederherstellung des beschädigten Livezustands ist jede weitere Featurearbeit jedoch gesperrt.

## Recovery-Ziel

Den WordPress-Livezustand auf das zuletzt belastbar funktionierende Verhalten der 6.72.108-Linie zurückführen, **ohne neue Fachlogik** und ohne weitere unbewiesene Plugininstallationen.

Belastbare Referenz:
- letzter getesteter/live verwendeter Basestand: **6.72.108**;
- Testartefakt SHA-256: `d8aeb69bd67a18072996da9ca8101923e6ff6765a40c5d0d6a6f74bde3be5bb3`;
- lokaler 6.72.108 Source-Manifest-SHA: `d7771d6f2d7816217b0ccd576580bf722a22a40f5d1e19b333e29b5775719b8e`;
- kanonische Repository-Source bleibt separat 6.72.105 und ist **nicht** der Recovery-Oracle für den beschädigten Livezustand.

## Aktuell ausdrücklich NICHT als bekannt annehmen

- aktuell installierte Live-Pluginversion nach den mehrfachen Install-/Downgradeversuchen;
- aktuelle Werte der von 6.72.109–117 veränderten WordPress-Optionen;
- aktueller Inhalt aller gespeicherten Artikel-/Produktpläne;
- aktueller Awin-Creative-Datenzustand nach den Ziel-URL-Mutationen;
- ob ein vorhandenes Backup exakt den Zustand unmittelbar vor 6.72.109 enthält.

Unbekannt = **lesen, nicht raten**.

## Zwingender Recovery-Weg

1. **Keine weitere Plugininstallation.**
2. Zuerst einen rein lesenden Live-Readback erstellen:
   - installierte Pluginversion;
   - `ppar_article_plan_revision_v1`;
   - `ppar_article_plan_log_v1`;
   - `ppar_article_plan_rebuild_state_v1`;
   - relevante `ppar_article_delivery_plan_v1`-Postmeta-Stichprobe/Abdeckung;
   - `ppar_network_idealo_v1` einschließlich `output_mode`;
   - `ppar_banner_placement_plan_v2`;
   - `ppar_partner_analytics_report_cache_v2`;
   - `ppar_partner_analytics_bootstrap_v672110`;
   - `ppar_multiprovider_category_repair_v672115`;
   - `ppar_v672115_article_revision_recovery_v1`;
   - `ppar_v672117_product_visibility_recovery_v1`;
   - relevante Cron-Hooks aus dieser Linie;
   - Awin-Bannerzeilen, deren Payload die nach 6.72.114 eingeführten `_destination_*`-Felder enthält.
3. Den Readback ausschließlich gegen 6.72.108-Semantik und die belegten 6.72.109–117-Mutationen vergleichen.
4. Erst danach genau **einen minimalen Recovery-Weg** bauen oder — falls ein exakt passender Backupstand beweisbar existiert — den belegten Zustand gezielt daraus wiederherstellen.
5. Keine globale Revisionserhöhung, kein ungebundener Gesamt-Rebuild und keine Provider-Umschaltung vor dem Readback.
6. POSITIV und NEGATIV lokal gegen den echten Recovery-Delta testen.
7. Danach Live-Readback. Erst ein realer Live-PASS beendet diesen Recovery-Zielvertrag.

## Recovery-Abnahme

Recovery ist erst PASS, wenn mindestens belegt ist:
- die zuvor vorhandenen realen Artikel-/Produkt-Ausgaben sind wieder sichtbar;
- keine generischen Platzhalter-Produktkarten ersetzen reale Produkte;
- keine neu eingeschleuste Direktwerbeplatz-Platzhalterausgabe erscheint an Stellen, an denen sie im 6.72.108-Verhalten nicht vorhanden war;
- Kategorie-Produktpfade sind nicht global auf einen Provider reduziert;
- eBay-/idealo-Zustand entspricht wieder dem belegten Vor-6.72.109-Verhalten, ohne erzwungenen Moduswechsel;
- geschützte Journal-/Glossar-/Pferderassen-/Kategorie-Ausgaben bleiben unverändert;
- Awin-Partnerdropdown/Programmlistenfunktion aus 6.72.108 bleibt erhalten;
- keine Recovery-Marker oder Folgejobs halten einen weiteren automatischen Umbau offen.

## Nicht anfassen

Bis Recovery-LIVE-PASS:
- keine neue Banner-Relevanzlogik;
- keine neue Produkt-Rankinglogik;
- keine neue Partnerstatistik;
- keine eBay-/idealo-Neuarchitektur;
- keine Creative-Schemaänderung;
- keine neue Version 6.72.119+;
- **keines der Pakete 6.72.109–6.72.118 installieren**;
- insbesondere **keine 6.72.118 verwenden**: es existieren zwei unterschiedliche lokale Artefakte mit derselben Versionsnummer und unterschiedlichen SHA-256-Werten.

## Danach

Erst nach Recovery-LIVE-PASS zurück zu `AFF-ERR-035`: exakten 6.72.108-Tree gegen die kanonische 6.72.105-Source reconciliieren. Danach erst wieder der normale Creative-/Awin-Zielvertrag.


## Korrektur 20.09.2026 – KISS-Recovery nach vollständiger Paketprüfung

Diese Korrektur folgt der ausdrücklichen Nutzeranweisung: **Kein direkter Live-Datenbankzugang ist Voraussetzung dieser Wiederherstellung.** Der zuvor gebundene DB-/Options-Readback als zwingender erster Schritt war zu streng und wird durch den belegten Paket-/Historienweg ersetzt.

Hart geprüft wurden die tatsächlich vorhandenen 6.72.108–6.72.118-Pakete sowie Affiliate-Büro und Plugin-Updateprotokoll. Dabei ist die konkrete Recovery-Fehlkette belegt:

- die breite 6.72.118 löscht die 6.72.115-/117-Nachweismarker;
- die schmale 6.72.118 verlangt anschließend genau beide Marker und kann deshalb `not_applicable` werden;
- die schmale 6.72.118 macht nur `idealo_only -> automatic` rückgängig und ist kein vollständiger Restore;
- bei bereits `running` wird ihr Batch auf normalen Requests nicht weitergeführt;
- die breite 6.72.118 kann einen Voll-Rebuild mit Grund `v672118_restore_exact_672108_runtime` hinterlassen.

Deshalb ist genau **ein** neuer Recovery-Kandidat als Ausnahme vom bisherigen Versionsstopp autorisiert, ohne neue Fachlogik:

`AFFILIATE_ZENTRALE_V6.72.119_KISS_EMERGENCY_RESTORE_POSNEG.zip`

SHA-256:
`eb51dcbd19c62dae1a3958d209676926aa02793cb13a8fe64292ed53c3bcea74`

Evidence:
`release/affiliate-zentrale/evidence/affiliate_672119_kiss_recovery_local_20260920.txt`

6.72.119 basiert fachlich exakt auf 6.72.108; außer Hauptdatei und Readme sind alle Dateien bytegleich. Es löscht keine Inventare, erhöht keine globale Revision, startet keinen neuen Voll-Rebuild, verändert keine Bannerfelder und erzeugt keine neuen Artikelpläne. Es stoppt ausschließlich einen eindeutig vom ersten 6.72.118-Restore hinterlassenen Voll-Rebuild und repariert ausschließlich die Produktteile bereits gespeicherter Artikelpläne.

Lokale Abnahme: Original-118-Fehlernachweis 12/12 PASS; Recovery statisch 55/55 PASS; Runtime 30/30 PASS; Banner-Mutationsprobe fail-closed PASS; PHP 21/21; Fresh-Unpack 26/26 byteidentisch.

**Neue einzige operative NEXT ACTION:** genau den oben genannten SHA einmal installieren und anschließend die zuvor beschädigten realen Ausgaben visuell prüfen. Kein LIVE-PASS vor diesem Readback. Beide alten 6.72.118 bleiben gesperrt. Keine Featurearbeit.

## Korrektur 21.09.2026 – vollständige Historie zuerst, kein weiterer Rateschuss

Der Recovery-Zielvertrag wird um folgende verbindliche Arbeitsregel präzisiert; das fachliche Langfristziel bleibt unverändert:

1. Vor jedem weiteren Recovery-Plugin ist die tatsächlich verwendete Paketkette ab dem letzten belastbaren 6.72.108-Verhalten vollständig zu vergleichen und im kompletten WordPress-/MariaDB-Workflow auszuführen.
2. Maßgeblich ist der **erste exakt bewiesene** produkt-/eBay-wirksame Delta. Nur dieser Delta darf anschließend zurückgenommen werden.
3. Kein Minifix aus einer vermuteten Ursache, kein Kombinieren mehrerer historischer Änderungen und keine neue Architektur.
4. Produktkacheln, sichtbares Layout, Renderer, Frontend-CSS und Frontend-JS sind Recovery-Hardlocks. Sie dürfen nur geändert werden, wenn der vollständige Workflow ausgerechnet dort den ersten Fehler beweist. Bis dahin: nicht anfassen.
5. Der Prüfweg muss mindestens binden:
   `persistenter WordPress-Zustand -> Provider/Kampagne -> Zielbindung -> category_product_1..3 -> eBay/idealo-Auswahl -> render_affiliate_slot -> finales Produktkarten-HTML -> Template-is_real -> sichtbare Kategorie`.
6. Positive und negative/fail-closed Fälle müssen im selben gebundenen Workflow laufen. Eine isolierte Methodenprobe oder ein synthetischer Zustand ist kein System-PASS.
7. Eine temporäre GitHub-Ausführungsbranch darf nur Evidence/Hobbyraum sein. Sie ist weder Current-, Release- noch Source-Autorität und darf nicht als neue Produktwahrheit promoted werden.
8. Kein neuer Installer und keine neue Versionsnummer, bevor der erste exakte Fehler in dieser vollständigen Kette belegt ist.

Diese Ergänzung beschreibt ausschließlich den Recovery-Ziel-/Arbeitsvertrag. Aktueller Status, Blocker und NEXT ACTION werden weiterhin ausschließlich durch `control/release-governance/CURRENT_RELEASE.json` bestimmt.
