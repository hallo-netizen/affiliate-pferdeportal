# PFERDE-ATELIER – PLUGINS – CURRENT_STATE

STAND: 2026-09-15
STATUS: BLOCKED / 6 ISOLIERTE CURRENT-ARTEFAKTE REAL SYNCHRONISIERT, 4 AKTIVE EINTRÄGE OFFEN

## Belastbarer Stand

Das zentrale PLUGINS-Büro ist angelegt.

Physischer Plugin-Schrank:
`/Campus-Plugins/PFERDE_ATELIER/`

Real als isolierte `CURRENT.zip` synchronisiert und aus der persistenten Ablage erneut gelesen/geprüft:
- PPA-001 Affiliate-Zentrale 6.72.19
- PPA-003 Bildzentrale 2.6.9
- PPA-004 Universal Research & Fill 1.9.9
- PPA-005 Portal SEO Topic Engine 0.56.25
- PPA-007 Pferde Atelier HivePress Anzeigensuche 2.1.5
- PPA-011 Pferde Atelier – Pferderassen Manager 0.2.7

Jeweils vorhanden:
`CURRENT.zip` + `MANIFEST.md`.

Readback-Prüfung:
- SHA-256 = autoritativer/belegter Quellhash PASS;
- ZIP-Lesetest PASS.

Für PPA-011 zusätzlich:
- WordPress-LIVE 0.2.7: PASS, Nutzerbestätigung 2026-09-15;
- persistente `CURRENT.zip` erneut materialisiert;
- SHA-256 `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1` PASS;
- Plugin-Version aus der persistenten ZIP: 0.2.7 PASS.

Darum gilt trotzdem ausdrücklich:
**Noch kein `ALLE_PFERDE_PLUGINS_ISOLIERT_PASS`.**

## Aktuell belastbar identifizierte Pluginfamilien

Siehe ausschließlich `REGISTER.md` für Inventar-/Syncstatus.

Fach-/Release-/LIVE-Status niemals aus diesem CURRENT_STATE ableiten, sondern aus der dort je Plugin verlinkten autoritativen Quelle.

## Offene aktive Einträge

- PPA-002 Pferde Atelier Design 1.50.472: finaler Installername + SHA-256 belegt; Binärdatei aktuell nicht direkt erreichbar.
- PPA-006 Portal SEO Editorial Plan Compiler: belegbare 0.28.16-Datei vorhanden, aber historische spätere 0.28.17 darf ohne frische CURRENT-Autorität nicht als aktuell behauptet werden. 0.28.16 liegt deshalb nur als `REFERENCE_0.28.16.zip`, nicht als `CURRENT.zip`.
- PPA-008 Universal Product Comparison 0.8.0-prototype: aktuelle hashgebundene ZIP ist Fachautorität; Datei aktuell weder in Library noch im autoritativen Technikbranch erreichbar; älterer Branch ist ausdrücklich unvollständig.
- PPA-009 Universal Product Knowledge: 0.5.0 ist als reale Abhängigkeit im aktuellen Produktvergleichstest belegt; exakte aktuelle Installer-ZIP + Hash sind aber noch nicht CURRENT-gebunden.

## NEXT ACTION

Nur die vier verbleibenden BLOCKED-Einträge aus ihren autoritativen Fach-/Releasequellen vervollständigen.

Erst wenn alle tatsächlich aktiven Pferde-Plugin-Einträge `ARTEFAKT_SYNC: PASS` oder belastbar `NICHT_ERFORDERLICH` sind, darf der Gesamtstatus PASS werden.

## Nicht anfassen

- keine Pluginversion nur wegen eines älteren Masters hoch-/herabstufen;
- keine Fach-/LIVE-Wahrheit hierher verlagern;
- keinen allgemeinen Modul-Kern als Pferde-spezifisch umklassifizieren;
- keine Secrets.
