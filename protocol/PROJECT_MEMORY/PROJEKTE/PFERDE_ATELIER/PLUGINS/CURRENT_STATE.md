# PLUGINS – CURRENT STATE

STAND: 2026-10-01
STATUS: AFFILIATE-PERFORMANCE-ROOTFIX 6.72.171 LOKAL 1:1 BEWIESEN / INSTALLATION + REALER READBACK OFFEN / KEINE ZWEITE FACH-/RELEASE-WAHRHEIT

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
- Affiliate-Zentrale (Portal-kompatibel): **6.72.167**, aktiv; Nutzer bestätigt Installation, danach eBay-OAuth erfolgreich geprüft. `PLUGIN_UPDATE_REF: PU-20260930-003`.
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

## AUFRÄUM-/PERFORMANCE-PRÜFSTAND 2026-10-01

Technische Affiliate-Releasewahrheit:
`affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.

Belastbarer Stand für PA-E-003:
- letzter ausdrücklich versionsbezogener WordPress-Readback: Affiliate-Zentrale **6.72.167 aktiv**; eBay-OAuth danach PASS;
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
- isolierter Repository-`CURRENT.zip`-Sync bleibt separat BLOCKED, solange der verfügbare Dokumentationsweg keinen bytegenauen Binärtransfer belegt; keine Ersatz-ZIP erfinden.

ERSTER OFFENER PUNKT:
**6.72.171 ist noch nicht als reale WordPress-Installation readback-bestätigt.**

GENAU EINE NEXT ACTION:
`INSTALL_AFFILIATE_ZENTRALE_6_72_171_AND_READBACK`.

Den final gegateten 6.72.171-Installer mit SHA-256 `dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba` installieren und nur Version/Aktivstatus readbacken. Erst nach diesem Readback wird als Folgeaktion dieselbe reale Performance-Diagnose wiederholt; kein weiterer Codefix vor dem Live-Readback.

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
