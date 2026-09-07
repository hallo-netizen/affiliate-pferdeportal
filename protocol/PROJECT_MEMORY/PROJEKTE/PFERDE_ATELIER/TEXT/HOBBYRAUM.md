# TEXT – HOBBYRAUM

STAND: 2026-09-06
STATUS: AKTIV / B01-ONLY #141 HARDLOCK PASS / #140 M01–M33 REGRESSION PASS / LIVE-PROOF OFFEN

## VERBINDLICHER ARBEITSPLAN – EINZIGE REIHENFOLGE

**Dieser Ablauf ist zwingend. Keine neue spontane NEXT-ACTION-Regel. Kein Seitensprung. Kein Minifix außerhalb dieses Plans.**

### A – Ausgangspunkt festhalten
- aktuelles `main`;
- erster echter Liveblocker;
- letzter echter funktionierender 7/7-Stand;
- keine Produktion ändern.

### B – Pflichtprüfung VOR jedem Kandidaten
1. Paul-Prüfung gelesen und relevanten Befund zugeordnet?
2. gesamte bisherige Fehlerhistorie B01–B15 / M01–M33 geprüft?
3. letzten funktionierenden Stand `d841ed…` / `de21f6…` verglichen?
4. unmittelbare Vor- und Nachstufe mit exaktem Artefaktzustand geprüft?
5. geprüft, ob derselbe Fehlertyp bereits früher vorkam?
6. lokalen Positiv- und Negativtest definiert und ausgeführt?
7. Qualität / Inhalt / Design / Sicherheit / Single Door / dumme Wächter / Chat-Zwangsjacke unverändert?

Ein `FAIL`, `UNKLAR` oder `NICHT BELEGT` = `FIX_FORBIDDEN`.

### C – Anti-Minifix-Regel
Wenn derselbe technische Fehlertyp bereits mehrfach aufgetreten ist:
- **kein weiterer isolierter Minifix**;
- zuerst die gemeinsame Ursache im direkten technischen Korridor bestimmen;
- daraus genau **einen konsolidierten KISS-Kandidaten** ableiten.

### D – Kandidat
Der Kandidat darf ausschließlich:
- bestehende technische Bindungen wieder korrekt verbinden;
- keine Fachregel neu definieren;
- keine Qualitäts-/Design-/SEO-/Link-/Tabellenregel verändern;
- keine neue Tür, keinen neuen Wächter, keinen neuen Runner/Workflow/Executor erzeugen;
- dem Chat keinerlei neue Freiheit geben.

### E – lokale Freigabe
Vor Codex:
- Positivtest: unveränderter Sollweg PASS;
- Negativtest: fehlende/falsche reale Evidence BLOCK;
- Vor-/Nachstufe bleiben kompatibel;
- historische Fehler werden nicht wieder geöffnet;
- Paul-Befunde werden nicht verletzt.

Nur dann: `FIX_ALLOWED_FOR_CODEX_TEST`.

### F – Codex-Test
- exakt aktuelles `main`;
- exakt bestehende eine Tür;
- exakt dumme Wächter;
- Chat ohne eigene Workflow-/Prüf-/Repairentscheidung;
- beim ersten echten technischen Blocker STOP;
- keine Reparatur im laufenden Test;
- Ergebnis zurück in **denselben Plan ab Punkt B**.

### Aktueller Arbeitsstand
- aktuelles main: `f14ccf187b94c4beab9a86d0c69144f792ba2f64`;
- erster echter Liveblocker: `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`;
- LanguageTool-Einzelbranch bleibt PARKPLATZ / NICHT INTEGRIEREN;
- wegen wiederholter K1/K3-Bindungsfehler ist C aktiv: **kein LT-Minifix**;
- nächster zulässiger Schritt: aus den bereits gewonnenen Paul-/Historien-/7/7-Befunden genau **einen konsolidierten KISS-Bindungskandidaten** ableiten und danach E ausführen.


## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros TEXT.

**HIER BIST DU RICHTIG, WENN …**  
du den aktuell gebundenen TEXT/SEO-Arbeitsbereich, Branch und nächsten Schritt sehen musst.

