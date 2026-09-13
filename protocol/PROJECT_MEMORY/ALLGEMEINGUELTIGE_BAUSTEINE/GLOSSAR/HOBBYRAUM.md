# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.6 FRESH + IN-PLACE HARDTEST PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**HIER BIST DU RICHTIG, WENN …**  
der projektunabhängige WordPress-Kern des Glossars gebaut, geprüft oder über einen gebundenen Updateweg weitergeführt wird.

**DU DARFST …**  
den neutralen Core, Datenvertrag, Projektkonfiguration und harte Positiv-/Negativtests entwickeln.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den Core schreiben, `main` verändern, das bestehende Designplugin als Glossar-Engine umbauen, unterschiedliche Pakete unter derselben Versionsnummer erzeugen oder vor realem Nachweis einen LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
den exakt hashgebundenen 0.2.6-Kandidaten nur über den geprüften WordPress-Updateweg in der Pferde-Anwendung testen und danach echten Readback der gemeldeten Frontendfehler durchführen.

## AKTUELLER AUFTRAG

`MOD-008 – Universal Glossar Engine` ist technisch bis zum 0.2.6-Fresh-/Upgrade-Hardtest geführt.

Aktuell keine neue Funktion bauen.

Nächste Arbeit ist Integrations-/Readback-Prüfung des exakt getesteten Kandidaten in der ersten realen Projektanwendung Pferde Atelier.

## ARBEITSORT

Isolierter Branch:
`hobbyroom/glossar-026-upgrade-hardtest-20260913`

Technisch getesteter Commit:
`e5f8c8ce1839a69f3e6fb712bd4a3d4a3e8ad059`

Autoritativer Testlauf:
`34748541630`

Technischer Kandidat:
`0.2.6`

Innerer Plugin-ZIP SHA-256:
`e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`

Actions-Artefakt-ID:
`10314822840`

Testdetails:
`TESTPROTOKOLL_0.2.6_20260913.md`

## HARTE KANDIDATENBINDUNG

0.2.6 wird deterministisch aus dem bereits geprüften 0.2.5-Kandidaten gebaut.

Erlaubtes Delta exakt:
1. Hauptplugin-Version 0.2.5 → 0.2.6;
2. Rewrite-Schema 4 → 5.

Kein weiteres verstecktes Delta zulässig.

Keine neue Ausgabe als 0.2.6 nach Codeänderung ohne neuen vollständigen Hardtest und neuen Hash.

## TESTSTAND

### Fresh-Install

Run `34748541630`, Job `103700782149` → PASS.

Positiv/negativ unter WordPress + MySQL + Astra:
- Plugin 0.2.6 / Schema 5;
- Startseite, Navigation, A–Z;
- alle Kartenlinks;
- echte Einzelbegriffsseite statt bloß HTTP 200;
- Draft/404/Preview;
- AJAX gültig/ungültig;
- Kategorie-/Begriffskollision;
- normaler WordPress-Beitrag unverändert;
- Hero-Abstand;
- responsive Hero-Darstellung;
- Breadcrumb-Achse;
- alte Regressionen erneut PASS.

### In-place-Upgrade 0.2.5 → 0.2.6

Run `34748541630`, Job `103700782306` → PASS.

Negativer Vorzustand:
- Einzelbegriff-Rewrite-Regel unter aktivem 0.2.5 gezielt entfernt;
- bekannter Einzelbegriff danach 404;
- Schema bleibt 4.

Echter WordPress-Updater:
- 0.2.5 mit 0.2.6 überschrieben;
- erster neuer Request migriert Schema 4 → 5;
- Regel wird wieder aufgebaut;
- bekannter Einzelbegriff wieder echte 200-Artikelseite.

Danach vollständige Positiv-/Negativmatrix erneut PASS einschließlich Daten-/Konfigurationspersistenz und Reaktivierung.

### Gated Package

Job `103700913568` → PASS.

Paket wurde erst nach beiden grünen Jobs gebaut.

### Lokaler exakter Artefaktcheck

PASS:
- Hashbindung;
- ZIP-Struktur;
- keine Traversal-/Symlink-Pfade;
- lokaler 0.2.5↔0.2.6-Dateivergleich exakt zwei erlaubte Dateien;
- positive Version-/Schema-/Frontendregeln;
- negative Altversion-/Altschema-/alte CSS-Hacks;
- PHP-Lint aller 10 PHP-Dateien.

## VERSIONIERUNGSREGEL

Dauerhaft:
`ENTSCHEIDUNG_20260912.md`

Keine materiell unterschiedlichen Pakete mehr unter derselben Versionsnummer.

## NEXT ACTION

1. Keine weitere technische Änderung am Kandidaten.
2. Exakt den hashgebundenen 0.2.6-ZIP verwenden.
3. In Pferde Atelier als Update über den WordPress-Pluginweg installieren.
4. Direkt danach Readback der vier gemeldeten Punkte:
   - Hero-Abstand;
   - Responsive Hero;
   - alle Einzelbegriff-Links inklusive echtem Seiteninhalt;
   - Kategorie-Breadcrumb Position/Darstellung.
5. Negativ zusätzlich normale Beiträge, 404, Draft und Kategorie/gleichnamiger Begriff prüfen.
6. Nur bei realem PASS darf Pferde-Anwendung hochgestuft werden.
7. Bei FAIL: erster exakter Fehler zurück in `PROJEKTE/PFERDE_ATELIER/GLOSSAR/FEHLERQUELLEN.md`; kein neues Paket ohne erneute harte Prüfung.

## DANACH OFFEN

- aktueller Astra+Yoast-Kombinationstest, soweit für endgültigen Release gebunden;
- realer Campus-Wissensdatenbankimport;
- größerer Bestand/Performance;
- separates zweites reales Portal.

## HARTE REGEL

**Technischer Kandidaten-PASS ist kein Pferde-Atelier-LIVE-PASS.**

`main` und bestehendes Designplugin bleiben unangetastet.

## RÜCKGABEWEG

Projektanwendung Pferde Atelier:
`../../PROJEKTE/PFERDE_ATELIER/GLOSSAR/`

Fachquelle Pferdebegriffe:
`../../PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
