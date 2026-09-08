# STARTMASTER0107 – VOLLSTÄNDIGES PROTOKOLL 30.08.–05.09.2026

**FORTLAUFENDE KANONISCHE PROTOKOLLQUELLE.** Der historische Dateiname bleibt aus Adressstabilitätsgründen unverändert; neue TEXT-Ereignisse werden hier weitergeführt.

## 30.08 – H7-Komplettstand

Kanonische H7-MASTER: `MASTER_PFERDE_ATELIER_STARTMASTER0107_H7_PROJECT_SINGLE_DOOR_FINAL_20260830.zip`, ca. 78,5 MB.
Damals main `be8a5a3e0059c5bb44bcbbe63ae85bdb42ac219a`, Step 107007, Generation 1, Batch bereit aber Produktionspaket noch vorgebunden/offen.

H7 bewies Single-Door-/Preproduction-Governance und lokale Wächtertests. Diese Tests waren kein späterer Beweis für die komplette reale Artikelproduktion.

## 31.08 – H8

H8 ergänzte `R_BOOT_001` vor `R_PRE_001` und härtere Herkunftsbindung. Fach-/Text-/Qualitätslogik sollte unverändert hinter der technischen Tür bleiben.

## 01.09 – Runtime / Environment / Codex-native Bridge

Stand der späteren Zwischenmaster: main `183b4167…`, Runtime `EXECUTION_READY`.
Probleme und Rootfixes um:
- stale/fehlendes Git origin,
- ED25519 Runtime,
- Trennung Preproduction/Production,
- nicht vorhandene synthetische `execute_bound_action` Capability,
- Codex-native Capsule Bridge,
- Environment hard sync auf current main.

## 04.09 – reale 7/7-Referenzen

`d841ed…`:
- 7/7 Artikel frisch erzeugt,
- je Artikel 12 Stage-Ergebnisse + Proofs,
- realer Produktionsweg funktionierte bis nach 107007;
- zunächst `STAGING_DESTINATION_COLLISION:ARTICLE.md`, späterer Lauf auf gleichem Stand erreichte 107008.

`de21f6cd…`:
- 7/7 akzeptiert,
- 107007 vollständig,
- 107008 Review PASS,
- späterer Fehler erst GitHub Endstempel/Auth/Persistenz.

Damit ist belegt: Der Workflow war real produktionsfähig.

## Danach – PPM-Härtung

Ab `6818cc…` wurde exakter echter PPM-6.7.9-Nachweis verpflichtend. Danach folgten in schneller Folge:
- realer PPM-Executor im Handoff,
- Sichtbarmachung des Handoffs,
- Paketpfade,
- Requestschema,
- Context-Härtung,
- interne Handoff-/Submit-Umstellungen,
- Signer-/107008-Härtungen.

Die Textmaschinen-Grundregeln und Article-Type-Templates blieben im entscheidenden Vergleich unverändert; die Regression entstand in den technischen Übergaben/Kontrollschichten.

## 04./05.09 – wiederkehrender erster Live-Blocker

Mehrere reale Läufe stoppten mit:
`BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`.

Die Steuerung verlangte aktuelle Fachworkflow-Ausgaben, behandelte Codex aber gleichzeitig so, als müsse dafür ein separater Executor existieren.

## 05.09 – PPM-Reihenfolge KISS-Fix

Im Hobbyraum wurde die Reihenfolge auf den vorhandenen Handoff zurückgeführt:
Fachworkflow-Ergebnisse → echter PPM → erst danach finaler PASS/Receipt.

Prinzipprüfung mit Originalpaketen:
- 4 Positivfälle PASS,
- 4 Negativfälle korrekt BLOCKED.

Dabei zusätzlich Fake-PPM-Lücke gefunden und geschlossen.

Sauberer Produktions-PR #135 enthielt nur notwendige Produktionsdateien und wurde nach grünen Hardlocks gemergt:
`2ec738613ca318cd2b168e95f14c1eea2febd161`.

Realtest danach: weiterhin `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING` vor Artikel 1.

## 05.09 – Worker-Rollenbindung

PR #136 bindet hart:
Current Codex = gebundener Fachworkflow-Worker,
kein separater Fachworkflow-Executor / keine separate Capability.

Merge → aktueller main `c8a96e7a2f598de69134d90b143257c3559bc98a`.
Hardlocks auf aktuellem main: PASS.

## Letzter echter Lauf auf aktuellem main

Der alte Fachworkflow-Kontext-Blocker trat nicht mehr auf.
Der Lauf erreichte einen neuen ersten Blocker:
`BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`.

Wichtigste Nutzerkorrektur:
- Kategorien werden von der SEO-Maschine gespeist und per JSON übergeben.
- Der SEO-Handoff ist bewusst exakt fünf Felder.
- Diese Grenze darf nicht geändert werden.
- Danach arbeitet die Textmaschine.

## Systemischer Testbefund

Die Regressionstests waren nicht ausreichend live-paritätisch. Insbesondere ist die im M01–M33-Runner bezeichnete Schlussprüfung gegen die letzte reale Regression kein echter Replay des letzten realen 7/7-Pfads; sie ruft nur einen Test erneut auf und druckt anschließend eine PASS-Zeile.

