# K10 – Arbeits-, Entscheidungs- und Fehlerhistorie bis 2026-10-02

**Rolle dieses Dokuments:** ausschließlich Historie/Nachweis.  
**Keine Current-Autorität. Keine NEXT-ACTION-Quelle.**  
Aktueller Stand steht ausschließlich in `CURRENT_STATE.json`.

## Ziel und Grundentscheidung

K10 wurde als strikt getrenntes Entwicklungsmodell neben dem funktionierenden K9 aufgebaut. K9 darf nicht verändert werden. Ziel ist ein zentraler Regelkatalog nach dem Prinzip:

**eine harte Regel → genau ein fachlicher Owner → genau eine inhaltliche Prüfung → genau ein hashgebundener Receipt.**

Nachgelagerte Stufen prüfen nur Vollständigkeit, Identität, Hash-Bindung und Unverändertheit; sie bewerten dieselbe redaktionelle Regel nicht erneut.

Der normale Produktionsendpunkt ist eine **verifizierte WordPress-Importdatei mit `publish_allowed=false`**. Ein echter WordPress-Write/Render gehört nicht zum normalen K10-Lauf.

## Dauerhafte fachliche Entscheidungen

- Tabelle:
  - `Vergleich`: Tabelle Pflicht.
  - `FAQ`, `Beratung`, `Pflege`: Tabelle optional.
  - Wenn Tabelle vorhanden: echter Informations-/Entscheidungsmehrwert erforderlich.
  - Bei optionaler Tabelle muss die Entscheidung ausdrücklich als `INCLUDE_ADDED_VALUE` oder `OMIT_NO_ADDED_VALUE` mit Begründung festgehalten werden.
- H2:
  - konkrete, abschnittsspezifische Sprache;
  - abstrakte Generatorformulierungen werden hart blockiert.
- Einstieg:
  - jeder Artikel beginnt mit einem kurzen natürlichen Orientierungssatz;
  - er erklärt sofort, worum es geht, was die Sache ist oder welchem Zweck sie dient;
  - keine starre Definitionsformel;
  - Ziel für die gesamte Einleitung: 60–80 Wörter; harter bestehender Maximalwert bleibt unverändert.
- Qualität:
  - keine Qualitätsabsenkung;
  - LT 6.8, PPM-6.7.9-Regelbestand, PSERC, ENDSTEMPEL und WordPress-Dateiverifikation bleiben erhalten;
  - `publish_allowed=false`.

## Architektur-/Implementierungsnachweise

- K10 eigener Branch: `konzept10-rule-ledger-20261001`.
- K9-Baseline nur read-only: `2cc8167fa1e31b4ffa2ff76c9819314be4b98555`.
- K10-Dateibaum ohne K9-Runtime, K9-Artikel, K9-Warehouse, K9-Final oder K9-Submissions.
- PPM 6.7.9 direkt aus dem hashgebundenen Paket inventarisiert.
- Exakte historische PPM-Summe reproduziert: **52 Content + 34 Struktur + 14 Known Error + 4 Render = 104 Regeln**.
- Die 104 PPM-Regeln wurden auf K10-Owner gemappt; alte starre Tabellenpflichten wurden ausschließlich durch die ausdrücklich genehmigte K10-Tabellenregel ersetzt.
- Hashgebundene Article-/System-/Package-Receipts implementiert.
- Artikelzustand bindet Titel, Keyword, Typ, Metadaten, Faktenbindung und HTML; relevante Änderung invalidiert alte Receipts.

## Fehler- und Reparaturprotokoll

### 1. K10-Trennung / Materialisierung

**Befund:** Direkte K10-Branch-/Dateineuanlage war anfangs durch den GitHub-Sicherheitsweg blockiert.  
**Folge:** Keine unsaubere Arbeit im K9-Branch. K9 wurde zunächst auf den sauberen Stand `2cc8167...` zurückgesetzt und danach nicht mehr verändert.  
**Lösung:** separater K10-Branch und eigener Dateibaum.  
**Belege:** K10-Root `c93bf55...`, Materialisierung `3ee2684...`, aktueller K9-Head blieb `2cc8167...`.

**Befund:** Isolation Guard schlug beim Bootstrap/Workflow auf Git-Metadaten bzw. notwendige read-only Referenzen an.  
**Lösung:** aktive K9-Arbeitsinhalte bleiben verboten; Git-Metadaten/read-only Baseline-Referenzen wurden aus der aktiven Mutationsprüfung herausgenommen.  
**Belege:** `245a3afd...`, `7222d0ea...`, `dadfe9e4...`.

### 2. PPM-104-Inventur

