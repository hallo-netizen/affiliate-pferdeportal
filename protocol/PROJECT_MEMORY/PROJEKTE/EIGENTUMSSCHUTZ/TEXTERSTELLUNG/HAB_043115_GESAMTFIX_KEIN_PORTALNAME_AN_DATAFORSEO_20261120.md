# Hab & Bewahr 0.4.31.15 – KISS-Gesamtbehebung, 20.11.2026

## Chronologische nachgewiesene Fehlerkette
- 0.4.31.10 Wiederaufnahme des alten Abschlussauftrags.
- 0.4.31.11 DataForSEO-Testumgebung auf echten API-Betrieb umgestellt.
- 0.4.31.12 harte falsche Versionsanzeige und unsichtbaren Echtdaten-Hinweis korrigiert.
- 0.4.31.14 gelockerte Portaleignung und drei vorangegangene Nullergebnisläufe wieder geöffnet.
- Trotzdem neuer echter Abholbox-Lauf: 100 RAW-Keywords, davon 92 blockierte Kandidaten, alle fachfremd (insbesondere „ich hab“, Liedtexte). Ursache in tatsächlich ausgeführtem Original-PHP gefunden: `PSTE_Category_Context::researchContext` hängte das extrahierte Portalnamenswort „Hab“ an den Fachseed „Abholbox“ an. Der vorhandene Ausnahmetest deckte „Hab & Bewahr“ ab, aber nicht die verwendeten Schreibweisen der Site. Die Quellfunktion beeinflusste alle vier Original-Recherchewege, einschließlich der gebildeten Keyword-Ideas-Suche. Der „Hab“-Treffer wurde außerdem zeitweise als Portal-Eignungsbeweis gewertet.

## KISS-Fix in bestehendem Hab-Plugin 0.4.31.15
- Die aktive Hab-Hauptdatei setzt `TXE_HAB_BRANDLESS_RESEARCH=true` vor Original-PSTE-Ladung. **In EINEM ursprünglichen Suchseed-Entscheidungsort** bleibt das breit ermittelte Fachkeyword unverändert; kein Portalname wird mehr hinzugefügt, unabhängig von Site-Titel oder Schreibung. Bereits kontaminierte Seeds mit `hab`/`bewahr` werden vor kostenpflichtigen Anfragen geblockt. Das ist **kein Wechsel zu enger Kategorie-Suche**.
- Portalnamen werden in der Hab-Portalrelevanz nicht mehr als Stichwort-Fachbeweis verwendet; die bestehende Relevanz anhand echter Sicherheitskategorien bleibt.
- Ein einziger kostenloser Wiederfreigabe-Knopf erlaubt die nachgewiesene **vierte, verunreinigte Abholbox-Echtrecherche** wieder zu öffnen. Die ursprünglichen drei Reset-Belege bleiben bestehen und alle Originalhistorien bleiben gespeichert. Keine Kosten oder WordPress-Artikelausgaben durch diesen Klick.
- Read-only Diagnose ergänzt gespeicherten eigentlichen `stored_seed` und `effective_seed`, Anbieterumgebung und alter Portal-Zusatz aus Original-Run. Keine neue Entscheidung durch die Diagnose.

## Prüfung am finalen ZIP
`Texterstellung_HAB_UND_BEWAHR_0.4.31.15_GESAMTFIX_OHNE_PORTALNAMEN.zip` (SHA256 `05405255e7b8c81e52744e74d297a1681ba236f558bc398fbb094378c1bae3d6`).

- Originalregressionen **134/134**, echte Provider-Originalklasse & Produktionsmodus **30/30**, zwei alte Reset-Tests **38/38**, Drei-Reset **46/46**, vierter Reset positiv/negativ **82/82**.
- Test der bisherigen tatsächlichen 100 Abholbox-RAW-Keywords und des früheren 118er-Bestandes sowie Varianten des Site-Titels **42/42**.
- Aufruf der **originalen vier PHP-Anbieterwege** mit abgefangenem Transport bei zwölf verschiedenen Site-Titeln: **48/48** simulierte Aufrufe ohne Portalnamen, **0 Netzwerk-/Kostenaufrufe**.
- **420/420 Prüfungen insgesamt**, 78/78 PHP-Dateien syntaktisch geprüft, 87/87 ZIP-Inhalte CRC-validiert, 82/87 Dateien bitidentisch zu Version 0.4.31.14.
- Unverändert: 4 DataForSEO-Methoden, Research-Job, Queue, MINI, K0, Import und Budgetmechanismus.
- **Grenze:** keine Live-WordPress-Ausführung; der sichere kostenlose Knopf prüft bei Ausführung den exakten gespeicherten Original-Run und verweigert die Rücksetzung ohne Beleg.

## Ablage / Nächster Schritt
Plugin, Originaldiff, QA-Bericht, Testprogramm und schriftlicher Fehlerketten-Bericht unter `/hab-und-bewahr/TEXTERSTELLUNG/` gespeichert. Nach WordPress-Backup das vorhandene Plugin **ersetzen**, nicht deinstallieren; `Texterstellung → Recherche → Abholbox-Fehlrecherche wieder öffnen – kostenlos` einmal auslösen; danach Diagnose-JSON exportieren. **Vor neuer kostenpflichtiger Recherche erst die kostenlos vorhandene Seed-Evidenz prüfen.**