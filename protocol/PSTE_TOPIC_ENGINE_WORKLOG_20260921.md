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


## Nachtrag – exakter Live-Paketpfad und getestete Bytes – 2026-09-21
- Bestehenden realen Plugin-Basename aus WordPress belegt: `Portal SEO Topic Engine/portal-seo-topic-engine.php`.
- Fehlerhafte Paketierung mit Root `portal-seo-topic-engine` erzeugte eine zweite Plugininstallation statt eines Ersatzes; Live-Seite wurde nach parallelen Pluginordnern zeitweise unzugänglich. Recovery ohne Datenlöschung: zusätzliche Pluginordner deaktiviert/umbenannt, Seite wieder erreichbar.
- Paketbuild auf exakten Root `Portal SEO Topic Engine` umgestellt.
- Paketprüfung im Workflow: 131 Dateien, 76 PHP-Dateien, Hauptdatei/Admin/Plugin-Kern vorhanden, falscher Lowercase-Root abwesend, verschachtelter Doppelroot abwesend.
- Head `9aa8b1e22679ef0e528e7cd45e9617c880dadd8a`: alle vier Workflows SUCCESS.
- Real WordPress HTTP E2E Run `35626042769`: Single PASS, Breadth `TARGET_REACHED` 40 nutzbare Themen, 25 COMPLETE, 2 ausschließlich fachlich `PSTE_CATEGORY_EXHAUSTION_NOT_PROVEN` geparkt, 0 technische Parkfehler, Providercounts exakt 26 je Stufe.
- Evidence artifact `10652182930`, Digest `sha256:24e7a54a7d962bd14637de7d2530feaef1d5682700340472e48d9d48b8326db1`.
- Exakt getestete ZIP SHA-256 `962684fe7a3d3d22e677684ab69d9e23771c6000490071a3836993677c8ec2e0`.
- Nachholprüfung entdeckte, dass eine später separat ausgegebene Nutzer-ZIP SHA-256 `30e89d7afd683a2b8bddb5cb6fef1a21d32f5c29ce7ee4c1083e44c306020799` nicht byteidentisch mit dem getesteten Artefakt war. Diese Datei ist gesperrt.
- Nächster zulässiger Schritt: ausschließlich die exakten `962684fe...`-Bytes aus Artifact 10652182930 bereitstellen/installieren und den echten Nutzer-WordPress-Start/Progress prüfen. Bis dahin kein Live-PASS und keine PPA-005-CURRENT.zip-Promotion.


## Nachtrag – echter 0.57.3-Live-Fail nach GitHub-PASS
- Exakte 0.57.3 wurde live gestartet.
- Stale-Queue-Fehler aus 0.57.2 trat zunächst nicht erneut auf; der Lauf erreichte FINALIZE PREPARE.
- Live danach BLOCKED mit PSTE_DRIVER_STEP_OVERDUE.
- Prüfung der Produktbytes zeigt: FINALIZE PREPARE ist noch nicht request-bounded, obwohl spätere FINALIZE-Stufen bereits in Batches arbeiten.
- Zusätzlich bestätigt: Die Browseroberfläche kann nach AJAX-Start ohne Reload keinen aktiven Fortschrittsblock anzeigen, weil dieser bei initial inaktiver Queue serverseitig nicht gerendert wurde.
- Damit war der bisherige Real-WordPress-E2E nicht 1:1 bezüglich live-repräsentativer PREPARE-Last und unmittelbarem Browserzustand nach START.
- Nächster Arbeitsweg: kein Timeout-Tuning; PREPARE persistent/bounded machen + Start/Progress-UI ohne Reload + Stress-E2E im kompletten Ablauf.