**DU DARFST …**  
den aktuellen Auftrag und alle autoritativen Quellen lesen und ausschließlich im gebundenen Hobbyraum-Branch prüfen/reparieren.

**DU DARFST NICHT …**  
main verändern, zu Paul wechseln, Paul-Dateien/-Branch benutzen, einen neuen Workflow/Runner/Gate/Executor bauen oder Fach-/SEO-/Textmaschinenregeln verändern.

**ALS NÄCHSTES …**  
Ausschließlich den Abschnitt **VERBINDLICHER ARBEITSPLAN – EINZIGE REIHENFOLGE** von A bis F abarbeiten. Keine andere NEXT-ACTION-Anweisung hat Vorrang.

## HARD RULE – FIX-SPERRE VOR JEDER ÄNDERUNG

**Ab sofort darf im TEXT-Hobbyraum kein technischer Fix begonnen, gebaut oder vorbereitet werden, bevor diese Prüfung vollständig mit PASS abgeschlossen ist.**

Pflichtprüfung vor **jedem** Fix:

1. **Paul-Prüfung gelesen?**
   - relevante Paul-Befunde für genau den betroffenen technischen Korridor geprüft;
   - insbesondere F2/A6/A12, F7/A7, A11, A37 sowie retracted F8 als Warnung vor vorschnellem Entfernen.

2. **Gesamte bisherige Fehlerhistorie geprüft?**
   - autoritative Fehlerquelle über `FEHLERREGISTER.md`;
   - B01–B15 und M01–M33 gegen den Kandidaten halten;
   - prüfen, ob der geplante Fix einen früheren Fehler wieder öffnen kann.

3. **Letzten funktionierenden Stand verglichen?**
   - `d841ed…` und besonders `de21f6…`;
   - nicht blind zurückbauen;
   - exakt feststellen, was an der betroffenen Stelle damals anders/gleich war.

4. **Unmittelbare Vor- und Nachstufe geprüft?**
   - exaktes Eingangsartefakt;
   - exakter Artefaktzustand;
   - exakter Output/Evidence;
   - exakter nächster Consumer;
   - prüfen, ob nach dem Fix exakt dasselbe validierte Artefakt weitergegeben wird.

5. **Ist es derselbe Fehler-Typ wie früher?**
   - K1: Ausführung/Abhängigkeit verlangt, aber nicht eindeutig gebunden;
   - K2: Upstream/Downstream verlangen inkompatible Zustände;
   - K3: PASS/Hash bindet nicht die reale Prüfung bzw. den richtigen Artefaktzustand;
   - K4: Test beweist nicht denselben realen Pfad.
   - Wenn derselbe Typ bereits wiederholt auftritt: **kein weiterer Minifix**; gemeinsame Ursache bearbeiten.

6. **Positiv + Negativ lokal geprüft?**
   - Positivfall muss den unveränderten Sollweg bestehen;
   - Negativfall muss exakt fail-closed blockieren;
   - kein Test darf nur Dateipräsenz oder behaupteten PASS prüfen, wenn reale Ausführung gefordert ist.

7. **Qualität/Inhalt/Design/Sicherheit unverändert?**
   - Qualität unverändert;
   - Inhalt/Fachlogik unverändert;
   - Design unverändert;
   - Single Door unverändert;
   - dummer Wächter unverändert;
   - Chat-Zwangsjacke unverändert;
   - Publish-Sperre unverändert;
   - PPM/PSERC/PSTE/LanguageTool/SEO/Tabellen/Links/Dubletten-/Kannibalisierungsschutz nicht abgeschwächt.

### Entscheidung

Nur wenn **1–7 = PASS**:
`FIX_ALLOWED`

Sobald ein Punkt **FAIL / UNKLAR / NICHT BELEGT**:
`FIX_FORBIDDEN`

Dann ausschließlich weiter analysieren. **Keine Codeänderung.**

### Anti-Minifix-Regel