Daher konnten technische Tests PASS sein, während der echte Workflow später erneut an Übergaben scheiterte.

## Status Ende dieses Protokolls

- main `c8a96e7a2f598de69134d90b143257c3559bc98a`
- PR #107 Head identisch
- 107007 offen
- 107008 im letzten Lauf nicht erreicht
- erster aktueller Live-Blocker: Kategorie-ID-Anforderung vor realem PPM
- SEO-5-Felder-Handoff und Textmaschine ausdrücklich unangetastet lassen
- kein Publish / keine WordPress-Schreibaktion
## 05.09 – Interne Signieraltlasten-Säuberung

Die historische Architekturentscheidung wurde erneut gegen Repository-Historie und aktuellen Code geprüft:
- interne Raum-/Worker-Signierung war bereits bewusst verworfen worden;
- innerhalb der Produktionsstraße sollen Wächter, Hash-/Herkunftsbindung, Fachprüfungen und PASS/Receipt-Kette arbeiten;
- kryptografische Versiegelung gehört erst an die externe Grenze nach abgeschlossener Produktion.

Trotzdem waren im aktiven Vorlauf noch technische Reste des alten Modells vorhanden: H8-Bootstrap/Provenance, Preproduction-Handoff, Runtime-Guard, Codex-Preflight sowie das gebundene Generation-1-H8-Paket verlangten noch ED25519-/Signer-/Key-Merkmale.

KISS-Säuberung auf Draft-PR #140 / Branch `hobbyroom/b01-semantic-category-seed`:
- interne ED25519-/Signer-/Key-Pflicht entfernt;
- H8 bleibt hash-, Batch-, Slot- und herkunftsgebunden;
- gebundenes Generation-1-Paket intern auf reine Hash-/Provenance-Bindung umgestellt;
- M22/M23 auf die heutige Signiergrenze korrigiert;
- stale M26/M28 zusätzlich auf den aktuellen Request → realer PPM → PASS/Receipt-Weg korrigiert;
- 107007/107008-/State-/Root-Hashketten nachgezogen.

Nicht verändert:
- Textmaschine;
- externe-Link-Regel;
- Tabellenpflicht/-stufe;
- LanguageTool;
- PPM 6.7.9 / PSERC / PSTE;
- SEO / Design;
- Publish-Sperre;
- externe Signierung nach 107008 und GitHub-ENDSTEMPEL/WordPress-Verifikation.

Beleg auf Head `c3244d5bf838817078a3821c045fb52e86f3db46`:
- `hardlock`: PASS;
- `hardlock-base`: PASS;
- aktiver Innenweg ohne ED25519-/Signer-/Key-Pflicht geprüft;
- externer ENDSTEMPEL weiterhin vorhanden.

Noch kein Abschlussbeleg:
- M01–M33 wurde auf diesem exakten Head noch nicht vollständig ausgeführt;
- kein neuer 7/7-Live-Lauf;
- main unverändert `c8a96e7a2f598de69134d90b143257c3559bc98a`.

### Abschluss internes Signierkonzept – SCOPE-PASS

Finaler Hobbyraum-Head: `7990029428399e8ba01d88a6543ce068812e9218`.

Abgrenzung:
- geprüft und bereinigt wurde ausschließlich die heute aktive interne Strecke bis 107007;
- historische H7-/Master-/Proof-Dokumente wurden nicht als Reparaturziel behandelt;
- externe Signierung ab 107008 wurde nicht entfernt.

Finaler Befund:
- aktiver interner Call-Graph ohne ED25519-, Signer-, Key-, `trusted_keys`- oder `WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED`-Pflicht;
- `worker_freshness_guard` verlangt kein `ed25519_runtime` mehr;
- H8-Bootstrap/Provenance/Runtime/Preflight arbeiten hash-/batch-/slot-/herkunftsgebunden;
- gebundenes Generation-1-H8-Paket: `WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND`, keine Signaturfelder;
- interner Fachworkflow-PASS verlangt `HASH_BOUND`-Release-Metadaten;
- erst `finalize_after_107008` wandelt diese in den extern signierten Release-Vertrag um;
- externer Production-Release-/ENDSTEMPEL-/WordPress-Schutz bleibt erhalten.

Nicht verändert:
- Textmaschine;
- externe-Link-Regel;
- Tabellenregel/-stufe;
- LanguageTool;
- PPM 6.7.9 / PSERC / PSTE;
- SEO / Design;
- Publish-Sperre.

Belege:
- `hardlock` PASS auf Head `7990029…`;
- `hardlock-base` PASS auf demselben Head;
- aktiver interner Call-Graph: CLEAN;
- aktuelles H8-Paket: HASH_BOUND ohne Signaturfelder.

Grenze:
Dies ist ausschließlich ein SCOPE-PASS der internen Signier-Säuberung. Kein M01–M33-GESAMT-PASS und kein neuer 7/7-Live-PASS.

### Zwischentest Signierthese – PASS

Head: `7990029428399e8ba01d88a6543ce068812e9218`.

