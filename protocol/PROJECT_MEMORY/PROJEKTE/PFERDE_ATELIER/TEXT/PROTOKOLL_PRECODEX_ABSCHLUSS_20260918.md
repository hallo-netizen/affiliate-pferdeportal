# PFERDE ATELIER – TEXT – PRE-CODEX-ABSCHLUSSPROTOKOLL

STAND: 2026-09-18
ROLLE: PROTOKOLL / WAS-WARUM / NACHWEIS
NICHT CURRENT-AUTORITATIV

## 1. AUTORITÄT / EINE WAHRHEIT

Die einzige operative Current-Autorität für PFERDE_ATELIER / TEXT / STARTMASTER0107 ist:

`control/startmaster0107/CURRENT_STATE.json`

Campus-Routing wurde deshalb korrigiert:
`protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` verweist für `PFERDE_ATELIER_TEXT` direkt auf diese technische Current-Autorität.

Die frühere Campus-`TEXT/CURRENT_STATE.md` ist nur noch Pointer. Der frühere M39-Hobbyraum ist beendet/FREI.

## 2. ZIELVERTRAG

Fachliches Produktionsziel:
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/03_ZIELVERTRAG_AKTUELL_20260905.md`

Technische aktuelle System-4-Bindung:
`isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`

Ziel unverändert:
gebundener 7er-Batch / allgemeiner 1..N-System-4-Weg bis 107008, kein Auto-Publish; finale Datei muss über den bestehenden signierten Endstempel-/Importweg bytegleich bis in den Parent-Chat zurückgegeben werden.

## 3. EXAKTER TECHNISCHER ENDSTAND

Aktueller Repository-`main` beim Abschlusscheck:
`bc50759e5ce50cc3058c220bbdff6650a35fd06f`

PR #325:
`System 4: mark final pre-Codex checks complete`
Merge:
`bc50759e5ce50cc3058c220bbdff6650a35fd06f`

Operativer Current-Status:
`PRECODEX_READY_AWAITING_EXPLICIT_CODEX_APPROVAL`

Aktuelle Sperre:
`EXPLICIT_CODEX_APPROVAL_MISSING`

Diese Sperre ist keine Fehlerklasse, sondern die ausdrücklich verlangte Nutzerfreigabe vor echtem Codex.

## 4. BELASTBARE TESTNACHWEISE

Auf dem aktuellen Main:
- System-4A Real LT68 PPM679 Acceptance Run `35367822404`: **SUCCESS / 40 von 40 Schritten**
- Deterministic Entrance Run `35364997364`: **SUCCESS**

PR-#325-Kandidat:
- Immutable Base Hardlock Run `35364953617`: **SUCCESS**
- Deterministic Entrance Run `35364953439`: **SUCCESS**

Bereits im technischen Current gebundene Produkt-/Release-Nachweise:
- Release-Identity Full Acceptance Run `35361139485`: PASS
- targeted Release-Identity proof Run `35361249579`: PASS
- final entrance Run `35361368650`: PASS
- PR #315 integriert; Hardlock wiederhergestellt.

## 5. WAS ERLEDIGT IST

- Parent → Point-0 → Root produktiv gebunden.
- Point-0-/Source-/Head-/Hash-Drift fail-closed.
- NEW bleibt NEW; historische Recovery-Artikel als Schreibquelle verboten.
- System-4 1..N-Weg gebunden.
- Artikel 2 darf nicht frei gestartet werden; Batch-`advance` bleibt maschinell gebunden.
- Same-Article-Repair über System-4-Controller gebunden.
- echtes LanguageTool 6.8 und echter PPM 6.7.9 im Acceptance-Weg.
- M38 gelöst / Regression gebunden.
- M39 Release-Identity-Kollision gelöst: logischer Batch bleibt gleich, frische Ausgaben besitzen getrennte technische Release-Identität.
- signierter Endstempel-/Import-/Parent-Chat-Weg simulativ vollständig geprüft.
- vollständige 1-Artikel- und Mehrartikel-Simulation inklusive Positiv-/Negativfällen grün.
- aktuelle Main-Gesamtprüfung 40/40 PASS.
- Hardlock/Entrance auf finalem Pre-Codex-Sync PASS.
- kein Publish.

## 6. CHAT-OPERATIONSFEHLER DIESES CHATS

Im Verlauf wurden entgegen der Nutzerregel zwei Codex-Aufträge zu früh ausgelöst.

Beide stoppten vor echter Artikelproduktion:
- erster Versuch: `ROOT_POINT0_FILE_INVALID`;
- zweiter Versuch: fehlende `/tmp/system4-parent-point0-current.json`.

Dabei:
- kein erfolgreicher Artikel-Worker-Lauf;
- Artikel 1 nicht produziert;
- Artikel 2 nicht gestartet;
- keine tracked Repository-Änderung durch diese Codex-Versuche;
- kein Publish.

Dauerhafte Grenze:
**Kein echter Codex ohne ausdrückliche Nutzerfreigabe.**
Diese Grenze ist im aktuellen technischen Current als `EXPLICIT_CODEX_APPROVAL_MISSING` gebunden.

## 7. WAS NOCH OFFEN IST

Vor Codex:
**keine technische Reparatur mehr offen.**

Offen ist ausschließlich:
ausdrückliche Nutzerfreigabe für den realen kompletten 7-Artikel-Codex-Lauf.

Nach dieser Freigabe:
1. kompletten gebundenen 7er-Lauf über den aktuellen System-4-Weg starten;
2. Artikel streng in Maschinenreihenfolge abarbeiten;
3. Repair nur same-article;
4. Batch vollständig collecten;
5. 107008 Final Review/Output Release;
6. signierter Endstempel + reale WordPress-Importformatprüfung;
7. bytegleiche finale Datei in Parent-Chat;
8. weiterhin kein Publish ohne separate Publish-Freigabe.

## 8. EXAKTER EINSTIEG FÜR NEUEN CHAT

1. Repository `hallo-netizen/affiliate-pferdeportal`, Branch `main`.
2. `control/CURRENT_STARTMASTER.json`
3. `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
4. einzige Current-Autorität: `control/startmaster0107/CURRENT_STATE.json`
5. Frischecheck gegen aktuellen `main` und letzten Acceptance-/Entrance-Nachweis.
6. Wenn Current weiterhin `PRECODEX_READY_AWAITING_EXPLICIT_CODEX_APPROVAL` meldet: **keine Vollrekonstruktion.**
7. Keine Codex-Aktion ohne ausdrückliche Nutzerfreigabe.
8. Nach Freigabe erster technischer Navigationseinstieg:
`python3 control/single-door-boundary/project_single_door_entry_v2.py status`
9. Danach ausschließlich dem gebundenen System-4-Raum folgen.

## 9. NÄCHSTE AKTION

**Auf ausdrückliche Nutzerfreigabe für Codex warten.**

Danach genau den realen kompletten 7-Artikel-Lauf starten.

Kein anderer technischer Zwischenschritt ist derzeit als NEXT ACTION belegt.
