# PFERDE ATELIER – TEXT – HOBBYRAUM

STAND: 2026-09-14
STATUS: SYSTEM 4 – NEUER REALER CODEX-EIN-ARTIKEL-LAUF ANGENOMMEN – ENDERGEBNIS OFFEN

## ÄLTERER OFFIZIELLER STAND

M37 / offizieller 107007-Stand vom 2026-09-11 bleibt historische Referenz und ist nicht mit dem isolierten System-4-Kandidaten gleichzusetzen.

History:
- PR248;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS.

Produktfix:
- PR247;
- Head `59ad44da3d89769c05f0725f9929135b0262f4dd`;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS.

Offizieller damaliger main:
`f1d1605f18bd23d9189f89ad173598958718d08a`

M01–M37 sind integriert.

## SYSTEM 4 – AKTUELLER HOBBYRAUMSTAND 2026-09-14

Ursächlich geschlossene Fehlerklasse:
Ein späterer Prüfer beanstandet einen von einer früheren Maschinenstufe erzeugten/bindenden Wert. Reparierbare Fehler dürfen nicht pauschal terminal abbrechen.

Zentrale Rückrouten:
- Titel / Kategorie / Slot -> Parent-Maschine;
- Links -> Context-Binder;
- Quellen / Facts -> Research-Stufe;
- Textkörper -> Same-Article-Repair.

Frischer kompletter Positiv-/Negativ-Artikeltest:
- Run `34882998263`;
- neuer Job-Versuch `104108404452`;
- Point0 positiv/negativ PASS;
- Supervisor-Grenzen PASS;
- Produktionsbindung PASS;
- Single-Button-Negativgrenze PASS;
- verbotener SEO-Provider PASS;
- gesamte System-4-Suite PASS;
- stage-aware Reparaturrouten positiv/negativ PASS;
- echtes LanguageTool 6.8 PASS;
- echter PPM 6.7.9 PASS;
- drei neue Realthemen PASS;
- 1 Artikel Start -> Datei/Handoff PASS;
- 3 Artikel Start -> Datei/Handoff PASS.

Sauberer Produktionsstand nach Router:
`e4ef916c89cf681aa8a2c4c1e5ff0ef07fc88058`

Immutable Base Hardlock:
Run `34883319385` -> PASS.

## AKTUELLER REALTEST

Neuer Artikel:
`Pferdeanhänger richtig beladen und Gewicht sicher verteilen`

Target Keyword:
`Pferdeanhänger richtig beladen`

Quellen vor Codex gebunden:
- FN Pferdetransport;
- § 22 StVO;
- § 34 StVZO;
- § 44 StVZO.

Ein falscher Snapshot-Hash wurde vor Codex beim Gegencheck erkannt und korrigiert; der fehlerhafte Stand wurde nicht gestartet.

Aktueller Produktions-Head mit korrigierter Kapsel:
`b66467468ca3f1cab9e3b86a5a96a7d7c1c70eaa`

Hardlock auf diesem Head:
Run `34884562137` -> PASS.

Codex-Auftrag:
PR #259, Kommentar `5669182565`.

Status:
Codex-Connector `eyes` -> Auftrag angenommen.
Terminales Endergebnis derzeit OFFEN.

## NEXT ACTION

Nur den bereits angenommenen Codex-Lauf zu Kommentar `5669182565` auswerten.

Keinen zweiten Artikel starten.
Keinen Parallel-/Ausweichlauf starten.
Kein Merge.
Kein Publish.
`publish_allowed=false`.

Bei PASS vollständigen End-to-End-Nachweis bis Batch Gate, V2-Handoff, Inline-Pack/Unpack und bytegleicher Rekonstruktion dokumentieren.

Bei Fehler exakt erste Fehlerstufe, Fehlercode, Feld, Ist/Soll und zuständige Reparaturroute dokumentieren.

## VERWEISE

- CURRENT: `CURRENT_STATE.md`
- aktuelle Fehlerquelle des offiziellen 107007-Stands: `QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md`
- M37-Protokoll: `M37_ARBEITSPROTOKOLL_20260911.md`
- System-4-Protokoll 14.09.: `SYSTEM4_ARBEITSPROTOKOLL_20260914.md`
- Standard: `protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md`
