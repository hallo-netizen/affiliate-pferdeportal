# PLUGINS – CURRENT STATE

STAND: 2026-09-30
STATUS: REALER WORDPRESS-PLUGINSTAND 2026-09-30 NACHGEFÜHRT / AUFRÄUM- UND PERFORMANCEARBEIT AKTIV / KEINE ZWEITE FACH-/RELEASE-WAHRHEIT

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des PLUGINS-Büros.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
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
- Affiliate-Zentrale (Portal-kompatibel): **6.72.165**, aktiv.
- Performance Diagnose Safe: **2.3.0 aktiv**; ältere **2.2.0 inaktiv**.
- Pferde Atelier – Affiliate Design Performance: **3.0.0 inaktiv**.
- Portal Production Machine: **6.7.9**, aktiv.
- Portal SEO Redaktionsplan Compiler: **0.28.27**, aktiv.
- Portal SEO Themenengine: **0.57.12**, aktiv.

Der frühere Kategorie-Stand weiter unten bleibt historische Scope-Dokumentation und darf diese reale Inventarbeobachtung nicht überschreiben.

## AKTUELLER AUFRÄUM-/PERFORMANCEAUFTRAG 2026-09-30

Ziel des laufenden Plugin-Arbeitsstrangs:
- Datenbank nachhaltig gegen unnötiges Wachstum schützen;
- vorhandene Altlasten kontrolliert bereinigen;
- Performanceverbesserungen erhalten und nicht gegenseitig überschreiben;
- Plugin für Plugin arbeiten, keine Serie von Miniversionen.

Arbeitsgrenze:
- Fach-/Release-/LIVE-Autorität bleibt im jeweiligen Fachbüro bzw. in der technischen Originalquelle.
- Keine Datenlöschung ohne belegte Schutz-/Recoveryprüfung.
- Keine Performanceoptimierung darf durch Storage-/Housekeepingänderungen rückgängig gemacht werden.
- Affiliate-Zentrale **6.72.165** wurde im laufenden Auftrag durch einen gleichversionierten Storage-Housekeeping-Build ersetzt; exakter Updatebeleg steht in `UPDATEPROTOKOLL.md`.
- PSTE **0.57.12** ist weiterhin real installiert; ein neuer PSTE-Kandidat ist **noch kein LIVE-Stand**.

## AUFRÄUM-/PERFORMANCE-PRÜFSTAND 2026-09-30

- Affiliate-Zentrale: real **6.72.165** aktiv; Storage-Housekeeping-Ersatz installiert und Performancepfade unverändert gebunden.
- PSTE: real weiterhin **0.57.12** aktiv. Final geprüfter **0.57.13-Kandidat** ist bereit, aber noch **NICHT LIVE**. Kandidaten-SHA-256: `9627705af4d934b6dcde5106476459af2f3959032da9caee2a33cc5621c22345`.
- PSERC: real **0.28.27** aktiv; vorhandene Generation-Retention/Dry-Run-Speicherwartung reicht nach Quellprüfung aus; **kein Update erforderlich**.
- PPM: real **6.7.9** aktiv; kein belegter Speicherfehler und geringe aktuelle DB-Größe; **kein Update erforderlich**.

Aktuelle Plugin-NEXT-ACTION:
`INSTALL_PSTE_0_57_13_DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS`.

Der PSTE-Kandidat ist nur Kandidat, bis WordPress-Installation und Readback bestätigt sind. Erst danach folgt Datenbankpflege; vorher keine manuelle Löschung.

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