Maschinell geprüfte These:
1. Internes H8-Paket ohne Signaturfelder + aktuelle HASH_BOUND-/Provenance-Bindung → **PASS**.
2. H8-/Batch-Herkunft manipuliert; Binding-Hash, Workflow-Hash, Package-ID und Package-Payload-Hash anschließend vollständig neu berechnet → normale Paketintegrität weiterhin konsistent, aber aktuelle Provenance-Bindung → **BLOCKED**.
3. Qualitätskette → `table_contract`, `internal_links`, LanguageTool, PPM, PSERC, PSTE, Dubletten/Kannibalisierung, SEO und Design weiterhin gebunden; Original-PPM-6.7.9-SHA unverändert → **PASS**.
4. Externe ED25519-Prüfung: gültige Signatur → **PASS**; manipulierte Signatur → **BLOCKED**.

Schlussfolgerung dieses Zwischentests:
Die entfernte interne Signatur war für die geprüfte innere Weg-/Herkunftssicherheit nicht erforderlich. Die externe kryptografische Grenze bleibt wirksam und getrennt.

Grenze: kein M01–M33-GESAMT-PASS und kein Live-7/7-PASS.

## 06.09 – Vollständiger Hobbyraum-Regressionsabschluss

Aktueller technischer Kandidat:
- Draft-PR #140;
- Branch `hobbyroom/b01-semantic-category-seed`;
- Head `3ed31aa78978a2098f324eead6f2a5335a10e2d4`;
- main unverändert `c8a96e7a2f598de69134d90b143257c3559bc98a`.

### M15-Testfehler gefunden und KISS behoben

Der erste echte vollständige M01–M33-Lauf stoppte nach M01–M14 PASS bei M15.

Ursache:
Die beiden M15-Negativtests verwendeten im Teststring ein literales `\\n` statt eines echten Zeilenumbruchs. Dadurch wurde der absichtlich ergänzte verbotene Satz nicht als eigene Zeile erkannt.

Fix:
Ausschließlich die beiden Teststrings auf echten Zeilenumbruch korrigiert.
Keine Produktionslogik, Fachregel, Textmaschine, PPM-, Link- oder Tabellenlogik geändert.

### Vollständiger Wiederholungslauf

Bestehender M01–M33-Runner danach vollständig ausgeführt.

Ergebnis:
- M01 bis M33: **PASS**;
- `LAST_REGRESSION PASS BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`;
- Abschluss: **`GESAMT PASS`**.

GitHub auf demselben Quellstand:
- `hardlock`: **PASS**;
- `hardlock-base`: **PASS**.

Testgrenze:
Regression-PASS ≠ Live-PASS.

### B06 erneut praktisch bestätigt – kein neuer Produktionsfehler

Ein Live-/7/7-Versuch aus dem Hobbyraum-Head wurde vom bestehenden Production Preflight korrekt vor 107007 blockiert:

`CODEX_CHECKOUT_NOT_CURRENT_MAIN:3ed31aa…:EXPECTED:c8a96e7…`

Folgen:
- 107007 nicht ausgeführt;
- 107008 nicht erreicht;
- keine Artikelproduktion;
- keine Codeänderung;
- keine WordPress-Schreibaktion.

Einordnung:
Das ist **kein neuer Produktionsfehler**, sondern der bereits bekannte B06-Testgrenzfall.
Dauerregel: Hobbyraum/PR-Head = Regression/Reparatur; echter Live-/7/7-Beweis erst nach regulärer Integration auf current `main`.

### Abschlussstand dieses Prüfblocks

Hobbyraum-Regressionsstand: **PASS**.
Live-/Produktionsstand: **nicht neu belegt**.
Nächster Übergang: keine weiteren Hobbyraum-Liveversuche; Integrationsentscheidung für PR #140 nur nach ausdrücklicher Nutzerfreigabe, danach Livebeweis auf current `main`.


## 07.09 – Plan A / Plan B / Live-LanguageTool / systemische Bindungsprüfung

### Plan B separat angelegt

Plan B wurde ausschließlich als getrennte Shadow-Linie angelegt:
- Draft-PR #143;
- Branch `plan-b/text-slimline-shadow-v1-20260907`;
- Basis `c8a96e7a2f598de69134d90b143257c3559bc98a`;
- ausschließlich neue Dateien unter `experiments/plan_b_text_slimline/`;
- keine Produktionsverdrahtung;
- kein Merge;
- keine automatische Übernahme von Plan-A-Fixes.

Zweck:
späterer A/B-Vergleich mit denselben Qualitäts-/Sicherheitsregeln, ohne Vermischung.

### Plan A – B01-only integriert und real getestet

PR #141 wurde nach Pflichtcheck regulär in main integriert.

Neuer/current main:
`f14ccf187b94c4beab9a86d0c69144f792ba2f64`.

Dispatcher #107 wurde auf exakt diesen main-Head gebunden.

Realer Codex-Lauf:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- Single Door READY;
- erster technischer STOP: `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`;
- state_advanced=false;
- 107007 nicht abgeschlossen;
- 107008 nicht erreicht;
- kein Publish / kein WordPress-Write.

B01 wurde dadurch **nicht erneut live bestätigt**, weil der Lauf vorher bei LanguageTool stoppte.

### LanguageTool – kein isolierter Fix freigegeben

