# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / V1-PROTOTYP LOKAL PASS

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**HIER BIST DU RICHTIG, WENN …**  
der projektunabhängige WordPress-Kern des Glossars gebaut oder getestet wird.

**DU DARFST …**  
den neutralen Core, Datenvertrag, Projektkonfiguration und Positiv-/Negativtests entwickeln.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den Core schreiben, `main` verändern, das bestehende Designplugin als Glossar-Engine umbauen oder vor Realtest einen Release/LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
den lokal grünen 0.1.0-Prototyp in einem echten WordPress-Testsystem installieren und die gebundenen Realtests ausführen.

## AKTUELLER AUFTRAG

`MOD-008 – Universal Glossar Engine` vom lokalen Prototyp-PASS zum echten WordPress-Smoke-Test bringen.

## ARBEITSORT

Isolierter Branch:
`hobbyroom/glossar-v1-current-20260912`

Quellstand:
`prototype/0.1.0/universal-glossary-engine/`

QA:
`PROTOTYPE_QA_0.1.0.md`

Aktueller lokaler ZIP-Hash:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

## V1-KERN – LOKAL VORHANDEN

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

Noch offen:
- echter WordPress-Install/Upgrade;
- Permalink `/glossar/<begriff>/` neben vorhandener Seite `/glossar/`;
- echter Yoast-Test;
- echtes Astra/Pferde-Frontend;
- realer JSON-Import;
- Performance größerer Bestand.

## NEXT ACTION – REALTEST

1. exakt den hashgebundenen 0.1.0-Kandidaten in isoliertem WordPress testen;
2. vorhandene Seite `Glossar` als Hauptseite wählen;
3. zwei Oberbereiche + mindestens drei Testbegriffe anlegen;
4. Backendtrennung von normalen Beiträgen/Seiten prüfen;
5. Hauptseite: Suche/A–Z/Oberbereiche/Aufklapper prüfen;
6. Begriff-URL + SEO-Titel + Meta-Description prüfen;
7. Yoast aktiv/inaktiv positiv und negativ prüfen;
8. JSON-Export → Reimport als Entwurf prüfen;
9. normalen Beitrag und bestehendes Designplugin negativ gegenprüfen;
10. erst bei Gesamt-PASS installierbaren Kandidaten freigeben.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

Nur bei echtem unkonfigurierbarem Zweitportalproblem:
neutraler Core + kleiner Adapter. Kein zweiter kompletter Plugin-Fork.

## HARTE REGEL

**Kein Release-/LIVE-PASS aus lokalem Stubtest ableiten.**

`main` und bestehendes Designplugin bleiben unangetastet.

## RÜCKGABEWEG

Projektanwendung Pferde Atelier:
`../../PROJEKTE/PFERDE_ATELIER/GLOSSAR/`

Fachquelle Pferdebegriffe:
`../../PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
