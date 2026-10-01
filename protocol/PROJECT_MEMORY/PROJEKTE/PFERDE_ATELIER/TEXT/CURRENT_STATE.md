# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-10-01
STATUS: PORTALABGLEICH COMPLETE / VORHANDENES THEMENPOTENZIAL WIRD ZU SCHWACH VERWERTET / LAUFENDE RECHERCHEWELLE NICHT UNTERBRECHEN

## AKTUELLER OPERATIVER TEXT-/SEO-STAND 2026-10-01

Diese Sektion supersediert für aktuelle TEXT-/SEO-Arbeit die historischen Produktions-/Kategorieblöcke weiter unten.

### Eine zuständige Current-Bindung je Arbeitsbereich

- **Artikelproduktion K9:** technische Current-Autorität ausschließlich
  `konzept9/greenfield-20260929:CURRENT_STATE.json`.
  Das Campus-TEXT-Büro kopiert daraus keinen dynamischen Produktionsstatus.
- **PSTE-Themen-/SEO-Bestand:** diese Datei ist die aktuelle Campus-Fachautorität; reale WordPress/PSTE-Readbacks bleiben operative Evidenz.
- **Pluginbestand/Versionen:** ausschließlich über `../PLUGINS/CURRENT_STATE.md` und die jeweilige technische Hauptquelle.

### Belastbarer aktueller PSTE-/PSERC-Readback

Der zuvor offene Portalabgleich ist abgeschlossen.

Letzter belegter Produktionsvorlauf:
- PSERC-Lauf: `COMPLETE`;
- Themen: 23;
- geeignet: 23;
- geprüft: 23;
- READY: 2;
- Snapshot danach aktualisiert;
- kompakter 5-Felder-Handoff mit 2 Artikeln erzeugt;
- diese 2 Artikel wurden anschließend in K9 vollständig bis STOP produziert.

Der Nutzer meldet danach am 01.10.2026 eine **neue bereits laufende Recherchewelle mit sehr magerer Ausbeute**.
Für diese laufende Welle liegt in der Campusquelle noch kein terminaler Zahlen-/Reason-Code-Readback vor.
Deshalb keine Ausfallursache raten.

### Frisch belegte vorhandene Automatik

Die automatische redaktionelle Aufbereitung ist bereits vorhanden und darf nicht neu erfunden werden.

Der bestehende PSTE-Normal-Metadata-Pfad kann vorhandene einzelne Keywords/Suchfragen sowie Familien-/Gruppenkontext – soweit eindeutig belegbar – automatisch auflösen in:
- Familie/Gruppe;
- Artikeltyp;
- guten redaktionellen Titel;
- Zielkeyword;
- Zielkategorie.

Der Retained-Backlog-Weg führt gespeicherte `topic_pool`-Zeilen bereits **ohne Provider-Aufruf** erneut durch diesen Normalpfad und danach durch Planning-Readiness.

Detaillierter Nachweis/Fehlerprotokoll:
`protocol/PSTE_EXISTING_POTENTIAL_CONVERSION_GAP_20261001.md`.

### Erster offener Blocker

`PSTE_EXISTING_POTENTIAL_LOW_CONVERSION_NOT_LOCALIZED`

Bedeutung:
Nicht die Titel-/Kategorie-Automatik fehlt.
Der offene Fehler ist, dass **zu wenige bereits gespeicherte Kandidaten durch den vorhandenen Aufbereitungsweg bis AUTO_RESOLVED / planning-ready / READY gelangen**.

Noch nicht belastbar bestimmt ist, an welcher Stufe die größte Menge ausfällt:
Portalrelevanz, Familie, Intent/Artikeltyp, Titel, Kategorie/STRUCTURE_GAP, Planning-Readiness, Kontext oder Reentry.

### Genau eine NEXT ACTION

`AFTER_CURRENT_RESEARCH_WAVE_COMPLETE_RUN_READ_ONLY_EXISTING_POTENTIAL_CONVERSION_FUNNEL_AUDIT`

Verbindlicher Arbeitsweg:
1. die bereits laufende Recherchewelle nicht abbrechen oder durch einen neuen Lauf ersetzen;
2. nach ihrem terminalen Readback **keine weitere Provider-Recherche starten**;
3. vorhandenen Bestand read-only als Funnel auswerten:
   `GESPEICHERT → SOURCE QUERY → PORTALRELEVANZ → FAMILIE → ARTIKELTYP → TITEL/ZIELKEYWORD → KATEGORIE → PLANNING-READINESS → CONTEXT CURRENT → READY`;
4. je Verluststufe Anzahl + führende Reason-Codes bestimmen;
5. besonders Lane B aus `ZV-PSTE-THEMENVERWERTUNG-001` herausarbeiten:
   Evidenz vorhanden, nur bestehende Titel-/Familien-/Kategorie-/Reentry-Automatik muss greifen;
6. erst danach den kleinsten belegten Fix umsetzen.

### 0.57.18-Kandidat

Der lokal geprüfte Kandidat `PSTE 0.57.18 – EXISTING POTENTIAL FIRST` ist **nur ein Teilfix**:
sichere `AUTO_REENTRY_ELIGIBLE`-Sandbox-Kandidaten werden vor Retained-Backlog und vor Provider-Recherche durch den bestehenden Normal-Reentry geführt.