Historischer LT-6.8-/Bestand-43-Weg wurde identifiziert; der begonnene Branch
`hobbyroom/languagetool-runtime-rebind-20260907`
bleibt ausschließlich PARKPLATZ / NICHT INTEGRIEREN.

Grund:
Paul-Audit + B01–B15/M01–M33 + aktueller Livebefund zeigen wiederkehrende technische Bindungs-/Artefaktzustandsfehler. Ein LT-Einzelfix würde die Fehlerklasse nur an einer Stelle behandeln.

### Systemische technische Prüfung

Dauerhafte Wirkungskarten:
- `TECHNICAL_CORRIDOR_ROOTCAUSE_20260907.md`;
- `TECHNICAL_CORRIDOR_MATRIX_20260907.md`.

Kernaussage:
Die zwölf Stage-Namen sind keine zwölf gleichartigen Worker-Jobs. Mehrere echte Autoritäten liegen upstream, im Fachworkflow, in LT/PPM/PSERC/PSTE oder an äußeren Sicherheitsgrenzen. Der aktuelle Handoff lässt bei Nicht-PPM-Stufen zu viel Nachweisinterpretation beim Worker.

Keine Fach-/Qualitäts-/Designregel wurde geändert.

### Hobbyraum-Fixsperre / Arbeitsplan

Der TEXT-Hobbyraum wurde auf einen einzigen verbindlichen A–F-Ablauf reduziert:
A Ausgangspunkt → B 7 Pflichtchecks → C Anti-Minifix → D ein KISS-Kandidat → E lokale Positiv-/Negativfreigabe → F Codex-Test.

Maschinenstatus:
`FIX_FORBIDDEN`.

Solange Positiv/Negativ + Invarianten nicht PASS sind:
- kein Kandidat;
- kein Merge;
- kein Produktionscode-Fix.

Security-PR #137 enthält die vorgesehene serverseitige Prüfung von `HOBBYROOM_WORK_LOCK_V1`, ist aber weiterhin **nicht gemergt**.


## 08.09.2026 – Abschluss-/Nachholprotokoll eingefrorener Wiederaufbau

### Reparaturkonzept

Der Reparaturweg wurde verbindlich eingefroren:
`de21f6…` Goldmaster → erster realer Blocker → Paul/Fehlerhistorie/letzter funktionierender Stand/Nachbarstufen → genau eine Pflichtänderung → Positiv/Negativ → echter Realtest → PASS einfrieren oder Regression vollständig zurückbauen.

Kein Sammelfix, kein Parallelkonzept, kein Fix auf fehlgeschlagenen Fix.

### Wiederherstellung Goldmaster-naher Eingangsstrecke

Ausgeführt:
- PR #149: ungültige YAML-Einrückung des `Pferde Atelier Immutable Base Hardlock` korrigiert;
- PR #150: hardlock-base-Kandidatentest auf echten Git-Worktree umgestellt;
- PR #151: motornahe Cloud-Entry-Strecke wieder exakt auf `de21f6…` zurückgeführt;
- Ruleset-Wartung: `hardlock-base` für kontrollierte Security-Wartung kurz entfernt und danach wieder als Required Check aktiviert.

### Chronologischer Pflichtaufbau nach Goldmaster

Einzeln mit Realtest aufgebaut:
- Step 01 / historischer PR #122 → Merge #153 / main `46a807ac…`;
- Step 02 / historischer PR #124 → Merge #154 / main `7df2008e…`;
- Step 03 / historischer PR #125 → Merge #155 / main `a9cde12a…`;
- Step 04 / historischer PR #126 → Merge #156 / main `67143a95…`.

Nach Step 04 erster Realblocker:
`BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`.

### B02 – vollständiger alter Snapshot verworfen, Semantikdelta gebaut

Der erste historische B02-Snapshot #152 wurde nach Hardlock-FAIL `INPUT_HASH_MISMATCH` vollständig verworfen; kein Fix auf diesen Kandidaten.

Danach nur die historische B02-Semantik auf die aktuelle Hashkette übertragen:
- Branch `hobbyroom/b02-semantic-worker-binding-current-hash-20260908`;
- Head `562b71c726e2232539412376c1b0a047dbd3485d`;
- Kandidatenchecks: `hardlock` PASS, `hardlock-base` PASS;
- Merge main `36d1ecb52cf80c91e2f30f5a1eb7ecc1f14782c9`.

### Echter Realtest nach B02

Ausgeführt auf exact current main `36d1ecb5…`.

PASS:
- Cloud Entry;
- Production Preflight;
- Runtime Entry;
- Current Action READY;
- Single Door READY.

B02 ist real überwunden.

Neuer erster echter Blocker:
`BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND`.

Befund:
`fachworkflow_handoff.command` exponiert `PPM679_PACKAGE_ZIP` / `PSERC_FIX_ZIP` nicht; echter PPM-6.7.9-Lauf kann über den gebundenen Befehl nicht starten.

107007 nicht abgeschlossen, 107008 nicht erreicht, kein Publish, kein WordPress-Write.

### Separate Testgrenze PR #107

Der permanente Dispatcher-PR #107 zeigte nach Umschalten seines Heads auf `36d1ecb5…` einen `hardlock-base`-FAIL `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`, weil sein alter Dispatcher-Base historische immutable Änderungen im PR-Diff sichtbar macht.

