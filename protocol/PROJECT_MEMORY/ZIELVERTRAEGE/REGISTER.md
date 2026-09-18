# ZIELVERTRAGSREGISTER

STAND: 2026-09-16

## Pflichtfelder

- ZV-ID
- TITEL
- GELTUNGSBEREICH
- STATUS: ENTWURF / AKTIV / ERFÜLLT / ABGELÖST
- FASSUNG
- HAUPTQUELLE
- VERANTWORTLICHER BEREICH
- PASS-BEDINGUNG
- NACHFOLGER, falls abgelöst

## Regel

Bei neuer Facharbeit prüft der zuständige Bereich, ob ein aktiver Zielvertrag existiert.

Bei:
- Projektstart
- größerem Umbau
- Modulfreigabe
- komplexer Reparatur mit festem Endzustand

soll ein Zielvertrag angelegt oder referenziert werden.

## Noch aufzunehmende bestehende Verträge

Bereits vorhandene historische Zielverträge aus Repository/Masterakten werden bei der Archiv-/Masterdatei-Aufnahme hier eingeordnet.

Nichts aus alten Zielverträgen still ersetzen.


## ZV-MOD-001 – Allgemeingültiger Kategorie-Master 016

TITEL:
ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK

GELTUNGSBEREICH:
MOD-001 KATEGORIENMODELL

STATUS:
AKTIV

FASSUNG:
R10/R9 Runtime Deployment / Plugin V1.8.0

HAUPTQUELLE:
R10-Master:
`00_STEUERUNG/STEUERDATEI.md`
und aktiver Lock:
`15_WORKFLOW_HARDLOCK/MASTER_LOCK.json`

VERANTWORTLICHER BEREICH:
`ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`

PASS-BEDINGUNG:
maßgeblich sind die im Master gebundenen 14 Stufen, Hardlocks, Research-/Coverage-/Affiliate-Gates und Post-FINAL-Deploymentbedingungen.

BELEGSTATUS:
lokal/fresh R10 stark PASS; echter Live-WordPress-Deploymentlauf noch offen.


## ZV-MOD-003 – Designvertrag V104

TITEL:
DESIGNVERTRAG ALLGEMEIN V104

GELTUNGSBEREICH:
MOD-003 Universal Portal Design Suite

STATUS:
AKTIV

FASSUNG:
V104 / Universal Plugin 2.2.40

HAUPTQUELLE:
Universal Master V2.2.40/V104 und GitHub Design-Baseline V104.

PASS-BEDINGUNG:
gebundene V104-Design-/QA-Regeln; keine stillen projektspezifischen Übernahmen.

PFERDE-ANWENDUNG:
Dieses Register führt **keinen dynamischen LIVE-Stand**. Der historisch belegte Referenz-LIVE-PASS 1.50.472 / V104 bleibt Beleg; den aktuellen belastbaren Projektstand ausschließlich aus `PROJEKTE/PFERDE_ATELIER/DESIGN/CURRENT_STATE.md` lesen.


## ZV-TEXT-001 – STARTMASTER0107 aktueller Produktionszielvertrag

TITEL:
STARTMASTER0107 – VERBINDLICHER ZIELVERTRAG – 05.09.2026

GELTUNGSBEREICH:
PFERDE_ATELIER / TEXT / STARTMASTER0107

STATUS:
AKTIV

FASSUNG:
05.09.2026

HAUPTQUELLE:
`PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/03_ZIELVERTRAG_AKTUELL_20260905.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/PFERDE_ATELIER/TEXT/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Wortgleich aus der Hauptquelle lesen.

NACHFOLGER:
keiner belegt.

ERGÄNZENDE TECHNISCHE SYSTEM-4-BINDUNG:
`isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`

ROLLE:
Dieser System-4-Vertrag präzisiert den technischen Maschinenweg des unveränderten STARTMASTER0107-Produktionsziels. Er ersetzt nicht das fachliche Endziel, sondern bindet dessen aktuelle technische Ausführung bis zur bytegleichen finalen Parent-Chat-Datei.


## ZV-AFFILIATE-OTTO-001 – OTTO/Awin vollautomatische Produkt- und Bannerintegration

TITEL:
OTTO/AWIN – AUTOMATISCHE PRODUKT-, BANNER- UND EXACT-PRODUCT-INTEGRATION

GELTUNGSBEREICH:
PFERDE_ATELIER / AFFILIATE / OTTO über Awin

STATUS:
AKTIV

FASSUNG:
2026-09-07

HAUPTQUELLE:
Branch `affiliate-release-current` →
`protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/PFERDE_ATELIER/AFFILIATE/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Vollständig aus der Hauptquelle und der gebundenen Release-Governance lesen.

AKTUELLER ARBEITSSTATUS:
Durch explizite Nutzerentscheidung vom 11.09.2026 pausiert zugunsten des ADCELL-Auftrags. Nicht erfüllt, nicht abgelöst, kein PASS.

NACHFOLGER:
keiner belegt.


## ZV-AFFILIATE-ADCELL-001 – ADCELL vollautomatische API-v2-Integration

TITEL:
ADCELL – AUTOMATISCHE PROGRAMM-, PRODUKT-, BANNER- UND DEEPLINK-INTEGRATION ÜBER API V2

GELTUNGSBEREICH:
PFERDE_ATELIER / AFFILIATE / ADCELL

STATUS:
AKTIV

FASSUNG:
2026-09-11

HAUPTQUELLE:
Branch `affiliate-release-current` →
`protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/PFERDE_ATELIER/AFFILIATE/`

