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


## Korrigiertes Gesamturteil nach ECHTER Sichtbarkeitsdiagnose – 16.11.2026

**QA84 darf NICHT als fertige Lösung der Zeitsteuerung gelten.** Die vom Nutzer hochgeladene `pferdeatelier-ebay-sichtbarkeit-20261116-102018.json` belegt einen weiterhin laufenden Verfügbarkeitszustand und massiven Frischeausfall:

- Snapshot 10:20:18 UTC: 309 freigegebene Kampagnen, davon 293 `source_freshness_expired`, acht `source_not_available`, acht Grundprüfungen bestanden (aber nicht als sichtbar bewiesen).
- Verfügbarkeitszustand `running=1`; 448 geprüft, 24 Fehler; letztes Arbeitspaket 09:22:53 UTC, nächstes fällig 09:24:23 UTC. Zum Snapshot war dieser Termin **55,9 Minuten überfällig**.
- 9.792 gespeicherte Quellen, nur 16 frisch, 9.776 abgelaufen. Davon darf **nicht** abgeleitet werden, alle 9.792 seien aktuell veröffentlichte Kampagnen.
- GitHub-Main-Workflow letztmalig Run 43834993089: `status=completed` um 08:55:13 UTC, `no successor runner required`; bis zum Vergleich mit dem Diagnosezeitpunkt kein neuer Lauf in der Actions-Liste.

### Rückfall in bereits dokumentierte Zeitgeberfehler – direkt im gepackten QA84-PHP nachgewiesen

**Originalmethoden:** `affiliate-portal-router/includes/trait-ppar-ebay-run.php::handle_ebay_external_tick`, `includes/trait-ppar-ebay.php::ensure_ebay_refresh_schedule`; echte gebaute QA84-6.72.352-ZIP SHA256 `acf8aedb1c21c75742107f07eb8b9e8c2964a5faebabc52e72d331c05cea9ce3`. Alle folgenden Abweichungen sind über direkte Quellreihenfolge eindeutig:

1. `operator_paused` und `failed` werden im Heartbeat **vor dem Availability-Aufruf** als `idle`/ `failed` zurückgegeben. Deshalb unterbleibt bei diesen Recherche-Statuswerten die unabhängige Verfügbarkeitsarbeit. Dies ist **derselbe bereits am 11.11. in QA16 korrigierte** Vertragspunkt.
2. Wenn ein kanonischer Recherchelauf `completed` ist, kann derselbe Heartbeat zwar ein fälliges Availability-Paket ausführen, aber bei nicht fälliger neuer Recherche/Refresh-Operation danach **`idle/no_due_operation`** zurückmelden, **auch wenn Availability `running=1` mit einem gespeicherten nächsten Termin bleibt**. Der bestehende GitHub-Main-Workflow beendet bei `idle|completed|failed|disabled` seine Selbstkette. Dieser Status-/Zeitgeberfehler ist die wiederkehrende, bereits in **QA24** mit echten Logs bewiesene Fehlerklasse.
3. QA84 `ensure_ebay_refresh_schedule` entfernt zugleich den alten WordPress-Verfügbarkeits-Cron. Wenn die GitHub-Kette endet und geplante Auslösungen ausbleiben, **fehlt ein verlässlich wirkender weiterer Auslöser für die noch offene Aktualisierung**. Damit wurde der getrennte Availability-Ansatz aus **QA9, QA16/17** nicht vollständig in den einen kanonischen Zeitgeber nach **QA69** übernommen.

**QA84-Regressionstests verfehlten diese Fälle:** Die vorhandenen 16 REST-Fälle prüften `paused_by_operator`, `old_failed_not_restarted`, `completed_not_yet_due`, aber **nicht** die kombinierte Zustandsfolge `Recherche completed/paused/failed + Availability running/überfällig + GitHub-Terminalantwort`. Ihre grünen Testzahlen beweisen deshalb nicht den Zeitvertrag.

### Bereits beschlossene Lösung, keine neue Engine

- **QA69 bleibt verbindlich:** genau **ein** vorhandener externer Zeitgeber, zwei voneinander unabhängige Arbeitssichten im selben vorhandenen PHP-Controller: Recherche/Fachauswahl und bestehende reine getItem-Verfügbarkeitskontrolle; getrennte gespeicherte Cursor; keine zweite fachliche Entscheidung und kein zweiter eBay-Suchlauf.
- Der Verfügbarkeitsanteil muss bei `completed`, `operator_paused` und `failed` der Recherche zugelassen bleiben, ohne deren Status zu überschreiben.
- Während Availability `running` und ein nächstes Paket fällig/ausstehend ist, darf die Heartbeat-Antwort **nicht als terminaler Recherche-Leerlauf die Versorgungskette beenden**. Der bestehende Verfügbarkeitscursor muss fortgesetzt werden; keine neue Recherche und kein Datenreset.
- Die bereits vorbereitete, regelmäßige **eine GitHub-Uhr** [PR #759](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/759) wäre die geplante Transportkorrektur: 5-Minuten-Schedule, keine Selbstverkettung. PR weiterhin `open`, `blocked`, `unmerged`, deshalb noch **keine produktive Übernahme**. Hardlock nicht umgehen.
- Bei einem realen Durchgang die gemessene Zahl tatsächlich öffentlicher, frischepflichtiger Quellen (nicht pauschal alle 9.792 Altquellen) und GetItem-Bearbeitungsrate mit der sechs-Stunden-Frist vergleichen. **Erst danach** ist die Dauerhaftigkeit der Reparatur bestätigt.

**Exakter offener Abschluss:** *Eine* gebündelte Korrektur der bereits bestehenden Heartbeat-/Availability-Statusführung **plus** reguläre Freigabe der bereits vorbereiteten GitHub-Uhr, danach *eine* reale Ablaufkontrolle derselben 309 bestehenden Kampagnen und ihrer öffentlichen Anzeige. **Keine Vollsuche, kein weiterer separater Fach-Worker, keine erfundenen freigegebenen Produkte, keine Einzel-Screenshot-Orgie.** Bis dahin QA69-Live-Zielvertrag **NICHT BESTANDEN**.
