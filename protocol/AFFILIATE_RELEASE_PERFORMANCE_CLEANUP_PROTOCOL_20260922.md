# Affiliate Performance Cleanup – Problem-/Fehler- und Arbeitsprotokoll 2026-09-22

Rolle: historisches WAS/WARUM-/Fehlerprotokoll und Nachweisweg.
KEINE CURRENT-/Status-/NEXT-ACTION-Quelle. Dafür gilt ausschließlich `control/release-governance/CURRENT_RELEASE.json`.

## Problemstellung

Der eingeschobene Performanceblocker wurde zunächst durch massive Affiliate-DB-Wiederholungen sichtbar:
- ca. 13.671 Queries / ca. 10,3 s Serverzeit;
- ca. 11.297 Control-Decision-Lookups;
- ca. 1.484 eBay-BUSINESS-Lookups;
- ca. 305 Creative-Library-Lookups.

6.72.144 beseitigte identische Same-Key-Wiederholungen request-lokal.
6.72.145 ergänzte bounded Batch-Reads für viele verschiedene Keys/Hashes.

Live-Readback nach 6.72.145:
- Affiliate-Einzelquery-Explosion beseitigt;
- gemessene Seiten nur noch ungefähr 318–339 DB-Queries;
- Backendzeit blieb dennoch ca. 4,8–6,7 s;
- damit verlagerte sich der belegte Hauptengpass auf PHP-/Hook-/Template-CPU.

Diagnosebefunde:
- sehr hohe Hookzahlen, u. a. get_post_metadata/get_term/options;
- Router: quadratische eBay-Titelähnlichkeitsarbeit und wiederholte identische Rankingberechnungen;
- Designplugin: derselbe große WordPress-Menübestand wird für Desktop und Mobile separat durch den teuren Core-Setup-Pfad geschickt.

## Durchgeführte Router-Bereinigung

Aufbauend auf dem live getesteten 6.72.145-Stand:
- exact-safe Vorfilter vor `similar_text()`; die bestehende Schwelle `>= 92.0` bleibt alleinige Duplikatentscheidung;
- Titelsignaturen einmal pro Titel vorberechnet;
- request-local Memo für identische `ranked_campaigns_for_slot()`-Aufrufe im öffentlichen Frontend;
- Admin/Cron/REST/WP-CLI/AJAX vom Ranking-Memo ausgeschlossen.

Harte Nachweise:
- 53.361 alte/neue Titelpaarentscheidungen identisch;
- kompletter zweistufiger Seller-/Diversity-Output identisch;
- 792 Unique-Titel: kein False Duplicate;
- 6.72.145 Batch-DB-Vertrag erhalten;
- Bannerregression erhalten;
- GitHub CPU Run 35693134066 SUCCESS;
- Ranking Memo Run 35693058767 SUCCESS;
- Combined Run 35693264536 SUCCESS.

Kandidat:
- `AFFILIATE_ZENTRALE_V6.72.147_PERFORMANCE_CPU_RANKING_CLEANUP_HARDTEST.zip`
- SHA-256 `905f6db0941c04d0275aad3e63db8bdca80fb95f6659de2d2bb118359a9d72a5`
- Fresh-Unpack 27/27 byteidentisch;
- PHP-Lint 21/21 PASS;
- gegenüber 6.72.145 nur `includes/trait-ppar-ebay.php` plus Versionsdatei geändert.
- 6.72.142 GOLDMASTER unverändert.

## Durchgeführte Design-Bereinigung

KISS-Lösung:
- beide bestehenden `wp_nav_menu()`-Aufrufe bleiben bestehen, weil Desktop und Mobile unterschiedliche Objektfilter benötigen;
- nur der teure WordPress-`wp_setup_nav_menu_item`-Setup wird für den zweiten Render request-lokal wiederverwendet;
- Umsetzung über die offiziellen Pre-/Post-Setup-Hooks.

WordPress-7.1.1-Hardtest mit 120 Menüeinträgen:
- Baseline zweiter Render: 2.520 Metadata-Hooks;
- bereinigt zweiter Render: 360;
- Reduktion 85,7 %;
- Desktop-HTML SHA unverändert;
- Mobile-HTML SHA unverändert;
- Desktop-/Mobile-spezifische Filter unverändert;
- GitHub Run 35693870974 SUCCESS.

Wichtige Grenze:
- der Designfix ist als semantischer Patch hart bewiesen;
- er ist noch KEIN installierbares Ersatzpaket;
- ein historischer Design-Vollstand darf den aktuellen Live-Stand nicht überschreiben;
- zuerst muss der exakt aktuelle Live-Vollstand von PPA-013 gebunden werden.

## Kubio-Befund

Kubio ist nicht Teil dieser Bereinigung.
Ein echter WordPress-Export enthält gespeicherte `wp:kubio/...`-Blöcke. Deshalb Kubio nicht blind deaktivieren; Migration/isolierter Test kommt erst nach Abschluss von PPA-001 und PPA-013.

## Sicherungs-/Rollbackregel

Router:
- unveränderlicher Rollbackanker: 6.72.142 GOLDMASTER;
- 6.72.147 bleibt bis Live-Abnahme separater Testkandidat;
- bei Regression keine Live-Flickserie, sondern sofortiger Rückweg auf den Goldmaster.

Design:
- keinen historischen Vollstand als Ersatz für den aktuellen Live-Stand verwenden;
- bestehendes Designplugin bleibt unverändert, bis sein aktueller Vollstand exakt gebunden, gepatcht und vollständig geprüft ist.

## Aktueller Status

Nicht hier ableiten.
Immer `control/release-governance/CURRENT_RELEASE.json` lesen und dessen Frischecheck/NEXT ACTION verwenden.
