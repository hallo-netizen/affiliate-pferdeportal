# BAUCONTAINER – ARCHITEKTUR-FEHLERKISTE

STAND: 2026-09-05

## Zweck

Fehler des Campus, seiner Struktur und seiner Arbeitsweise werden getrennt von Fachfehlern erfasst.

Das ist die Fehlerkiste für:
- falsches Routing;
- doppelte Wahrheiten;
- unnötige Bürokratie;
- fehlende oder veraltete Verweise;
- zu große produktive Räume;
- falsche Modulklassifizierung;
- Architekturänderung ohne WHY/Protokoll;
- Archivierung aktiver oder ungeklärter Dinge;
- Pförtner-/Hausmeister-/Baucontainer-Prozessfehler.

Fachfehler wie TEXT-M26 oder ein Plugin-Bug gehören weiterhin ins zentrale Fach-`FEHLERREGISTER.md`.

## Felder

- BAU-FEHLER-ID
- STATUS: OPEN / BLOCKED / CLOSED
- KURZ
- AUSWIRKUNG
- URSACHE, wenn belegt
- KISS-FIX
- BELEG
- REGRESSIONSSCHUTZ / Regel

## BAU-001 – Doppeltes Modulregister

STATUS: CLOSED
KURZ:
Es existierten vorübergehend `REGISTER.md` und `MODULREGISTER.md`.
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

## Harte Regel

OPEN/UNGEKLÄRTE Architekturfehler werden nicht durch spontane Großumbauten „gelöst“.

Erst:
Fehler belegen → kleinste nachhaltige Lösung → protokollieren → prüfen.
