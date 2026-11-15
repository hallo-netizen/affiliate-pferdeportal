# QA78 – Pferdeatelier eBay: geprüfter Verfügbarkeitsweg (15.11.2026)

**Nur lokale Originaldatenprüfung – nicht live installiert, keine weitere Pluginversion.**

## Beleg der bereits vorhandenen einen Fachentscheidung

- Die bestehende PHP-Routine `ebay_refresh_process_row` verlässt bei BUSINESS-Quellen den Pfad **sofort** nach `ebay_public_availability_refresh_one`. Die spätere Geschäftsartikel-Neuklassifizierung ist auf diesem Weg **nicht erreichbar**. Eine vorherige Annahme, hier werde wirklich doppelt klassifiziert, war falsch. **Keine Codeänderung vorgenommen.**
- `ebay_public_availability_refresh_one` ändert bei identischer Ware nur ihre Verfügbarkeits-/Frischeangaben sowie Preis und Währung. Familie, Auswahl, Rang und öffentlicher Freigabebestand bleiben unverändert. Geänderte Identität: `needs_review`, keine heimliche Neuzuordnung.
- Direkter Original-PHP-Test: **17/17** Fälle bestanden, davon **95 unterschiedliche echte alte eBay-Artikel-IDs** mit ausdrücklich **nachgestellter** gleichbleibender Anbieterantwort und nur einem gespeicherten Frischeergebnis. Das ist kein Echtverfügbarkeitsnachweis.
- Vollständige QA77-Regression über echte Original-Lauf-CSV (2.811, 3.832 und 87 Einträge derselben bzw. neuer UUID, ursprüngliche 278 Fehlfamilien und 283er Katalog), echte PHP-Methoden mit WP/eBay-Modell-I/O: **26.967/26.967 Assertions**, 0 Fehler; großteils Audit-Konsistenz, keine echten 26.967 Produktprüfungen. Unveränderter QA77-Testkandidat.

## Echter noch offener Zielvertrags-Konflikt: zwei Zeitgeber für Quellenfrische

- Im unveränderten PHP wird über `ensure_ebay_refresh_schedule` **alle zwei Stunden ein WP-Cron-Termin** auf `EBAY_REFRESH_CRON_HOOK` registriert. Er ruft `ebay_public_availability_tick` auf.
- Zusätzlich läuft der vorhandene GitHub-Zeitgeber; in QA77 fragt sein kanonischer Fälligkeitstest stündlich `refresh` ab. Auch dieser Quellenabgleich führt über `ebay_refresh_process_row` auf dieselbe reine Verfügbarkeitsroutine.
- **Wichtig differenzieren:** Zwei zeitliche Auslöser sind belegt, jedoch **keine zweite fachliche Entscheidung** und auch kein aus Originaldateien bewiesener doppelter eBay-GetItem-Aufruf. Der lokale Sicherheitsmechanismus prüft/übernimmt nur die passende gespeicherte Version.
- Das WP-Cron-Kontrollfenster kann bestehende öffentliche Produkte auch während eines langen GitHub-Vollsuchlaufs frisch halten. Einfaches Abschalten ohne Ersatz im selben einen Arbeitstakt wäre sachlich gefährlich. Deshalb **noch nichts deaktiviert oder verändert**.
- Der eine endgültige Taktgeber benötigt im bestehenden kanonischen Arbeitsablauf einen nachweislich sicheren, klein begrenzten Verfügbarkeitsanteil auch während längerer Vollsuchen. **Noch nicht umgesetzt / nicht echt bewiesen.** Kein zusätzlicher autonomer Worker, kein weiterer Zeitgeber, keine neue Auswahlroutine.

**QA69 realer Live-Abschluss: NICHT BESTANDEN.** Keine live bestätigte installierte Version, kein endgültiges echtes 283er-Regalbuch samt SAFE-Checkpoint/öffentlichen Produktanzeigen. Die 634 Kampagnen aus Nutzer-Screenshot sind Bestandszahl, kein Beleg für 634 gültige Produktfamilien.

QA77-Originalbericht: `protocol/PROJECT_MEMORY/ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/QA77_KISS_ZWEI_LAEUFE/QA77_BERICHT.md`.
