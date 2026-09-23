# PLUGINS – CURRENT STATE

STAND: 2026-09-23
STATUS: INVENTARBASIS + KATEGORIE-SCOPE-INVENTARDELTA ERFASST / KEINE FACH-/RELEASE-WAHRHEIT

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des PLUGINS-Büros.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- vollständiger beobachteter Pluginbestand → `PLUGINREGISTER.md`
- Update-Chronik → `UPDATEPROTOKOLL.md`
- Update-/Pflegeregeln → `REGELWERK.md`
- Fach-/Release-/LIVE-Status → zuständiges Fachbüro / technische Originalquelle
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- dauerhaftes WAS/WARUM → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

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
- Portal SEO Themenengine: **0.57.6**
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

- Affiliate-Zentrale: WordPress beobachtet `6.72.17`; ältere Campus-Registerbelege nennen frühere Stände → AFFILIATE autoritativ frisch abgleichen.
- Portal SEO Redaktionsplan Compiler: WordPress beobachtet `0.28.20` aktiv und `0.28.16` inaktiv; campusweiter Installerindex enthält ältere 0.28.16-Belege → TEXT autoritativ abgleichen.
- Universal Product Comparison: WordPress beobachtet `0.8.5-prototype`; PRODUKTVERGLEICH-CURRENT_STATE enthält älteren Testkandidaten → Fachbüro frisch abgleichen.
- Universal Product Knowledge: WordPress beobachtet `0.5.1-prototype`; frühere Produktvergleichsbelege referenzieren 0.5.0 → Fachbüro frisch abgleichen.

Diese Punkte sind **Inventardrift**, nicht automatisch Fehler und nicht automatisch Release-PASS.

## AUFRÄUMLOGIK

Aktuell eindeutigster Eigenentwicklungs-Altbestand: inaktiver `Portal SEO Redaktionsplan Compiler 0.28.16` neben aktivem 0.28.20. **Entfernung trotzdem erst nach TEXT-Abhängigkeits-/Rollbackprüfung.**

Weitere Audit-/Diagnose-/Exporter-Plugins sind im `PLUGINREGISTER.md` als Prüf-/Aufräumkandidaten gekennzeichnet. Bewertung allein berechtigt niemals zur Löschung.

## EINE-WAHRHEIT-GRENZE

PLUGINS verwaltet Inventar, betriebliche Zuordnung, Bewertung und Update-Ereignis-ID.  
Es wird **keine zweite Fach-, Release-, LIVE-, Fehler- oder Modulwahrheit** geführt.