Dies ist kein TEXT-Produktionsblocker und ersetzt keinen Realtest.

### Maschinengehärteter Wiederaufbau – Fortsetzung 08.09.2026

RECOVERY_BASE_SHA: `de21f6cd35c60849c551fd82f78e75ce57c99fab`.

#### B07/M32 – repositorygebundene PPM-/PSERC-Runtimepfade

Ausgangspunkt:
- main `36d1ecb52cf80c91e2f30f5a1eb7ecc1f14782c9`;
- erster realer Blocker `BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND`.

Historischer M32-Fix wurde auf seine Semantik reduziert:
- bestehender repo-relativer Fallback für PPM 6.7.9 und PSERC-FIX;
- keine neue Route, kein neuer Executor;
- Kandidat PR #158 / Head `41849f012a381bd0ee0a362b788ea772ed03d382`;
- Kandidatendatei byte-identisch zur historisch bewiesenen M32-Datei;
- `hardlock`: PASS;
- `hardlock-base`: PASS.

PR #158 regulär gemergt.
Neuer main:
`30e933357dd9e5d3dde7cbd361c930b2a0c352c1`.

#### Realtest nach B07/M32

Echter 7/7-Produktionsweg auf `30e93335…`:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- Single Door READY;
- `fachworkflow_proof_handoff.py materialize` wurde real erreicht.

Damit B07/M32 real überwunden.

Neuer erster echter Blocker:
`FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`.

Exakte Ursache:
Die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` für den ersten Artikel existiert am erwarteten Quarantine-Pfad nicht.

107007 nicht abgeschlossen.
107008 nicht erreicht.
Kein Publish.
Kein WordPress-Write.
Keine Reparatur während des Realtests.

#### M28 als bekannte historische Regression identifiziert

Die schriftliche Fehlermatrix enthält M28 bereits:
fehlende `FACHWORKFLOW_HANDOFF_REQUEST.json` / nicht ausführbarer Fachworkflow-Handoff-Request.

Historische funktionierende Request-first-Reparaturen wurden nachgewiesen, u. a. über PR #110/#111.

Root-Cause:
Der aktuelle Worker erzeugt die fachlichen Daten, wurde aber gleichzeitig durch die 107007-Instruktion auf
`kein Handoff-Request`
festgelegt.
Damit widersprachen Worker-Vertrag und vorhandener Adapter einander.

Commit `a5f0fba0…` hat diese widersprüchliche Sperre beim B02-Worker-Binding erneut/persistierend festgeschrieben.

#### Kontrollsystem-Fehler gefunden

Nicht nur Produktionslogik war regressiert:
der ausführbare historische Regression-Runner war selbst stale.

Befunde:
- schriftliches M28 verlangt ausführbaren Request-first-Handoff;
- ausführbares M28 prüfte stattdessen direkten ITEM_RECEIPT-Submit;
- M31 verlangte fälschlich das Fehlen von `fachworkflow_handoff`, obwohl der heutige gebundene Fachworkflow diesen benötigt;
- M26 referenzierte ebenfalls stale Semantik.

Damit konnte ein manuelles `CHECK_HISTORY: PASS` formal gesetzt werden, obwohl ausführbarer Test und schriftliche Historie nicht übereinstimmten.

Schlussfolgerung:
Ein PASS-Feld ist kein Beweis.
Historie muss ausführbar und serverseitig gegen den Kandidaten geprüft werden.

#### PR #159 – Regression-Runner-Bootstrap

Exakt eine bestehende Runner-Datei korrigiert:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`.

PR #159:
- stale M26/M28/M31-Prüfungen korrigiert;
- M28 erhielt einen Negativ-Mutanten-Selbsttest;
- normaler `hardlock`: PASS;
- `hardlock-base`: PASS;
- kein Produktionsfix.

PR #159 gemergt.
Current main:
`2f3678aa495d40e5377881a6aa3655fb60e0c12e`.

M28-Produktionsfehler dadurch ausdrücklich **nicht** repariert.

#### PR #160 – serverseitige Reparatur-Zwangsjacke

PR #160 verändert exakt eine Security-Datei:
`control/paul-scope-gate/paul_scope_gate.py`.

Aktueller Head:
`a6f6240c05adb75883416440b4618a6ce428ecc6`.

Gebundene Evidenz:
- vollständiges Ausführungs-/Testprotokoll selbst;
- current main;
- `RECOVERY_BASE_SHA`;
- aktueller Realblocker;
- autoritative Fach-Fehlerquelle;
- CURRENT_STATE;
- Paul-Pipeline-Audit;
- historische Fehlermatrix;
- vertrauenswürdiger Regression-Runner vom PR-Base/main;
- Änderungs-/Erklärungsregister;
- campusweiter Hobbyraum-Standard.