Wenn zwei oder mehr Fehler derselben technischen Fehlerklasse auftreten:
- keine weitere Einzelreparatur;
- zuerst gemeinsame Ursache im kompletten direkten Korridor prüfen;
- erst danach ein konsolidierter KISS-Kandidat.

### Aktueller Status

Der begonnene Branch
`hobbyroom/languagetool-runtime-rebind-20260907`
bleibt **PARKPLATZ / NICHT INTEGRIEREN**, bis diese 7-Punkte-Prüfung für den gesamten betroffenen Korridor abgeschlossen ist.


## ARBEITSKONTROLLPUNKT – NUR DIE AKTUELLE ARBEIT

- **BÜROSTAND:** `CURRENT_STATE.md`
- **AKTUELLER AUFTRAG / NEXT ACTION:** ausschließlich diese `HOBBYRAUM.md`
- **CURRENT_BLOCKER:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Quelle
- **AKTIVER ZIELVERTRAG:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- **NICHT ANFASSEN / WARUM:** Ziel-/Originalquelle + `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

## Aktuelle Arbeitsbindung

Aktiver Arbeiter:
**normaler TEXT-Arbeitschat**

**Paul ist für diesen Auftrag tabu und nicht gebunden.**

Bevorzugter KISS-Testkandidat:
`hobbyroom/b01-only-kiss-20260906`

Draft-PR:
`#141`

Aktueller KISS-Head:
`94917596adce04765380c60dd7ade0fb23793393`

Breiterer Prüfstand bleibt erhalten, aber ist **nicht** bevorzugter Integrationskandidat:
PR #140 / `hobbyroom/b01-semantic-category-seed` / Head `3ed31aa78978a2098f324eead6f2a5335a10e2d4` = B01 + B15 + Testanpassungen.

main bleibt unverändert:
`c8a96e7a2f598de69134d90b143257c3559bc98a`

## KISS-Isolierung B01 – 2026-09-06

Aus dem bestehenden #140-Verlauf wurde der bereits vorhandene reine B01-Prefix direkt auf current `main` isoliert:
- Basis: `c8a96e7a2f598de69134d90b143257c3559bc98a`;
- Head: `94917596adce04765380c60dd7ade0fb23793393`;
- 4 Commits / 4 Dateien;
- tatsächliche Fachworkflow-Codeänderung: nur Kategorie-Guard Name+Slug+Taxonomy sowie lokale Seed-ID; Rest = notwendige Hashkette;
- keine B15-Signierbereinigung;
- keine Fach-/Inhalts-/Textmaschinen-/SEO-/Link-/Tabellen-/LanguageTool-/PPM-/PSERC-/PSTE-/Design-/Publish-Regeländerung;
- GitHub `hardlock`: PASS;
- GitHub `hardlock-base`: PASS;
- PR #141: Draft, mergeable=true;
- kein Merge.

**Warum #141 bevorzugt:** Der letzte reale Lauf auf unverändertem `main` kam mit der bisherigen Signierstrecke bereits bis B01. B15 ist daher nicht erforderlich, um den aktuell belegten ersten Live-Blocker zu testen. Ein B01-only-Kandidat erhält die Kausalität.

**Grenze:** M01–M33 wurde auf #141 nicht neu als kompletter Lauf ausgeführt; kein Live-/7/7-PASS.

## Aktueller Prüfstand

