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
