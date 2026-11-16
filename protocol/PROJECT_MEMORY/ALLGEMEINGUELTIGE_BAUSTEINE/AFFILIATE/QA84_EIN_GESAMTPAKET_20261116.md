# QA84 – ein konsolidiertes KISS-eBay-Pluginpaket, 16.11.2026

## Status

**Lokaler Gesamtstand gebaut und am gepackten Original getestet. Noch keine Live-Abnahme oder Freigabe für produktive Installation.**

Quelle: vollständiges Originalpaket `Affiliate_6.72.351_EBAY_KISS_GESAMTWORKFLOW_TESTINSTALLATION.zip` aus der Projektbibliothek `/pferdeatelier/PLUGINS/QA/QA76_ECHTDATEN_GESAMTWORKFLOW/`.

Einziger neuer vollständiger Paketkandidat: `QA84_AFFILIATE_ZENTRALE_6.72.352_STAGING_INSTALLATION.zip` (Projektbibliothek `/pferdeatelier/PLUGINS/QA/QA84_KISS_GESAMTKETTE/`).

SHA256: `acf8aedb1c21c75742107f07eb8b9e8c2964a5faebabc52e72d331c05cea9ce3`.

Gegenüber 6.72.351 sind **genau 4** Dateien unterschiedlich: zwei vorhandene eBay-PHP-Traits, Versionskopf in der Plugin-Hauptdatei, Readme. 62 weitere ZIP-Einträge bytegleich. Keine Änderung anderer Partner, K0, WordPress-Core, eBay-Produkttabellen, Website-Design, GitHub-Workflow oder öffentlicher SAFE-Bestände.

## Erledigte bestehende Ursachen in einer einzigen Quellkopie

- Die bestehende Recherche-Fälligkeit auf 7 Tage; ein aufgeschobener Suchversuch führt nicht zum sofortigen Neubeginn.
- Der stündliche Aktualitätslauf endet nach Frischeprüfung und startet keine neue Fachauswahl und keine neue Veröffentlichung.
- Untergeordneter Discovery-Abschluss überschreibt nicht mehr den nachgewiesenen öffentlichen Familienabschluss.
- Der bestehende Abschluss speichert aus dem **bereits verifizierten** SAFE-Manifest den 283er-Familiennachweis und trennt den bestätigten öffentlichen Schlussstand von einem beendeten Suchversuch. Keine neue Produktauswahl.
- Der schon vorhandene GitHub-Heartbeat steuert dieselben beiden **bestehenden** Arbeitsanteile; der zusätzliche WP-Cron für den eBay-Verfügbarkeitslauf wird im Kandidat entfernt, die Frischearbeit paketweise mit gespeichertem Cursor und 22-Sekunden-Budget begrenzt. Kein konkurrierender Zeitgeber.
- Die bestehende Backend-Anzeige stellt den letzten nachweislich abgeschlossenen öffentlichen Familienstand getrennt vom laufenden Zwischenstand dar.

Das ist die konsolidierte Korrektur auf Basis der bekannten QA69–QA82-Ursachen, **kein zweites Regelwerk**. Die Original-Delta-Datei `QA84_QA76_ZU_6.72.352_GESAMTPATCH.patch` liegt beim Plugin in derselben Projektbibliothek.

## Paketprüfung direkt aus dem frisch entpackten ZIP

- 66/66 Archivdateien lesbar, 23/23 PHP-Syntaxprüfungen bestanden.
- 9 originale Controller-Modellszenarien: 5 kontrolliert `completed`, 4 kontrolliert `failed`, ohne unerlaubten Erfolg bei Speicherfehlern; alle mit derselben zuvor definierten Pflichtfamilienzahl von 283, soweit ein abgeschlossener Public-Manifest-Testfall vorliegt.
- 9/9 Termin-/Fristfälle, 16/16 REST-Laufstatusfälle.
- 95/95 **originale historische Artikelkennungen** am vorhandenen PHP-Test, jeweils Anbieter- und WordPress-Antworten nachgestellt. Kein echter heutiger eBay-Artikel-Verfügbarkeitsbeweis.
- Der gemeinsame GitHub-Takt verarbeitet in der lokalen Probe abwechselnd Frischepaket und kanonisches Suchpaket, ohne einen zweiten autonomen Worker.
- Prüfbericht `QA84_GESAMTPRUEFUNG.json` in derselben Projektbibliothek; Gesamtergebnis `PASS_LOCAL_STAGING_CANDIDATE`, keine Fehlfälle.

## Exakter nächster Betriebsschritt

**Ein einziger kontrollierter Staging-Lauf mit dieser einen ZIP und den real gespeicherten WordPress/eBay-Daten; nicht weitere Simulationen oder Neu-Suchläufe auf Verdacht.** Vorher eine tatsächliche Sicherung des vorhandenen WordPress-Standes. Dabei muss die publizierte 283er-Familienliste aus dem **bereits vorhandenen** Freigabeort entstehen; kein zweiter Produktprüfer.

Der vorhandene GitHub-Wecker-PR [#759](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/759) bleibt weiterhin `open / blocked / unmerged`; seine Workflowdatei kann nur über den regulär erlaubten Freigabeweg übernommen werden. Kein Hardlock-Bypass. Eine erfolgreiche lokale Simulation ist keine Freigabe zur Produktivinstallation.

**Wichtig:** Dieser Stand ist der erste gebündelte Testkandidat und darf nicht mit einer bewiesenen Live-Abdeckung verwechselt werden.
