# K0 Arbeits-/Fehlerprotokoll 2026-10-02

**Rolle:** HISTORIE / NACHWEIS. **Keine CURRENT-, Status- oder NEXT-ACTION-Autorität.**  
Aktuelle K0-Wahrheit ausschließlich: `K0_CURRENT_STATE.json`.

## Zielbindung

- K0-Ziel: `K0_GOAL_CONTRACT.json`
- globaler Medium-Zielvertrag: `control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` auf `main`
- Qualität darf nicht reduziert werden.
- `publish_allowed=false`.

## Ausgangsfehler

Der alte 16er-Pferdeatelier-Batch aus K9 war in allen 16 Artikeln von einer generischen Entscheidungs-/Kauf-Schablonenfamilie betroffen. Besonders sichtbar bei „Warum sagt man du alte Schabracke?“: informationaler Sprach-/Wissensartikel wurde in Auswahl-/Passform-/Entscheidungslogik gedrückt. Die alte Schabracke wurde fachlich in `pferdewissen-grundlagen` verschoben.

## Fehlerfolge dieses Chats

### E1 – erster K0-Neuschreiblauf nutzte einen Sonderweg
- Fertige Texte wurden direkt als `K0_ARTICLE_PACKAGE_V1` erzeugt und erst danach K0-Gates/LT/PPM/Export zugeführt.
- Folge: der echte Writer-Regelblock wurde umgangen.
- Sichtbare Qualitätsregression:
  - zu viele H2;
  - zu kurze Textblöcke zwischen H2;
  - Fazit teilweise zu kurz;
  - „Weiterführende Informationen“ fehlten.
- Die daraus erzeugte 16er-Datei wurde später **widerrufen / nicht importieren**.

### E2 – Writer-Provenance-Lock war zunächst unvollständig
- Erste Reparatur verlangte Writer-Provenance, erlaubte aber, einen bereits fertigen Artikel nachträglich zu stempeln.
- Damit blieb derselbe Sonderweg technisch möglich.
- Ursache: Produktionsworkflow akzeptierte einen fertigen Artikel als Einstieg und konnte den Writer-Nachweis selbst erzeugen.

### E3 – WordPress-Datei wurde vom Importer abgelehnt
- Der damalige K0-Exporter ließ das vom Importer 0.28.30 benötigte kanonische `article_id` weg.
- Der Importer blockierte bereits beim ersten Artikel.
- Richtige Bindung:
  `plan_slot -> genau ein PPM-6.7.9-Registry-Slot -> canonical_article_id`
  und Roundtrip
  `SHA256("pserc-plan-slot-v2|" + article_id) == plan_slot`.

### E4 – direkte Artikelpaket-Produktion wurde deshalb vollständig entfernt
Neue verbindliche K0-Kette:
`5-Feld-Intake -> textfreier AUTHORING_CONTEXT -> unveränderbarer WRITER_JOB -> K0_WRITER_DRAFT_V1 -> Writer-Seal -> K0-Gates/PPM 6.7.9 -> LT 6.8 -> canonical article_id -> WordPress 0.28.30`.

Technische Bindungen:
- `.github/workflows/k0-authoring-context.yml`
- `.github/workflows/k0-writer-accept.yml`
- `engine/k0_writer_station.py`
- `engine/writer_contract_guard.py`
- `engine/k0_production_gate.py`
- `engine/canonical_binding.py`
- `engine/k0_wordpress_export.py`

Harte Negativregeln:
- fertiges `ARTICLE_PACKAGE.json` darf nicht Produktionsstart sein;
- AUTHORING_CONTEXT darf keinen sichtbaren Artikeltext enthalten;
- fertiger Artikel darf nicht als Writer-Draft eingereicht werden;
- Writer-Seal muss an unveränderten Writer-Job, Draft-Hash, Identität, sichtbaren Text und Struktur gebunden sein;
- WordPress-Export ohne gültigen Writer-Seal blockiert;
- WordPress-Export ohne kanonische `article_id` blockiert.

### E5 – paralleles Anlegen der 16 Authoring-Kontexte verursachte Workflow-Kollisionen
Mehrere `AUTHORING_CONTEXT.json` wurden zu schnell hintereinander committed. Die Workflow-Concurrency führte zu Cancel/Fail; ein Lauf scheiterte beim Push mit `non-fast-forward`.

Beleg:
- Authoring run `37056827345`: Vorbereitung PASS, Persist-Writer-Job FAIL durch non-fast-forward.
- Dadurch blieben Artikel 13 und 14 zunächst ohne `WRITER_JOB.json`.
- Das ist kein Artikel-/Qualitätsfehler; die vorhandenen AUTHORING_CONTEXT-Dateien sind textfrei und gültig.

