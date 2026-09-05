# BAUCONTAINER – ARCHITEKTUR-FEHLERKISTE

STAND: 2026-09-05

## Zweck

Fehler des Campus, seiner Struktur und seiner Arbeitsweise werden getrennt von Fachfehlern erfasst.

Fachfehler bleiben im zentralen Fach-`FEHLERREGISTER.md`.

## Felder

- BAU-FEHLER-ID
- STATUS: OPEN / BLOCKED / CLOSED
- KURZ
- AUSWIRKUNG
- URSACHE
- KISS-FIX
- BELEG
- REGRESSIONSSCHUTZ

## BAU-001 – Doppeltes Modulregister

STATUS: CLOSED

KURZ:
Vorübergehend existierten `REGISTER.md` und `MODULREGISTER.md`.

AUSWIRKUNG:
Risiko zweier Wahrheiten.

KISS-FIX:
`REGISTER.md` entfernt; genau ein `MODULREGISTER.md`.

REGRESSIONSSCHUTZ:
Ein Modulregister = eine zentrale Navigationsquelle.

## BAU-002 – Modulklasse mit Masterakte vermischt

STATUS: CLOSED

KURZ:
Die Bildzentrale wurde vorübergehend als Modulklasse „GEMISCHT“ beschrieben.

AUSWIRKUNG:
Allgemeiner Modul-Kern und projektspezifische Masterakte wurden vermischt.

KISS-FIX:
Modulklassen nur ALLGEMEINGÜLTIG / PROJEKTBEZOGEN / UNGEKLÄRT.
„Gemischt“ gilt nur für Masterakten/Artefaktpakete.

BELEG:
ARCH-013.

## BAU-003 – Campus liegt im Pferde-Atelier-Repo

STATUS: OPEN / ARCHITEKTURENTSCHEIDUNG

KURZ:
Campus-Prototyp liegt aktuell im öffentlichen Projekt-Repository des Pferde-Ateliers.

AUSWIRKUNG:
Mehrere künftige Projekte und zentrale geschützte Akten passen logisch nicht dauerhaft unter ein einzelnes Projekt.

KISS-KANDIDAT:
Eigenes privates Campus-Repository nach V1-Freigabe.

REGEL BIS DAHIN:
Keine Secrets in den öffentlichen Prototyp.

## BAU-004 – Hausmeister durfte Fachinhalte verändern

STATUS: CLOSED

KURZ:
Der erste Hausmeisterentwurf erlaubte u. a. CURRENT_STATE zu verkürzen und HOBBYRAUM auf FREI zu setzen.

AUSWIRKUNG:
Eine reine Verwaltungsrolle hätte fachliche Wahrheit verändern können.

URSACHE:
Verwaltung und Fachpflege waren nicht hart genug getrennt.

KISS-FIX:
Hausmeister darf nur unverändert ordnen/verschieben und reine Archiv-/Verwaltungsakten pflegen.

REGRESSIONSSCHUTZ:
**Hausmeister = Verwaltung. Finger weg von Fachinhalten.**

## BAU-005 – Pförtnerrolle und Architekturarbeit vermischt

STATUS: CLOSED

KURZ:
Der Pförtner-Eingang enthielt Architektur-Sonderrecht, ohne den Rollenwechsel hart genug zu trennen.

AUSWIRKUNG:
Ein Pförtner hätte als schreibende Architekturrolle verstanden werden können.

KISS-FIX:
Pförtner = READ/ROUTE ONLY.
Architekturarbeit erst nach ausdrücklich beendetem Pförtner-Modus in der Baucontainer-Rolle.

REGRESSIONSSCHUTZ:
**Rolle bestimmt Rechte. Pförtner schreibt nichts.**

## Harte Regel

OPEN/UNGEKLÄRTE Architekturfehler werden nicht durch spontane Großumbauten gelöst.

Erst:
Fehler belegen → kleinste nachhaltige Lösung → protokollieren → prüfen.


## BAU-006 – Sonderräume ohne vollständigen 1-Klick-Eingang

STATUS: CLOSED

KURZ:
Archiv und Zielverträge hatten keinen vollständigen 1-Klick-Block; Baucontainer hatte keinen eigenen START_HERE.

KISS-FIX:
1-Klick-Eingänge ergänzt.

