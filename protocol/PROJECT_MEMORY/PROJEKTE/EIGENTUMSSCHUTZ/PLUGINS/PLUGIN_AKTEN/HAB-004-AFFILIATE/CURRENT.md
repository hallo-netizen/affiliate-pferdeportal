# HAB-004 – Hab & Bewahr Affiliate-Zentrale

## Aktuelle Version 0.1.0-rc3 – 06.11.2026

**Status:** Vollständiger isolierter **Installationskandidat**, nicht auf WordPress live freigegeben.
**Offizieller Voll-ZIP-Pfad:** `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`.
**ZIP:** 605.196 Bytes, 27 Dateien, WordPress-Pluginordner `affiliate-portal-router/`.
**SHA-256:** `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`.
**Git-Blob:** `b6b19e7a739b70a813c5e9de2e290d98c898156f`.
**Nachweis:** GitHub-Workflow `42252394077` PASS; unabhängiger vollständiger GitHub-Readback, identischer SHA. Im offiziellen Design-ZIP 0.1.189 waren 546 Knoten; der neue Hab-Adapter ermittelt daraus sechs Schutzwelten, 285 zugeordnete Artikelkategorien und 13 konkretere Produktkategorien. **Dies ist der im Design hinterlegte Kategorienstand, keine Aussage zum Live-WordPress-Inhalt.**

### Was geprüft und verändert ist
- 26 Originaldateien aus dem neutralen Affiliate-Stamm **unverkürzt erhalten** und 1 eigener Hab-Adapter: keine bestehende PHP-Funktion entfernt.
- Gegen vorige RC2-ZIP **24 von 27 Dateien bytegleich**, Änderungen nur an Plugin-Hauptdatei, eigenem Hab-Adapter und Readme. Unveränderte Engine der Provider, eBay, idealo, Awin, ADCELL, Digistore24, Produktplanung, Kampagnen, Werbemittel, Chefentscheidungen, Nachverarbeitung bleibt erhalten.
- Fünf vorher nur beiliegende Zusatzmodule für Produktquellen, Admin-KISS, Deal-Radar, Partnerstatistik und Digistore24-Weitergabe beim tatsächlichen WordPress-Hook-Start aktiviert. **92** registrierte Hook-Typen im isolierten CLI-Test.
- Fehler aus RC2 behoben: harte Positivliste suchte Produkte nur in Seitenüberschriften und traf den Designbestand nicht. RC3 bindet tatsächliche Kategorie-Namen an echte gemappte, veröffentlichte WordPress-Parent-Seiten (nicht an erfundene Produktseiten); enge Fachproduktprüfung, Verwechslungs-/Zubehörsperre, sechs echte Schutzwelten, alle 285 belegten Kategorien.
- Bestehende Hab-&-Bewahr-Design-Filter für Artikel, Bereichsseiten, Schutzwelten und Magazin-/Anzeigenmarkt-Werbeplätze angebunden; kein automatisches doppeltes Artikeldesign-Rendering.
- Seitenklassifizierung verwendet einmaligen, pro Request zwischengespeicherten Index statt mehrfach vollständigen Kategorien-Scan. Alle 27 PHP-Quellen lint-geprüft, Frontend-JS syntaktisch geprüft, ZIP CRC PASS.
- Voll-ZIP wurde zweimal unabhängig gebaut: beide bytegleich, erneuter kompletter GitHub-Download bytegleich.
- Fremde Pferdeatelier-/Hobbydepot-Designbindungen und Portaldaten werden nicht aktiviert; vorhandene allgemeine Affiliate-Engine bleibt in den Originalfunktionen erhalten.

### Grenzen / keine erfundenen Freigaben
- **Keine Live-Abnahme im echten WordPress** und keine realen API-/Provider-Konto-Tests. Automatische Affiliate-Auslieferung standardmäßig aus.
- Die vollständige Pferdeatelier-Referenz **6.72.306** (66 Dateien) liegt im Hab-Affiliate-Büro nicht als installierbares Gesamtarchiv; Gleichheit aller jüngsten Pferdeatelier-Funktionen ist **nicht belegt**. Nachweis betrifft die 26-Dateien-Quelle.
- Keine Messung der Website-Gesamtperformance im Hosting. Gemessen/qualifiziert ist lediglich die schnellere Lookup-Logik und das Vermeiden unnötiger wiederholter Options-/Baumzugriffe im selben Request.
- Historische fachliche Vergleichsbeispiele können als harmlose Kommentare der unverändert gehaltenen neutralen eBay-Engine vorkommen. Das ist kein aktiver Pferdeatelier-Zielkatalog; die reale fachliche Produktzuordnung nutzt allein den Hab-Kategorie-Workflow. Keine blinde Löschung notwendiger Recovery-/Sicherheitslogik.
- Glossar-Einzelbanner: Die Design-Glossarfunktion hat keine allgemein gültige echte WordPress-CPT-Zielkennung. Daher wird keine erfundene Zielzuordnung behauptet. Andere echte Bannerplätze sind angebunden.

**Nächster Schritt:** RC3 auf gesichertem Hab-&-Bewahr-WordPress installieren, **nicht** auf Pferdeatelier. Zuerst Backend-Seiten, Kategorie-Readback, echten Artikel und echte Werbeplätze prüfen. Erst nach eindeutiger Liveprüfung Provider für Hab & Bewahr separat anbinden und Automatik aktivieren.