- B01-KISS-Fix bleibt enthalten: keine vorgezogene WordPress-ID im echten Produktionsplan; interne Seed-ID nur für den isolierten lokalen PPM-Testzustand.
- M15/M31 waren stale und wurden auf den aktuellen gebundenen Request-/Handoff-Weg korrigiert.
- M26/M28 waren ebenfalls noch auf den alten Direkt-Receipt-/Prepass-Weg ausgerichtet und wurden auf Request → realer PPM → erst danach PASS/Receipt korrigiert.
- **Interne Signieraltlasten wurden aus dem aktiven 107007-Vorlauf entfernt:** H8-Bootstrap, Provenance, Runtime-Guard, Codex-Preflight und das gebundene Generation-1-H8-Paket verlangen keine ED25519-Signatur, keinen Signer und keinen Schlüssel mehr. Herkunft/Integrität bleiben hash- und batchgebunden.
- M22/M23 wurden entsprechend auf H8-Provenance/Integrität statt interner Signatur ausgerichtet.
- **Unverändert:** Textmaschine, Linkregel, Tabellenstufe, LanguageTool, PPM, PSERC/PSTE, SEO/Design und Publish-Sperre.
- **Externe Signierung bleibt unangetastet:** hostseitige Finalisierung erst nach 107008 sowie GitHub-ENDSTEMPEL/WordPress-Verifikation.
- GitHub `hardlock` und `hardlock-base` auf Head `3ed31aa…`: PASS.
- **SCOPE-PASS internes Signierkonzept:** aktiver Call-Graph bis 107007 ohne ED25519-/Signer-/Key-/`SIGNED`-Pflicht; gebundenes H8-Paket `WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND` ohne Signaturfelder; Host-Signer erscheint erst im 107008-Endzustand.
- **ZWISCHENTEST INTERN/EXTERN: PASS im belegten Umfang.** Internes unsigniertes HASH_BOUND-Paket + aktuelle H8-Provenance PASS; fehlende, falsche oder nicht-current H8-Provenance wird fail-closed blockiert; Qualitätsstufen inkl. Link/Tabelle/PPM unverändert; externe ED25519-Positiv-/Negativprüfung PASS. **Nicht stärker behaupten:** Ein kombinierter Angreifer-Test „Herkunft manipuliert + alle normalen Hashes passend neu berechnet“ ist im aktuell dauerhaft auffindbaren Testbestand nicht vollständig als eigener End-to-End-Negativtest belegt.
- **M01–M33 GESAMT PASS:** vorhandener Runner real ausgeführt gegen den Quellstand `3ed31aa…`; M01–M33 PASS, `LAST_REGRESSION PASS`, `GESAMT PASS`.
- M15-Negativtest enthielt einen Escape-/Zeilenumbruchfehler; ausschließlich dieser Testfehler wurde KISS in Commit `3ed31aa78978a2098f324eead6f2a5335a10e2d4` korrigiert. Der dokumentierte vollständige M01–M33-Re-Run erfolgte auf genau diesem Quellstand und endete PASS.
- **B06 gilt hart:** Hobbyraum-/PR-Head ist kein Live-/7/7-Testort; Production Preflight verlangt current `main`.
- Kein Live-7/7-PASS behauptet.

## Integrations-/Fehlschlag-Sicherheitsplan für den nächsten B01-Live-Test

Solange kein Kandidat ausdrücklich freigegeben ist: **kein Merge**.

Für den nächsten kausalen Live-Test ist **PR #141 (B01-only)** gegenüber #140 vorzuziehen. #140 bleibt als separater breiterer B01+B15-Prüfstand bestehen.

Falls später ausdrücklich integriert wird:
1. Vorherigen `main`-Anker unverändert dokumentieren: `c8a96e7a2f598de69134d90b143257c3559bc98a`.
2. Für den ersten kausalen Test ausschließlich den B01-only-Kandidaten #141 integrieren; #140/B15 nicht parallel mitziehen.
3. Auf dem neuen current `main` zuerst bestehende Identitäts-/Preflight-Prüfung.
4. Danach **genau der bestehende produktive 7er-Lauf**; keine neue Canary-Route und kein alternativer Runner.
5. Beim **ersten realen Blocker sofort stoppen** und nur diesen gegen Fehlerhistorie/Zielvertrag analysieren.
6. Kein automatischer Rückbau. Falls der Merge selbst als Ursache belegt wird, ist der Merge-Commit gezielt reversierbar; Rücknahme nur mit ausdrücklicher Nutzerfreigabe.
7. Keine Aussage „B01/#141 gelöst“, bevor der echte Lauf B01 passiert; keine Aussage „System wiederhergestellt“, bevor 7/7 + 107008 auf demselben produktiven Stand belegt ist.

