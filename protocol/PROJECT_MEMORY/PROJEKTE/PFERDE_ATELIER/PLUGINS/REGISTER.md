# PFERDE-ATELIER – PLUGINREGISTER

STAND: 2026-11-03 (LIVE-SNAPSHOT aktualisiert; ältere PPA-Artefaktstände als Historie erhalten)
ROLLE: ZENTRALES INVENTAR-/ARTEFAKTREGISTER, KEINE FACH-/LIVE-WAHRHEIT

`ARTEFAKT_SYNC: PASS` gilt nur für real vorhandene isolierte `CURRENT.zip` + Manifest/Hashprüfung. Fachstatus immer im Fachbüro lesen.

## LIVE-Beobachtung vom 03.11.2026 – vollständiger Pluginbestand

Quelle: tatsächlicher WordPress-Systembericht der produktiven Website, Serverzeit **03.11.2026, 11:37 UTC** (nicht GitHub-Dateinamen, nicht Kandidatenversionen). **46 aktiv, 3 inaktiv, insgesamt 49.** Diese Liste ist die datierte **LIVE-Beobachtung**; sie erteilt keine Freigabe, bildet keine physische Plugin-ZIP ab und ersetzt nicht die autoritativen Fachbüros oder `PLUGINS/CURRENT_STATE.md`.

| Plugin (Systembericht) | Installierte Version | LIVE |
|---|---:|---|
| Affiliate-Zentrale (Portal-kompatibel) | 6.72.298 | aktiv |
| Affiliate Portal Template Kit (Pferde-kompatibel) | 1.50.613 | aktiv |
| Akismet Anti-spam: Spam Protection | 5.7.2 | aktiv |
| All-in-One WP Migration and Backup | 7.113 | aktiv |
| Allgemeine Bildzentrale | 2.7.6 | aktiv |
| Canonical Table Contract V1 | 1.1.0 | aktiv |
| CookieYes / GDPR Cookie Consent | 3.5.8 | aktiv |
| DBStorage Insights | 1.2.0 | aktiv |
| HivePress | 1.8.1 | aktiv |
| HivePress Authentication | 1.1.5 | aktiv |
| HivePress Claim Listings | 1.1.5 | aktiv |
| HivePress Favorites | 1.2.2 | aktiv |
| HivePress Paid Listings | 1.1.10 | aktiv |
| HivePress Reviews | 1.4.1 | aktiv |
| Kubio | 2.9.5 | aktiv |
| Performance Diagnose Safe | 3.0.0 | aktiv |
| Pferde Atelier Editorial Guard | 0.1.1-quarantine | aktiv |
| Pferde Atelier Glossar Core | 1.4.0 | aktiv |
| Pferde Atelier HivePress Anzeigensuche | 2.1.5-ajax-category-label | aktiv |
| Pferde Atelier Mail-Absender | 1.0.0 | aktiv |
| Pferde Atelier – Anzeigenmarkt & Journal Breadcrumbs | 1.1.1 | aktiv |
| Pferdeatelier – eBay Ursachencheck (nur lesen) | 1.0.0 | aktiv |
| Pferde Atelier – HivePress Anzeigensuche | 1.0.1 | aktiv |
| Pferde Atelier – Komplettsicherung | 2.1.1 | aktiv |
| Pferde Atelier – Pferderassen Manager | 0.2.6 | aktiv |
| Portal Production Center | 1.1.1 | aktiv |
| Portal Production Link Policy Gate | 1.0.1 | aktiv |
| Portal Production Machine | 6.7.9 | aktiv |
| Portal SEO Redaktionsplan Compiler | 0.28.43 | aktiv |
| Portal SEO Themenengine | 0.57.120 | aktiv |
| Relevanssi | 4.28.8 | aktiv |
| Relevanssi Live Ajax Search | 2.6 | aktiv |
| Reveal IDs | 1.6.3 | aktiv |
| SEO-Quellpaket Exporter | 1.0.0 | aktiv |
| Shortcodes Ultimate | 7.9.2 | aktiv |
| Single Sign-On | 2.3.2 | aktiv |
| Site Kit by Google | 1.191.0 | aktiv |
| Universal Product Comparison | 0.8.5-prototype | aktiv |
| Universal Product Knowledge | 0.5.1-prototype | aktiv |
| Universal Research & Fill | 1.9.9 | aktiv |
| WordPress Importer | 0.9.7 | aktiv |
| WordPress Speicheranalyse | 1.1.0 | aktiv |
| WP-Optimize - Clean, Compress, Cache | 4.7.0 | aktiv |
| WPForms Lite | 2.0.3.1 | aktiv |
| WPvivid Backup Plugin | 0.9.139 | aktiv |
| Yoast SEO | 28.8 | aktiv |
| HivePress Geolocation | 1.3.11 | inaktiv |
| HivePress Messages | 1.4.1 | inaktiv |
| Pferdeatelier – Affiliate Einzelbeitrag Diagnose (nur lesen) | 1.0.0 | inaktiv |