PASS-BEDINGUNG:
- exakter ADCELL-API-v2-Authentifizierungsvertrag autoritativ belegt;
- provider-spezifisches ADCELL-Routing ohne Awin-Fallthrough;
- accepted+active Programme nur über explizite `programId`-Allowlist, fail-closed;
- CSV/Banner/Deeplink automatisch über dokumentierte API-v2-Wege;
- kein manueller Import/Export bzw. keine manuelle CSV-URL als Normalbetriebs-Voraussetzung;
- kanonischer Positiv-/Negativ-/Gesamtworkflow-/Fresh-Unpack-/Source-ZIP-Identity-PASS;
- echter ADCELL-Live-API- und WordPress/MariaDB-End-to-End-PASS;
- alte/fachfremde accepted Partnerschaften ohne Freigabe bleiben gesperrt.

NACHFOLGER:
keiner belegt.


## ZV-TRESOR-001 – GitHub-Komplettsicherung

TITEL:
REGELMÄSSIGE GITHUB-KOMPLETTSICHERUNG

GELTUNGSBEREICH:
`hallo-netizen/affiliate-pferdeportal` / GITHUB

STATUS:
AKTIV

FASSUNG:
2026-09-08 – UNABHÄNGIGER TRESOR + LOKALES BACKUP

HAUPTQUELLE:
`protocol/PROJECT_MEMORY/TRESOR/KONZEPT.md`

ERGÄNZENDE VERBINDLICHE QUELLEN:
- `protocol/PROJECT_MEMORY/TRESOR/INHALTSVERTRAG.md`
- `protocol/PROJECT_MEMORY/TRESOR/PRUEFVERTRAG.md`
- `protocol/PROJECT_MEMORY/TRESOR/STATUS.md`

VERANTWORTLICHER BEREICH:
`protocol/PROJECT_MEMORY/TRESOR/`

PASS-BEDINGUNG:
Git-/Ref-/Campus-Wiederherstellung real geprüft; automatische externe Tresorsicherung real geprüft; lokaler Backupstand real unabhängig geprüft; Providergrenzen ausdrücklich ausgewiesen.

`GITHUB_KOMPLETT_PASS` erfordert zusätzlich einen realen end-to-end Neuaufbau der erforderlichen exportierbaren GitHub-Metadaten/Einstellungen in einem leeren Zielsystem und ist derzeit nicht belegt.

SICHERUNGSWEGE:
1. Tresor automatisch, wöchentlich und extern unter `/Campus-Tresor/`.
2. Lokales Backup manuell per `GITHUB_BACKUP_STARTEN.command` auf dem Nutzer-Mac.

Beide Wege sichern denselben GitHub-Projektbestand, sind aber unabhängig voneinander.

NICHT IM SCOPE:
WordPress / Website / Projektarchiv.

NACHFOLGER:
keiner belegt.


## ZV-PFERDERASSEN-REL-001 – Pferderassen-Relationen

TITEL:
PFERDERASSEN – GETRENNTE SEMANTIK VON RASSENGRUPPE UND ÄHNLICHEN RASSEN

GELTUNGSBEREICH:
PFERDE_ATELIER / WISSENSDATENBANK / PFERDERASSEN / WORDPRESS

STATUS:
AKTIV

FASSUNG:
1.0 / 2026-09-15

HAUPTQUELLE:
`PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/ZIELVERTRAG_RELATIONEN.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Vollständig aus der Hauptquelle lesen. Den dynamischen Fach-/LIVE-Status ausschließlich aus der zuständigen WISSENSDATENBANK-/Fachquelle lesen.

NACHFOLGER:
keiner belegt.


## ZV-DESIGN-20260915-001 – Pferde Design Pagination/Glossar/Linkhover Reparatur

TITEL:
PFERDE ATELIER DESIGN – FUNKTIONIERENDE ROUTEN + PAGINATION 16 + GLOSSAR-ZIEL + LINKHOVER

GELTUNGSBEREICH:
PFERDE_ATELIER / DESIGN + MOD-003-INTERAKTION

STATUS:
AKTIV

FASSUNG:
1.0 / 2026-09-15

HAUPTQUELLE:
`PROJEKTE/PFERDE_ATELIER/DESIGN/ZIELVERTRAG_DESIGN_20260915.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/PFERDE_ATELIER/DESIGN/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Vollständig aus der Hauptquelle lesen; insbesondere exakte installierte Plugin-Kombination, Positiv-/Negativ-/Kombinationsprüfung und realer WordPress-Readback.

NACHFOLGER:
keiner belegt.


## ZV-BILD-20260916-001 – Bildzentrale Custom-Post-Type-Hero / Pferderassen

TITEL:
BILDZENTRALE – GENERISCHER CUSTOM-POST-TYPE-HERO / PFERDERASSEN

GELTUNGSBEREICH:
MOD-002 BILDZENTRALE + PFERDE_ATELIER / BILD / `pa_breed`

STATUS:
AKTIV

FASSUNG:
1.0 / 2026-09-16

HAUPTQUELLE:
`PROJEKTE/PFERDE_ATELIER/BILD/ZIELVERTRAG_BILDZENTRALE_PFERDERASSEN_HERO_20260916.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/PFERDE_ATELIER/BILD/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Vollständig aus der Hauptquelle lesen. Den aktuellen technischen/LIVE-Stand ausschließlich aus `PROJEKTE/PFERDE_ATELIER/BILD/CURRENT_STATE.md` lesen.

NACHFOLGER:
keiner belegt.