Harte Wirkung nach Aktivierung:
- manuelle `CHECK_*`-Felder sind keine Freigabeautorität;
- Quellen werden per Git-Blob gebunden;
- Historie muss ab M01 lückenlos sein, mindestens M01–M33;
- Runner/Matrix/Fehlerquelle müssen dieselbe akzeptierte Historie tragen;
- aktueller Blocker, main und letzter guter Stand müssen in den autoritativen Quellen real vorhanden sein;
- Produktionskandidat muss den kompletten vertrauenswürdigen historischen Runner PASS machen;
- Kandidat darf seinen eigenen Runner nicht zusammen mit Produktionscode ändern.


#### Vorher-/Nachher-Beweis jedes Produktionsfixes

Zusätzliche harte Bindung:
`ACTIVE_HISTORY_CASE` verbindet den aktuellen Realblocker mit genau einem historischen Regressionstest.

Für den aktuellen Blocker:
`ACTIVE_HISTORY_CASE: M28`.

Die autoritative M28-Fehlerzeile enthält exakt:
`FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`.

Vor jedem Produktionsfix erzwingt der serverseitige Gate:
1. `RECOVERY_BASE_SHA` muss als realer Git-Commit existieren und Vorfahr des current main sein;
2. der vertrauenswürdige Base-Runner läuft isoliert gegen current main;
3. current main muss exakt bei `ACTIVE_HISTORY_CASE` als erstem Fehler FAIL liefern;
4. derselbe unveränderte Base-Runner läuft isoliert gegen den Kandidaten;
5. Kandidat muss die vollständige akzeptierte Historie GESAMT PASS machen.

Damit gilt maschinell:
**erst Fehler beweisen → dann Fix beweisen**.

Ein Fix kann nicht mehr allein durch einen grünen Kandidaten legitimiert werden.

Der Gate testet zusätzlich seinen eigenen PASS-/FAIL-Auswertungsmodus bei jedem serverseitigen `verify-pr`:
- synthetischer GESAMT-PASS wird akzeptiert;
- synthetischer M28-FAIL wird bei erwartetem M28 akzeptiert;
- derselbe M28-FAIL wird bei erwartetem M29 blockiert.

#### Dauerregel für neue Fehler M34/M35/…

Neue reale Fehler dürfen nicht direkt repariert werden.

Zwingende Reihenfolge:
1. neuen realen Fehler zuerst in autoritativer Fehlerquelle erfassen;
2. separater `HISTORY_AUTHORITY_MAINTENANCE`-Kandidat nur für Matrix/Runner;
3. `HISTORY_EXPECTED_FAIL` bindet exakt den neuen/zu korrigierenden Mxx;
4. bisheriger Base-Runner muss die bisher akzeptierte Historie weiter PASS halten;
5. neuer Kandidaten-Runner muss auf dem **noch unreparierten** Stand exakt bei `HISTORY_EXPECTED_FAIL` als erstem Fehler FAIL liefern;
6. erst dann Produktionsfix;
7. Produktionsfix muss die gesamte erweiterte Historie GESAMT PASS machen;
8. danach genau ein echter 7/7-Realtest.

Damit wird jeder neue reale Fehler vor seiner Reparatur dauerhaft zu maschineller Erinnerung.
M34, M35 usw. benötigen keine neue Security-Gate-Architektur.

#### PR #160 – reale Aktivierungsgrenze

Aktueller `hardlock-base` blockiert PR #160 bereits in der immutable-Security-Prüfung:
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.

Das ist absichtlicher Selbstschutz:
`control/paul-scope-gate/` darf vom normalen PR-Weg nicht geändert werden.

Historischer Vergleich:
PR #137 hatte bis kurz vor seinem Merge denselben `hardlock-base`-FAIL und wurde anschließend über kontrollierte Admin-Wartung aktiviert.

Direkter Mergeversuch von PR #160:
GitHub verweigerte den Merge mit Repository-Rule-Verstoß:
zwei Required Checks nicht erfolgreich (ein erwarteter, ein fehlgeschlagener).

GitHub-Connectorprüfung:
- Ruleset lesen: möglich;
- Ruleset-Historie: 403 / nicht zugänglich;
- Ruleset-/Bypass-Schreibaktion: nicht verfügbar;
- `current_user_can_bypass = never`.

Codex-Security-Selbsttest:
- offizieller Cloud Entry: `CODEX_CLOUD_ENTRANCE_PASS`;
- anschließend blockierte die bestehende Single-Door-Regel die angeforderten separaten `py_compile`-/`selftest`-Befehle mit
  `EXECUTE_ONLY_CURRENT_BOUND_STEP_THEN_WRITE_RECEIPT_AND_COMPLETE`;
- damit wurden diese zwei Befehle **nicht** ausgeführt;
- kein Code geändert, kein Produktionslauf, kein Publish, kein WordPress-Write.

Status:
Das Ausführungsprotokoll ist nun selbst Bestandteil der gebundenen Evidenz: vor jedem nächsten Fix müssen aktueller Blocker, current main und `RECOVERY_BASE_SHA` auch hier real dokumentiert sein.
PR #160 ist vorbereitet, aber noch nicht auf main aktiviert.
M28-Produktionsfix bleibt bis zur Aktivierung gesperrt.

### PR #160 integriert – Maschinenbeweis aktiv

PR #160 wurde kontrolliert über den temporären Ruleset-Wartungsweg gemergt.

Exakter Security-Head:
`a6f6240c05adb75883416440b4618a6ce428ecc6`.

