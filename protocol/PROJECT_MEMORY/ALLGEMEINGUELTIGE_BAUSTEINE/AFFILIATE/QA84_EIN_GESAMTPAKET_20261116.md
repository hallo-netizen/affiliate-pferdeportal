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

## Ergänzung – öffentliche Sichtbarkeit (Screenshot vom 16.11.2026, 10:56 MEZ)

**Keine Live-Abnahme.** Das vom Benutzer gezeigte WordPress-eBay-Dashboard des Pferdeatelier meldet einen technisch abgeschlossenen Lauf und gleichzeitig `309` im SAFE-Checkpoint gespeicherte BUSINESS-Kampagnenkennungen, `139/283` im gespeicherten Lauf zugerechnete Produktfamilien, `144` offene Familien, `24` Verfügbarkeitsprüfprobleme und **keinen** gespeicherten letzten verifizierten öffentlichen Familienabschluss. Der Hinweis zu einem fehlgeschlagenen Audit-Schreibvorgang besteht ebenfalls. Das Dashboard erklärt selbst: gespeicherte Freigabe ist **kein** Nachweis gerade sichtbarer Kacheln.

Ein direkter öffentlicher Aufruf der Schabracken-Seite am selben Tag zeigt die Produktbereichsüberschriften ohne auslesbare Produktlinks/Kacheln: https://pferde-atelier.de/ausruestung/ausruestung-sattel/schabracken/ . Der exakte Grund des Versagens **auf diesem Live-System** ist durch die Zähler allein nicht bestimmt.

**Originalcode der gebauten 6.72.352 geprüft:** `ebay_business_campaign_source_allows_delivery_base` verweigert ein gespeichertes eBay-Produkt u.a. bei `fresh_until <= time()`, inaktivem oder beendeten Quellstatus, Policy-Veto, fehlendem zulässigen Quell-Identitätsbezug bzw. nicht bereiter Route. `ebay_business_campaign_source_allows_delivery` fordert zusätzlich die SAFE-Checkpoint-Mitgliedschaft. Eine Kampagne kann daher im gespeicherten 309er-Checkpoint stehen und **dennoch nicht im Frontend angezeigt werden**. Dies ist ein sicherer Programm-Befund, kein Beweis, welches dieser Tore am 16.11. auf die konkreten Live-Produkte zutrifft.

**Wichtige Fehlbedienungsprävention:** Das bestehende `Gespeicherte Angebote neu prüfen` startet `operation=local`; im Originalcode verhindert dieser Modus ausdrücklich die öffentliche Commit-Phase (nur Diagnose/Abdeckung). Er ist **keine Veröffentlichungskorrektur**. Ebenso ist eine erneute eBay-Vollsuche kein zielgerichteter Ausgabefix.

**Bereits vorhandene einmalige Eingrenzung ohne neue Plugins oder Vollsuche:** Die read-only WordPress-Seite `/wp-admin/admin.php?page=affiliate-portal-ebay-business` zeigt für bis zu 100 gespeicherte Produkte je Aufruf Quelle, Bild, Zielseite, Designslot, materialisiertes Ausgabeobjekt und gespeicherten Ablehnungsgrund. Sie ruft den letzten dynamischen Frontend-Quell- und SAFE-Gate-Test **nicht** erneut für alle Produkte auf; deshalb eine Meldung „Basis bereit“ nicht mit einem bewiesenen sichtbaren Produkt verwechseln. Ein fokussierter Abgleich der publizierten Ausgabeobjekte gegen die tatsächliche öffentliche Ausgabe ist der ausstehende letzte Nachweis.

**Die alte QA80-Ursache bleibt nachgewiesen, aber die Live-Wirkung der 6.72.352 nicht:** In früheren Original-Audits wurden 5 Quellen je etwa 2 Stunden bearbeitet bei sechs Stunden Publikations-Frischegrenze. Dieses alte Tempo ist für einen Bestand in der Größenordnung 309 unzureichend. Der konsolidierte Kandidat enthält eine neue gebündelte Kapazitätssteuerung, die auf dem echten Server noch nicht gegen aktuelle Quellen- und Laufzeiten belegt wurde. **Keine pauschale Aussage, dass alle 309 Quellen heute abgelaufen sind.**
