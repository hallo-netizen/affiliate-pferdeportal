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


## BAU-016 – Projekt-Flur ohne Eingang

STATUS: CLOSED

KURZ:
`PROJEKTE/` war ein begehbarer Campus-Flur ohne START_HERE.

KISS-FIX:
`PROJEKTE/START_HERE.md` ergänzt.

## BAU-017 – Affiliate-Bestandsordner suggerierte durch Ablageort Allgemeingültigkeit

STATUS: CLOSED

KURZ:
`ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/` enthielt nur ein Inventar, obwohl Modulklasse UNGEKLÄRT ist.

KISS-FIX:
START_HERE + CURRENT_STATE mit harter UNGEKLÄRT-Kennzeichnung.

## BAU-018 – Tresor übersprang Roharchiv-Redundanz als ersten Blocker

STATUS: CLOSED

KURZ:
Tresorstatus nannte bereits Recovery-Secrets als ersten Blocker, obwohl relevante Archivrohdateien laut Archivregister noch GELB/ROT sind.

KISS-FIX:
Fail-closed auf `TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`.


## BAU-019 – TEXT-Quellenraum ohne 1-Klick-Standard

STATUS: CLOSED

KURZ:
`TEXT/QUELLEN_AKTUELL/START_HERE.md` war als einzige von 22 Eingangstüren nicht 1-Klick-konform.

KISS-FIX:
Gleiche Adresse beibehalten und 1-Klick-Übersicht ergänzt.

REGRESSIONSSCHUTZ:
ARCH-040.


## BAU-020 – Neubauvorlage hinkte der realen Bauordnung hinterher

STATUS: CLOSED

KURZ:
NEUES_PROJEKT_VORLAGE enthielt den alten Grundstandard, aber nicht die während der Bauabnahme ergänzten Regeln.

AUSWIRKUNG:
Ein neues Projekt hätte direkte Büro-/Hobbyraum-/Flurfehler reproduzieren können.

KISS-FIX:
Vorlage auf ARCH-032 bis ARCH-040 nachgezogen.

REGRESSIONSSCHUTZ:
ARCH-041.


## BAU-021 – Ausschilderung des aktuellen Arbeitspunkts

STATUS: CLOSED

KURZ:
Die vorhandenen Quellen waren korrekt, aber der Weg zu Stand, aktueller Arbeit, Fehler und Ziel war noch zu verteilt.

KISS-FIX:
Einheitlicher Quellenwegweiser in Gebäude, Büros, Hobbyräumen, Archiv, Fehlerregister und Paul.

REGRESSIONSSCHUTZ:
ARCH-042.

## BAU-022 – Dynamische Angaben in Wegweisern

STATUS: CLOSED

KURZ:
Einzelne Wegweiser enthielten Angaben, die bereits im CURRENT_STATE oder einer Originalquelle geführt wurden.

KISS-FIX:
Wegweiser auf reine Navigation reduziert.

REGRESSIONSSCHUTZ:
ARCH-043.


## BAU-023 – Normaler TEXT-Chat wurde automatisch zu Paul geroutet

STATUS: CLOSED

KURZ:
Der TEXT-Hobbyraum führte jeden Arbeitschat direkt in den Paul-TEXT/SEO-Eingang.

AUSWIRKUNG:
Arbeitschat und Paul konnten als zwei gleichzeitige Bearbeiter desselben Problems verstanden werden. Das hätte parallele Writes, veraltete Zustände und Integrationskonflikte begünstigt.

URSACHE:
Bei der letzten Ausschilderungsvereinheitlichung wurde „Paul als gebundener Spezialworker“ fälschlich zu „Paul als normaler NEXT ACTION“ verkürzt.

KISS-FIX:
Paul aus der normalen TEXT-Navigation entfernt; Paul-Eingänge WORKER_ONLY; PROJECT_MEMORY für Paul READ ONLY; technischer Schreibbereich explizit; Integration nur durch Arbeitschat.

REGRESSIONSSCHUTZ:
ARCH-044 + ARCH-045 + EINGANGSSTANDARD + NEUES_PROJEKT_VORLAGE.


