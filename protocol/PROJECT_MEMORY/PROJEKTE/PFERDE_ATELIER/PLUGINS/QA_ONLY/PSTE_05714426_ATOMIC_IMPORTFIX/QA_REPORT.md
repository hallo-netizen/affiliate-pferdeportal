Pferdeatelier PSTE 0.57.144.26 – QA ONLY, 09.11.2026

Gemeldeter WordPress-Fehler der v25:
PSTE_MINI_ATOMIC_OPTION_CONFLICT_RELOAD_AND_RETRY

Nachweis anhand der unveraenderten v25:
- Der Code wirft diesen Fehler, wenn der SQL-UPDATE nicht genau eine Zeile aendert ODER wenn ein SQL-Fehler gemeldet wird.
- Der Code rekonstruiert den DB-Vergleichswert per maybe_serialize($before). $before stammt aber aus dem normalisierten WordPress-get_option-Zustand. Bei fehlenden alten Standardfeldern kann diese Neukodierung vom gespeicherten Original abweichen, obwohl sich die Fachdaten nicht veraendert haben.
- Ohne Original-Optionszeile und MySQL-Protokoll der Testseite ist nicht beweisbar, ob genau dieser Fall oder tatsaechliche Parallelmodifikation/SQL-Fehler die konkrete Fehlermeldung verursachte.

KISS-Fix v26:
- Nur die bestehende Importspeicherung wird korrigiert: exakten Originalwert aus derselben vorhandenen Optionszeile lesen und gegen den unveraenderten semantischen Vorzustand pruefen.
- Danach atomarer SQL-UPDATE mit binergenauem Vergleich zum gelesenen Originalwert; echte parallele Aenderungen werden weiter gestoppt.
- Lese-, Schreib-, Aenderungs- und Nachkontrollfehler sind getrennt; keine zusaetzliche Tabelle und kein weiterer SEO-Entscheider.
- Keine Aenderung an der SEO-Entscheidungsdatei, PSERC, K0, WordPress-Inhalten oder Live.

QA lokal:
- 83/83 PHP-Syntaxpruefungen bestanden.
- 121/121 ZIP-Pruefungen bestanden.
- Gegen Original-v25 ZIP genau 2 Quelltextdateien geaendert (inkl. Versionsheader).
- Original-v25-Testnachbau: 5/5 erwartete Faelle bestanden.
- v26-Testnachbau: 6/6 Faelle bestanden: normalisierte Legacy-Option; aktueller normaler Fall; veraenderter Vorzustand; Parallel-Aenderung; DB-Schreibfehler; DB-Lesefehler.
- Ergebnis-JSON SHA256 e50ae4eb934eddf7ec2d47feeaba5b6f30d0803756c1301d5ad545fec8dfb34c unveraendert.
- Vorherige 159 lokale SEO-Validierungen stammen aus v25; in v26 keine Aenderung an der Validierungslogik.

Grenze: Keine echte WordPress/MySQL-End-to-End-Wiederholung; keine Serverinstallation und kein echter Rueckimport erfolgt. Nur TESTseite freigeben, K0/Live unangetastet, PR #682 Draft.

Naechster Schritt: v26 ausschliesslich auf der isolierten WordPress-TESTseite anstelle der .25 installieren; denselben unveraenderten SEO-JSON-Import einmal ausfuehren; danach 61 FREI, 20 BELEGT, 6 KLAERUNG direkt in der WordPress-Statusanzeige bestaetigen. Bei Abweichung NICHT an Planung uebergeben.