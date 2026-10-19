# ZIELVERTRAGSREGISTER

STAND: 2026-10-18

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


## ZV-TEXT-001 – STARTMASTER0107 historischer Produktionszielvertrag

TITEL:
STARTMASTER0107 – VERBINDLICHER ZIELVERTRAG – 05.09.2026

GELTUNGSBEREICH:
PFERDE_ATELIER / TEXT / LEGACY K1–K9

STATUS:
ABGELÖST

FASSUNG:
05.09.2026

HAUPTQUELLE:
Archiv-Branch `archive/pferdeatelier-textoffice-k1-k9-20261016`.

VERANTWORTLICHER BEREICH:
PFERDE_ATELIER / TEXT / ARCHIV

NACHFOLGER:
`ZV-TEXT-K0-001`

## ZV-TEXT-K0-001 – K0 aktuelle Produktionsbasis

TITEL:
K0 – PORTALNEUTRALE PRODUKTIONSBASIS

GELTUNGSBEREICH:
PFERDE_ATELIER / TEXT / K0

STATUS:
AKTIV

FASSUNG:
K0_PORTAL_NEUTRAL_GOAL_V1

HAUPTQUELLE:
Branch `konzept0-portal-neutral-20261002` → `K0_GOAL_CONTRACT.json`.

CURRENT:
Branch `konzept0-portal-neutral-20261002` → `K0_CURRENT_STATE.json`.

PASS-BEDINGUNG:
Ausschließlich aus dem K0-Zielvertrag und der K0-Current lesen; keine Legacy-Regel als zweite Wahrheit.

NACHFOLGER:
keiner.

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


## ZV-HOBBYRAUSCH-HD001-001 – Integrierte Hobby-Architektur bis Frontend

TITEL:
HOBBYRAUSCH HD-001 – INTEGRIERTE HOBBY-ARCHITEKTUR BIS FRONTEND

GELTUNGSBEREICH:
HOBBYRAUSCH / SEO_KATEGORIEN / HD-001

STATUS:
AKTIV

FASSUNG:
2.8 / 2026-10-17

HAUPTQUELLE:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Vollständig und ausschließlich aus der Hauptquelle Fassung 2.8 lesen. Aktuellen Arbeits-/LIVE-Status ausschließlich aus der zuständigen `SEO_KATEGORIEN/CURRENT_STATE.md` lesen.

NACHFOLGER:
keiner belegt.





## ZV-HOBBYRAUSCH-DESIGN-001 – Hobby Depot Portaldesign

TITEL:
HOBBY DEPOT – PORTALDESIGN / STARTSEITE / RESPONSIVE / AFFILIATE-INTEGRATION

GELTUNGSBEREICH:
HOBBYRAUSCH / DESIGN

STATUS:
AKTIV

FASSUNG:
5.4 / 2026-10-19

HAUPTQUELLE:
`PROJEKTE/HOBBYRAUSCH/DESIGN/ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`

VERANTWORTLICHER BEREICH:
`PROJEKTE/HOBBYRAUSCH/DESIGN/`

PASS-BEDINGUNG:
Nicht hier dupliziert. Vollständig aus der Hauptquelle lesen. Aktuellen Arbeits-/LIVE-Status ausschließlich aus `PROJEKTE/HOBBYRAUSCH/DESIGN/CURRENT_STATE.md` lesen.

NACHFOLGER:
keiner belegt.


## ZV-HB-KONZEPT-R3-001 – Hab & Bewahr Kategorien 3–10

TITEL: Hab & Bewahr – fachlich unterscheidbare Kategorieebenen

GELTUNGSBEREICH: EIGENTUMSSCHUTZ / KONZEPT / CORE und angrenzende Portalsäulen

STATUS: ABGELÖST

FASSUNG: 1.0 / 2026-10-13

HAUPTQUELLE: `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/ZIELVERTRAG_KATEGORIEN_3_BIS_10_20261013.md`

VERANTWORTLICHER BEREICH: `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/`

PASS-BEDINGUNGEN: Historischer Stand. Nicht für aktuelle Kategorieentscheidungen oder Freigaben verwenden.

AKTUELLER STATUS UND GENAU EINE NEXT ACTION: ausschließlich per `AUTORITAETSPLAN.json` aus `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/CURRENT_STATE.md`, **nicht** aus diesem Register.



## ZV-HB-KONZEPT-C22 – Hab & Bewahr Kategorieaufbau C2.2

TITEL: Hab & Bewahr – konkrete Themenseite und vertiefende Artikelkategorien

GELTUNGSBEREICH: EIGENTUMSSCHUTZ / KONZEPT / CORE

STATUS: AKTIV

FASSUNG: C2.2 / 2026-10-16

HAUPTQUELLE: `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md`

VERANTWORTLICHER BEREICH: `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/`

PASS-BEDINGUNGEN: Drei Seitenebenen, Seite 3 konkretes Produkt/Sachthema; darunter nur dazu passende flache Artikel-/Intentkategorien mit mindestens drei plausiblen späteren Beiträgen je Kategorie. Mindestens drei fachlich sinnvolle direkte Unterkategorien ohne Obergrenze. Keine starre FAQ/Beratung/Vergleich-Schablone, kein Artikeltitel-Zwang, Bestandsschutz und ausschließlich kontrollierte WordPress-Änderung über das zentrale Kategorienbüro. Megamenü-Vorschau begrenzt nur die Anzeige auf drei Direktlinks je Gruppe und lässt weitere über den Bereichshub erreichbar.

AKTUELLER STATUS UND GENAU EINE NEXT ACTION: ausschließlich `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/CURRENT_STATE.md`.
