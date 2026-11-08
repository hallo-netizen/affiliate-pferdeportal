# Pferdeatelier – PSERC 0.28.55 vollständige Paketfassung und WordPress-Versionskopf, 08.11.2026

**Checkpoint 7 – echter Originalpaketfehler korrigiert, als QA unverändert isoliert.** K0, gespeicherter PPM679-Redaktionsplan, WordPress-Live und ursprüngliche Plugin-ZIPs unverändert. Keine neue Prüfschicht, keine neuen PHP-Klassen, keine Tabellen.

## 1. Tatsächlich gefundener Fehler

Die bisherige **vollständige PSERC-QA-ZIP 0.28.55** mit SHA256 `5fb82d0b35346d71d1cc0d9a796e5ca19d1ac3ad595ec5aab9643154db8a8578` enthielt:
- PHP-Laufzeitversion: `PSERC_VERSION=0.28.55`, `PSERC_BUILD=0.28.55-one-owner-no-fallback`.
- **WordPress-Sichtversion im Plugin-Kopf: `Version: 0.28.54`**.

Das ist ein konkreter Versionierungsfehler in der bereits verfügbaren kompletten Binärdatei. WordPress hätte deshalb die falsche Versionsnummer angezeigt.

## 2. KISS-Rootfix – nur vorhandener Bauweg

- Im bereits vorhandenen, auf GitHub gesicherten `QA_ONLY/rebuild_pserc_02855_from_02854.py` wird **auch der WordPress-Plugin-Kopf** von `0.28.54` auf `0.28.55` korrigiert.
- Das bestehende Manifest `compiler-package-binding-v1.json` wird mit exakt den richtigen neu berechneten Hashes aktualisiert. Die einzige Funktion, die zusätzlich von der Vorgänger-Version 0.28.54 abweicht, bleibt die bereits korrigierte `class-pserc-seo-reader.php` (bei ungültigem Beleg **HELD statt zweiter SEO-Prüfung**).
- **Neues, vollständiges PSERC-0.28.55-QA-ZIP:** `PSERC-0.28.55-EIN-OWNER-VERSIONSKOPF-KORRIGIERT-NUR-QA-NICHT-INSTALLIEREN.zip`. **SHA256: `042772cd3c8d594e39ff28ea46b3c74e431cd26fe680a7c95c7522d337e44e43`.** ZIP umfasst weiterhin **63 Originalpfade**, keinerlei hinzugefügte PHP-Laufzeitklasse.
- Der Bau wurde **aus dem ursprünglichen geprüften 0.28.54-ZIP** (SHA256 `2c31ae1bf89613abf456576039f9bd52ef6ed41c1f84c28fd0c57410846033a1`) **vollständig neu und bytegleich reproduziert**: Ergebnis erneut `042772cd3c8d594e39ff28ea46b3c74e431cd26fe680a7c95c7522d337e44e43`.
- Das vorhandene `QA_ONLY/test_pserc_staging_pair_packaging.py` wurde auf den neuen korrekten SHA256 gebunden. Neuer genau dafür abgelegter Bootstrap-Selbsttest: `QA_ONLY/test_pserc_full_plugin_bootstrap_02855.php`.

## 3. Tests, die am tatsächlichen vollständigen ZIP durchgeführt wurden

**Alle lokal unmittelbar auf Original-PHP-Dateien mit dem gerade erzeugten ZIP ausgeführt:**

- **43/43 PHP-Dateien:** Syntax PASS.
- `PSERC_Package_Integrity::validate()`: **PASS**, **61/61** tatsächlich im Paketmanifest gebundene Dateien, erwartete Version/Build.
- Vollständige Plugin-Hauptdatei geladen, alle 43 PHP-Dateien eingebunden und `PSERC_Plugin::init()` ausgeführt, mit simulierten **WordPress-Hook-Funktionen**: **PASS Frontend** (15 ursprüngliche Hooks), **PASS Admin** (25 ursprüngliche Hooks).
- WordPress-Plugin-Kopf stimmt jetzt exakt mit der Programmlaufzeit überein: **0.28.55 = 0.28.55**.
- Sechs vorhandene Positiv-/Negativfälle des ursprünglichen PSERC-SEO-Readers: **PASS** (gültig weiter, ungültig/alt/fehlend zurückgestellt, unbeteiligte Alt-Themen unverändert).
- Drei echte PHP-Verarbeitungsschritte bis zur schon bestehenden `SLOT`-Phase: **PASS, null doppelte semantische SEO-Läufe**.
- Bestehende exakt-fünf-Felder-K0-Metadaten-Firewall: **PASS**, eingeschmuggelter `body_html` wird abgelehnt.