REGRESSIONSSCHUTZ:
EINGANGSSTANDARD gilt auch für Sonderräume.

## BAU-007 – Alltagssprache nicht explizit als Routingauftrag gebunden

STATUS: CLOSED

KURZ:
Der Trigger „Hauptpförtner.“ war definiert, natürliche Formulierungen aber nicht hart beschrieben.

KISS-FIX:
Campus START_HERE + Hauptpförtner akzeptieren eindeutige Alltagssprache als Routingauftrag.

## BAU-008 – Paul TEXT/SEO hatte keine direkte vollständige Quellenkette

STATUS: CLOSED

KURZ:
Paul-Eingang verwies allgemein auf Register, aber nicht direkt auf die sechs aktuellen TEXT-/SEO-Akten.

KISS-FIX:
Wortgleiche aktuelle Quellenkopien + `PAUL/TEXT_SEO/START_HERE.md`.

## BAU-009 – Tresorstatus war implizit statt eindeutig

STATUS: CLOSED

KURZ:
Tresorkonzept verlangte TRESOR_PASS, aber es gab weder START_HERE noch expliziten aktuellen FAIL-Status.

KISS-FIX:
`TRESOR/START_HERE.md` + `TRESOR/STATUS.md`.

WICHTIG:
Architekturlücke geschlossen; operativer TRESOR_PASS bleibt korrekt BLOCKED, bis der Prüfvertrag erfüllt ist.


## BAU-010 – Dauerakten enthielten temporäre Chat-Zustände

STATUS: CLOSED

KURZ:
Gebäude-/Büro-/Hobbyraumtexte enthielten „Sortierchat“ bzw. einen veralteten Parallelchat-Hinweis.

AUSWIRKUNG:
Ein neuer Chat/Paul konnte widersprüchliche Rechte oder veraltete Belegung lesen.

KISS-FIX:
Temporäre Chatbezüge entfernt; dauerhafte Rollen-/Arbeitsweglogik eingesetzt.

REGRESSIONSSCHUTZ:
ARCH-034 + EINGANGSSTANDARD.

## BAU-011 – Paul-Pflichtlektüre mit abgekürzten Pfaden

STATUS: CLOSED

KURZ:
Fünf Paul-Quellen waren als `.../datei.md` angegeben.

AUSWIRKUNG:
Menschlich verständlich, aber kein deterministischer 1-Klick-Weg.

KISS-FIX:
Alle fünf Pfade vollständig ausgeschrieben.

REGRESSIONSSCHUTZ:
Paul-Pfade immer vollständig; keine Ellipsen.

## BAU-012 – Hobbyraum-Zustände/Kennwort nicht zentral normiert

STATUS: CLOSED

KURZ:
„Ein Hobbyraum pro Büro“ war definiert, aber Zustände und Routing-Kennwort nicht.

KISS-FIX:
`HOBBYRAUM_STANDARD.md` mit FREI / AKTIV / BLOCKED und Routing-Kennwort „Hobbyraum“.

SICHERHEIT:
Kein Passwort; echte Rechte bleiben rollen-/branchgebunden.

## BAU-013 – Veraltete Statusduplikate in zentralen Architekturakten

STATUS: CLOSED

KURZ:
Änderungsregister nannte noch alten Tresorblocker und alten Bild-Dateilückenstatus.

KISS-FIX:
Nur den belegten aktuellen Metadatenstand nachgezogen; keine Fachbewertung ergänzt.


## BAU-014 – Direkter Büroeintritt konnte zentrale Leitungen umgehen

STATUS: CLOSED

KURZ:
Büro-START_HERE führte zwar zu Current/Hobbyraum, aber nicht überall sichtbar zu Fehler-/Änderungs-/Ziel-/Handlungsregistern.

KISS-FIX:
Einheitliche Arbeitsfreigabe an allen sechs Pferde-Atelier-Büroeingängen ergänzt.

## BAU-015 – Hobbyräume waren bei Direktlink nicht selbsterklärend

STATUS: CLOSED

KURZ:
Mehrere HOBBYRAUM-Dateien enthielten nur STATUS/FREI und keine Rechte-/Weiterweg-Erklärung.

KISS-FIX:
Alle sechs Hobbyräume mit derselben 1-Klick-Übersicht ausgestattet.