**Wichtige Korrekturen zur September-Inventur:**
- Als LIVE installiert bestätigt: Template Kit **1.50.613**, Affiliate-Zentrale **6.72.298**, Themenengine **0.57.120**, Redaktionsplan Compiler **0.28.43**, Bildzentrale **2.7.6**, Pferderassen Manager **0.2.6** (historischer Artefakteintrag **0.2.7** ist **kein** Beweis einer LIVE-Installation).
- **Nicht** im 03.11.-LIVE-Bericht: LiteSpeed Cache, Blogger-Importer, WP Import Export Lite, Minimal Coming Soon, gesonderter Portal Link Policy Runtime Verifier, gesonderter Portal Category Structure Repair Guard. Ihr früherer Eintrag ist **kein** Nachweis aktueller Installation.
- **Neu oder bisher nicht in der September-Liste erfasst:** DBStorage Insights, Performance Diagnose Safe, eBay Ursachencheck (read-only), Affiliate Einzelbeitrag Diagnose (inaktiv). Diese gehören in die technische Aufräumprüfung.
- **Mögliche Vereinfachungen – vor Entfernen erst testen:** reine Audit-/Diagnose-/Importer-/Exporter-Werkzeuge; WPvivid / All-in-One WP Migration / eigenes Komplettsicherungssystem; zwei ähnlich benannte HivePress-Anzeigensuchen; Suche (Relevanssi + Live Ajax), wobei Index und Suchvorschläge unterschiedliche Aufgaben haben können. **Nicht** mehr die im September genannte `LiteSpeed Cache + WP-Optimize`-Doppelung als gegenwärtigen Ist-Zustand behaupten.
- Freigabestand und Teststand **strikt getrennt**: Themenengine **LIVE 0.57.120**, letzter dokumentierter WordPress-STAGING-Beleg **0.57.144.4**, **0.57.144.5 ausschließlich lokal geprüfte Test-ZIP**, nicht installiert/bestätigt; siehe aktuelle `PLUGINS/CURRENT_STATE.md`. Kein Release daraus ableiten.

### Einordnung der älteren PPA-Artefakte

Die nachfolgenden PPA-001 bis PPA-015-Einträge dokumentieren **Artefaktbindungen und Abgleiche des 16.09.2026**. Ihre Überschriften wie „AKTUELLER STAND“ oder „KANONISCHER STAND“ dürfen **nicht** als Behauptung einer heutigen LIVE-Version gelesen werden. Für heutige Fach-/Release-Entscheidungen immer aktuellen Fach-CURRENT und den tatsächlichen physisch verifizierten Plugin-Schrank prüfen.

---

## PPA-001 – Affiliate-Zentrale
- FACHBÜRO: `../AFFILIATE/`
- KANONISCHER STAND: 6.72.19
- SHA-256: `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`
- AKTUELLER FACHSTATUS: BLOCKED; lokale 6.72.20–6.72.27 nicht kanonisch.
- ARTEFAKT_SYNC: PASS auf 6.72.19.

## PPA-002 – Pferde Atelier Design
- FACHBÜRO: `../DESIGN/`
- AKTUELLER STAND: **1.50.541**
- WORDPRESS-LIVE: **PASS 2026-09-16**
- CURRENT: `/Campus-Plugins/PFERDE_ATELIER/PPA-002/CURRENT.zip`
- SHA-256: `f93870321df4a989e8ceeb71d6a9b4a0780831184f3b9a36f1e6e29b5e8a6ee6`
- UPDATEVORGANG: `PU-20260916-016`
- ARTEFAKT_SYNC: PASS.

Hinweis: `PPA-013` war irrtümlich als zweite ID für dasselbe Designplugin verwendet worden. Diese ID ist **nicht aktiv**; ihre alte physische Kopie liegt nur noch unter `/Campus-Plugins/PFERDE_ATELIER/ARCHIV/PPA-013`.

## PPA-003 – Bildzentrale / MOD-002
- FACHBÜRO: `../BILD/`
- ALLGEMEINE HAUPTQUELLE: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
- AKTUELLER STAND: **2.7.6**
- PFERDE-LIVE-FUNKTION: PASS 2026-09-16; kein Vollbestands-Bebilderungsbeleg.
- CURRENT: `/Campus-Plugins/PFERDE_ATELIER/PPA-003/CURRENT.zip`
- SHA-256: `12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`
- UPDATEVORGANG: `PU-20260916-011`
- ARTEFAKT_SYNC: PASS.

