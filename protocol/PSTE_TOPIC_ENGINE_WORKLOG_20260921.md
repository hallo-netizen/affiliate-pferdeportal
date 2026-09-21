# PSTE Arbeits-/Änderungsprotokoll – 2026-09-21

Rolle: Historie/Nachweis. **Keine CURRENT-Autorität.**
Aktueller Status steht ausschließlich in `control/pste-topic-engine/CURRENT_STATE.json`.

## Erledigt
- 0.57-Server-Step-Driver-Strang aufgebaut.
- DataForSEO-Retry so getrennt, dass ein sicherer Retry in einem späteren Serverrequest erfolgt; historisches 45-Sekunden-Providerlimit bleibt unverändert.
- Unknown-Transport: kein Blind-Replay, Jobdaten werden erhalten/archiviert.
- Separate-PHP-Prozess-Harnesses für Einzellauf und Breadth aufgebaut.
- Separater Prozess-Breadth-Lauf lokal/GitHub bis 14 Familien / 42 nutzbare Themen / `TARGET_REACHED` geprüft.
- echter PSERC-Compiler im kombinierten Harness bis `READY_FOR_METADATA_HANDOFF + plan_slot` geprüft.
- exakte ZIP-Bytes in separatem GitHub-Retest geprüft; dieser Nachweis war **kein** Real-WordPress-Live-PASS.
- nach realem 0.57.1-Live-Fail vollständigen WordPress-Hobbyraum aufgebaut:
  - WordPress + MySQL,
  - Multiworker-PHP,
  - echtes `admin-ajax.php`,
  - echte Loopbacks,
  - unabhängiges WP-Cron,
  - echter Admin-Login/Nonce,
  - DataForSEO nur am externen Provider-Rand deterministisch gemockt.
- manueller Real-WordPress-Einzellauf inzwischen stabil PASS.
- Produktionswelle real bis `TARGET_REACHED` geführt; finale Systemprüfung bleibt rot.
- nicht atomare Lock-Freigaben als reale Race-Klasse nachgewiesen und im Hobbyraum atomar gehärtet.
- harte Build-Postconditions ergänzt, damit Driver-/Step-/Queue-Lock-Härtung nicht still teilweise angewendet werden kann.
- Job-/Queue-Fencing untersucht; keine Freigabe erteilt, solange Real-WordPress-Breadth rot bleibt.
- Kosten-/Job-State-Tracing, Lock-Ownership-Tracing, Active-Job-Delete-Tracing und Driver-Lock-SQL-Source-Tracing ergänzt.
- letzter Run belegt: `deleteIfSame()` entfernt den fehlerhaften Job erst **nach** dem Cost-Ledger-Mismatch. Die Löschung ist nicht Primärursache.

## Warum diese Änderungen
Die früheren In-Process- und ZIP-Prüfungen konnten echte Multiworker-Interleavings nicht vollständig abbilden. Der reale WordPress-HTTP-Hobbyraum zeigte dadurch Fehler, die isolierte Harnesses nicht sichtbar machten. Seitdem gilt für diese Reparatur:
- keine Freigabe nur aus Klassen-/Harness-PASS,
- keine Symptombehandlung am Cost-Ledger,
- KISS: nur den zuerst belegten Systembruch bearbeiten,
- nach jeder Produktänderung wieder kompletter echter WordPress-Einzellauf + Breadth-Lauf.

## Verworfen / nicht weiterführen
- bloßes Erhöhen der OVERDUE-Zeit;
- pauschales Kürzen des historischen 45-Sekunden-Providerlimits;
- Cost-Ledger-Mismatch weichmachen;
- aktiven Job bei Fehlern löschen, um den Fehler zu verdecken;
- weitere neue Nebenarchitektur;
- Plugin-Freigabe vor Real-WordPress-Breadth-PASS.

## Aktueller technischer Arbeitsweg
Branch:
`pste-05700-server-step-driver-proof`

Letzter relevanter technischer Head:
`f2cc6c058b0a52b4cf3df77cd83dd1144a63849a`

Letzter echter WordPress-Lauf:
`35595789702` — FAILURE im Breadth-Schritt.

Nächste Arbeit ausschließlich nach `control/pste-topic-engine/CURRENT_STATE.json`.
