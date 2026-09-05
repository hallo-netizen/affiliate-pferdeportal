# CAMPUS – KRITISCHE BAUABNAHME 05.09.2026

STATUS:
**ARCHITEKTUR / NAVIGATION / ROLLEN: PASS**
**SICHERHEIT / KATASTROPHEN-WIEDERAUFBAU: BLOCKED**

## Prüfmodell – „Strom, Wasser, Luft, Licht“

### LICHT – Orientierung
PASS.

- 22/22 PROJECT_MEMORY-Verzeichnisse besitzen `START_HERE.md`.
- 22/22 Eingänge erfüllen:
  - WAS IST DAS?
  - HIER BIST DU RICHTIG, WENN …
  - DU DARFST …
  - DU DARFST NICHT …
  - ALS NÄCHSTES …
- Campus, Projektflur, Pferde-Gebäude, alle Büros, Paul, Archiv, Baucontainer, Tresor, Zielverträge und Quellenräume sind direkt erklärend.

### STROM – technische Anbindung
PASS für den aktuellen Betriebsstand.

- technische Fachwahrheit bleibt in GitHub-Originalquellen;
- PROJECT_MEMORY ist Wegweiser/Gedächtnis, nicht zweite technische Wahrheit;
- Paul TEXT/SEO ist an aktuellen main-Basisstand und eigenen Branch gebunden;
- keine direkte main-Schreibbefugnis aus Campusrollen.

### WASSER – aktueller Zustand / Quellenzufluss
PASS.

6/6 Pferde-Büros besitzen:
- `START_HERE.md`
- `CURRENT_STATE.md`
- genau einen `HOBBYRAUM.md`

TEXT besitzt zusätzlich:
- sechs unveränderte aktuelle Originalakten;
- Zielvertrag;
- Fehlerliste;
- Protokoll;
- Test-vs-Live-Befund;
- Hard Rules;
- technische Originalquellen.

### LUFT – Rollen/Befugnisse
PASS.

Hauptpförtner:
READ/ROUTE ONLY.

Hausmeister:
reine Verwaltung; keine Fachinhalte, kein CURRENT_STATE-/HOBBYRAUM-Umschreiben, keine Löschung.

Facharbeit:
erst nach Rollenwechsel + gebundenem Arbeitsweg.

Paul:
nur eigener Branch; kein main; kein Blind-Merge.

Baucontainer:
Architekturänderungen aus jedem Chat möglich, aber nur in Baucontainer-Rolle + Protokoll/WHY.

## Kommunikationskanäle
PASS.

Bei direktem Büroeintritt führen alle 6 Büros sichtbar zu:
1. CURRENT_STATE
2. HOBBYRAUM
3. HANDLUNGSVERZEICHNIS
4. FEHLERREGISTER
5. AENDERUNGSREGISTER
6. ZIELVERTRAGSREGISTER
7. gebundener Arbeitsweg

Zentrale Register:
- Fehlerregister
- Änderungs-/Erklärungsregister
- Zielvertragsregister
- Modulregister
- WordPress-Register
- Archivregister

## Hobbyräume
PASS.

Genau 6 Pferde-Büros → genau 6 Hobbyräume.

Zustände:
- FREI
- AKTIV
- BLOCKED

Routing-Kennwort:
`Hobbyraum`

Kein geheimes Passwort.
Sicherheit entsteht durch Rolle, Auftrag, Branch-/Repository-Rechte und Fachregeln.

TEXT:
AKTIV / Paul TEXT/SEO gebunden.

DESIGN, BILD, AFFILIATE, HIVEPRESS, GEMEINSAM:
FREI zum Abnahmezeitpunkt.

## Paul-Etage
PASS.

Adresse bleibt:
`protocol/PROJECT_MEMORY/PAUL/TEXT_SEO/START_HERE.md`

Branch bleibt:
`paul/text-seo-campus-ready-20260905`

Alle Pflichtquellen sind mit vollständigen Pfaden angegeben.
Keine `.../`-Abkürzungen.

## Baucontainer
PASS.

Vorhanden:
- START_HERE
- BAUPLAN
- BAUPROTOKOLL
- BAUÄNDERUNGEN
- ENTWICKLUNGSPROTOKOLL
- ARCHITEKTUR-FEHLERKISTE
- EINGANGSSTANDARD
- HOBBYRAUM_STANDARD
- HAUSMEISTER
- MASTERDATEIEN_REGEL

## Archiv
STRUKTUR: PASS.
REDUNDANZ: BLOCKED.

ROT/GELB/GRÜN ist eindeutig.

Nur GRÜN darf:
`LOKALE_KOPIE_ENTBEHRLICH: JA`

Aktuell mehrere relevante Roharchive GELB bzw. ROT.
Lokale Originale deshalb NICHT löschen.

## Tresor
BLOCKED – korrekt fail-closed.

Git-/GitHub-Metadaten-PREPASS:
PASS / Restore-Test vorhanden.

Erster aktueller Blocker:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`

Danach zusätzlich zu prüfen:
nicht automatisch exportierbare Recovery-Abhängigkeiten/Secrets/Autorisierungen.

Kein `TRESOR_PASS` behauptet.

## Zugriffsschutz / dauerhafter Campus-Ort
BLOCKED / offene Architekturentscheidung BAU-003.

Campus-Prototyp liegt weiterhin im öffentlichen Pferde-Atelier-Repository auf separatem Campus-Branch.

Folgen:
- keine Secrets in PROJECT_MEMORY;
- völlig neuer Chat ohne bekannten Repo-/Branch-Kontext braucht weiterhin die robuste Campus-Adresse;
- reine Alltagssprache allein ist erst nach dauerhafter Campus-Verankerung garantiert.

## Bewusst UNGEKLÄRT – kein Architekturfehler

- MOD-004 HivePress-Anzeigensuche: Modulklasse UNGEKLÄRT, sauber fail-closed im Modulregister.
- allgemeiner Affiliate-Bestand: Modulklasse UNGEKLÄRT, jetzt am Eingang ausdrücklich gekennzeichnet.

UNGEKLÄRT wird nicht als PASS umgedeutet.

## Endurteil

### POSITIV
Der Campus ist für Orientierung, tägliche Arbeit, Büro-Routing, Paul-Einstieg, Rollensteuerung und Architekturpflege **betriebsbereit**.

### NEGATIV
Ein vollständiger „alles sicher, Festplatte kann weg, Katastrophen-PASS“-Status ist **nicht** erreicht.

Offen bleiben ausschließlich die bewusst dokumentierten Infrastruktur-/Sicherheitsblöcke:
1. dauerhafter/private Campus-Ort – BAU-003;
2. zweite unabhängige Roharchiv-Sicherung;
3. danach Recovery von Secrets/externen Autorisierungen.

Keine dieser offenen Stellen wird durch Raten oder einen falschen PASS verdeckt.
