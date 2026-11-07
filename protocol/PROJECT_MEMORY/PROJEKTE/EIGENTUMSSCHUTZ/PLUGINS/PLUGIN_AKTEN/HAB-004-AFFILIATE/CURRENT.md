## 07.11.2026 – aktueller technischer HAB-004-Stand RC4

HAB-004 0.1.1-rc4: vollständige CURRENT.zip, 616072 Bytes, 28 Einträge, SHA256 c601c1f540fccdd18dde59b7c15fc55cfe53b68a59459d45182a2cf1bcd55017, Git-Blob f3a77efff2cb16de34c91eb0c4ec3b072a3999db (remote Größe und Blob bytegleich geprüft).

Original: Hab-RC3, 27 Dateien. Von deren Dateien 25 byteidentisch, geändert Haupt-PHP und includes/trait-ppar-idealo.php, hinzugefügt includes/trait-ppar-hb-amazon.php. Existing Banner-, Frontend-, Produktkarten-, Ausgabe- und Artikelplandateien unberührt. DataForSEO: Opt-in, stündliche WP-Cron-Verarbeitung, max. 5 kostenpflichtige POSTs/UTC-Tag, gespeicherte offene task-ID, eindeutiger Variantenabgleich. Amazon: eigene Tracking-ID habundbewahr-21 ausschließlich nach Speicherung/Aktivierung; direkte Links nur für belegte einzelne ASIN aus idealo oder streng geprüfte DataForSEO-Treffer. Kein eigener manueller Amazon-Kampagnenweg. Alte fremde idealo-Defaults (Adspace 568313, Feed 2901) aus Hab entfernt/gesperrt. Keine Fremd-Provider-Zugangsdaten übertragen.

Lokal geprüft: PHP Syntax 25/25, 24 Assertions (Positiv/Negativ, Variantenabweichung, falsche Portal-ID, bezahlter POST vs kostenloser GET, Tagesgrenze, keine doppelten Buttons), ZIP CRC, installierbare Original-Pluginwurzel, 25/27 originale Dateien bytegleich. Keine authentifizierte WordPress-Installation oder echte Provider-Verbindung und keine Google-/Frontend-Liveprüfung; nur ein Upgrade-Testkandidat. Die Standardautomatik bleibt deaktiviert.

Nächster Schritt: nur das bestehende Hab-004-WordPress-Plugin mit CURRENT.zip aktualisieren; Affiliate-Zentrale → Amazon-Automatik öffnen; habundbewahr-21 speichern, Amazon-Produktbuttons einschalten; eigene DataForSEO-Zugangsdaten erst nach Kostenfreigabe eingeben; an einer echten passenden Produktkarte Ziel/Tracking und Slot prüfen. Pferdeatelier und Hobbydepot/K0 unverändert.

---

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
