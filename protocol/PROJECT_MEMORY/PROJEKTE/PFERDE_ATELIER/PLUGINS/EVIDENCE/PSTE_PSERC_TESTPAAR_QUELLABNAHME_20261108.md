# Pferdeatelier – echter gemeinsamer PSTE/PSERC-TESTPAAR-Quellnachweis, 08.11.2026

**Status:** Isolierte QA-Quellabnahme **PASS**, **KEINE** WordPress-/Live-/K0-Installationsfreigabe. Nur Branch `fix/pste-kisten-einmalige-pruefung-20261107`, Draft-PR #682. Alle ursprünglichen Plugin-ZIPs, gespeicherter PPM679-Redaktionsplan, K0, Live und Sicherheitsdateien unverändert.

## 1. PSTE: gesichertes Original + bestehende Funktionen

- Unverändertes Ursprungs-ZIP: `INSTALLATIONS_PAKETE/PSTE-0.57.144.22-NUR-TEST.zip`, SHA256 `479260fc210683b0e4867588bafa0889a66af3443341c69ec19452d9476b403a`.
- Reproduzierbare isolierte PSTE-Testfassung aus genau diesem ZIP: `QA_ONLY/apply_existing_mini_kisten_import.py` + `QA_ONLY/apply_wp_single_owner_gate.py`, **nur die bereits vorhandenen Klassen**.
- Daraus GitHub-Actions-Test-ZIP `PSTE-ONE-OWNER-0.57.144.22-QA-ONLY-NICHT-INSTALLIEREN.zip` mit SHA256 **`0d01ea4552a322278e45f2390915cb8352ffe0862f8e0a5d00490fac942400e0`**.
- GitHub Actions **[42464940106](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42464940106) SUCCESS**, Artefakt-ID `13611212701`, Name `PSTE-ONE-OWNER-STAGING-QA-NICHT-INSTALLIEREN`; gespeichert als zeitlich begrenztes GitHub-Artefakt (Ablauf **08.12.2026**). Die dauerhafte Reproduktionsquelle liegt im Plugin-Büro.
- 100 unveränderte originale MINI-Keywords als Ausgangsdaten; externe **SEO-Urteile in diesen Tests sind fiktiv**. `forwardToPlan` vorhandene Funktion in WP-Datenbankmock GOOD/STALE/ONEBAD PASS; Kontext-/Planweg ohne doppelte semantische SEO-Bewertung. 83/83 PSTE-PHP-Dateien Syntax PASS.
- Das Original-PSTE-v22 liefert eine **reale** unveränderte Compiler-Lesefähigkeit, nicht nur eine erfundene Schnittstelle. Die echte Methode `PSTE_Compiler_Read_Capability::describe()` wurde tatsächlich im Original-PHP ausgeführt: GitHub Actions **[42465127195](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42465127195) SUCCESS**. Originalausgabe im QA-Büro: `QA_ONLY/PSTE_V22_REAL_READ_CAPABILITY_20261108.json`, SHA-Feld `f7d7ad918b0925c4f7cf99f8b18f56419d55d06f4fc1edb2952767a4d5d8dc5b`.

## 2. PSERC: unverändertes Ursprungs-ZIP und NUR die bestehende Klasse korrigiert