### E6 – K0-Selftest kollidierte mit geerbter K10-Isolationsregel
- Die geerbte Isolationsprüfung verbot jeden Pfad namens `writer_drafts`, obwohl K0 diesen Pfad nun als einzigen kanonischen Texteingang benötigt.
- Folge: K0-Selftests blockierten, obwohl Writer-Accept-Läufe selbst korrekt PASS waren.
- K0-spezifische Reparatur: `engine/isolation_guard.py` akzeptiert in `writer_drafts/` ausschließlich JSON mit:
  - `contract=K0_WRITER_DRAFT_V1`;
  - gültiger `k0w-...` Job-ID;
  - `publish_allowed=false`.
  Andere Inhalte dort bleiben BLOCKED.
- Nachweis: K0-Selftest run `37059664443` = **SUCCESS**.

## Aktueller belegter Produktionsfortschritt bei Erstellung dieses Protokolls

Kanonisch vollständig bis verifiziertem `WORDPRESS_SINGLE.json`:
- 0 Das Wichtigste über Reitplatzplaner für Pferde
- 1 Frieren Pferde unter Regendecken?
- 2 Ist eine Reitplatzbewässerung von unten möglich?
- 3 Kann man mit Kappzaum spazieren gehen?
- 4 Longiergurte mit Bogen im Ratgeber
- 5 Passende Kühlgamaschen für Pferde wählen
- 6 Pferdehaftpflicht mit Fremdreiterrisiko auswählen
- 7 So findest du einen passenden Kappzaum für dein Pferd
- 8 So wählst du passende Schermaschinen für Pferde
- 9 Warum sagt man eigentlich „alte Schabracke“? – `pferdewissen-grundlagen`
- 10 Was ist der Unterschied zwischen Schabracke und Satteldecke?
- 11 Was ist ein Reitplatzplaner?
- 12 Welche Magnetfelddecke ist besser geeignet BEMER oder ActivoMed?
- 15 Wie teuer ist der TÜV beim Pferdeanhänger?

Noch nicht kanonisch bis Writer-Job/Seal geführt:
- 13 Wie lege ich einen Longiergurt an?
- 14 Wie oft muss ein Pferdeanhänger zum TÜV?

Alle 14 vorhandenen WordPress-Singles:
- Vertrag `SYSTEM4_WORDPRESS_HANDOFF_V1`;
- Plugin `0.28.30`;
- Build `0.28.30-pste-v5-binding-safe`;
- `direct_wordpress_upload_ready=true`;
- gültige `article:[0-9a-f]{24}`-ID;
- gültiger plan_slot-Roundtrip;
- `publish_allowed=false`.

Letzter Writer-Accept vor Closeout:
- run `37058612043` = SUCCESS.

## Widerrufene / nicht zu verwendende Artefakte

Nicht importieren:
- der frühere kombinierte 16er-K0-Export mit SHA-256 `c9a4dbfa517cb8af9f914bbb6b24090b4b3bc8c3ca7d526f65460b7a6024b7e3`;
- alle daraus abgeleiteten Aussagen „16/16 canonical normal path“;
- direkte `ARTICLE_PACKAGE.json`-Altprodukte in alten Run-Verzeichnissen sind keine Produktionsautorität.

## Nicht betroffen / unverändert

- K9-Produktion selbst wurde durch den K0-Fix nicht als Produktionspfad umgebaut.
- Plugins wurden in diesem Arbeitsstrang nicht entwickelt oder geändert.
- Kein Publish.


### E7 – Abschlussrefresh entfernte kurz das K10-Isolationsfeld
- Beim Closeout-Refresh von `K0_CURRENT_STATE.json` wurde `k10_unchanged` zunächst entfernt, obwohl der K0-Selftest dieses Feld als Isolations-Hardlock verlangt.
- Selftest Run `37061273870`: FAIL ausschließlich bei `K0 current hardlocks` mit `KeyError: k10_unchanged`.
- Feld wiederhergestellt; K10 bleibt zugleich als separater Arbeitsbereich über seine eigene Current referenziert und ist keine K0-Abhängigkeit.
- Reparatur-Commit: `ebdef6afba593e419358b2a224ac272b5b6cbe56`.
- Finaler K0-Selftest Run `37061356909`: SUCCESS.
- Kein Produktionsfortschritt verändert; K0 bleibt 14/16 mit Artikel 13 als erstem offenen Blocker.
