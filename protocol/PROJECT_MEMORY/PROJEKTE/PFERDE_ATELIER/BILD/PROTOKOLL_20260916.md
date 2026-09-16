# BILD – PROTOKOLL 2026-09-16

## Tatsächlich ausgeführte Arbeit

- Wasserzeichenkonzept als separaten Backlog `TODO-BILD-WASSERZEICHEN-001` im BILD-Büro abgelegt.
- Verbindlichen Zielvertrag für Pferderassen-Hero angelegt.
- Bildzentrale 2.6.9 auf 2.7.0 erweitert: generischer Custom-Post-Type-Hero-Weg, kein `pa_breed`-Hardcoding im allgemeinen Kern.
- Pferde-Atelier-Zielnutzung: `pa_breed`.
- neues Hero-Profil: 3:1 / 1200×400 / WebP.
- Featured-Image-Readback + Dateiformatprüfung + Rollback auf vorheriges Featured Image eingebaut.
- bestehende Artikel-/Kategorie-/HivePress-Wege als Regression geprüft.
- Pferde-Design 1.50.536 statisch geprüft: Featured Image wird vor dem Standard-Rassenbild gelesen; daher aktuell kein Designpatch erforderlich.
- 2.7.0-Release persistent in der allgemeinen Bildzentrale abgelegt und PPA-003 als isolierte Ausgabekopie synchronisiert.

## Prüfungen

- finaler ZIP-Lesetest: PASS.
- Version 2.7.0 aus finaler ZIP: PASS.
- SHA-256 final: `8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`.
- PHP-Lint aus finaler ZIP: PASS.
- Positiv-/Negativ-/Regressionstest: 28/28 PASS.
- persistenter Readback `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/CURRENT.zip`: Version/Hash PASS.
- persistenter Readback `PPA-003/CURRENT.zip`: Version/Hash PASS.
- WordPress-LIVE-Test 2.7.0: NOCH NICHT AUSGEFÜHRT.

## Fehler / Korrektur

`BILD-DOC-20260916-001` – CLOSED.

Eine zwischenzeitliche Dokumentationsbehauptung lautete, die bisherige PPA-003-Ausgabekopie sei inkonsistent bzw. enthalte ein fremdes Plugin. Das war falsch.

Frischer Readback vor der 2.7.0-Synchronisierung ergab:
- Version 2.6.9;
- SHA-256 `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`;
- damit Übereinstimmung mit dem damaligen Manifest.

Die falsche Behauptung wurde aus Hobbyraum/Testbeleg entfernt bzw. korrigiert. Sie ist keine aktuelle Wahrheit.

## WARUM / Entscheidungen

- Der neue Weg ist generisch statt `pa_breed`-spezifisch, damit MOD-002 allgemeingültig bleibt.
- Das Design wird nicht vorsorglich geändert, weil die vorhandene Featured-Image/Fallback-Logik den Bedarf bereits abdeckt; erst ein realer Gegenbeleg rechtfertigt einen Designpatch.
- Wasserzeichen werden nicht in den Hero-Release gemischt. Das verhindert eine unnötige Mehrfachänderung und hält Rollback/Testgrenzen klar.
- Wasserzeichen sollen später technisch nach der Bildgenerierung/Medienaufnahme erfolgen, nicht als Promptbestandteil.

## LIVE-Grenze / nächste Abnahme

2.7.0 ist erst LIVE PASS nach Installation in WordPress, Speicherung von `pa_breed`, realer Hero-Erzeugung für mindestens eine Pferderasse, Featured-Image-Readback und Frontend-Positiv-/Negativprüfung des Fallbacks.
