# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / ECHTER WORDPRESS+MYSQL-SMOKE-TEST PASS

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**HIER BIST DU RICHTIG, WENN …**  
der projektunabhängige WordPress-Kern des Glossars gebaut oder getestet wird.

**DU DARFST …**  
den neutralen Core, Datenvertrag, Projektkonfiguration und Positiv-/Negativtests entwickeln.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den Core schreiben, `main` verändern, das bestehende Designplugin als Glossar-Engine umbauen oder vor Release-/LIVE-Nachweis einen Release/LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
den unveränderten 0.1.0-Core real mit Astra + Yoast prüfen.

## AKTUELLER AUFTRAG

`MOD-008 – Universal Glossar Engine` nach bestandenem WordPress/MySQL-Smoke-Test gegen die reale Zielkombination Astra + Yoast prüfen; danach realen Wissensdatenbankimport binden.

## ARBEITSORT

Isolierter Branch:
`hobbyroom/glossar-v1-current-20260912`

Quellstand:
`prototype/0.1.0/universal-glossary-engine/`

QA:
`PROTOTYPE_QA_0.1.0.md`

Früher lokal gebauter Prototyp-ZIP-Hash:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

Dieser Hash ist kein finaler Release-Installer.

## V1-KERN

- eigener Backend-Menübereich;
- eigener Glossarbegriff-Inhaltstyp;
- eigene hierarchische Glossar-Oberbereiche;
- eigene Zieladresse je veröffentlichtem Begriff;
- eigene SEO-Titel-/Meta-Description-Felder;
- auswählbare vorhandene Glossar-Hauptseite;
- A–Z + Suche + Oberbereiche + Aufklapper;
- kein Bildzwang;
- kein normales Beitragsarchiv;
- kein Auto-Publish;
- JSON-Import/Export;
- Import ausschließlich als Entwurf;
- keine Yoast-Pflichtabhängigkeit;
- keine Fachbegriffe im Core;
- erweiterbares Feldschema;
- konfigurierbare Designwerte.

## TESTSTAND

Lokal:
- PHP-Lint 8/8 PASS;
- statisch positiv/negativ 15/15 PASS;
- Runtime-Stub PASS;
- Pferde-Profil PASS;
- fachfremdes `Lexikon`-Profil PASS ohne Coreänderung;
- ZIP-Struktur PASS.

Echter WordPress/MySQL-Test:
- Run `34699122729` → PASS;
- WordPress 6.9 / PHP 8.1.34 / MySQL 8.0 → PASS;
- WordPress 7.1 / PHP 8.3.33 / MySQL 8.0 → PASS;
- `/glossar/` + `/glossar/kolik/` parallel → PASS;
- SEO ohne Yoast → PASS;
- JSON Import/Export → PASS;
- Import bleibt Entwurf → PASS;
- unbekanntes Importfeld wird verworfen → PASS;
- Zusatzfeld ohne Coreänderung → PASS;
- reale `Lexikon`-Zweitkonfiguration → PASS;
- Deaktivieren/Reaktivieren ohne Daten-/Seitenverlust → PASS;
- keine normalen Seiten pro Glossarbegriff → PASS.

## NEXT ACTION – ASTRA + YOAST

1. unveränderten 0.1.0-Core in isoliertem WordPress installieren;
2. Astra aus dem offiziellen WordPress-Verzeichnis installieren und aktivieren;
3. Yoast SEO aus dem offiziellen WordPress-Verzeichnis installieren und aktivieren;
4. `/glossar/` und Begriffszieladresse real laden;
5. eigenen SEO-Titel/Description/Canonical/Robots prüfen;
6. negativ prüfen: keine doppelte Description/Canonical/Robots-Ausgabe;
7. Astra-Darstellung darf Glossarindex und Einzelansicht nicht zerstören;
8. normalen Beitrag/normale Seite negativ unverändert prüfen;
9. danach realen Campus-Wissensdatenbankimport als nächsten einzigen offenen Integrationsschritt binden.

## DANACH OFFEN

- realer Campus-Wissensdatenbankimport;
- größerer Bestand/Performance;
- finaler ZIP-Install-/Update-/Reinstall-Test;
- separates zweites reales Portal;
- Pferde-Atelier-LIVE-Installation.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

Nur bei echtem unkonfigurierbarem Zweitportalproblem:
neutraler Core + kleiner Adapter. Kein zweiter kompletter Plugin-Fork.

## HARTE REGEL

**WordPress-Smoke-PASS ist kein Pferde-Atelier-LIVE-PASS.**

`main` und bestehendes Designplugin bleiben unangetastet.

## RÜCKGABEWEG

Projektanwendung Pferde Atelier:
`../../PROJEKTE/PFERDE_ATELIER/GLOSSAR/`

Fachquelle Pferdebegriffe:
`../../PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