**Befund:** Erster Extraktor zählte rohe Validator-Aufrufstellen statt semantisch eindeutiger Regeln; Content-Validator ergab dadurch 63 statt der historischen 52.  
**Ursache:** dieselbe Regel kommt in mehreren Prüfpfaden vor.  
**Lösung:** Regelidentität = eindeutige Kombination aus Fehlercode + fehlgeschlagener Regel.  
**Beleg:** `acf2aa4f...`; danach exakte Kontrollsumme 52+34+14+4=104.

**Befund:** Regex für PPM-Konstanten war doppelt maskiert und konnte Originalwerte nicht extrahieren.  
**Lösung:** Regex korrigiert, Originalgrenzwerte aus dem echten gebundenen PPM-Paket übernommen.  
**Belege:** `f1f0f543...`, `0637401d...`.

### 3. Doppelte Prüfpfade

**Befund:** Während der K10-Zentralisierung entstanden zeitweise doppelte Prüfpfade/Receipts, u. a. durch zusätzliche PPM-Paritätsprüfung.  
**Lösung:** semantische Doppelprüfung entfernt; pro harter Regel exakt ein Owner und ein Receipt.  
**Nachweis:** Exact-Receipt-Tests in K10-Selftest; Artikel-/Package-Regeln werden auf eindeutige Receipts geprüft.

### 4. Erster Realartikel – Longiergurt

**Artikel:** „Wie lege ich einen Longiergurt an?“  
**Befund:** erste reale LT-Funde mussten sprachlich repariert werden.  
**Lösung:** Text repariert, LT 6.8 anschließend 0 Findings.  
**Beleg:** `ae8d3cb2...`.

**Befund:** Der Lauf wurde zeitweise unnötig bis zu echten WordPress-Renderhaken verfolgt.  
**Entscheidung:** Für den normalen Produktionsweg ist das falsch. Gewollter Endpunkt ist die verifizierte Importdatei; echter WordPress-Write/Render ist nicht nötig.  
**Lösung:** Pre-WordPress-Integrität und spätere Rendergates getrennt; normaler Lauf stoppt nach verifizierter Importdatei.  
**Belege:** `256e732c...`, `dcc2390f...`, `24a2d783...`, `6fe9adc7...`, `6a58e346...`.

### 5. Einleitung und Tabellenentscheidung

**Befund:** Erster Longiergurt-Artikel hatte formal zulässige, mobil aber recht lange Einleitung; außerdem war bei fehlender optionaler Tabelle nicht dokumentiert, ob das bewusst oder versehentlich geschah.  
**Entscheidung:** allgemeiner Orientierungssatz + 60–80-Wörter-Einleitungsziel; explizite Tabellenentscheidung.  
**Implementierung:** `8a390397...`, `b5a04004...`, `3f7c1cae...`, `ed650f04...`.

### 6. Unmöglicher 750-Wörter-Hardlock

**Befund:** K10 hatte alte „nicht mit Tabelle/Fazit künstlich auffüllen“-Flags beim Zentralisieren als zusätzliche harte 750-Wort-Sperre interpretiert. Für Beratung/Pflege/Vergleich war das zusammen mit Abschnittsmaxima rechnerisch teilweise unmöglich.  
**Ursache:** Ziel-/Guidance-Felder wurden zu Hardrules überhärtet; so hatte K9 sie nicht durchgesetzt.  
**Lösung:** echte Qualitätsgrenzen 750–900 Wörter, Abschnittsgrenzen, Fazitgrenzen blieben unverändert. Nur die Padding-Flags wurden zurück zu Writer-Zielen klassifiziert; `exempt_blocks` wurde korrekt dem Owner `words.section_range` zugeordnet.  
**Belege:** `6affa4be...`, `5321e9cf...`, `257c23b0...`, `f98520b4...`, `9e7d1c52...`, `84d31b28...`.

### 7. Dreierlauf – Runner-Abbruch

**Befund:** Der erste Dreier-Runner brach beim ersten LT-Block ab und protokollierte die übrigen zwei Artikel nicht.  
**Lösung:** Runner sammelt alle drei Befunde und stoppt erst nach vollständiger Protokollierung.  
**Beleg:** `a1091705...`.

### 8. Reitplatzplaner – Erstpass

**Befunde:**
- LT: „Glättelemente“ und eine missverständliche Formulierung;
- Fact-Trace in Tabellenzellen zu knapp;
- eine H2 zu abstrakt;
- später noch „zurückverteilt“ als LT-Fund.

**Lösungen:** sprachliche Reparatur, konkretere H2, Faktbindung/Tabellenformulierungen präzisiert.  
**Belege:** `96989eaf...`, `34ef52c6...`, `3a4b5317...`.

