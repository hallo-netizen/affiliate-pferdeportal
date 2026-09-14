# GLOSSAR – ENTSCHEIDUNGEN / WARUM – 2026-09-14

ROLLE: Dauerhafte lokale WAS/WARUM-Entscheidungen; keine zweite CURRENT-/Fehlerwahrheit.

## GLOSSAR-DEC-001 – Verwandte Begriffe ausschließlich in eigener Linkbox

**WAS:** Verwandte Glossarbegriffe werden als Links ausschließlich im Block `Verwandte Begriffe` ausgegeben.

**WARUM:** Beziehungen sichtbar und strukturiert halten, ohne redundante Links im Text.

## GLOSSAR-DEC-002 – Fließtext vollständig linkfrei

**WAS:** Im Glossar-Fließtext sind ausnahmslos **0 Links** zulässig. Das Portalziel wird ausschließlich rechts in `Mehr zum Thema` verlinkt; Journal nur dort ersatzweise, wenn kein passendes Portalziel existiert.

**WARUM:** Nutzerentscheidung 2026-09-14; der Begriffstext soll ruhig und vollständig linkfrei bleiben. Navigation und Beziehungen sind klar in den rechten Blöcken getrennt.

**REGELQUELLE:** `TEXT_UND_LINKREGELN.md`.

## GLOSSAR-DEC-003 – Glossar-Single-Design strikt auf `uge_term`

**WAS:** Breadcrumb, Kurzdefinition, Icons und rechte Infoboxen der Glossar-Einzelansicht dürfen ausschließlich bei `uge_term` wirken.

**WARUM:** normale WordPress-Artikel und Seiten dürfen durch die Glossargestaltung nicht regressieren.

## GLOSSAR-DEC-004 – Bestandsbegriffe überschreiben statt löschen

**WAS:** vorhandene Glossarbegriffe werden anhand eindeutiger Slugs/IDs aktualisiert; keine pauschale Löschung und Neuerzeugung. Neue Linkregeln gelten ausdrücklich auch für den Bestand.

**WARUM:** bestehende IDs/URLs und Verknüpfungen erhalten, Duplikat- und Redirectrisiko reduzieren.

## GLOSSAR-DEC-005 – Öffnungs-/Routingweg nach LIVE PASS nicht erneut umbauen

**WAS:** nachdem der Nutzer `artikelanzeige pass` bestätigt hat, gilt der Öffnungs-/Single-Routingweg als funktionierend und ist nicht Teil der aktuellen Layout-/Linkreparatur.

**WARUM:** bestätigten funktionierenden Bereich nicht bei einer unabhängigen Design-/Inhaltsreparatur erneut gefährden.

## GLOSSAR-DEC-006 – Neue Begriffe nur aus frisch belegter `GEPRUEFT`-WDB-Quelle

**WAS:** kein neuer Glossarbegriff wird allein aus Chatwissen oder älteren Produktionspaketen als fachlich freigegeben erzeugt.

**WARUM:** Wissensdatenbank bleibt alleinige Fachautorität; keine erfundenen oder nicht nachweisbar geprüften Fakten.

## GLOSSAR-DEC-007 – Single-Breadcrumb nur einmal erzeugen

**WAS:** auf `uge_term` wird der globale Universal-Breadcrumb nicht erzeugt; die Single-Ansicht rendert genau ihre eigene Kette `Startseite > Glossar > Oberbereich > Begriff`.

**WARUM:** der reale Screenshot zeigte trotz früherem CSS-Ausblenden weiterhin eine falsche/doppelte Breadcrumb-Kette. Serverseitiges Nicht-Erzeugen ist robuster als bloßes Verstecken.

## GLOSSAR-DEC-008 – Rechte Ocker-Oberkante dünner

**WAS:** die obere Ockerlinie der rechten Single-Boxen wird von 4 px auf 2 px reduziert.

**WARUM:** direkte Nutzerentscheidung 2026-09-14; sonstige Boxengeometrie bleibt unverändert.
