# STARTMASTER0107 – 16er Live-Produktion – Arbeits-/Nachweisprotokoll 2026-09-26

## Rolle dieses Dokuments

Dieses Dokument ist ausschließlich **Historie/Nachweis (WAS/WARUM)**.

Es ist **keine CURRENT-Autorität**, enthält **keine eigenständige NEXT ACTION** und darf nicht zur Rekonstruktion eines aktuellen Status gegen die zuständige Current-Autorität verwendet werden.

Aktuelle Wahrheit ausschließlich über:

`control/CURRENT_STARTMASTER.json`
→ `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
→ `control/startmaster0107/CURRENT_STATE.json`

Frischepolicy:
`READ_CURRENT_AUTHORITY_AND_ONLY_CHECK_DELTA`.

## Zielbindung

Autoritative Zielquelle unverändert:

`control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json`

Ziel:
`MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`.

Keine Änderung an LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL, Qualitätsregeln oder Publish.

## Tatsächlich ausgeführte Arbeit

### Bestehender Start / bestehende Produktionskette

- Zentraler Startlauf: `36248438204` – SUCCESS.
- Pferdeatelier-Receiver: `36248446685` – SUCCESS.
- Batch SHA-256: `df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0`.
- Persistierter Recherchebestand wurde weiterverwendet; kein Recherche-Neulauf.
- Bound Worker: `BOUND_CHAT_WORKER`.
- Bestehende Produktionslogik unverändert: `production_bridge.py`, `progress_guard.py`, `universal_reentry_guard.py`.

### LanguageTool-6.8-Recovery

Der frühere Blocker `LANGUAGETOOL_6_8_HASH_BOUND_JAR_MISSING_IN_BOUND_CHAT_WORKER_ENVIRONMENT` wurde ohne Checker-/Regeländerung beseitigt.

Gebundene Originalidentität:

- LanguageTool: 6.8 / Bestand 43.
- Original-ZIP SHA-256:
  `6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d`.
- Commandline-JAR SHA-256:
  `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`.

Nachgewiesener früherer SUCCESS-Lauf:
`36055683717`, ZIP-Hash PASS und JAR-Hash PASS.

Für die aktuelle Recovery wurde der bestehende historische Testbranch
`hobbyroom/system4a-startgate-test-20260914`
nur temporär als Ausführungsfläche benutzt, um exakt die bereits gebundenen Originalbytes zu exportieren.

Temporäre Exportläufe:
- `36252026526`: JAR-Export nach erfolgreichem Original-ZIP-/JAR-Hashcheck.
- `36252102872`: vollständiges Original-ZIP exportiert.

Der Testbranch wurde anschließend wieder auf seinen vorherigen Stand
`602e383d1906c5ea2a53b1f103fa70c657f0243e`
zurückgesetzt.

Keine dauerhafte Produktionsroute über diesen Hobbyraum/Testbranch angelegt.

### Reale Artikelproduktion

Im bestehenden Bound-Worker-Checkpoint wurden die Artikel 0 bis 9 real durch die unveränderten Prüfer geführt.

Belegter Stand bei Abschluss dieses Protokolls:

- Artikel 0–9: LT 6.8 PASS.
- Artikel 0–9: PPM 6.7.9 PASS.
- Artikel 10: echter Draft im laufenden Produktionscheckpoint gespeichert.
- Artikel-10-Draft SHA-256:
  `6f649bd208f2df8bae6fd99edfa3b3b8115d65713d54c3e893d25717b14225b8`.
- Checkpoint-Vertrags-Hash:
  `16e52fcfa669d5a8c869d29f96ce3dccac6102c700b5cd1eb0d423156c8ab252`.
- Exakte Datei-SHA-256 des gespeicherten Checkpoint-JSON:
  `8140b805c88d919748d8b0508d90d215d7bc41b32c4e1909189cfd944af97a36`.
- Publish: nicht ausgeführt.

Artikel 10 wurde zusätzlich auf einer Testkopie bearbeitet. LT 6.8 war dort bereits PASS; beim Abbruch der Testbearbeitung blieben noch PPM-Textqualitätsbefunde zu Satzdopplungen und Tabellen-Eigenständigkeit. Diese Testkopie ist **kein Ersatz für den echten Checkpoint** und keine Current-Wahrheit.

### Recovery-Evidence

Der aktuelle lokale Arbeitsstand wurde zusätzlich als Recovery-Evidence gesichert:

`/Pferdeatelier/Produktionssicherung/PFERDE_ATELIER_16ER_LIVE_RECOVERY_CHECKPOINT36_20260926.zip`

SHA-256:
`2784118ec5644d3ee8139970528cc98987dfb0abec64d544c4cbef48d38ffda8`.

Rolle:
**Recovery-Evidence only – nicht Current, nicht NEXT-ACTION-Quelle.**

Das Paket enthält den aktuellen Produktionscheckpoint, Binding sowie die bisherigen Artikel-/Workspace-Spuren.

## Wiederkehrende Reparaturmuster – nur Analysevormerkung

Während Artikel 0–9 traten wiederholt Textreparaturen auf, insbesondere:

- LT-Wortwiederholungen bzw. unnatürliche Wortbildungen;
- PPM-Satzdopplungen;
- zu geringe Tabellen-Eigenständigkeit;
- zu schwache sichtbare Faktenspur in kurzen Listen-/Tabellenfeldern;
- fehlender gebundener Suchbegriff in einzelnen Überschriften;
- vereinzelt Mindestwortzahl knapp unterschritten.

Diese Punkte sind **keine Änderung der Qualitätsregeln**. Sie werden erst nach Abschluss des laufenden 16er-Laufs als mögliche Geschwindigkeitshebel analysiert.

Vom Nutzer ausdrücklich gewünschte spätere Vergleichsfragen:

1. aktueller 16er-Lauf gegen den deutlich schnelleren früheren 7er-Testlauf;
2. alle Befunde eines Artikels möglichst gebündelt statt unnötig seriell bearbeiten;
3. dem Schreiber bekannte feste Prüfkriterien bereits vor dem Erstentwurf vollständig bereitstellen;
4. Zeitanteile Schreiben / LT / PPM / Reparaturschleifen / Übergaben vergleichen;
5. nur Beschleunigungen übernehmen, die **keinen Qualitäts-, Gate- oder Sicherheitsverlust** verursachen.

Während des laufenden 16er-Laufs wurde bewusst **keine Geschwindigkeitsarchitektur verändert**.

## Werkzeugregel – Klarstellung

Vom Nutzer erneut klargestellt:

- Codex und GitHub dürfen während Fixes und Produktion bei Bedarf benutzt werden.
- Im **endgültigen Ergebnis / finalen Produktionsweg** dürfen Codex und GitHub keine Abhängigkeit, kein Controller und keine Runtime-Voraussetzung bleiben.

Diese Klarstellung ändert keine Qualitätsregel und begründet keinen neuen Produktionsweg.

## Current-Synchronisierung

Abschluss-/Frischecheck ergab, dass die bisherige Current-Autorität noch den bereits beseitigten Artikel-0-LT-Runtimeblocker enthielt.

Minimaler Current-Sync:
- PR #437
- Merge-SHA: `2833e02392f89e17040d192059d2e9492004515e`
- exakt zwei Dateien:
  - `control/startmaster0107/CURRENT_STATE.json`
  - `control/startmaster0107/PFERDE_ATELIER_START_HERE.json` ausschließlich Current-Hash-Sync.
- Deterministic Entrance Gate Run `36258577132`: SUCCESS.
- Immutable Base Hardlock Run `36258577133`: SUCCESS.

## Nicht betroffen

- Plugins: nicht betroffen.
- Plugin-Ausgabeartefakte: nicht betroffen.
- Zielvertrag: unverändert.
- Publish: nicht ausgeführt.
- PSERC: für den laufenden 16er-Batch noch nicht erreicht.
- ENDSTEMPEL: für den laufenden 16er-Batch noch nicht erreicht.
- Neue Architektur: keine.
- Neue Produktionsroute: keine.
- Recherche-Neulauf: keiner.

