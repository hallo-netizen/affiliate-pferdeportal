# SYSTEM 4 — REALER 1-ARTIKEL-TEST — BRANCH-IDENTITÄTSBLOCKER — 2026-09-13

Status dieses Dokuments: **Beleg-/Fehlerprotokoll, keine zweite CURRENT_STATE.** Aktuelle System-4-Statuswahrheit bleibt `isolated_system4/README.md`.

## Freigabe und Ausgangslage

Der Nutzer gab genau **einen realen 1-Artikel-Codex-Testlauf** frei und verlangte ausdrücklich die Protokollierung.

Getesteter PR-Head vor Laufstart:

`66403e6143858205573915355d56335902c04bce`

Vor dem Live-Lauf waren auf bytegebundenem Stand lokal nachgewiesen:

- 93/93 Unittests PASS;
- kompletter lokaler Root-bis-Datei-Acceptance-Lauf 8/8 PASS;
- reales LanguageTool 6.8;
- reales PPM 6.7.9;
- Same-Article-Repair;
- Batch-Gate;
- V2-Handoff und bytegenaue Dateirekonstruktion;
- Immutable Base Hardlock SUCCESS.

Kein Merge, kein Publish.

## Gebundener Testartikel

- `article_type`: `Beratung`
- `category`: `putzbox-beratung`
- `plan_slot`: `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- `target_keyword`: `Putzbox für Pferde`
- Titel: `Putzbox für Pferde richtig auswählen`
- `batch_sha256`: `7b471ee2acef71531b067d2a8324a72580f4d9c8bc8d67412d021c1facf2e6e3`
- `item_count=1`
- `publish_allowed=false`

Der Auftrag verlangte den vollständigen realen Weg bis zur kanonischen `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json` und zum kompletten `SYSTEM4_PARENT_CHAT_INLINE_V2`-Relay.

## Reale Ausführung

Codex nahm den Auftrag an und führte diesmal **nicht** die alte Legacy-Cloud-Entry-Strecke aus.

Tatsächlich erreicht wurde:

`SYSTEM4_ROOT_INDEXED_INGRESS`

Ausgeführt wurde:

`python3 isolated_system4/root_entry.py start-stdin /tmp/system4-one-article-production`

Terminaler Hard-Blocker:

`SYSTEM4_HARD_BLOCKER:ROOT_ENTRY_BRANCH_NOT_SYSTEM4`

`status=SYSTEM4_ROOT_ENTRY_FAIL`

`error=ROOT_ENTRY_BRANCH_NOT_SYSTEM4`

Danach wurde korrekt fail-closed gestoppt.

Nicht gestartet wurden:

- Recherche;
- Facts;
- Fact-Pack/Context;
- Draft;
- LanguageTool;
- PPM;
- Repair;
- Batch-Gate;
- Handoff;
- Dateirekonstruktion.

Keine Repository-Datei wurde durch Codex geändert oder committed. Kein Merge, kein Publish.

## Gegenüber dem vorherigen Real-Lauf

Der vorherige reale 1-Artikel-Versuch wurde **vor System 4** durch die alte offizielle Runtime-Entry-Strecke mit `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING` blockiert.

Dieser Fehler trat hier **nicht erneut** auf.

Damit ist real bewiesen:

- `AGENTS.override.md` brachte Codex diesmal bis zur System-4-Root-Tür;
- die alte Legacy-Cloud-Entry-Strecke war nicht der aktuelle Blocker;
- der neue Blocker liegt innerhalb der System-4-Root-Identitätsprüfung.

## Konkreter technischer Fehler

`isolated_system4/root_entry.py` enthält aktuell:

- festen erwarteten Namen `hobbyroom/system4-true-single-room-v1`;
- `_branch()` über `git branch --show-current`;
- Fail-Closed-Bedingung: Rückgabewert muss exakt diesem symbolischen Branch-Namen entsprechen.

Der reale Codex-Lauf scheiterte genau an dieser Bedingung.

**Nicht bewiesen und deshalb nicht behauptet:** Welchen konkreten Branch-String Codex Cloud in diesem Checkout geliefert hat oder ob der Checkout detached war. Der Codex-Abschluss hat nur den terminalen Fehler zurückgegeben, nicht den tatsächlichen Wert von `git branch --show-current`.

## Warum der lokale Volltest diesen Fehler nicht fand

Die positiven Tests in `test_root_entry.py` starten `root_entry.py` im vorhandenen lokalen Checkout. Der lokale Testcheckout lag auf dem erwarteten symbolischen Branch und erfüllte deshalb die Branch-Namensprüfung.

Es gab keinen positiven Test, der eine Codex-/PR-Checkout-Situation mit anderer oder fehlender symbolischer Branch-Bezeichnung nachstellt.

Damit war der bisherige lokale Root-bis-Datei-Nachweis für die **lokal getestete Checkout-Identität** korrekt, aber als Beweis für die reale Codex-Cloud-Checkout-Semantik zu breit interpretiert.

## Status / Next Action

Aktueller System-4-Blocker:

`S4-BLOCK-REAL-ROOT-BRANCH-IDENTITY`

Bis zur lokalen Reparatur gilt:

- **kein weiterer Codex-Lauf**;
- keine Änderung an Textmaschine, LT, PPM, Batch-Gate, Handoff, WordPress oder Design;
- keine Rückkehr zur Legacy-Cloud-Entry-Strecke;
- kein Merge/Publish.

Der nächste technische Schritt muss ausschließlich die Root-Checkout-Identität betreffen:

1. symbolischen Branch-Namen nicht mehr als alleinige System-4-Identität verwenden;
2. eine fail-closed, PR-/Cloud-taugliche Checkout-/Content-Identitätsbindung definieren;
3. positive und negative lokale Tests für die reale Cloud-Checkout-Semantik ergänzen;
4. danach den **kompletten** lokalen Root-bis-Datei-Lauf erneut positiv/negativ ausführen;
5. Immutable Base Hardlock erneut PASS;
6. erst danach und nur mit erneuter ausdrücklicher Nutzerfreigabe ein weiterer realer 1-Artikel-Codex-Lauf.

Dieses Protokoll wertet den Lauf ausdrücklich als **FAIL/BLOCKED**, nicht als Teil-PASS.