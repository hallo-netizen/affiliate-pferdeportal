# Hab & Bewahr: 0.4.31.18 – Context-Grenze / sicherer Original-Wiederanlauf, 21.11.2026

**Status:** Lokal bestandene technische Kette mit isolierten synthetischen 2128 Kategorien und 163 Kandidaten. **Keine bestandene Live-Abnahme**, keine neuen kostenpflichtigen DataForSEO-Anfragen. **K0 vollständig unberührt.**

## Echter Ausgangsfehler 0.4.31.17
Screenshot und Diagnose `texterstellung-diagnose-20261121-135843.json`: `PSTE_CONTEXT_BLOCKED_PSTE_CONTEXT_STAGE_ARTICLE_TYPE_REGISTRY_SIZE_LIMIT_EXCEEDED`. Gespeicherte Abholbox-Recherche 192 RAW, 163 Kandidaten, 0 usable, kein tatsächlich neuer Gratis-Recheck. Fachlicher Filter aus v0.4.31.16 wurde noch nicht neu ausgeführt.

## Ursachenbeweis
Der originale Context-Registry-Builder vervielfacht Hab-Kategorieknoten pro Artikelart; Simulation 2128 realistisch lange (synthetische) Namen → **19.655.319 Byte**. Bestehende Höchstgröße **8 MiB** führt in Original 0.4.31.17 nach **21 echten PHP-Schritten** exakt zum Screenshot-Stopp. Grenze auf **32 MiB** gesetzt; derselbe alte signierte Auftrag bleibt nach strengem Vorzustands- und Quellhash-Abgleich fortsetzbar. Keine neue Architektur, Entscheidung oder Datenbank.

## Original-PHP-Simulation am finalen ZIP
- Alt: `BLOCKED`, identischer Originalfehler, 21 Schritte, UUID `00000000-0000-4000-8000-000000000001`.
- Neu: exakt diese gespeicherte UUID, 41 echte Fortsetzungsschritte, `COMPLETE`, 163/163 **synthetische** Datensätze, 2128/2128 Registry-Familien aus WP-Mock wieder eingelesen, identische Checksummen; 0 Provideraufrufe.
- Originale `PSTE_Breadth_Research_Queue::startExistingOnly` plus originale Worker-Fortsetzung nach gültigem Kontext: `0→40→80→120→160→163→COMPLETE`, originale Queue aus Mock-Speicher zurückgelesen, keine Anbieterabfrage. **Fachliche Kandidatenurteile im Worker simuliert, nicht die 163 echten WordPress-Urteile.**
- 10 negative Fälle (unter anderem falsche Phase, geänderte Quelle, falsche UUID, fehlende Freigabe) bleiben blockiert; übergroßer synthetischer Registry-Test mit 4000 Kategorien stoppt weiterhin (37 MB).
- Final ZIP SHA256 `cbbab0e1c1e635ce4759a3ba64b9732e68659168fc622f36ad316329a0eace35`; 87/87 CRC, 78/78 PHP Syntax, gültige JSON, **83/87 Dateien byteidentisch** zu 0.4.31.17. Geändert nur Hauptdatei, zwei Original-Kontextklassen, README. Original-Recherche, Keyword-Entscheidungen, MINI, K0 nicht geändert.

## Gesicherte Abnahmegrenze
Das historische Hab-Kategorieinventar vom 14.11.2026 hat 2198 Kategorieobjekte; kein echter vollständiger aktuell live Kategorie-Registry-Abzug. Synthetische Inputdaten bilden die Dimension, nicht den Inhalt der WordPress-Datenbank ab. Kein nachgewiesener positiver Keywordbestand oder echte MINI-Übergabe. Kein „Gesamtworklow in Produktion erledigt“ behaupten.

## Büro-Archiv / Weiterarbeit
`/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/Texterstellung_HAB_UND_BEWAHR_0.4.31.18_KONTEXT_2128_ORIGINAL_ABNAHME.zip`
und `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ORIGINAL_KONTEXT_043118_20261121/` enthält Bericht, QA-JSON, Wiederholtests, Quellvergleich.

Nach Backup bestehendes Plugin **ersetzen, nicht deinstallieren**. Einmal `Texterstellung → Recherche → Gespeicherte Keywords kostenlos erneut prüfen`. Diagnose-JSON nach Abschluss. **Keinen kostenpflichtigen DataForSEO-Lauf starten und K0 nicht ausführen**. Bei neuer Sperre Diagnose, keine spekulative Freigabe.