Damit wird die B06/B14-Testlücke nicht wegbehauptet, sondern operational begrenzt: Vor Merge nur Regression/Scope; nach Merge erster echter Live-Beweis mit klarer Rückkehrgrenze.


## HARTE SCOPE-GRENZE – NUR TECHNIK

**Architektur und Inhalte sind für diesen Auftrag tabu.**

Erlaubt ist ausschließlich die technische Ausführungsebene:
- konkrete Ein-/Ausgabeartefakte;
- Hash-/Identitätsbindung;
- Gate-Reihenfolge;
- technische Übergaben/Handoffs;
- Stage-/Receipt-/Status-Logik;
- Dateipfade/Bindings;
- technische Fail-closed-/Pass-Weitergabe;
- technische Positiv-/Negativtests bestehender Mechanismen.

Nicht erlaubt:
- Architekturumbau oder neue Architektur;
- neue Runner/Gates/Executor/Workflows;
- Fach-/Inhaltsregeln verändern oder neu interpretieren;
- Textmaschine, SEO, Linkregel, Tabellenregel, LanguageTool, PPM, PSERC/PSTE, Design oder Publish-Regeln verändern;
- neue Artikeltypen-/Contentlogik;
- technische Probleme durch Fachregeländerung „lösen“.

Prüffrage:
**Erfüllt die bestehende technische Implementierung die bereits festgelegten Verträge korrekt und auf dem richtigen Artefaktzustand?**

## Harte Altlasten-/Rückbau-Prüfung

Vor jedem Rückbau im aktiven TEXT-/STARTMASTER-Weg zwingend:

1. **Mikro:** Kandidat positiv/negativ prüfen; konkrete Funktion und Fehlerwirkung trennen.
2. **Abhängigkeiten:** direkte und indirekte Nutzer, Hashbindungen, Übergaben, Receipts und spätere Schritte prüfen.
3. **Fehlerprotokoll-Gegencheck:** die vollständige autoritative Fehlerquelle über FEHLERREGISTER lesen und ausdrücklich prüfen, welcher historische Fehler/Fix durch den Rückbau wieder geöffnet werden könnte.
4. **Schutzliste:** Textmaschine/Fachregeln, externe-Link-Regel, Tabellenstufe, LanguageTool, echter PPM 6.7.9, PSERC/PSTE, Dubletten/Kannibalisierung, SEO, Design, Publish-Sperre, Hash-/Herkunftsbindung und externe Signierung ab 107008 dürfen nicht verloren gehen oder gelockert werden.
5. **Makro:** vollständigen bestehenden Regressionstest auf demselben Kandidatenstand ausführen. Lokaler PASS allein reicht nicht.
6. **Realitätsgrenze:** Regression-PASS bleibt ausdrücklich kein Live-/7/7-PASS.

**Fail-closed:** Ist Notwendigkeit, Seiteneffekt oder historischer Fehlerbezug nicht belastbar geklärt, wird nicht zurückgebaut.
**KISS:** immer nur ein kausal abgegrenzter Kandidat; keine Sammel-Aufräumaktion.

## Single Writer

- Dieser normale TEXT-Arbeitschat ist für den aktuellen B01-Hobbyraumauftrag der einzige aktive technische Schreiber.
- Paul wird nicht benutzt.
- main wird nicht verändert.
- Andere Büros/Arbeitsbereiche bleiben unangetastet.
- Erst nach belastbarer Prüfung werden offizieller Stand und nächste Aktion weitergeschrieben.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.

**Paul-Pipeline-Prüfkarte:** `PAUL_PIPELINE_AUDIT_20260906.md` – priorisiert direkte Gate-/Vertragskollisionen gegenüber späteren WordPress/Public-Folgethemen.

**Systemische Root-Cause-Karte:** `TECHNICAL_CORRIDOR_ROOTCAUSE_20260907.md` – gemeinsame Fehlerklassen aus Paul + B01–B15/M01–M33 + LanguageTool-Livebefund; verhindert weitere Minifix-Ketten.

