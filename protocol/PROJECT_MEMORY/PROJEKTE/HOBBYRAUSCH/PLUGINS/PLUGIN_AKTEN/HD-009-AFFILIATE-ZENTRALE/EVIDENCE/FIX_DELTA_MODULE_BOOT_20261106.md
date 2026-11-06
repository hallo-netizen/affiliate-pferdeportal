# HD-009 0.1.7-dev: geprüfter gezielter Moduldurchlauf (06.11.2026)

## Quelle, Status und Scope

- Betreiber-Original: `affiliate-portal-router.zip`, Version `0.1.7-dev`, SHA256 `34c0a9b42c62f71025212bfba3756e48bf4c6ab21fdd000c9894a1ce2bf12cfa`; unveränderte Quelle bleibt unverändert.
- Dieser Bericht dokumentiert ausschließlich **offline erprobte Änderungen an einer Arbeitskopie**. **Keine fertig harmonisierte Hobby-Release-ZIP; noch keine GitHub-ZIP**, keine Live-Installation.
- Fachliches Affiliate-Büro: `PROJEKTE/HOBBYRAUSCH/AFFILIATE/`. Technische Ablage: `PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/`. Keine neuen Büros und keine zweite Pluginlinie.

## Verifizierte Ursache

In der Original-Hauptdatei `affiliate-portal-router/hobby-depot-affiliate-router.php` fehlen die Require-/Bootstrap-Aufrufe für fünf physisch vorhandene Module:

1. `includes/class-ppar-product-source-plan.php` / `PPAR_Affiliate_Source_Plan::bootstrap()`.
2. `includes/class-ppar-admin-kiss.php` / `PPAR_Affiliate_Admin_KISS::bootstrap()`.
3. `includes/class-ppar-deal-radar.php` / `PPAR_Deal_Radar::bootstrap()`.
4. `includes/class-ppar-partner-analytics.php` / `PPAR_Partner_Analytics_Admin::bootstrap()`.
5. `includes/class-ppar-ds24-manual-downstream.php` / `PPAR_DS24_Manual_Downstream::bootstrap()`.

Bei bloßem Aktivieren fiel eine **neue Amazon-Regression** auf: `PPAR_Affiliate_Source_Plan::extend_provider_registry()` überschreibt die vorhandene aktive Amazon-Brücke mit `state=prepared`, `access_owner=adapter`. Die Hobby-Registry besitzt jedoch eine aktive Amazon-Tracking-/ASIN-Brücke. Blindes Kopieren aus Hab & Bewahr ist deshalb **nicht zulässig**.

## Lokal getesteter KISS-Fix (nur Arbeitskopie)

- Hauptdatei: die fünf oben aufgeführten existierenden Module nach den normalen Includes laden, am normalen Bootstrapende nach `Hobby_Depot_Affiliate_Router::instance()` jeweils einmal `::bootstrap()` aufrufen.
- `includes/class-ppar-product-source-plan.php`: in `extend_provider_registry` eine vorhandene `amazon`-Registry **unverändert lassen**. Die vorbereitete Amazon-Registry nur ergänzen, falls `amazon` **nicht** als Array vorhanden ist. Die anderen vorhandenen Provider unverändert lassen.
- Die bestehende HD003-/HD004-Anbindung, Amazon ASIN-Brücke, Optionsnamen und Pluginpfad **unverändert** lassen.

## Tatsächlich ausgeführte Offline-Prüfungen

- Original-ZIP: vollständig lesbar, ZIP-Integrität PASS; 23 PHP-Dateien aus der Originalstruktur.
- Arbeitskopie nach Fix: PHP 8.4 Syntaxprüfung aller 23 PHP-Dateien PASS.
- WordPress-Hook-Smoke mit minimalen `add_action`-/`add_filter`-Testdoubles: Plugin lädt, 88 Hook-Namen registriert, fünf Module existieren PASS.
- Prüffall `Amazon state=active, access_owner=core`: nach Provider-Plan-Filter **unverändert** PASS.
- Zusätzliche vorbereitete OTTO-Quelle vorhanden PASS.
- Keine wörtlichen Pferdeatelier-/pferdeportal-Treffer in den 23 PHP-Dateien nach diesem Fix.
- Dies ist **kein WordPress-Ende-zu-Ende-Test und kein vollständiger 6.72.306-Funktionsvergleich**.

## Noch zwingend für eine finale ZIP

Das Pferdeatelier-Paket `6.72.306` liegt im gemeinsamen GitHub-Hobby-Affiliate-Büro nur als **Textreferenz** vor (PR #636); keine vollständigen 66 Originaldateien. Die neueren eBay-Löschungs-, Checkpoint- und Banner-Fixes können ohne ihren tatsächlichen Quellstand nicht sicher und vollständig in Hobby übernommen werden. Die ZIP des hochgeladenen Hobby-Originals ist im Chat vorhanden und geprüft, wurde aber wegen fehlender direkter lokaler-Datei-zu-GitHub-Binärübertragung durch die verfügbare GitHub-Schnittstelle noch nicht als GitHub-Blob veröffentlicht.

**Kein altes 0.1.2-dev und keine bloße Textdatei als `CURRENT.zip` ausgeben.** Nächste Aktion: echte Plugin-Originalbytes nach GitHub übertragen, allgemeine Fixes gegen 6.72.306 prüfen, vollständige Gesamttests, dann ausschließlich eine aktuelle HD009-Installations-ZIP im bestehenden Pluginbüro.