Merge / neuer main:
`914638e67a265cf2e8951b1177a7d80fdf904e98`.

Verifiziert auf main:
- exakt `control/paul-scope-gate/paul_scope_gate.py`;
- `ACTIVE_HISTORY_CASE`;
- `HISTORY_EXPECTED_FAIL`;
- Protokollbindung;
- current-main-Vorher-FAIL;
- Kandidaten-Nachher-PASS;
- Recovery-Ancestor-Prüfung;
- dynamische M34+-Historie;
- Gate-Selbsttests.

Keine Produktionsreparatur parallel.

Sicherheitsgrenze:
Der temporäre Ruleset-Bypass `Repository admin / pull requests only` ist nach dem Merge noch aktiv.
Bis zu seiner bestätigten Entfernung:
`FIX_FORBIDDEN`.

### Ruleset wieder geschlossen und M28-Kandidat vorbereitet

Temporärer Security-Bypass nach PR #160 entfernt und frisch verifiziert:
- `bypass_actors: []`;
- `current_user_can_bypass: never`;
- Ruleset aktiv;
- Required Checks `hardlock` und `hardlock-base` aktiv.

M28-Produktionskandidat:
- Branch `hobbyroom/m28-handoff-request-current-main-20260908`;
- Head `78263594456bb58ae004b5b064816de0f3531720`;
- Base `914638e67a265cf2e8951b1177a7d80fdf904e98`.

Geändert exakt:
1. `control/single-door-boundary/codex_current_action.py`
2. `control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json`
3. `control/startmaster0107/CURRENT_STATE.json`
4. `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`

Semantik:
- vorhandenes M28-Request-Schema wird als `request_required_fields` exponiert;
- gebundener Current Codex bleibt derselbe Fachworkflow-Worker;
- reale Fachworkflow-Ausgaben werden weiterhin durch denselben Worker erzeugt;
- danach erzeugt er exakt `FACHWORKFLOW_HANDOFF_REQUEST.json` unter `fachworkflow_handoff.request_ref`;
- vorhandener `fachworkflow_handoff.command` validiert Artefakte, führt den realen PPM-Weg aus und schreibt Fachworkflow-PASS + Item Receipt;
- erst nach `FACHWORKFLOW_PROOF_HANDOFF_PASS` läuft die bestehende Submission;
- kein zweiter Executor, keine Capability-Suche, kein neuer Adapter, kein neuer Runner.

Statische Vorprüfung:
- exakt vier Kandidatendateien: PASS;
- Current-Action-SHA → 107007 authorized_inputs: PASS;
- 107007-SHA → CURRENT_STATE execution_gate + rearm: PASS;
- CURRENT_STATE-SHA → Root: PASS;
- M28 required fields vorhanden: PASS;
- Request-Datei/ref/command in Instruktion vorhanden: PASS;
- alte Sperre `kein Handoff-Request`: nicht mehr vorhanden;
- Submission ausdrücklich erst nach Handoff-PASS.

Noch kein Integrationsbeleg.
Nächster Schritt ist der erste serverseitige Maschinen-Test.

### Erster serverseitiger Maschinen-Test PR #161

Runs:
- `hardlock` Run `34210147572` / Job `102008943659`: **PASS**;
- `hardlock-base` Run `34210147673` / Job `102008943674`: **FAIL**.

`hardlock` bestand vollständig:
- Legacy deterministic gate regression;
- Codex Cloud entrance positive/negative;
- Production continuity;
- API-frei;
- domain-blind.

`hardlock-base`:
- immutable path guard: PASS;
- danach neuer Maschinen-Gate;
- `HOBBYROOM_WORK_LOCK_SELFTEST_PASS:8/8`;
- erster Stop:
  `HOBBYROOM_ACTIVE_HISTORY_CASE_ROW_INVALID:M28`.

Root-Cause hart im auf main integrierten Gate geprüft:
`_error_row_for_case()` enthält einen doppelt escaped Markdown-Zeilenregex:
`r"(?m)^\\|\\s*" + re.escape(case) + r"\\s*\\|.*$"`.

Die autoritative Fehlerquelle besitzt dagegen korrekt die reale Zeile
`| M28 | Fachworkflow-Handoff request executable | ... FACHWORKFLOW_PROOF_HANDOFF_BLOCKED ... |`.

Einordnung:
- dies ist ein Fehler des neuen Maschinen-Gates selbst;
- nicht der M28-Produktionskandidat;
- der Gate-Lauf kam noch nicht bis zur vorgeschriebenen current-main-M28-Reproduktion und Kandidaten-GESAMT-PASS-Prüfung.

Keine Reparatur im laufenden Test.
Kein Merge.
Kein Realtest.
Kein Publish / WordPress-Write.

### Security-Parserfix PR #166 – Vorprüfung

PR #166:
`hobbyroom/security-fix-m28-row-parser-20260908`
Head `a742c5c917b5e6fe164be2a6267470de89e9d744`.

Diff:
- ausschließlich `control/paul-scope-gate/paul_scope_gate.py`;
- +1 / -1;
- korrigiert ausschließlich `_error_row_for_case()` von doppelt escaptem auf echten Markdown-Zeilenregex.