**Vor-Codex-Readiness:** `PRE_CODEX_READINESS_20260906.md` – vollständige technische Vorprüfung, Belege, Grenzen und STOP-Regel für #141.

**First Codex Runbook:** `FIRST_CODEX_RUN_B01_20260906.md` – exakter bestehender Liveweg nach ausdrücklich freigegebenem #141-Merge; STOP beim ersten realen Blocker.

## Altlasten-Audit – Zwischenstand 2026-09-06

**Noch kein zusätzlicher Rückbau freigegeben.**

Geprüft:
- `m.DUAL = SELF`: bewusster KISS-Kompatibilitätskleber zur Wiederverwendung der bestehenden Room-Bridge; löst/umgeht alte DUAL-Fachlogik. **BEHALTEN.**
- alte Recovery-/Existing-Article-Logik im `STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py`: im heutigen Current-Action-Workerpfad nicht aktiv. **Kein aktueller Fehlerverursacher; nicht anfassen.**
- `PPM679_PACKAGE_ZIP` / `PSERC_FIX_ZIP` Env-Overrides: Repo-Fallback + exakte SHA-Bindung vorhanden; kein belegter aktueller Fehler durch den Override. **Verdacht allein reicht nicht; nicht entfernen.**
- `test_fachworkflow_proof_handoff.py`: gegenüber dem seit 05.09. zwingenden realen `ppm679_binding` stale und nicht Bestandteil des aktuellen M01–M33-/PR-Beweises. **Testballast/Testlücke, kein aktiver Produktionsblocker.**
- B01-ID-Pflicht: numerische ID wurde erst mit dem realen PPM-Handoff am 04.09. als technische Vorbedingung eingeführt; historischer Kategorie-Hardlock verlangt Name + Slug + Taxonomy. **#141** isoliert ausschließlich diesen B01-Fix und nutzt eine Seed-ID nur im lokalen PPM-Seedzustand. #140 bleibt der breitere B01+B15-Prüfstand. **Kausal begründeter Kandidat; Live-Beweis weiterhin offen.**

Konsequenz:
Bis zu einem neuen echten Live-Lauf keine weitere technische Bereinigung auf Verdacht in #141 aufnehmen; #140 nicht als parallelen Live-Kandidaten verwenden.

### 107008-/Abschlussweg-Audit 2026-09-06

- Delivery/Recovery-Persistenz (`chat_delivery_payload.py` → `recovery_sources/<batch>`) entstand als Reaktion auf den realen B13-Endstempel/Auth-/Persistenzfehler nach dem belegten 7/7+107008-PASS. **BEHALTEN.**
- Hostseitige PSERC-Signatur und GitHub-ENDSTEMPEL sind keine identische Doppelprüfung: Host signiert/verifiziert den fachlichen `workflow_release`; GitHub signiert später das persistierte 7-Artikel-Manifest. **BEHALTEN; externe Signiergrenze ist geschützt.**
- PPM-/PSERC-Runtimepakete sind auch in 107008 hashgebunden, obwohl dort kein neuer PPM-Lauf stattfindet. Das ist ein möglicher Vereinfachungspunkt, kann aber zugleich die Identität desselben produktiven Standes absichern. **Keine belegte Störung / kein Rückbau.**
- gzip/base64/Import-Envelope transportiert die bereits geprüften sieben Artikel und den hostseitig geprüften Release in die dauerhafte GitHub-Quelle; die Artikelbytes werden gegen Produktionsplan und Hashes gegengeprüft. **Kein belegter unnötiger Transportlayer.**

**Audit-Ergebnis:** Außer B01 und der bereits ausgeführten B15-Signierbereinigung ist aktuell keine weitere aktive Altlast kausal oder sicher entfernbar belegt.

### Paul-Technikmodell – neuer READ-ONLY-Audit-Kandidat 2026-09-06

Paul hat **unseren realen System-/Workflowtyp mit unseren Plugins und Verträgen** in seiner Testinfrastruktur end-to-end durchgespielt; der Artikel „Duschhocker kaufen“ war nur ein beliebiger Testdatensatz. Die dokumentierten Findings sind deshalb als **direkte Befunde zu unserem System** zu behandeln, soweit sie den jeweils geprüften aktuellen Modulstand betreffen:

