# HOBBY DEPOT – AFFILIATE – EINZIGE AKTUELLE FACH-AUTORITÄT

**Neu zur Design- und Produktstrategie 0.1.20:** Siehe `BANNER_ZIELREGELN_20261107.md`. Banner-Design ist in der neuen aktuellen Voll-ZIP, DataForSEO-Recherche weiterhin manuell; kein automatischer Produktlinkwechsel. Sonstige ältere Prüfabschnitte unten beschreiben den 0.1.18/0.1.19-Vorläufer.

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

**Stand 07.11.2026 · Affiliate-Zentrale HD009 0.1.20-dev.**

## Einziger aktueller Download

- `../PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip`
- **1.066.589 Bytes · SHA-256 `cd6cb75f3ef0f393f94f3f93b974f3663ffa1f449c579886ae9520bc3d920cbb`**.
- WordPress-Originalordner `affiliate-portal-router/` bleibt erhalten. **Keine parallele Plugininstallation.**
- Details und Nachweise im `../PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/MANIFEST.md`.

## Hobbyregister – verbindliche neue Anzeigenplätze (0.1.19)

Die HD007-Hobbyregister-Inhalte und das HD003-Design bleiben unverändert. Nur das **vorhandene HD009-Affiliate-Plugin** steuert die Position der beiden Banner auf den Register-Einzelprofilen:

- **Desktop:** `Auf einen Blick` → quadratischer Amazon-Partnerbanner → `Hobbygruppe` → übrige Seitenleistenblöcke.
- **Zusätzlich im Haupttext:** ein responsiver Querbanner **unmittelbar nach `Kosten und Ausrüstung`**.
- **Mobil:** zuerst der Hauptartikel (mit einer Inlineanzeige nach `Kosten und Ausrüstung`), **anschließend** die quadratische Seitenleistenanzeige **als erster Block vor der Hobbygruppe**. Nicht direkt ganz oben.
- **In 0.1.20 optisch verfeinert:** wärmerer Verlauf, 2px-Rundungen, kleinerer Amazon-Button, Foto dezent zurückgenommen.
- Derselbe native Pferdeatelier-/Hobby-Partner-, Kategorie- und Werbemittelweg bleibt zuständig. Keine zusätzliche Quelle, neuer Import oder neues Plugin.

**Nachweis:** Original-Plugins HD003+HD007+HD009 in realem WordPress mit MariaDB und Browser getestet. Öffentliche Test-Registerseite HTTP 200, Desktop- und Mobil-Anzeigenordnung sowie vollständige Gestaltung, eine Sidebar- und eine Inline-Anzeige pro Profil **PASS**. Einzelwerte und Testbericht in der HD009-`EVIDENCE`.

**Grenze:** Die 0.1.19-Positionen hat der Betreiber live bestätigt; die neue 0.1.20-Gestaltung ist noch nicht live geprüft.

## Verbindlicher Amazon-Eigenbanner nach Auswahl Variante 4

- **Eigenes Hobby-Depot-Logo im Werbebanner entfernt.** Kein zusätzliches „Entdecke deine Ausrüstung“.
- Oben nur der Hobby-Titel, z. B. „Airbrush-Modellbau“, auf **schmalem warmem Verlauf**.
- Darunter ein **großes, nachweislich passendes Hobbyfoto** aus dem bestehenden HD003/HD007-Bestand, keine Collagen.
- **Im Foto:** gelb-oranger Button mit Pfeil und dem *originalen, unveränderten, von Amazon für Werbung zugelassenen deutschen* Logo **„Erhältlich bei Amazon“**. Das gewöhnliche Amazon-Logo ist ohne Sondergenehmigung **nicht** zulässig. Bei extrem schmalen Werbeplätzen wird auf einen Textlink umgestellt.
- **Quadrat 1:1**: vorhandene Hobbyregister- und Glossar-Einzelbanner, Desktop und Mobil.
- **Querformat**: vorhandene Kategorien-/Hubbanner, volle verfügbare Breite und flexible Mindesthöhe. Original-HD003-Problem (76px feste Höhe einschließlich der Bilder) für **diesen einen eigenen Banner-Typ** gezielt aufgehoben.
- **Nur einmal „Anzeige“**: vorhandene Kategorien-Kennzeichnung „Anzeige · Partner“ bleibt, das zweite Label des Eigenbanners dort unsichtbar.
- Richtige Ziel-URL: hinterlegte Amazon-Tracking-ID, aus dem echten Hobbyteil abgeleiteter Suchlink. WordPress-HTML-Entities in Titeln werden vor Generierung korrigiert. **Keine Produkt-/Preisbehauptungen ohne echte Daten.**

## Vorhandene Technik bleibt zuständig

Pferdeatelier-basierte Kampagnenauswahl, Relevanz, Kategorien/Elternpfad, Bildformat, Freigaben/Veto und bestehende HD004-/HD007-Kontakte bleiben unverändert. Amazon/idealo/DataForSEO-Funktion nicht neu entwickelt; weder neuer Bannerverteiler noch Tabelle oder zusätzliches Plugin. Mietwerbung `Hier könnte Ihre Werbung stehen` gehört allein zum unveränderten HD003-Design.

## Nachweis und noch offener Livepunkt

- 24/24 PHP geprüft, ZIP CRC PASS; PHP-Amazon/Partner-Regressionschecks PASS.
- Vier echte Chromium-Browserfälle bestanden – **700px Quadrat, 186px Register-Quadrat, 770px Querformat, 355px schmales Querformat**. Alter fester 76px-Streifen in der Simulation beseitigt; Amazon-Logo dort mindestens 140px, ohne Verzerrung.
- Screenshots plus Prüfnachweis in der einzigen HD009-Plugin-Akte.
- **Produktivinstallation 0.1.18 noch nicht durchgeführt/bestätigt.** Kein behauptetes Live-PASS.

## Einmaliger WordPress-Test nach Installation

1. `https://hobby-depot.de/gestalten/malen-zeichnen/` – Querbanner unter „Weiter in Malen & Zeichnen“.
2. `https://hobby-depot.de/hobbyregister/airbrush-modellbau/` – Quadratbanner in der Register-Seitenleiste.
3. Es muss in beiden Fällen genau ein deutlich sichtbarer Banner mit Titelstreifen, großem Hobbyfoto und orangefarbenem Amazon-Button erscheinen. Keine doppelte Anzeigenkennung auf der Querseite.
