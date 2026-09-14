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

**WAS:** nachdem der Nutzer `artikelanzeige pass` bestätigt hat, gilt der Öffnungs-/Single-Routingweg als funktionierend und ist nicht Teil unabhängiger Layout-/Inhaltsreparaturen.

**WARUM:** bestätigten funktionierenden Bereich nicht bei einer unabhängigen Design-/Inhaltsreparatur erneut gefährden.

## GLOSSAR-DEC-006 – Neue Begriffe nur aus frisch belegter `GEPRUEFT`-WDB-Quelle

**WAS:** kein neuer Glossarbegriff wird allein aus Chatwissen oder älteren Produktionspaketen als fachlich freigegeben erzeugt.

**WARUM:** Wissensdatenbank bleibt alleinige Fachautorität; keine erfundenen oder nicht nachweisbar geprüften Fakten.

## GLOSSAR-DEC-007 – Single-Breadcrumb nur einmal erzeugen

**WAS:** die Glossar-Singleansicht darf nur eine Breadcrumb-Kette ausgeben; finaler Pfad muss dem gebundenen Glossar-/Journal-Designvertrag entsprechen.

**WARUM:** doppelte/verschachtelte Breadcrumbpfade waren real fehleranfällig. Serverseitig eindeutiger Pfad ist robuster als CSS-Verstecken.

## GLOSSAR-DEC-008 – Rechte Ocker-Oberkante dünner

**WAS:** die obere Ockerlinie der rechten Single-Boxen wird von 4 px auf 2 px reduziert.

**WARUM:** direkte Nutzerentscheidung 2026-09-14; sonstige Boxengeometrie bleibt unverändert.

## GLOSSAR-DEC-009 – Automatischer Text-/Discovery-Produktionsweg wird abgelöst

**WAS:** Der bisherige Versuch, Kandidatenfindung, Research/Textpaket, Worker-Kette und Veröffentlichung als vollautomatische Glossar-Produktion im Core zu betreiben, ist **nicht mehr der verbindliche Produktionsweg**.

**NEUER WEG:**
`geprüfter Glossar-Aktenschrank -> Chat erstellt fertige Glossartexte nach festen Regeln -> JSON-Batch -> Glossar-Importer prüft -> WordPress-Draft -> definierter Readback`.

**WARUM:** Der bisherige Automationsbau wurde technisch komplex, ohne dass die eigentliche Texterstellung verlässlich als vollständig geschlossene Strecke eingebunden war. Damit entstand hoher Aufwand ohne den gewünschten einfachen Produktionsnutzen. Der bereits bewährte Pferderassen-Manager zeigt den einfacheren kontrollierbaren Weg.

**GRENZE:** Die bisherigen 1.3.5–1.3.8 Automations-/Worker-Entwicklungen bleiben als technische Historie erhalten, sind aber keine aktive NEXT ACTION und keine aktuelle Produktionsautorität.

## GLOSSAR-DEC-010 – Zentrale Glossar-Inhalte im WDB-Aktenschrank

**WAS:** Fachbegriffe, Definitionen, Relationen und belegte Fachdaten bleiben zentral im bereits vorhandenen Aktenschrank
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.

Die späteren WordPress-JSON-Batches sind Transport-/Produktionspakete, keine zweite Fachwahrheit.

**WARUM:** analog zu den Pferderassen soll Inhalt zentral versionierbar und unabhängig von WordPress erhalten bleiben. WordPress ist Ausgabesystem, nicht einzige Wissensquelle.

## GLOSSAR-DEC-011 – Glossar-Plugin wird importerorientiert wie der Pferderassen-Manager

**WAS:** Der nächste Glossar-Pluginumbau soll sich konzeptionell am `Pferde Atelier – Pferderassen Manager 0.2.0` orientieren: eigener Bestand, JSON-Validierung, Draft-Write, Readback, Rollback/fail-closed; kein Auto-Publish als Normalweg.

**WARUM:** ein klarer, kontrollierter JSON->Draft-Weg ist einfacher prüfbar, nachvollziehbarer und vermeidet die fehleranfällige Worker-/Cron-/Loopback-Komplexität für die eigentliche Textproduktion.