## PPA-004 – Universal Research & Fill
- FACHBÜRO: `../HIVEPRESS/`
- STAND: 1.9.9
- SHA-256: `154102215a0ef4bf7de3362dbf835f05dc5c10b870e3507dbf173c62fb7079e0`
- ARTEFAKT_SYNC: PASS.

## PPA-005 – Portal SEO Topic Engine
- FACHBÜRO: `../TEXT/`
- STAND: 0.56.25
- SHA-256: `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`
- ARTEFAKT_SYNC: PASS.

## PPA-006 – Portal SEO Editorial Plan Compiler
- FACHBÜRO: `../TEXT/`
- STATUS: Versionsbindung weiterhin BLOCKED.
- PHYSISCHE REFERENZ: `/Campus-Plugins/PFERDE_ATELIER/PPA-006/REFERENCE_0.28.16.zip`
- ARTEFAKT_SYNC: BLOCKED; keine CURRENT.zip bis eindeutige technische Bindung vorliegt.

## PPA-007 – Pferde Atelier HivePress Anzeigensuche
- FACHBÜRO: `../HIVEPRESS/`
- STAND: 2.1.5
- SHA-256: `5879bb257026ec72fa83fc817994a4764009a7c1fde75a13fcec129eae45d0c3`
- ARTEFAKT_SYNC: PASS.

## PPA-008 – Universal Product Comparison
- FACHBÜRO: `../PRODUKTVERGLEICH/`
- PRÜFGEGENSTAND: 0.8.0-prototype
- STATUS: aktuelle exakte ZIP nicht aus CURRENT-Autorität erreichbar.
- ARTEFAKT_SYNC: BLOCKED.

## PPA-009 – Universal Product Knowledge
- FACHBÜRO: `../PRODUKTVERGLEICH/`
- BELEGTE ABHÄNGIGKEIT: 0.5.0
- STATUS: exakte aktuelle Installer-/Hashbindung offen.
- ARTEFAKT_SYNC: BLOCKED.

## PPA-010 – Affiliate-Portal Kategorie-Workflow / MOD-001
- ALLGEMEINE HAUPTQUELLE: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`
- STAND: 1.8.0
- SHA-256: `4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`
- PFERDE-PROJEKTANWENDUNG: nicht separat als CURRENT gebunden.
- ARTEFAKT_SYNC: NICHT_ERFORDERLICH.

## PPA-011 – Pferde Atelier – Pferderassen Manager
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- STAND: 0.2.7
- WORDPRESS-LIVE: PASS 2026-09-15
- SHA-256: `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`
- ARTEFAKT_SYNC: PASS.

## PPA-012 – Universal Glossary Engine
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
- STAND: **1.4.7**
- WORDPRESS-LIVE: PASS; Endbestand 92 vom Nutzer bestätigt.
- CURRENT: `/Campus-Plugins/PFERDE_ATELIER/PPA-012/CURRENT.zip`
- SHA-256: `6db2e5ad78ddbf6242cbca0059c7ab60b0a3f5e5bc68e948acc012e5700f4389`
- UPDATEVORGANG: `PU-20260916-001`
- ARTEFAKT_SYNC: PASS.

## PPA-014 – WordPress Speicheranalyse
- FACHBÜRO: `../TECHNIK/`
- VON/AUF: 1.0.1 → 1.1.0
- SHA-256: `3acb62811ec8e7ea1940ec0968e5b51fc2cb0d1ae2f9e86eeeb6718c11873891`
- LOCAL: PASS; WORDPRESS-LIVE: OFFEN.
- ARTEFAKT_SYNC: PASS.

## PPA-015 – Rassentexte 196 Textpflege Updater
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- KLASSE: EINMALIGES WARTUNGSPLUGIN
- STAND: **1.1.0**; 1.0.0 verworfen.
- WORDPRESS-LIVE: PASS; finaler Dry-Run 196/196 Zielstand, Nutzer-Stichprobe bestätigt.
- CURRENT: `/Campus-Plugins/PFERDE_ATELIER/PPA-015/CURRENT.zip`
- SHA-256: `4bca49f986da897c4941674bda6646cdf5de26c7a7ea78fa26b3e82aefe6fd37`
- UPDATEVORGANG: `PU-20260916-017`
- BETRIEB: Auftrag abgeschlossen; Plugin kann in WordPress deaktiviert/gelöscht werden. Tatsächliche Löschung nicht bestätigt.
- ARTEFAKT_SYNC: PASS.

## Harte Regel
Neue Plugins/Versionen niemals aus Dateinamen oder Erinnerung ableiten. Erst Fachquelle + Version + Hash + erforderliche Tests + ggf. LIVE; danach Artefaktsync.
