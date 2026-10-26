# HD-009 – FEHLERQUELLEN

ROLLE: Autoritative Fehlerchronik für HD-009. Aktueller Gesamtstatus und genau eine NEXT ACTION ausschließlich aus `CURRENT.md`.

## HD009-ERR-001 – Verwaister Recovery-Rest erzeugt PHP-Parsefehler

Status: **CLOSED – 2026-10-26**

Befund:
Gate-4-Lauf `40319097524` stoppte im PHP-Lint mit `unexpected token "return", expecting "function"` in `hobby-depot-affiliate-router.php`, Zeile 4155.

Ursache:
Beim fachlich korrekten Abschalten des Pferdeatelier-spezifischen historischen Recovery-Lookups wurde dessen Rückgabeende nicht vollständig entfernt; `return $lookup; }` blieb außerhalb einer Methode stehen.

Fix:
Nur die beiden verwaisten Zeilen entfernt; der Hobby-Depot-Lookup bleibt bewusst leer/fail-closed.

Fix-Commit:
`a5fca469dda22d459dd65f040bb8cd872c697982`

Nachweis:
Folgelauf PHP-Lint **23/23 PASS**.

## HD009-ERR-002 – Fremdprojekt-Scanner meldet „fohlen“ in „empfohlen“

Status: **CLOSED – 2026-10-26**

Befund:
Gate-4-Lauf `40319345523` meldete im idealo-Admintext einen Fremdprojektmarker `fohlen`.

Ursache:
Der Scanner suchte `Fohlen` als beliebigen Teilstring und traf dadurch das neutrale Wort `empfohlen`. Kein Pferdeatelier-Inhalt im Quelltext.

Fix:
Nur diesen Marker auf Wortgrenzen eingeschränkt; die übrigen Fremdprojektmarker unverändert.

Fix-Commit:
`a1b482e4e1b70163ec48b32dc2bd5780eb5f72ec`

Nachweis:
Gate-4-Lauf `40319481655`: Fremdprojekt-Regression **PASS**, Gesamtjob **PASS**.
