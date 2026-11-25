# Hab & Bewahr – verbindliche Änderungssperre und kritischer Originalabgleich (19.11.2026)

## Verbindliche Nutzeranweisung
**„änderungen nur mit absprache. gerade bei den textlängen bin ich kritisch was veränderungen angeht“**

Deshalb **ab sofort keinerlei Änderung an Textregeln**, weder an der zentralen K0-/K-Multi-Basis noch an den fünf Hab-Entwürfen, ohne vorherige ausdrückliche inhaltliche Freigabe. Das gilt auch für Umformulierung, feste Zahlen, Pflichtblöcke, interne Links, Quellenmarker, Tabellen und Bedeutungsverschiebung durch Umbenennung. Prüfungen, Quellenabgleich und Vorschläge sind zulässig; ein Prüfbericht ist **keine** Regeländerungsfreigabe.

## Nachgeprüfte Originale (READ ONLY)
Repository `hallo-netizen/affiliate-pferdeportal`, Originalzweig `konzept0-portal-neutral-20261002`:
- `RULE_VALUES.json` (globale Word- und Abschnittsgrenzen, die vier Originaltypen, Metadaten, Tabellen/Links).
- `ARTIKELTYPEN/Anleitung.json` (zusätzliches Original-Regelfach für Anleitung).
- `K0_CURRENT_STATE.json` (aktuelle Link-/Eigentümerbindung).

### Feste Werte – unverändert und vorerst zwingend
| Sachverhalt | Nachweis Original | Entscheidung hier |
|---|---|---|
| Gesamtwortzahl | `balance.hard_total_words_min=750`, `hard_total_words_max=900` | **Beibehalten. Keine Anpassung ohne vorherige Zustimmung.** |
| H2 und Absätze | `ppm_parity.content.minimum_h2=4`, `minimum_paragraphs=16` | Unverändert; kritische Bewertung nur als Vorschlag. |
| H2-Abschnitt | `balance.normal_h2_section_min_words=100`, `max_words=220` | Unverändert. |
| Interne Links | `K0_CURRENT_STATE.link_distribution`: exakt 3 passende WP-Ziele mit gebundenen Rollen und Verteilung | Unverändert; keine stillschweigende Umstellung auf 1–3. |
| Tabellen | Vergleich: Tabelle Pflicht; andere bestehende Originaltypen: Pflicht, soweit keine definierte Ausnahme | Unverändert; keine freie Tabellen-Auslassung. |
| FAQ | Original-Pflichtabschnitte intro, answer, details, checklist, conclusion, further_information; Liste key_answers | Unverändert. |
| Beratung | Pflichtabschnitte intro, criteria, decision, conclusion, further_information; `decision_goal` und `decision_criteria` | Unverändert. |
| Pflege | intro, steps, risks, conclusion, further_information; Listen steps/risks | Unverändert. |
| Vergleich | intro, options, comparison, table, conclusion, further_information; advantages/disadvantages und Ziel-/Kriteriendaten | Unverändert. |
| Anleitung | intro, preparation, steps, risks, verification, conclusion, further_information; steps/mistakes + sechs Pflichtmetadaten | Unverändert. |

### Fachliche Differenzen, die vor jeder Regelbearbeitung zu besprechen sind
1. **Ratgeber & Wissen:** Das Pferdeatelier kennt `Beratung`, aber deren feste Entscheidungs-Metadaten passen nicht automatisch zu neutralem Grundlagenwissen. Keine Übernahme durch irreführendes Ausfüllen von Scheinkriterien.
2. **Anleitung & Checkliste:** Pferdeatelier trennt einmalige `Anleitung` von wiederkehrender `Pflege`. Keine automatische technische Gleichsetzung.
3. **Bericht & Praxisfall:** Kein originales Bericht-Typfach nachgewiesen. Eigener Typ ist fachlich geplant, aber in K0 und Magazin-Routing nicht READY.
4. **FAQ:** Direkte Antwort ist richtig; der starke bestehende FAQ-Aufbau bleibt erst einmal bestehen, selbst wenn eine kurze Frage redaktionell auch kürzer beantwortbar wäre.
5. **Sicherheitsvorgaben:** Ergänzungen für Selbstschutz, Versicherung, Recht, Datenschutz, Ausfallsicherheit und reale Fälle **nur als Vorschläge** bis zur Zustimmung. Die vorhandenen separaten Hilfsdateien sind keine neue produktive Prüfung.
6. **Autarke Typregeln:** Ziel sind eigenständige, vollständig ausgefüllte Hab-Regeldateien. Die bisherigen fünf Dateien verweisen noch auf zwei Hilfsdateien und sind daher konzeptionell **nicht fertig**. Unveränderte Kopiervorlagen sind keine Erlaubnis, bestehende zwingende Kontrollwerte abzuändern.

## Prüfstrategie ohne Vorfestlegung
- Ausgangsregeln **1:1 mit Quellenverweis erfassen** und unverändert als Standard einplanen.
- Pro Beitragsart **nur nachgewiesene fachliche Lücken** und die wirklich nötigen Hab-Sonderfälle notieren.
- Jede vorgeschlagene Änderung gesondert mit Originalwert, vorgeschlagenem Wert, Grund und möglicher technischer Auswirkung vorlegen. Bis zur Entscheidung: **Original gilt**.
- Noch keine Original- oder Hab-Regeldatei ändern, kein K0/K-Multi-Release, keine neue Plugin-ZIP. Erst dokumentierte Entscheidung, dann Bau und Tests.

## Tatsächlich ausgeführt
Nur GitHub-Originaldateien lesend geprüft und **dieses Freigabe-/Auditprotokoll** neu gespeichert. Keine der fünf Hab-Beitragsregeldateien geändert. Die früheren Empfehlungen im Konzept, z. B. kürzere FAQ oder 1–3 interne Links, sind **nicht genehmigt und nicht aktiv**.
