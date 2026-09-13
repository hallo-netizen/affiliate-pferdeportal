# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.7 FRESH + IN-PLACE HARDTEST PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**DU DARFST …**  
den neutralen Core und seine gebundenen Positiv-/Negativtests pflegen.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den Core schreiben, `main` verändern, unterschiedliche Paketbytes unter derselben Versionsnummer erzeugen oder vor realem Nachweis einen LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
den exakt hashgebundenen 0.2.7-Kandidaten in der Pferde-Anwendung über den geprüften WordPress-Updateweg installieren und real zurücklesen.

## GEBUNDENER TECHNISCHER KANDIDAT

Version:
`0.2.7`

Rewrite-Schema:
`5`

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`

Getesteter Commit:
`7191f15358cc73a78231652e9479f3a9fb5a9c37`

Run:
`34749231699`

Fresh Job:
`103702569466` → PASS

Update Job 0.2.5 → 0.2.7:
`103702569602` → PASS

Gated Package Job:
`103702749853` → PASS

Innerer ZIP-SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`

Actions-Artefakt-ID:
`10315142446`

Testdetails:
`TESTPROTOKOLL_0.2.7_20260913.md`

## VERSIONIERUNGSREGEL

0.2.6 bleibt reine Entwicklungs-/Testhistorie und wird nicht mehr übergeben.

Aktueller Kandidat ausschließlich 0.2.7.

Dauerhaft:
**Unterschiedliche Paketbytes = unterschiedliche Pluginversion.**

Jede materielle Änderung nach 0.2.7 benötigt eine neue Versionsnummer und erneut:
Fresh-Install + echter In-place-Updateweg + Positiv/Negativ + gebundener Paketjob + lokaler exakter Artefaktcheck.

## TESTSTAND

PASS:
- Fresh WordPress/MySQL/Astra;
- Version 0.2.7 / Schema 5;
- absichtlich defekter 0.2.5-Rewritezustand;
- echter WordPress-Updater 0.2.5 → 0.2.7;
- nach OPcache-Revalidierung Schema 4 → 5;
- echte Einzelbegriffsseite statt nur HTTP 200;
- Draft/404/Legacy/AJAX-Negativfälle;
- Kategorie-/Begriffskollision;
- normale Beiträge unverändert;
- Daten-/Konfigurationspersistenz;
- Reaktivierung;
- Hero-Abstand;
- responsive Hero-Darstellung;
- Breadcrumb-Achse;
- komplette alte Regressionen erneut PASS;
- exakt erzeugtes ZIP lokal Hash-/Struktur-/Version-/Schema-geprüft.

## NEXT ACTION

1. Keine weitere Codeänderung am Kandidaten.
2. Exakt das hashgebundene 0.2.7-ZIP verwenden.
3. Pferde Atelier über den WordPress-Pluginupdateweg aktualisieren.
4. Real prüfen:
   - Hero-Abstand;
   - responsive Hero-Darstellung;
   - alle Einzelbegriff-Links mit sichtbarem Titel/Inhalt;
   - Kategorie-Breadcrumb Position/Darstellung.
5. Negativ zusätzlich normale Beiträge, unbekannten Begriff, Draft und Kategorie/gleichnamigen Begriff prüfen.
6. Erst nach realem PASS Projektstatus hochstufen.
7. Bei FAIL: erster exakter Fehler in der Pferde-Fehlerquelle; neues Paket nur mit neuer Version und kompletter neuer Hardtestkette.

## HARTE REGEL

**Technischer Kandidaten-PASS ist kein Pferde-Atelier-LIVE-PASS.**

`main` und bestehendes Designplugin bleiben unangetastet.
