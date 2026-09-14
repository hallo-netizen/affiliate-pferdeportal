# PFERDE ATELIER – TEXT – SYSTEM 4 – ARBEITSPROTOKOLL 2026-09-14

## STATUS

System 4 wurde nach wiederholten Live-Abbrüchen ursächlich nachgeschärft. Schwerpunkt: reparierbare Fehler dürfen nicht pauschal den gesamten Artikel beenden, sondern müssen zur zuständigen Maschinenstufe zurückgeroutet werden.

## URSÄCHLICH GESCHLOSSENE FEHLERKLASSE

Bekanntes Fehlermuster:
- eine frühere Maschinenstufe erzeugt/bindet einen Wert;
- ein späterer echter Prüfer beanstandet diesen Wert;
- bisher führte das trotz Reparierbarkeit teilweise zum terminalen Abbruch.

Neue zentrale Rückroute:
- Titel / Kategorie / Slot -> Parent-Maschine;
- Links -> Context-Binder;
- Quellen / Facts -> Research-Stufe;
- Textkörper -> Same-Article-Repair.

Ziel: reparierbarer Fehler -> zuständige Vorstufe -> Reparatur/Neubindung -> erneute echte Prüfung -> Weiterlauf desselben Artikels. Nur echt nicht reparierbare Fehler dürfen terminal blockieren.

## FRISCHER KOMPLETTER ARTIKELTEST POSITIV / NEGATIV

Frisch neu ausgeführt, kein alter PASS übernommen.

Run: `34882998263`, neuer Job-Versuch `104108404452`.

PASS:
- Python syntax;
- Point0 prepared -> finalized source-bound lifecycle;
- Point0/Supervisor/Controller hard boundary;
- Machine production binding hard boundary;
- Single-button hard negative boundary;
- Forbidden SEO provider hard boundary;
- gesamte bestehende System-4-Suite;
- neue stage-aware Reparaturrouten positiv/negativ;
- exaktes LanguageTool 6.8;
- echter LT-6.8 / PPM-6.7.9-Korridor;
- drei neue Realthemen;
- 1 Artikel Start -> Datei/Handoff;
- 3 Artikel Start -> Datei/Handoff.

Gesamter frischer Artikeltest: **PASS**.

## SAUBERER PRODUKTIONSSTAND

Branch: `hobbyroom/system4-parent-start-token-clean-v1`

Produktionsstand nach stage-aware Repair-Router:
`e4ef916c89cf681aa8a2c4c1e5ff0ef07fc88058`

Immutable Base Hardlock:
Run `34883319385` -> **PASS**.

## NEUER REALER CODEX-ARTIKEL

Neues Thema:
`Pferdeanhänger richtig beladen und Gewicht sicher verteilen`

Target Keyword:
`Pferdeanhänger richtig beladen`

Artikeltyp:
`Beratung`

Kategorie:
`checklisten-fuer-pferdeanhaenger-beratung`

Quellen wurden vor Codex gebunden/versiegelt:
- FN / Pferdetransport;
- § 22 StVO;
- § 34 StVZO;
- § 44 StVZO.

Bei der eigenen Kapselprüfung wurde vor Codex ein falscher Snapshot-Hash erkannt. Der Lauf wurde deshalb nicht gestartet. Kapsel wurde korrigiert und erneut gebunden.

Aktueller Produktions-Head mit korrigierter Kapsel:
`b66467468ca3f1cab9e3b86a5a96a7d7c1c70eaa`

Immutable Base Hardlock auf diesem Head:
Run `34884562137` -> **PASS**.

Codex-Auftrag auf PR #259:
Kommentar `5669182565`.

Codex-Connector-Reaktion:
`eyes` -> Auftrag angenommen.

## AKTUELLER OFFENER PUNKT

Der neue Codex-Lauf ist gestartet/angenommen, aber zum Zeitpunkt dieser Protokollierung liegt noch **kein terminales Endergebnis** vor.

Daher ausdrücklich:
- kein Produktions-PASS behauptet;
- kein zweiter Codex-Lauf gestartet;
- kein Merge;
- kein Publish;
- `publish_allowed=false`.

## NEXT ACTION

Nur den bereits angenommenen Codex-Lauf zu Kommentar `5669182565` auswerten.

Bei PASS: echten End-to-End-Nachweis bis Batch Gate, V2-Handoff, Inline-Pack/Unpack und bytegleicher Rekonstruktion dokumentieren.

Bei Fehler: exakt erste fehlschlagende Stufe, Fehlercode, Feld, Ist/Soll und zuständige Reparaturroute dokumentieren; keinen Parallel- oder Ausweichlauf starten.
