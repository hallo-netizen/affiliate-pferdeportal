# 20.11.2026 – Hab & Bewahr 0.4.31.11: DataForSEO-Echtdaten, belegter Grundfehler

## Live-Fehler und Ursache
Zwei unterschiedliche abgeschlossene Hab-Kategorien (Abholbox; Abluftanlagen & Unterdruck) hatten jeweils 9 Roh-Keywords und 0 nutzbare, darunter Pizza, Phone, SEO-Marketing. Die KEYWORD_IDEAS-Anbieterantwort hatte in beiden Diagnosen denselben Hash. Zwei unterschiedliche Suchthemen mit identischen generischen Anbieterbeispielen.

**Original-ZIP 0.4.31.10** wurde aus dem vorhandenen Hab-Büro materialisiert und gegen **Pferdeatelier 0.4.39** und **Hobbydepot 0.4.24.17** verglichen. `original/pste/includes/class-pste-plugin.php` setzt in Hab `environment=sandbox` als Default und `migrateSettings` lässt gespeicherte Sandbox-Werte stehen. Die originale Research-Job-Klasse speichert `$settings['environment']` im Job. Der originale DataForSEO-Client sendet dann an `sandbox.dataforseo.com` statt `api.dataforseo.com`. Hobbydepot hat den bereits vorhandenen Produktionsmodus-Fix (Default und Migration erzwingen `production`); bei Hab wurde diese Übernahme ausgelassen. Pferdeatelier hat einen konfigurierbaren Originalmodus; die LIVE-WP-Einstellung von Pferdeatelier ist hier nicht belegt.

## Gebündelter Fix
**Hab 0.4.31.11** übernimmt exakt die zwei bereits in Hobby verwendeten Konfigurationszeilen. Eine zentrale Anbieterentscheidung: `PSTE_Plugin::settings()` liefert `production`, auch wenn alte Sandbox-Einstellungen gespeichert wurden. Keine Änderung am Original-Client. Anzeige im vorhandenen Recherche-Backend zeigt `Echtdaten (api.dataforseo.com)`; read-only Diagnose gibt effektiven Provider-Modus und Host aus. Keine extra fachliche Entscheidung, keine neue API-Abfrage durch die Installation. Alte COMPLETE-Sandbox-Läufe bleiben unverändert erhalten und werden nicht stillschweigend neu beauftragt.

## Tests an entpacktem finalem ZIP
- 134/134 ursprüngliche Original-PHP-Regressionsfälle bestanden (vier Recherchewege 48; Finalize-Job 9; Queue 11; beide gemeinsam 5; Hab-MINI 17; Hab-Import 14; PAA direkt 11; PAA-Queue 8; PAA-Restore 11).
- 30/30 neue Originalklassen-Prüfungen: alte gespeicherte Sandbox-Option, Neustart ohne Option, production/invalid/empty, Budgets & Freigaben unverändert; Client produziert Produktions-URL; Sandbox-/Production-Cache sind getrennt; Original-Request erfolgreich vor Netzwerk abgefangen. 0 echte Anbieteranfragen.
- 78/78 PHP-Lints; 87/87 ZIP-CRC; 83/87 Dateien bitidentisch zum ZIP 0.4.31.10.
- Nur geändert: `original/pste/includes/class-pste-plugin.php`, `texterstellung.php` (Version/Anzeige), `includes/class-txe-diagnose.php` (read-only Modus), `README-TESTINSTALLATION.txt`.
- Original-K0, vier Anbieterwege, Budget, MINI, Kategoriezuordnung, Import und alte Aufträge unverändert. **Kein Live-End-to-End-Erfolg behauptet.**

## Ablage und Nächster Schritt
ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.11_DATAFORSEO_ECHTDATEN_FIX.zip`, SHA256 `893546b5b14ced799c9e508c0bcf3d7cb9814558f01adf38002fb51ac523d7f4`, im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/` gespeichert. Vollbericht, QA-JSON und Originaldiff unter `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ECHTDATEN_20261120/`.

Nächster Schritt: WordPress-Backup; bestehendes Plugin 0.4.31.10 **durch 0.4.31.11 ersetzen, nicht deinstallieren**. In `Texterstellung → Recherche` zunächst nur den Echtdaten-Host prüfen – kostenlos. **Erst danach** ist ein einziger ausdrücklich kostenpflichtig bestätigter neuer Recherchelauf für eine offene Kategorie als Live-Abnahme sinnvoll. Alte COMPLETE-Sandbox-Kategorien werden nicht automatisch neu geöffnet.