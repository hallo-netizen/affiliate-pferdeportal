# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.7 TECHNISCH HARDTEST PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
den exakt gebundenen Glossar-Kandidaten prüfen und den realen Pferde-Atelier-Readback durchführen.

**DU DARFST NICHT …**  
`main` verändern, neue Funktionen bauen, das Designplugin umbauen, den getesteten ZIP nachträglich verändern oder vor realem Readback einen Pferde-LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
exakt das hashgebundene 0.2.7-ZIP über den geprüften WordPress-Updateweg installieren und die vier gemeldeten Frontendpunkte plus negative Regressionen real prüfen.

## GEBUNDENER KANDIDAT

Plugin:
`Universal Glossary Engine 0.2.7`

Rewrite-Schema:
`5`

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`

Getesteter Commit:
`7191f15358cc73a78231652e9479f3a9fb5a9c37`

Autoritativer Run:
`34749231699`

Fresh-Install Job:
`103702569466` → PASS

In-place-Update Job 0.2.5 → 0.2.7:
`103702569602` → PASS

Gated Package Job:
`103702749853` → PASS

Innerer Plugin-ZIP SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`

Actions-Artefakt-ID:
`10315142446`

Testprotokoll:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.7_20260913.md`

## VERSIONSREGEL

0.2.6 ist nur Entwicklungs-/Testhistorie und nicht mehr übergabefähig.

Aktuelle Übergabe ausschließlich 0.2.7.

Dauerhaft:
**Unterschiedliche Paketbytes = unterschiedliche Versionsnummer.**

## HARTER PRÜFSTAND

Positiv/negativ PASS:
- Fresh-Install WordPress + MySQL + Astra;
- echter WordPress-Updater 0.2.5 → 0.2.7;
- absichtlich entfernte Rewrite-Regel erzeugt 404;
- nach Update und normaler OPcache-Revalidierung Schema 4 → 5;
- Einzelbegriffe liefern echtes Glossar-Artikelmarkup und Inhalt;
- unbekannter Begriff 404;
- Draft 404;
- Legacy 301;
- AJAX gültig/ungültig;
- Kategorie-/Begriffskollision getrennt;
- normale Beiträge unverändert;
- Daten/Konfiguration erhalten;
- Reaktivierung ohne Routingverlust;
- Hero-Abstand;
- responsive Hero-Darstellung;
- Breadcrumb-Achse;
- vollständige alte Regression-/Frontend-/Acceptance-Matrix erneut PASS;
- erzeugtes ZIP lokal erneut auf Hash, Struktur, Version 0.2.7 und Schema 5 geprüft;
- negativ: Pluginheader enthält keine aktuelle Version 0.2.6.

## DIE VIER REAL ZU PRÜFENDEN PUNKTE

1. Abstand vom Hero nach oben.
2. Hero-Bild responsive auf schmalem Bildschirm.
3. Alle Einzelbegriff-Links: keine weiße Seite; Titel und Inhalt sichtbar.
4. Kategorie-Breadcrumb: Position und Darstellung gemäß Pferde-Atelier-Standard.

## NEGATIV-READBACK

Zusätzlich zwingend:
- unbekannter Glossarbegriff bleibt 404;
- Entwurf bleibt nicht öffentlich;
- normale WordPress-Beiträge bleiben unverändert;
- Kategorie und gleichnamiger Einzelbegriff bleiben getrennt;
- keine doppelte Breadcrumb-Ausgabe;
- keine globale Layoutverschiebung außerhalb Glossar.

## INSTALLATIONSWEG

Nur:
WordPress-Pluginupdate/Überschreiben der vorhandenen 0.2.5 mit dem exakt hashgebundenen 0.2.7-ZIP.

Nicht:
- Dateien einzeln austauschen;
- 0.2.6 installieren;
- anderes 0.2.7-Paket bauen;
- getestetes ZIP nachträglich verändern.

## RÜCKGABELOGIK

Bei realem PASS:
- `FEHLERQUELLEN.md` nur für tatsächlich bewiesene Punkte schließen;
- `CURRENT_STATE.md` auf realen Stand ziehen;
- erst danach weitere Integrationsarbeit.

Bei FAIL:
- ersten exakten Fehler dokumentieren;
- Kandidat bleibt BLOCKED;
- kein neues Paket ohne neue Versionsnummer und erneute Fresh + Upgrade + Positiv/Negativ + lokale ZIP-Kontrolle.

## HARTE REGEL

**Technischer Hardtest-PASS ist kein Pferde-Atelier-LIVE-PASS.**

`main` bleibt unangetastet.