**Beweisgrenze:** Diese zwei vollständigen Bootstrap-Läufe benutzen **WordPress-Hook-Testfunktionen**, nicht die reale WordPress-Installation; sie beweisen vollständige PSERC-Plugin-Ladefähigkeit, Paketintegrität und registrierte Hooks, aber **nicht** das gleichzeitige Installieren von PSTE und PSERC auf einer echten WordPress-Datenbank. Der letzte reale WordPress-MySQL-Test `42477636295` lief mit PSTE und authentischen PSERC-Ausgabehüllen, **nicht** mit der installierten vollständigen PSERC-0.28.55-ZIP.

**Archivstand:** Binäre QA-ZIP ist im lokalen isolierten Arbeitsbereich erzeugt und auf SHA geprüft; **im GitHub-Büro liegt der vollständige reproduzierbare Bau- und Prüfsatz, nicht die binäre ZIP-Datei.** Nicht so tun, als sei das ZIP bereits als GitHub-Release hochgeladen.

## 4. Noch offen / nächster zulässiger Schritt

Das nun **korrekt versionierte volle QA-ZIP** mit dem bestehenden PSTE-Original-0.57.144.22-QA-Plugin in einer echten gesicherten WordPress-Testinstallation gemeinsam starten. Vor dem ersten vollständigen externen SEO-Owner-Lauf muss der komplette **wirklich vorhandene** WP-/PSTE-/PSERC- und gespeicherte PPM679-Artikelplanstand lesend vorhanden sein. Die echte externe SEO-Abnahme und K0-Übergabe sind **noch nicht** erfolgt. **Kein Merge, keine produktive Installation und keine Veränderung an K0 oder gespeichertem Redaktionsplan.**


## Checkpoint 8 – echter vollständiger WordPress-Paartest technisch vorbereitet

Die einzige erforderliche Abnahme der **zwei vollständig geladenen Plugins im selben echten WordPress** ist jetzt als **ein read-only Testprogramm** im Büro `QA_ONLY/test_real_wp_pste_pserc_pair_once.php` gesichert. Es prüft mit den unveränderten, bereits vorhandenen WordPress- und Pluginfunktionen in einem Durchgang: beide vollständig geladenen Klassenbäume, tatsächliche WordPress-Anzeigeversion 0.28.55, 61/61 echtes PSERC-Manifest, die echte PSTE→PSERC-Lesebindung und **einen vollständigen originalen WP-/PSTE-/PSERC-/gespeicherten PPM679-Bestands-Snapshot**. Es schreibt weder Artikel noch K0 noch einen neuen Plan, legt keine Tabelle und keinen zweiten semantischen Worker an.

**Ehrlicher Ausführungsstatus:** Dieses neu gesicherte gemeinsame WordPress-Paarprogramm wurde **noch nicht im echten WordPress ausgeführt**, da die komplette korrigierte PSERC-QA-ZIP zwar im isolierten Arbeitscontainer erzeugt und verifiziert vorliegt, aber noch nicht als binäre Datei dem externen GitHub-Actions-WordPress-Testsystem zur Verfügung gestellt wurde. Der vollständige Admin-/Frontend-Plugin-Bootstrap in lokalen PHP-WordPress-Hook-Dummies ist hingegen bereits PASS. Nicht so tun, als sei der tatsächliche Test auf der Nutzer-Testseite durchgeführt oder der echte PPM679-Plan schon übertragen. Die GitHub-Ablage umfasst Quellcode, exact hash, Original-Testbelege und reproduzierbaren Paketbau, **keinen** freigegebenen Installer.

**Nächster sauberer Test:** Das vorhandene validierte PSERC-0.28.55-QA-ZIP und PSTE-v22-QA gemeinsam **nur in einer isolierten Wegwerf-WordPress-Installation** laden, dann `wp eval-file QA_ONLY/test_real_wp_pste_pserc_pair_once.php` einmal ausführen. Bis dieser gemeinsame Lauf mit wirklicher aktueller Plan-/Artikelkopie PASS meldet und die echte externe einmalige SEO-Entscheidung erfolgt ist: keine produktive Freigabe.