**Gate-/Vertragskollision:** Zwei für sich sinnvolle Module können gemeinsam unerfüllbar werden, wenn sie unterschiedliche Zustände desselben Artefakts erwarten oder ein Gate nicht exakt das Artefakt prüft, das später weitergegeben wird.

Direkter STARTMASTER-Befund:
- Fachvertrag: PASS-Reuse nur bei identischem, hashgebundenem Input/Vertrag.
- Aktueller Handoff prüft bei Nicht-PPM-Stufen `input_sha256` nur auf formale 64-Hex-Gültigkeit.
- Er erzwingt dort nicht mechanisch, welches konkrete Artefakt dieser Hash bezeichnet oder wie es mit Vor-/Nachstufe zusammenhängt.
- PPM ist enger: dort wird `input_sha256` ausdrücklich auf den finalen Artikel-SHA gebunden.
- derselbe lose Nicht-PPM-Hashcheck existierte bereits auf den belegten früheren 7/7-Ständen `d841ed…` / `de21f6…`; daher **kein Beleg als Ursache des aktuellen B01-Livefehlers**, sondern latente technische Vertrags-/Paritätslücke.
- B01 selbst passt jedoch zur von Paul reproduzierten Fehlerklasse „Downstream-Gate verlangt ein Feld/einen Zustand, den der gültige Upstream-Vertrag nicht liefern soll“: numerische WP-ID vs. semantischer Kategorievertrag.

Nächster READ-ONLY-Prüfgegenstand:
Für die bestehende 12-Stufen-Kette je Stufe bestimmen:
1. welches konkrete Eingangsartefakt geprüft wird;
2. welcher Hash dieses Artefakt identifiziert;
3. ob die Stufe das Artefakt verändern darf;
4. welches Ausgangsartefakt entsteht;
5. welches nachfolgende Gate genau dieses Ergebnis konsumiert;
6. ob die technische Prüfung diese Übergabe wirklich bindet oder nur einen beliebigen formal gültigen Hash akzeptiert.

**Keine neue Architektur / kein neuer Runner.**
Ergebnis zuerst nur als Wirkungskarte. Erst ein konkret reproduzierter Vertragskonflikt darf Fehler-/Rückbaukandidat werden.



## HARD RULE – NULL-FREIHEIT / ZWANGSJACKE 2026-09-07

**Unantastbar:**
- pro Raum genau **eine Tür**;
- genau **ein dummer, fachblinder Wächter**;
- Chat/Codex besitzt **null freie Workflow-, Routing-, State-, Prüf-, Qualitäts-, Ersatz- oder Publishentscheidung**;
- keine neue Capability, kein separater Executor, kein zweiter Handoff, kein Parallelpfad;
- Fachworkflow/Textmaschine/SEO/Links/Tabellen/LanguageTool/PPM/PSERC/PSTE/Design/Publish-Regeln unverändert.

Der Worker darf nur die vom bereits gebundenen Fachworkflow verlangten Arbeitsprodukte erzeugen. Er darf **nicht** selbst bestimmen:
- welcher Prüfer gilt;
- welche Evidence genügt;
- welcher Artefaktzustand zu prüfen ist;
- wie PASS begründet wird;
- ob ein Ersatzproof zulässig ist.

Ein selbst geschriebenes `PASS`, `execution_performed=true`, beliebiger 64-Hex-Hash oder Stage-Proof ist niemals allein ausreichende Evidence.

**NEXT ACTION:** Fix-Sperre bleibt aktiv. Nur noch die zwei offenen technischen Bedeutungsbindungen schließen: (1) allgemeine NEW-Link-Provenienzquelle des bestehenden Fachworkflows; (2) exakte Bedeutung von `design_format` vor dem WordPress-Render versus späterem echten Rendered-DOM-Gate. Danach erst konsolidierten Kandidaten lokal positiv/negativ prüfen. Bis dahin: `FIX_FORBIDDEN`.
