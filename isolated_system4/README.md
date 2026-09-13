# SYSTEM 4 — TRUE SINGLE ROOM

Status: **LOKALER ROOT-TO-FILE-PFAD INKL. DETACHED HEAD POSITIV/NEGATIV BEWIESEN / REALER CODEX-WIEDERHOLUNGSLAUF NOCH NICHT AUSGEFÜHRT / isolated prototype / test only.** Kein Merge, kein Publish.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand in `control/startmaster0107/CURRENT_STATE.json` bleibt getrennt und unverändert.

## Verbindliches Ziel

`gebundene Metadaten -> System-4-Root-Einstieg -> Codex recherchiert -> Research Evidence -> Facts/Fact-Pack -> Context -> Draft -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-Gate -> V2-Handoff -> Parent-Chat-Rekonstruktion -> exakte WordPress-JSON`

Codex bleibt der eine fachliche Worker. System 4 übernimmt keine alte Legacy-Orchestrierung.

## Aktueller Root-Einstieg

Der reale Ein-Artikel-Lauf vom 2026-09-13 erreichte System 4, stoppte aber vor Recherche mit:

`ROOT_ENTRY_BRANCH_NOT_SYSTEM4`

Damit war nachgewiesen, dass die damalige Root-Identitätsprüfung falsch war: sie verlangte den symbolischen lokalen Branch-Namen `hobbyroom/system4-true-single-room-v1`. Dieser reale Fehler ist im Protokoll festgehalten:

`PROTOKOLL_REALRUN_20260913_ONE_ARTICLE_BRANCH_IDENTITY_BLOCKER.md`

Die Root-Prüfung wurde anschließend geändert. Sie bindet jetzt **nicht mehr den Branchnamen**, sondern den tatsächlich geladenen kritischen System-4-Inhalt über `system4_root_manifest_sha256`.

Geprüfter Manifestwert:

`3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

Die Prüfung ist fail-closed: fehlende/abweichende Bindung, manipulierte kritische Dateien, fehlende getrackte Dateien, falscher Git-Root oder dirty kritische Dateien blockieren.

## Aktueller Testnachweis

Autoritativer Beleg für diese Korrektur:

`TESTNACHWEIS_20260913_CHECKOUT_IDENTITY_MANIFEST.md`

Ausgeführt ohne Codex:

- Root-Eingangstests: **14/14 PASS**;
- übrige Regressionen: **87/87 PASS**;
- Gesamt: **101/101 PASS**;
- vollständiger Root-bis-Datei-Acceptance-Lauf mit sichtbarem Branchnamen: **10/10 PASS**;
- vollständiger Root-bis-Datei-Acceptance-Lauf unter **detached HEAD / leerem Branchnamen: 10/10 PASS**;
- echter LanguageTool-6.8-Pfad im Acceptance-Lauf;
- echter PPM-6.7.9-Pfad im Acceptance-Lauf;
- Same-Article-Repair;
- Batch-Gate;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- Inline-Pack / Inline-Unpack;
- bytegenaue WordPress-Datei.

Enddatei beider kompletten Acceptance-Läufe:

- 1 Artikel;
- Revision 2;
- 66753 Bytes;
- SHA256 `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`.

Geprüfte Code-Blobs:

- `root_entry.py` -> `7624a851432f7e0a8575a8421e33cfabfe29794d`
- `test_root_entry.py` -> `593a39d78b396515e72015d85ac7488637073d5b`
- `full_local_acceptance.py` -> `0fe61d04c8656c87727862d5b587530696d1bf50`

Code-Head `18f16610e72e9d32f46827cd0c801786f79a0320`: Immutable Base Hardlock **SUCCESS**, Run `34752658005`.

## Beweisgrenze

**Bewiesen:** der technische Root-Einstieg und die komplette lokale Root→Datei-Kette funktionieren sowohl mit beliebigem symbolischem Branchnamen als auch mit detached HEAD, solange exakt die gebundenen kritischen System-4-Bytes geladen sind. Falsche/fehlende/manipulierte Bindungen blockieren.

**Nicht bewiesen:** ein neuer realer Codex-Artikel-Lauf nach dieser Korrektur. Seit dem Branch-Identity-Blocker wurde kein weiterer Codex-Lauf gestartet.

Deshalb gibt es ausdrücklich noch **keinen REAL-CODEX-PASS**.

## Universelle Produktionsgrenze

- exakt die nichtleere gebundene Item-Menge;
- `1..N`, keine künstliche System-4-Obergrenze;
- `article_type` kommt aus Metadaten, keine System-4-Typ-Whitelist;
- `publish_allowed=false`;
- Signing/ENDSTEMPEL aus;
- kein Merge, kein Publish.

## Unverhandelbare Grenzen

- Textmaschine/content rules READ-ONLY;
- PPM 6.7.9 READ-ONLY;
- LanguageTool 6.8 unverändert;
- PSERC/PSTE-Fachregeln READ-ONLY;
- WordPress-Plugin, Theme/CSS, Designregeln READ-ONLY;
- Same-Article-Repair nur über Controller;
- `controller.py fullcheck` bleibt einziger Produktions-Prüforchestrator;
- keine Legacy-/STARTMASTER-/H7-/H8-/ACM-/System-3-Laufzeitabhängigkeit;
- finale geprüfte Artikelbytes werden nach dem Fullcheck nicht mehr transformiert.

## HOBBYRAUM / NEXT ACTION

Status: **LOKAL GRÜN / REAL-CODEX-NACHWEIS AUSSTEHEND.**

Nächster Schritt ist ausschließlich ein neuer **einzelner realer gebundener Artikel-Testlauf**, aber nur nach ausdrücklicher Nutzerfreigabe. Dieser Lauf muss mit dem aktuellen `system4_root_manifest_sha256` starten und entweder die komplette Kette bis zur bytegenau rekonstruierten WordPress-Datei durchlaufen oder am ersten realen Blocker fail-closed stoppen.

Bis dahin: kein weiterer Codex-Lauf, kein Merge, kein Publish.