- Unverändertes Ursprungs-ZIP aus dem bisherigen Paketbestand: `PFERDEATELIER_PSERC_0.28.53_GESAMT_KISS_NUR_TEST.zip`, SHA256 **`80340faff2323e5ede86ddd095ac3570a53474ae64771df3bec70fb6f6c6f060`**.
- Vorheriger QA-Stand 0.28.54: SHA256 `2c31ae1bf89613abf456576039f9bd52ef6ed41c1f84c28fd0c57410846033a1`, bereits gesicherte Änderungen gegenüber 0.28.53 in `QA_ONLY/PSERC_EXISTING_OWNER_NO_SECOND_SEMANTIC_QA.patch`.
- **Neu gefundener echter Fehler in PSERC v0.28.54:** Die vorhandene `PSERC_SEO_Reader::normalizeCandidate` konnte einen Thema mit externem SEO-Owner bei veralteter oder verschwundener externer Freigabe weiter als **ELIGIBLE** ausgeben. Damit war der alte zweite PSERC-Semantikvergleich erneut erreichbar. Tatsächlich mit dem **originalen PSERC-Reader** reproduziert: gültige externe Freigabe `ELIGIBLE`, veralteter Rückbeleg vorher fälschlich ebenfalls `ELIGIBLE`.
- **Ursache behoben in der vorhandenen Reader-Funktion:** Sobald eine externe SEO-Entscheidung bereits beansprucht wird, aber die zugehörige Quellen-/Titel-Freigabe nicht mehr gültig ist: **HELD** mit `SEO_EXTERNAL_SINGLE_OWNER_PROOF_MISSING_OR_STALE`. **Kein zweiter SEO-Vergleich**, keine Ersatzautorität, kein zusätzlicher Worker. Unabhängige alte Themen laufen über ihre bisherige Legacy-Prüfung.
- Neue **vollständige PSERC-QA-Version 0.28.55**, intern mit Build `0.28.55-one-owner-no-fallback`, SHA256 **`5fb82d0b35346d71d1cc0d9a796e5ca19d1ac3ad595ec5aab9643154db8a8578`**. Original **63/63 ZIP-Pfade erhalten**; gegenüber dem unveränderten 0.28.53 nur **drei bereits vorhandene PHP-Klassen**, Hauptversionsdatei und existierendes Paketintegritätsmanifest abweichend. **43/43 PHP Syntax PASS**, **61/61 Paketintegritätsbindungen PASS**. Kein K0-, Redaktionsplan- oder WordPress-Datei-Umbau.
- Die v0.28.55-Datei wurde **zweimal unabhängig von der vorherigen QA-ZIP reproduziert und bytegleich** zurückgerechnet (gleicher SHA256). Der dauerhafte, einzige reproducible QA-Bausschritt steht unter `QA_ONLY/rebuild_pserc_02855_from_02854.py`.
- **Sechs echte Reader-Proben PASS:** gültige externe Freigabe; veraltete Freigabe HELD; geänderter Titel HELD; fehlender Beleg HELD; einzelner Besitzerstatus ohne echte Antwort HELD; altes unabhängiges Thema unverändert. Testprogramm `QA_ONLY/test_pserc_02855_stale_owner_no_fallback.php`.
- **Echte Paar-Schnittstelle PASS:** Das aus dem echten PSTE-PHP erzeugte Capability-JSON wurde vom **tatsächlichen PSERC-0.28.55-Quellcode** `PSERC_SEO_Source_Binding::validate` bei exakt passendem SHA als `PSERC_SEO_CAPABILITY_BINDING_PASS` bestätigt. Ein freigegebener Schreibzugriff wird abgelehnt. Gleichfalls direkte Tests gegen unverändertes `PSERC_Metadata_Boundary`: exakt fünf Skalarfelder PASS, zusätzlicher Artikeltext und `publish_allowed=true` BLOCK. Gesicherter reproduzierbarer Test `QA_ONLY/test_real_pserc_package_02855_boundary.php`.
- Der exakte PSERC-Paketscope ist durch `QA_ONLY/test_pserc_staging_pair_packaging.py` überprüfbar. Das PSERC-QA-ZIP wurde im Arbeitscontainer erzeugt, **noch nicht als vollständige binäre ZIP-Datei im GitHub-Repository eingecheckt**; dauerhaft auf GitHub liegen vollständiger reproduzierbarer Baucode, Quellenpatch, unveränderte Ursprungshashwerte und Testprotokoll. **Keine falsche GitHub-ZIP-Behauptung.**

## 3. Gesamtabnahme / tatsächliche Grenze

**PASS (wirklich bewiesen):** Beide vollständigen Plugin-Testpakete einzeln auf Quell- und Integritätsebene; direkte echte Lese-Schnittstelle der PSTE-Original-PHP-Klasse gegen die tatsächliche PSERC-0.28.55-Bindung; fail-closed bei fehlender externer Freigabe; PSERC keine semantische Zweitbewertung für extern entschiedene Themen; unveränderte exakt fünf K0-Metadatenfelder. Keine neue Laufzeitarchitektur.

**NICHT PASS / offen:**
1. Keine nachweislich gemeinsam **in einer echten Test-WordPress-Instanz gestarteten** PSTE-/PSERC-Pakete. Der Quelltest ist kein MySQL-/WP-Echtlauf.
2. Kein aktueller vollständiger TEST-WordPress-Export, daher kein tatsächliches **eines externen SEO-Owners** gegen alle echten vorhandenen Artikel/Pläne. Die 100 ursprünglichen Keywords sind Quelle, die simulierten `FREI/BELEGT/KLAERUNG` keine realen Urteile.
3. Kein kompletter WordPress→PSERC→K0-Realtest. K0 darf für diese Vorprüfung **nicht** umgebaut oder unkontrolliert gestartet werden.
4. GitHub-Immutable-Hardlock-Prüfung ist derzeit **nicht grün**. Die QA-Quelltests gelten **nicht** als Security-Hardlock-Freigabe; Hardlock wurde nicht verändert oder umgangen.
5. Die technische Paketversion ist isolierte QA, nicht kontrolliert auf TEST installiert; daher **NICHT INSTALLIEREN / NICHT MERGEN / NICHT LIVE**.

**Nächster zielgerichteter Schritt:** Einmalige, gesicherte TEST-Installation **nur nach separater Sicherheits-/Versionsfreigabe** des tatsächlich aktuellen Stagingstands, dann echtes WordPress-Parkhaus-Exportfile; darauf nur eine externe SEO-Entscheidung und kontrollierte Rückgabe in vorhandenes PSTE/PSERC bis an die K0-Grenze. Jeder Zwischenstand/Beleg bleibt im Pferdeatelier-Plugin-Büro.
