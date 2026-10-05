# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.10.0 PORTAL-WEITE ENGINE LOKAL HARD PASS / ECHTER HD-002-BESTAND NOCH NICHT GEBUNDEN / KEIN RELEASE

## Live

V1.9.9 Content-Pilot real bestätigt:
Buchbinden + vier Kategorien + zugeordneter Testartikel im Frontend sichtbar.

## V1.10.0

Gesamtportal-Arbeitskopie vorhanden und lokal geprüft.

Funktion:
- bis 5000 Rohkandidaten;
- DataForSEO Overview in bounded batches;
- Null-/Missing-Kandidaten getrennt;
- Core-Keyword/Synonymgruppen;
- canonical Seed-Auswahl;
- Concept-Batches;
- 8 Konzeptwelten;
- Weltzuordnung aus DataForSEO-Suggestions;
- variable Hierarchie;
- getrennte Content/Magazin/HivePress-Ziele;
- Resume ohne erneute bereits gespeicherte Overview-Batches.

Tests:
- Legacy 270/270 PASS;
- Portal Discovery PASS;
- World Routing PASS;
- 8 Worlds E2E PASS;
- Portal Scale PASS;
- Portal Negative PASS;
- Admin/Resume PASS.

## Kein falscher PASS

Der reale vollständige Hobby-Depot-Baum ist noch **nicht** erzeugt.

Grund:
Der bereits erfasste echte Gesamtbestand ist laut HD-002-Current vorhanden, aber im aktuell verfügbaren Archiv nicht als exportierte Kandidatenliste und nicht als HD-002-Source verfügbar.

Keine Rekonstruktion aus Chatgedächtnis.

## ERSTER BLOCKER

`HD001_V1100_REAL_HD002_INVENTORY_INPUT_NOT_BOUND`

## NEXT ACTION

Echten HD-002-Gesamtbestand read-only übernehmen/exportieren und unverändert als `hobby_candidates`-Quelle an Portal Discovery binden.

Danach erst kompletter realer DataForSEO→Gesamtbaum→WordPress-E2E.
