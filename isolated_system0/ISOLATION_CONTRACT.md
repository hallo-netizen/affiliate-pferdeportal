# BÜRO NULL — ISOLATIONSVERTRAG

## Verbotene Nachbarsysteme
SYSTEM0_FORBIDDEN_RUNTIME_CONTACT = 1,2,3,4,4A

## Erlaubt
- Dateien innerhalb isolated_system0/
- historische 28.08.2026-Quellen ausschließlich read-only zur Rekonstruktion
- eigene Tests und eigene Laufzeit innerhalb isolated_system0/

## Verboten
- Import aus isolated_system4/
- Aufruf von isolated_system4/
- Lesen oder Schreiben seiner CURRENT/STATE/HANDOFF-Dateien
- Aufruf aktueller Konzept-1/2/3/4/4A-Worker
- gemeinsamer Runtime-Ordner
- gemeinsamer Handoff
- gemeinsamer Controller
- Änderung fremder Systeme für SYSTEM 0

## Fail closed
Sobald für eine Funktion Kontakt zu 1/2/3/4/4A erforderlich wäre, gilt BÜRO NULL als BLOCKED. Es darf keine automatische Ausweichroute geben.
