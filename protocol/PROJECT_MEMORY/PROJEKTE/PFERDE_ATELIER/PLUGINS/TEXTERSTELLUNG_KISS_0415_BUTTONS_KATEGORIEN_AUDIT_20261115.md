# Texterstellung KISS 0.4.15 – abgenommene lokale QA, NUR TEST

Stand: 2026-11-15. Ausschließlich oliver-beil.de. **Kein Live-Release.**

## Nachgewiesener Fehler 0.4.14
- Beide Recherchebuttons wurden mit `submit_button(...,['disabled'=>$busy])` gebaut. WordPress gibt auch bei `false` ein `disabled=""` aus. Deshalb waren die Buttons immer deaktiviert.
- Die alte Recherche-Statusanzeige berücksichtigte je Produktfamilie nur den ersten Artikelkategorie-Anker. In einer Schwesterkategorie abgeschlossene Recherchen wurden übersehen. PARKED/research running waren potenziell als neu/offen dargestellt.

## Umsetzung 0.4.15 (KISS)
- Nur bei tatsächlich gesperrtem Start `['disabled'=>'disabled']` übergeben; bei freiem System `[]`.
- Original `PSTE_Repository::categoryProgress` ist EIN Statusentscheider für die Anzeige und die originale `PSTE_Breadth_Research_Queue`. Liest alle zugehörigen Artikel-Kategorien der Produktfamilie und historische abgeschlossene Durchläufe.
- Unterbrochene, geparkte, gesperrte und unklare Aufträge werden nicht automatisch kostenpflichtig wiederholt; bereits abgeschlossene Recherchen bleiben erkannt.
- Anzeige zählt Produktfamilien getrennt von Artikelkategorien und aktuellen WordPress-Kategorien, damit die scheinbar geringe Familienzahl erklärbar ist.
- Jede Produktkategorie wird in der Abdeckung gezählt. Aktueller WordPress-Kategorienbestand versus gespeicherter PSTE-Bestand abgeglichen; Abweichung oder nicht zugeordnete Artikelkategorien werden sichtbar gemeldet und verhindern eine unvollständige neue kostenpflichtige Recherche.
- Original-K0, MINI, Keyword-/Datenspeicher und Rückimport unverändert; keine zweite Research-Engine.

## Größenordnung und Genauigkeit
Echter gespeicherter WP-Prüfstand vom **09.11.2026**: 1.176 Kategorien, davon 1.165 unterste Artikelkategorien. Screenshot 15.11.2026 zeigt **267 Produktfamilien** (124 offen + 143 recherchiert + 0 gesperrt). Das sind unterschiedliche Zählebenen.
**Nicht behaupten**: dass die 124/143 am 15.11. fachlich korrekt sind. Das kann nur ein tatsächlicher Abgleich mit aktueller MySQL-/WordPress-Laufhistorie bestätigen.

## Tests
- 41/41 **lokale Simulationen PASS**: tatsächliche Plugin-Admin-Seite mit WP-HTML-Attributverhalten, originaler Familien-Resolver, originaler Status-Reader, originaler persistenter Recherche-Queue-Start automatisch und gezielt, Doppelstart-Block, fehlende/stale Kategorie, PARKED/RESEARCH_RUNNING/ANALYZED, Verteilung über Hauptbereiche.
- Lastnachbau mit **synthetischen** 1.165 Artikelkategorien -> 267 Produktfamilien -> 143 abgeschlossen / 124 offen / 0 gesperrt; alle 1.165 zugeordnet und 40 eindeutige offene Kandidaten ausgewählt. **Keine echte Messung der aktuellen WP-Laufhistorie.**
- 77/77 PHP-Syntaxprüfungen PASS, ZIP-CRC PASS. 86 Dateien, genau 5 Dateien gegenüber 0.4.14 verändert (README und 4 PHP); keine hinzugefügt/gelöscht.

## Verifizierte ZIP und Büro
`Texterstellung_KISS_0.4.15_TEST_Kategorien_Audit_Buttonfix.zip`
SHA256 `144dde58cdb465f3900cc520039033d3ad9d3b7c508dcb4be25f783cdb3ab494`; 534432 Bytes.
Plugin ZIP plus `TEXTERSTELLUNG_KISS_0.4.15_STAND_UND_QA_20261115.md` in der persönlichen Library unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` tatsächlich abgelegt.

## Nächster echter Schritt
Nach Test-Backup 0.4.15 **nur auf oliver-beil.de** über bestehende Plugininstallation **ersetzen, nicht löschen**. Rechercheanzeige prüfen: Produktfamilien, Artikelkategorien, WP-Kategorien, Umsetzungsstatus. Wenn Bestand konsistent, erst **1 offene Familie** recherchieren und danach **1 vollständigen Artikel** über MINI -> original K0 -> WordPress-Draft-Import. Kein Live-Go vor Echttest.
