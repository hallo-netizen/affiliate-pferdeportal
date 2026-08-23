# Root Cause – PSTE_BREADTH_SEQUENCE_GUARD_EXCEEDED

## Befund
PSTE 0.56.9 konnte nach 180 clientseitigen Breitenrecherche-Fortsetzungszyklen `PSTE_BREADTH_SEQUENCE_GUARD_EXCEEDED` ausgeben, obwohl der serverseitige Queue-Zustand bereits terminal sein konnte.

## Ursache
Der Browser-Loop brach nach 180 Iterationen ohne abschließenden autoritativen Server-Readback ab. Dadurch konnte eine stale RUNNING-Antwort den Client-Guard auslösen, obwohl die serverseitige Queue inzwischen `COMPLETE`, `PAUSED_ERROR` oder `OUTCOME_UNKNOWN` erreicht hatte.

## Korrektur 0.56.10
- genau ein read-only Final-Readback nach Erreichen des Client-Limits
- neuer AJAX-Statuspfad ruft ausschließlich `PSTE_Breadth_Research_Queue::peek()` auf
- `peek()` liest und validiert den persistenten Queue-Zustand ohne Recovery, Resume, Advance oder Persistenz
- Server `COMPLETE` => normaler Abschluss
- Server `PAUSED_ERROR`/`OUTCOME_UNKNOWN` => vorhandener fail-closed Zustand
- weiterhin nichtterminal => `PSTE_BREADTH_SEQUENCE_GUARD_EXCEEDED_AFTER_FINAL_READBACK`

## Nicht verändert
Keine Änderung an Rechercheauswahl, API-/Kostenlogik, Themenpersistenz, Titellogik, Redaktionsplan, PSERC, PPM, Artikelinhalt, Design oder Publish-Verhalten.

## QA
- 72/72 PHP-Dateien Syntax PASS
- 52/52 JSON-Dateien Parse PASS
- Source/Fresh-Extract-Parität 210/210 PASS
- ZIP-Integrität PASS
- read-only `peek()` positiv: COMPLETE 3/3, 0 Writes
- statische Delta-/Guard-Prüfung PASS

Installer SHA-256: `ad9d1f737e299933760e2622ec547c5f8e3ed17d5dcd5ca1af369913aa5d95bd`

Status: LOCAL PASS / LIVE INSTALLATION NOCH OFFEN.