Lokale Positiv-/Negativprüfung PASS:
- real M28 = 1;
- wrong case = 0;
- embedded fake = 0;
- duplicate = 2 -> Block.

GitHub:
`hardlock-base` Run `34226241411`, Job `102060960182`.
Immutable path guard blockiert erwartungsgemäß:
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
`PATH_GUARD_SELFTEST_PASS`.

Keine M28-Produktionsdatei geändert.
Keine Reparatur an PR #161.

### PR #166 integriert

Security-Parserfix gemergt.

Merge / neuer main:
`755b531ec08298a86cb0342c2db8c81f5b4df6f9`.

Verifiziert:
- genau der korrigierte M28-Zeilenregex auf main;
- keine M28-Produktionsdatei mitgemergt.

Temporärer Ruleset-Bypass ist noch aktiv.
Bis zu seiner bestätigten Entfernung:
`FIX_FORBIDDEN`.

Anschließend wird PR #161 nur auf den neuen main synchronisiert, ohne Änderung seiner vier M28-Dateiinhalte, und derselbe Maschinen-Test erneut ausgelöst.

### Ruleset nach PR #166 wieder geschlossen / PR #161 Synchronisation vorbereitet

Nach Merge von PR #166:
- temporärer `Repository admin / For pull requests only`-Bypass entfernt;
- frisch verifiziert: `bypass_actors: []`;
- `current_user_can_bypass: never`;
- Required Checks `hardlock` + `hardlock-base` unverändert aktiv.

PR #161 blieb inhaltlich unverändert.

Für den Wiederholungstest wurde ein reiner Synchronisations-Mergecommit **noch ohne Branch-Ref-Update** erzeugt:
`26d7b5b53044729ab6350f88d16d4ac0f6cacd03`.

Baum:
- Basis = current main `755b531ec08298a86cb0342c2db8c81f5b4df6f9`;
- exakt die vier bisherigen PR-#161-M28-Blobs darübergelegt;
- Parents = bisheriger PR-#161-Head `78263594456bb58ae004b5b064816de0f3531720` + current main.

Damit:
- Parserfix aus PR #166 ist im Kandidaten-Ausgangsstand enthalten;
- die vier M28-Dateiinhalte sind byte-identisch zum ersten PR-#161-Test;
- kein neuer Produktionsfix zwischen den Tests.

### Zweiter serverseitiger PR-#161-Test – shallow ancestry false negative

Re-Run `hardlock-base`:
Run `34228573901`, aktueller Job `102069474348`.

PASS bis zum Stop:
- immutable path guard;
- Work-Lock-Selbsttest 8/8;
- Evidenz-Selbsttest 10/10;
- Runner-Modus-Selbsttest 3/3;
- M28-Reproduktionsmodus-Selbsttest;
- `HOBBYROOM_WORK_LOCK_PR_PASS`.

Stop:
`HOBBYROOM_RECOVERY_BASE_NOT_ANCESTOR:de21f6cd35c60849c551fd82f78e75ce57c99fab:MAIN=755b531ec08298a86cb0342c2db8c81f5b4df6f9`.

GitHub-Commitgraph separat geprüft:
- `de21f6… -> 755b531e…`: status ahead, 176 Commits;
- Merge-Base exakt `de21f6…`;
- Gegenrichtung status behind;
- Goldmaster existiert real und ist Vorfahr.

Workflow-Ursache:
Trusted Base Checkout `fetch-depth: 1`.
Candidate fetch `--depth=1`.
Damit kann lokale `git merge-base --is-ancestor` die reale Ahnenkette nicht vollständig sehen.

Keine Änderung am M28-Kandidaten.
Kein Merge.
Kein Realtest.

### Security-Wartungs-PR #177 – Vorprüfung

PR #177:
`hobbyroom/security-fix-shallow-recovery-ancestry-20260908`
Head `f69b415099f7d9f936a81f21a56bbaa408e8dfc7`.

Diff:
- ausschließlich `control/paul-scope-gate/paul_scope_gate.py`;
- +2/-0;
- bei shallow Repository unshallow trusted base history;
- danach unverändert `cat-file` + `merge-base --is-ancestor`.

Lokale Positivprüfung mit echtem shallow Git-Repo:
- vor unshallow kein belastbarer Ahnenbeweis;
- nach unshallow korrekter PASS.

GitHub:
Run `34229441561`, Job `102071584302`.
Erwarteter Stop:
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
`PATH_GUARD_SELFTEST_PASS`.

Keine Änderung an PR #161 oder M28-Inhalten.

### PR #177 integriert / Kontrollsystem eingefroren

PR #177 wurde integriert.
Neuer main:
`a61a380e948e15f2ed3ce5ddec41b128efbe7ae6`.

Danach Ruleset wieder geschlossen:
kein Bypass, `hardlock` + `hardlock-base` aktiv.

Entscheidung:
Keine weitere Ausbau-/Absicherungsrunde am Kontrollsystem.
Ab hier ausschließlich eigentliche Produktionsarbeit.

PR #161 wird nur technisch mit current main synchronisiert.
Test-Head:
`a2a4aca682e46ac5913d4cad554a604f4edd8d59`.

Die vier M28-Dateiblobs bleiben identisch.