### 9. Regendecken – Erstpass

**Befunde:**
- unglückliche Link-Satzkonstruktion in LT;
- Orientierungssatz traf das Thema technisch nicht robust genug;
- abstrakte H2 mit „einordnen“;
- nach Reparatur 749 sichtbare Wörter, also 1 Wort unter dem harten Minimum.

**Lösungen:** Link-Satz neu formuliert, Einstieg klar auf „Regendecken“ bezogen, H2 konkretisiert, sicherer Abstand zur 750-Wort-Untergrenze geschaffen.  
**Belege:** `3485450e...`, `c5df173e...`, `2b915f57...`.

### 10. Schermaschinen – Erstpass

**Befunde:**
- mehrere legitime Fachwörter fehlten in der LT-Fachwortliste;
- „Wattzahl“ und eine Wiederholung wurden sprachlich verbessert;
- echte Quelle „CAVALLO – Schermaschinen im Test“ wurde vom Placeholder-Checker fälschlich als Testquelle blockiert.

**Lösung:** legitime Fachwörter ergänzt; Text verbessert; Placeholder-Prüfung so geändert, dass echte Quellentitel mit dem Wort „Test“ erlaubt bleiben, reine Platzhalter wie „Test“ weiterhin blockieren.  
**Belege:** `96bcfe56...`, `de61b993...`, Regressionstest `fd76e6dd...`.

**Folgefehler:** negativer Placeholder-Schutztest blieb zunächst grün statt zu blockieren, weil die Regex technisch doppelt maskiert war.  
**Lösung:** exaktes Regex-Escaping korrigiert.  
**Belege:** Fehlruns `36938448285`, `36938552197`; Fix `ed3b7269...`; anschließender K10-Selftest PASS.

## Finaler Dreiernachweis

Finaler grüner Dreierlauf:
- Workflow Run: `36938796049`
- getesteter Workload-Commit: `8fa26288c82b6a9d74db5096eb6403f93dbb274f`
- Ergebnis: SUCCESS
- alle drei Artikel:
  - Artikelregeln PASS
  - LanguageTool 6.8: 0 Findings
  - PSERC PASS
  - ENDSTEMPEL PASS
  - WordPress-Importdatei-Verifikation PASS
  - `publish_allowed=false`

Gemessene Maschinenstrecke **nach vorliegendem Artikelinput**:
- Reitplatzplaner: 12.991 s
- Regendecken: 9.271 s
- Schermaschinen: 11.929 s
- Summe: 34.191 s
- Mittel: 11.397 s/Artikel

Die Messung umfasst Category-Binding, LanguageTool 6.8 und K10-Prüf-/Finalisierungsstrecke bis zur verifizierten WordPress-Importdatei.

## Geschwindigkeitsvergleich K9/K10

Ein vollständig fairer End-to-End-Vergleich ist noch **nicht** belegt, weil die K10-Zeit oben mit bereits vorliegenden Artikelinputs beginnt, während der historische K9-Auto-Proof Recherche, Schreiben, mehrere Reparaturrunden und Finalisierung umfasst.

Belegbarer K9-Historienrahmen:
- K9 AUTO Research-Job gestartet: Commit `60e8784c...`, 2026-09-30 11:15:53Z.
- Artikel für AUTO-Proof isoliert: `ccc2eea4...`, 11:20:20Z.
- Terminale WordPress-Datei/STOP: `b16299c4...`, 11:37:52Z.

Damit:
- Research-Job → STOP: ca. **21 min 59 s**.
- isolierter Artikel → STOP: ca. **17 min 32 s**.

Diese Werte sind **nicht direkt** gegen die K10-11.397-s-Prüfstrecke zu rechnen. Sie zeigen aber, warum K10 für die reine Prüf-/Finalisierungsstrecke deutlich schlanker wirkt. Für eine belastbare Gesamtgeschwindigkeit muss K10 künftig Recherche/Schreiben ab einem klar definierten Startpunkt mitmessen.

## Abschluss-Nachweis nach Finalisierung

Nach dem final grünen Dreierlauf wurde `CURRENT_STATE.json` auf den geprüften Stand gezogen. Auf dessen Commit `062615af...` liefen erneut:
- K10 isolated selftest: Run `36975267798` → SUCCESS.
- K10 PPM 6.7.9 inventory: Run `36975267711` → SUCCESS.

K9 blieb auf `2cc8167fa1e31b4ffa2ff76c9819314be4b98555` unverändert.

## Nicht betroffen

- Hobbyraum: nicht verwendet.
- Paul/Worker/Parallelbranch außerhalb des getrennten K10-Branches: nicht betroffen.
- Pluginentwicklung: nicht betroffen.
