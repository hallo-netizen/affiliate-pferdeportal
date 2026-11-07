# HOBBY DEPOT – Affiliate – EINZIGE CURRENT-AUTORITÄT

**Stand: 07.11.2026** · Einziges fachliches Affiliate-Büro; technische ZIP und Prüfnachweise weiterhin ausschließlich in HD009 unter `PLUGINS`.

## Aktuelle Version

**HD009 Hobby Depot Affiliate-Zentrale 0.1.16-dev**

- `../PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip`
- 712.675 Bytes, SHA-256 `7f65fae7a3aac98bfb5f9bc7f7673fc726f64f0b3cbf5eb8b5a51c3e4ad40640`.
- PHP 24/24 PASS, ZIP CRC PASS. WordPress-Liveprüfung **noch nicht erledigt**.
- Bestehender WordPress-Pluginordner `affiliate-portal-router/`, keine Zweitinstallation.

## Warum die Korrektur notwendig war

**Tatsächlicher Screenshot:** `https://hobby-depot.de/gestalten/malen-zeichnen/` zeigt das abgeschnittene „Hier könnte Ihre Werbung stehen“ auf dem normalen **Partnerbannerplatz**, zusätzlich drei für eingeloggte Administratoren sichtbare leere Produktpositionen.

**Ursache im Quellcode nachgewiesen:** 0.1.15 hatte die freigegebene Werbeflächen-Mietgrafik (2170×725, Verhältnis etwa 3:1) außerhalb der vorhandenen Bannerautomatik als Ersatz für jeden freien schmalen Querbannerplatz eingesetzt. Die bereits vom Pferdeatelier übernommene native Formatregel für solche Kategorieplätze (5:1 bis 12:1), Relevanz und Elternpfad-Zuordnung wurde dabei umgangen. Außerdem führte die Mietwerbung zu den internen Seiten Werbebedingungen/Preise, nicht zu einem passenden Amazon-/idealo-Angebot. **Falsche Werbeart am falschen Platz**, nicht primär ein Bilddateifehler.

**Minimalfix 0.1.16:** Nur diese in 0.1.15 hinzugefügte Ausnahme wieder entfernt. Die Pferdeatelier-/Hobby-Automatik bleibt **unverändert aktiv**, kein neuer Import, neues Plugin, neue Tabelle oder neues eigenes Verteilungsverfahren. Die freigegebene Original-Mietwerbegrafik mit Hobby-Original-Logo verbleibt ausschließlich im vorhandenen HD003-Designplugin auf dafür vorgesehenen **freien Mietflächen**. HD009 spielt sie nicht mehr als Affiliate-Produkt-/Partnerbanner aus.

## Geprüfte vorhandene Funktionen – nicht noch einmal entwickeln

- Amazon + idealo als gewählte Startpartner (bei aktivierter Einstellung).
- DataForSEO-Amazon-Recherche und kostenloser Verbindungstest.
- idealo-iPN-Feedimport samt Automatik, sobald eine echte Hobbydepot-Freigabe/Feed besteht.
- HD004-Hobby-Kategorie/Elternpfad und HD007-Register-Zuordnung.
- Bestehende Kampagnen-/Banner-Auswahl inklusive belegter Bannerformatregel und Themenprüfung.
- Glossar-Einzelwerbeplätze `glossary_single_desktop_banner` / `glossary_single_mobile_banner` existieren bereits.

## Konkrete öffentliche Testorte

1. **Querformat:** `https://hobby-depot.de/gestalten/malen-zeichnen/` – direkt unter „Weiter in Malen & Zeichnen“ darf kein abgeschnittenes Mietbanner im Affiliate-Partnerplatz stehen. Passende echte Partnerbanner nur bei vorhandener Kampagne.
2. **Quadrat/hoch:** Nur in einem bereits veröffentlichten **Glossar-Einzelbeitrag** (`uge_term`) an den existierenden Desktop-/Mobil-Slots zu prüfen; noch kein passend freigegebenes Werbemittel im bekannten Bestand, daher ohne Banner kein Fehlerbeweis. **Für das Hobbyregister liegt ein Quadratbanner-Integrationspunkt noch nicht eindeutig nachgewiesen vor.**

## Offene Punkte

- Betreiber hat WordPress-Installation 0.1.16 und öffentliche Darstellung noch **nicht** bestätigt.
- Live-Ausgabe echter Amazon-/idealo-Werbung setzt real zugeordnete Angebote und zulässige Werbemittel voraus. idealo DE/Feed für Hobby Depot weiterhin offen. DataForSEO-Login ersetzt keine freigegebenen Partnerangebote.
- Der ehemalige 0.1.15-Versuch, eine mietbare Eigenwerbefläche als allgemeines Affiliate-Banner auszuspielen, ist **aufgehoben**.
- Keine Freigabe/Anmeldung für ein eigenes Quadratbanner mit Original-Logo nachgewiesen; nichts erfinden.
