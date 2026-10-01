# K10 Rule Ledger

K10 ersetzt die monolithische Mehrfachprüfung durch einen zentralen Regelkatalog. Jede harte Regel hat genau einen Owner und erzeugt nach einmaliger Prüfung einen hashgebundenen Receipt. Nachgelagerte Stufen prüfen nur Receipt, Identität, Vollständigkeit, Katalog-/Regelwerte-Hash und Unverändertheit.

Aktueller Nachweis: 104/104 PPM-6.7.9-Regeln exakt inventarisiert und gemappt; 89 fachliche Regeln, 15 Integritätsregeln; 3 alte Tabellenpflicht-Regeln ausdrücklich durch die genehmigte K10-Tabellenregel ersetzt. Lokale Positiv-/Negativsuite: 21/21 PASS.

K9 wird nicht importiert oder verändert. Die einzige K9-Bindung ist die unveränderliche Baseline-Referenz. `publish_allowed=false`.
