# HD-003 – EVIDENCE 1.50.738

STAND: 2026-10-24
STATUS: LOCAL RUNTIME HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.738_KUBIO_RUNTIME_SERVICE_FIX_HARDPASS.zip`

SHA-256:
`dae578a359f29ff64ee58e82732b7731278f4283da65fa405c1fad979bef138c`

## Reproduzierte Ursache
Die Live-Seite blieb in 1.50.736/737 schmal, obwohl statische Fixtures PASS meldeten. Der fehlende Fall war ein nachträglicher Kubio-DOM-Aufbau nach dem ersten Fix-Pass.

## Neuer Testvertrag
- echter importierter `preise`- und `disclaimer`-Inhalt;
- initial leere `.entry-content`;
- nach 420 ms nachträgliches Einsetzen in drei verschachtelte Wrapper mit 68 %, 76 % und 82 % Breite plus linken Margins/Paddings;
- Runtime-Script muss erst danach korrigieren.

## Gemessene Ergebnisse
Preise:
- Hero x=150 / width=900;
- Site x=150 / width=900;
- Outer/Mid/Inner jeweils x=150 / width=900;
- 3/3 Tabellen jeweils x=150 / width=900;
- 6/6 definierte Zwischenüberschriften: margin-top 30px / margin-bottom 18px.

Disclaimer:
- Hero x=150 / width=900;
- Site/Outer/Mid/Inner jeweils x=150 / width=900;
- 9/9 definierte Zwischenüberschriften: margin-top 30px / margin-bottom 18px.

## Finales ZIP
- Fresh-Unpack erneut mit derselben verzögerten Runtime-Simulation geprüft: PASS;
- PHP 11/11 PASS;
- ZIP CRC PASS;
- 936 Dateien Source↔ZIP bytegleich.