Er ist **nicht** als Lösung für die niedrige Gesamtverwertbarkeit des gespeicherten Topic-Pools abgenommen.
Die laufende Recherchewelle wird nicht für diesen Kandidaten unterbrochen.

### Harte Grenzen

- kein pauschales Freigeben gespeicherter Themen;
- keine neue Themen-Datenbank;
- keine neue Titel-/Kategorie-Architektur;
- bestehende Normal-Metadata-/Title-/Family-/Reentry-Wege verwenden;
- Dubletten-, Kannibalisierungs-, Kategorie-, Artikeltyp-, Titel-, Plan-Slot-, PSTE-/PSERC- und Publish-Regeln unverändert;
- `PENDING_EXTERNAL_RELEVANCE`, echte `STRUCTURE_GAP`, Dubletten und Nicht-Redaktionelles nicht künstlich produzieren;
- kein Publish.

STAND: 2026-09-24
STATUS: KATEGORIE-SCOPE CLOSED / ÄLTERE PRODUKTIONSHISTORIE UNTEN NICHT ALS AKTUELLE KATEGORIE-NEXT-ACTION

## PLUGIN-PFLEGE-DELTA 2026-09-30

Portal SEO Themenengine ist real in WordPress als **0.57.13 aktiv** bestätigt.

`PLUGIN_UPDATE_REF: PU-20260930-002`

Dieses Storage-/Performanceupdate ändert keine Kategorie-, Recherche-, Qualitäts- oder Produktionsregel und öffnet den geschlossenen Kategorie-Scope nicht erneut. Die unten genannte 0.57.12 bleibt ausdrücklich die historische Kategorie-Closeout-Baseline vom 24.09.; der aktuelle reale Pluginstand wird ausschließlich im PLUGINS-Büro geführt.

## KATEGORIE-/PLUGIN-STATUSDELTA 2026-09-24

Der frühere Produktionsblocker unten bleibt historische Text-/Produktionslage, ist aber **nicht** der aktuelle Status der abgeschlossenen Kategorieintegration.

Für Kategorie/Struktur sind aktuell gebunden:
- Portal Link Policy Runtime Verifier **1.0.0** – kein statisches Vollkopie-Delta erforderlich
- Portal Production Center **1.1.1** – **1149 / 9 / 5790**, Build-Integrity PASS
- Portal Production Link Policy Gate **1.0.1** – dynamischer/source-getriebener Kategoriepfad
- Portal Production Machine **6.7.9** – **25/25 neue Kategorien + 125/125 neue Slots PASS**
- Portal SEO Redaktionsplan Compiler **0.28.23** – vollständiger **1149-Lauf PASS**
- Portal SEO Themenengine **0.57.12 (Kategorie-Closeout-Baseline 24.09.)** – **LIVE_READBACK_PASS_CLOSED**, `pferde putztasche` = Recherchekeyword, Kontext PENDING, Originalbegriff erhalten

Finale Kategorie-Nachweise:
- Run `36005442270` = SUCCESS
- Run `36005442188` = SUCCESS

Kategorie-/Strukturscope: **CLOSED**. Kein PSERC-, Linkregistry-, E2E- oder Kategorie-Preflight erneut starten ohne neue harte Defektevidenz.

## EINE AKTUELLE WAHRHEIT

Current technical main:
`f1d1605f18bd23d9189f89ad173598958718d08a`

Letzter belastbarer Live-/Recovery-Baseline-Stand vor M37:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Aktuelle autoritative Fehlerquelle:
`QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md`

## M37 – ABGESCHLOSSEN UND INTEGRIERT

History-Phase:
- PR248;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS.

Produktfix:
- PR247;
- Kandidat `59ad44da3d89769c05f0725f9929135b0262f4dd`;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS;
- neuer Main `f1d1605f18bd23d9189f89ad173598958718d08a`.

M01–M37 sind damit die integrierte bekannte Regression.

## AKTUELLER REALBLOCKER

Der letzte frische Lauf vor M37 erreichte realen PPM/PSERC und endete äußerlich bei:
`PPM679_REAL_EXECUTION_BLOCKED`.

Der damalige innere Grund ist nicht mehr rekonstruierbar.
**Produktions-Rootcause bleibt UNKNOWN.**

## HISTORISCHE PRODUKTIONS-NEXT-ACTION AUS STAND 2026-09-11

Die folgende Anweisung gehört zum damaligen Produktionsdiagnose-Stand und ist **keine aktuelle Kategorie-NEXT-ACTION**. Kategorie/Struktur ist geschlossen.

Damals vorgesehen: genau einen frischen ersten Artikel über den offiziellen damaligen 107007-Weg bis zum realen LanguageTool-/PPM-/PSERC-Handoff ausführen.

Bei erstem BLOCKED/REPAIR_REQUIRED:
- exakt stoppen;
- nur den ersten konkreten neuen Grund übernehmen;
- keine Reparatur im laufenden Test.

Bei Ein-Artikel-PASS:
- erst danach Restbatch fortsetzen.

## HARTE GRENZEN

- kein neuer Runner/Gate/Controller/Sidecar;
- keine Regeländerung;
- kein Rootcause raten;
- kein zweiter Artikel vor Auswertung des ersten;
- kein 7/7-Diagnoselauf vor Ein-Artikel-Beweis;
- kein WordPress-Write;
- Kein Publish.
