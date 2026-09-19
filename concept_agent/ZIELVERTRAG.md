# CONCEPT AGENT / KONZEPT 5 — ZIELVERTRAG

## Endziel
Aus einem frisch gebundenen SEO-/Redaktionsplan-Metadatenbatch werden **1..N neue Artikel** vollständig erzeugt, hart geprüft und als **genau eine korrekte WordPress-Uploaddatei** im Chat ausgegeben.

## Verbindlicher Eingang
Der Eingang ist eine vom aktuellen SEO-Redaktionsplan exportierte Metadaten-Datei mit den gebundenen Planungsfeldern je Artikel:
- `title`
- `target_keyword`
- `category`
- `article_type`
- `plan_slot`

Die gebundene Beitragsart darf nicht eigenmächtig auf `Beratung` geändert werden. Gemischte Batches sind zulässig. Neue Typen wie `Produktvergleich` werden verarbeitet, sobald ihr eigener Fach-/Qualitätsvertrag upstream verbindlich gebunden ist.

## Writer
- Writer: ChatGPT / GPT-5.6 Sol.
- Codex: VERBOTEN, solange der Nutzer es nicht ausdrücklich neu freigibt.
- Claude: nicht Teil des aktuellen Produktionswegs.
- Jeder Artikel ist ein neuer Lauf; keine Wiederverwendung alter Artikeltexte als Schreibvorlage.

## Feste Produktionskette
`gebundener Input → Quellen/Research → Fact-Pack → Writer → Artikelprüfung → Repair nur am konkreten Fehler → kompletter Recheck → Batchprüfung → WordPress-Datei`

Vor dem Schreiben müssen die drei internen Links verbindlich gebunden sein.

## Dauerhafte redaktionelle Regeln
- gute/natürliche gebundene Titel bleiben unverändert;
- nackte Aktionsoberflächen wie `<Keyword> wählen/auswählen/finden` sowie `So findest du <Keyword>` ohne sinnvolle sprachliche Ergänzung dürfen bei Beratung nicht FINAL passieren;
- natürliche Attribute wie `richtig`, `passend`, `geeignet`, `optimal`, `ideal` sind zulässig, wenn sie sprachlich passen;
- Zwischenüberschriften müssen konkret und menschlich klingen; bürokratisch-mechanische Formulierungen werden blockiert;
- Inline-Links dürfen nicht mit dem folgenden Wort verkleben (`</a>Wort` = BLOCK);
- gute Fälle dürfen durch Nachschärfungen nicht unnötig umgeschrieben werden.

## Qualitätsgrenze
Vor FINAL zwingend:
- LanguageTool 6.8: PASS / 0 Findings;
- PPM 6.7.9: `TECHNICAL_CHECK_OK`;
- PPM 6.7.9: `CONTENT_QUALITY_CHECK_OK`;
- Fail-Closed-Aggregat: PASS;
- Batch-Dubletten-/Wiederholungsprüfung;
- redaktionelle Natürlichkeits-/HTML-Textflussprüfung;
- nach jeder Reparatur kompletter Recheck.

Kein Worker/Writer darf seinen eigenen PASS behaupten.

## WordPress-Enddatei
Der aktuell belegte Direktimportvertrag des installierten **Portal SEO Redaktionsplan Compiler 0.28.23** ist:

`SYSTEM4_WORDPRESS_HANDOFF_V1`

Pflicht:
- `publish_allowed=false`
- `signing_deferred=true`
- `batch_gate_status=SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- `no_legacy_status=PASS`
- `test_suite_status=PASS`
- je Artikel korrekte Hash-, Plan-, Kategorie-, LT- und PPM-Bindung
- lokaler Positiv-/Negativtest gegen den echten 0.28.23-Vertrag vor Chat-Ausgabe.

Der Import erzeugt ausschließlich WordPress-Entwürfe und liest/schreibt den SEO-Redaktionsplan nicht.

## Ausgabe
Genau **eine** WordPress-Datei für den gesamten Batch im Chat.
Keine Temp-only-Ausgabe.
Kein Publish.
Kein WordPress-Write durch Concept Agent selbst.

## Lernschleife
Nach jedem realen Lauf dürfen belegte Fehler als kleine, gezielte Guard-Regeln ergänzt werden.
Jede Nachschärfung braucht mindestens einen Positiv- und einen Negativtest und gilt danach für alle folgenden passenden Artikel.
