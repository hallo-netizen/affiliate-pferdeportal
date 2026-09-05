# STARTMASTER0107 – VOLLSTÄNDIGES PROTOKOLL 30.08.–05.09.2026

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
