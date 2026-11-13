# Pferdeatelier KISS – Pilot-Arbeitsprotokoll (laufend)

**Stand:** 13.11.2026. **Arbeit im getrennten Arbeitsverzeichnis**, nicht in vorhandenen WordPress-Plugins oder Live.

## Schritt 1 – Originale gesichert und Grenze bestätigt
- Originale als nur-lesbare Vorlage: PSTE QA 0.57.144.50, SHA256 `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`, 83 PHP-Dateien; PSERC QA 0.28.71, SHA256 `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`, 42 PHP-Dateien.
- Sie sind **QA-Originale**, nicht mit unbekanntem Live-Installationsstand gleichzusetzen.
- Nachgewiesen: PSTE verarbeitet SEO-Freigabe, Titel und Analytics; PSERC enthält K0-5-Felder-Grenze und Export/Import. Bestehender PSERC-Import ruft PPM679 Runtime Gate auf; nicht einfach entfernen.
- **Ziel:** separat installierbarer Pilot mit eigenem Ordner, eigenem Datenbereich, ohne Schreiben/Deaktivieren bisheriger Plugins. Sofortiges Umschalten der produktiven Worker ausdrücklich verboten.
- GitHub-Protokoll dokumentiert nur Arbeitsstand, keine offizielle neue Current-Autorität. Nach jedem relevanten Arbeitsschritt ergänzen.

**Status:** Quellenzuordnung und Pilotentwicklung laufen; keine Installation, keine WordPress-Live-Änderung, noch kein durchgängiger Echtlauf.
