# Hobby Depot – Abdeckungsprüfung 13.11.2026 (lesend, ohne Pluginänderung)

## Stand, bewiesen
- Aktuelle zentrale Hobby-Affiliate-Zentrale HD009 0.1.33 aus exakt geprüftem `CURRENT.zip` SHA256 `b6482b5d880e941c97ac726dffa85fbc46ba8514587e23700951d176ebcb63db`. Prüfworkflow: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43390790799
- **Hab-&-Bewahr-50er-Grenze ist bei Hobby Depot NICHT Ursache des idealo-Imports.** Im HD009 werden alle Konzept-IDs aus dem aktiven CORE-Kategoriebaum in den Idealo-Matcher aufgenommen. Alle 381 aktuellen aktiven Hobbyziele gelten als beachtbare Kontexte, nicht eine Auswahl der ersten 50. In anderen Workflows vorhandene 50er-Zahlen betreffen unter anderem eBay-/Abfrage-/Hintergrund-Stapel, nicht diesen Idealo-Konzeptkatalog.
- **Tatsächlich 381 aktive terminale Hobbys** im HD007-Register aus 862 Gesamtregistern; für alle 381 ist `result_profile.what_do_you_need` vorhanden. Datei `EVIDENCE/HD009_HOBBYREGISTER_AUSRUESTUNGSINVENTUR_381_20261113.csv`. Quellarchiv HD007 SHA256 `ba838946d5b04a5f31f92bc993aba69a924250cbd78bd6beb6a52ed32144ec4f`. Evidenz https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43391488408
- Nach realem Hobbydepot-WP-Import am 12.11.2026: Feed 2747, ca. 543.676 Feedprodukte, 2.530 PASSED, 0 WARN, 429 Idealo-Kampagnen, 52 Zielkonzepte, 23 Hobbyfamilien (Screenshot des Betreibers; nicht live aus dem Nutzer-Backend durch den Auditor neu abgerufen).
- **Kein Beleg für 52 geeignete von insgesamt 381 geeignet.** 52 = bereits erfolgreich gemappte Ziele, nicht Gesamtzahl der käuflichen Hobbys.
- Der Idealo-Matcher liest bisher nur `business_concepts[].title` (kurze Hobbynamen) und nicht `result_profile.what_do_you_need`. Der schon vorhandene Amazon/DataForSEO-Pfad liest das Bedürfnisfeld, jedoch ausdrücklich mit eigenen Regeln für **kostenpflichtige** Suchanfragen. Diese müssen nicht automatisch die semantische Idealo-Freigabe bestimmen.
- Die physische und semantische Qualität der Ausrüstungsbedarfe ist verschieden: `3D-Druck` -> `3D-Drucker`; `Airbrush` -> `Airbrushpistole`; `Münzen` -> `Sichere Aufbewahrung`, später `Lupe`; `Buchbinden` -> `Papier`, später `Schneidwerkzeug, Faden, Leim`; `Kettenhemdflechten` -> `Metallringe` ohne sicheren Verwendungsnachweis. Einfach jede zweite/dritte Wortgruppe als Produktziel aufzunehmen wäre fachlich falsch.
- Eine **rein sprachliche Erstprüfung** ergab 337 spezifisch wirkende erste Begriffe und 44 generische; das ist **KEINE** tatsächlich geeignete/ausgeschlossene Produkteinteilung und darf weder als Werbequote noch als Freigabe genutzt werden.
- **Feedwahl ist ein eigener ungeprüfter Abdeckungsfaktor**: Feed 2747 heißt laut iPN-Portal `Fashion, Sport, Outdoor`; Feed 2901 `Standard Datafeed` wurde bei Pferdeatelier nachgewiesen. Vor einem Wechsel muss seine **tatsächliche Freigabe für Hobby Depot PID 568912** festgestellt werden; Vorab-Hinweise aus anderer Korrespondenz ersetzen keinen API-Test. Es ist nicht bewiesen, dass 2901 sämtliche Produkte aus 2747 einschließt. Kein blindes Austauschen einer laufenden Feed-ID.

## Ursache und Reihenfolge – ohne Doppeltechnik
1. **Datenversorgung**: Für dieselbe Hobby-Depot-Werbefläche feststellen, welche Feeds idealo tatsächlich freigegeben hat. Falls 2901 verfügbar ist, zunächst getrennten, nicht störenden Vergleich des Inhalts/GTIN-Umfangs mit 2747 und gleicher Zuordnungslogik. Die bestehende Datenbasis nicht allein zum Testen ersetzen.
2. **Zuordnung**: Für noch offene Hobbyziele mit echten Feedzeilen feststellen, ob der Grund `nicht im Feed`, `Hobbynamen-Abgleich zu eng`, `mehrdeutig` oder `nicht als physisches Produkt sinnvoll` ist. Ohne echte Zeilendaten lassen sich diese Gründe nicht seriös pro Hobby behaupten.
3. **Wenn nötig gezielter KISS-Fix**: Nur sichere konkrete Ausrüstungsbegriffe aus dem existierenden HD007 einbeziehen (kein frei erfundener Artikel), nur bei eindeutiger Produktidentität/Kontext. Vor einer Freigabe komplette Quell- und Live-Funktionstests inklusive falscher Zuweisung/Marken/GTIN/Adapter, Kaufmöglichkeit, Originalbilder und unveränderter Amazon-/eBay-Wege.
4. **Getrennte Quote**: Die endgültige Analyse muss `aktive Hobbyziele`, `nachweislich kaufbar`, `explizit ausgeschlossen`, `beim Feed nachweislich nicht vorhanden` und `wirklich versorgt` getrennt ausweisen. Derzeit sind nur 381 und 52 wirklich bekannt; für die übrigen fehlt die Zuordnung.

**Nicht umgesetzt:** Kein Plugin-Update und kein Feedwechsel, um bereits 429 funktionierende Zuordnungen nicht durch einen unbegründeten Eingriff zu gefährden.

## Belege
- Vollständige Bestandsinventur CSV `EVIDENCE/HD009_HOBBYREGISTER_AUSRUESTUNGSINVENTUR_381_20261113.csv`
- Strukturierter Bericht JSON `EVIDENCE/HD009_HOBBYREGISTER_AUSRUESTUNGSINVENTUR_SUMMARY_20261113.json`
- Idealo-Matcher und 50er-Codeprüfung: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43278691866
- Register und ursprünglicher Amazon-Keyword-Mechanismus: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43390964524