## BAU-024 – Paul-Schreibgrenze noch nicht serverseitig erzwungen

STATUS: BLOCKED / SECURITY-MAINTENANCE

KURZ:
Campus und Paul-Eingänge verbieten Paul Änderungen an `protocol/PROJECT_MEMORY/**`, aber der aktuelle main-`hardlock-base` prüft diese Worker-Grenze noch nicht technisch.

AUSWIRKUNG:
Ein fehlgeleiteter Paul-Worker könnte auf seinem Branch weiterhin PROJECT_MEMORY-Dateien committen. Die dokumentierte Regel verhindert das logisch, aber noch nicht serverseitig beim Integrationsweg.

KISS-FIX:
Eine einzige trusted-base-Diffregel in `.github/workflows/pferde-atelier-immutable-base-hardlock.yml`:
`paul/*` + `protocol/PROJECT_MEMORY/**` = `PAUL_PROJECT_MEMORY_WRITE_BLOCKED`.

BELEG:
Security-PR #137, Commit `68aaced0cb8629577c3b82f02da298b4b74fff93`.

BLOCKER:
Der bestehende immutable Base-Hardlock blockiert absichtlich jede Änderung seiner eigenen Workflow-Security mit `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
Der verfügbare GitHub-Zugriff besitzt keinen Ruleset-Admin-Write/BYPASS.

REGRESSIONSSCHUTZ NACH ADMIN-AKTIVIERUNG:
echter Positiv-/Negativtest auf main; erst danach CLOSED.


## BAU-025 – Architekturfix änderte unbelegt den aktuellen Worker

STATUS: CLOSED

KURZ:
Im Zuge der Paul-Isolation wurde der TEXT-HOBBYRAUM von einer belegten Paul-Arbeitsbindung auf `TEXT-ARBEITSCHAT FÜHRT` umgestellt, obwohl keine neue Fachzuweisung belegt war.

AUSWIRKUNG:
Die Architektur hätte selbst eine neue aktuelle Arbeitswahrheit erzeugt – genau entgegen dem Eine-Wahrheit-Prinzip.

URSACHE:
Rollen-/Routingkorrektur und dynamische Arbeitszuweisung wurden vermischt.

KISS-FIX:
Paul-Bindung als aktuellen Arbeitsstatus wiederhergestellt; nur Routing/Schreibgrenzen geändert. HOBBYRAUM_STANDARD verbietet künftig unbelegte Status-/Worker-/Branch-Umschreibungen durch Architekturarbeit.

REGRESSIONSSCHUTZ:
ARCH-049 + HOBBYRAUM_STANDARD.


## BAU-026 – Protokollpflicht war dokumentiert, aber nicht technisch erzwungen

STATUS: BLOCKED / SECURITY-MAINTENANCE

KURZ:
Campus-START_HERE und EINGANGSSTANDARD verlangen die Nachhol-/Protokollprüfung, aber ein Chat konnte trotzdem einen PR ohne diese Prüfung erzeugen.

AUSWIRKUNG:
Auch der Baucontainer selbst konnte seine eigene Dokumentationspflicht vergessen. Die Regel hing weiterhin teilweise am Chatgedächtnis.

URSACHE:
Es existierte noch kein Required-Check, der PROJECT_MEMORY-Diffs mit einer expliziten Abschlussentscheidung koppelt.

KISS-FIX:
Security-PR #137 um universellen `PROJECT_MEMORY_PROTOCOLCHECK` im bestehenden `hardlock-base` erweitert.

REGRESSIONSSCHUTZ NACH AKTIVIERUNG:
- fehlender/inkonsistenter PROTOKOLLCHECK blockiert;
- Architekturänderung ohne AENDERUNGSREGISTER + BAUPROTOKOLL blockiert;
- Tests oder Eine Wahrheit ohne PASS blockieren;
- gilt auch für Baucontainer-/Archiv-/Tresor-/Paul-/Büroänderungen.

BLOCKER:
Aktivierung benötigt denselben einmaligen Admin-Wartungsweg wie BAU-024.
