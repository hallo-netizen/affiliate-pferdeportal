# K9 Abschluss-/Nachholprotokoll – Regelbindung, Tabellenregel und realer 16er-Lauf – 2026-09-30

**Rolle:** Historie / Nachweis / WAS-WARUM / Fehlerhistorie. **Keine CURRENT-Wahrheit und keine NEXT-ACTION-Quelle.**  
**Aktuelle operative Wahrheit für diesen K9-Arbeitsstrang:** ausschließlich root `CURRENT_STATE.json` auf Branch `konzept9/greenfield-20260929`.  
**Statischer K9-Einstieg:** `hallo-netizen/text-start#46` → erlaubtes Repo/Branch → root `CURRENT_STATE.json`.

## Zielvertrag

Autoritative Zielquelle bleibt unverändert auf `main`:

`control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json`

Ziel: `MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`.

Nicht verändert:
- LanguageTool 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Publish-Sicherheit / `publish_allowed=false`;
- keine Qualitätsabsenkung;
- kein neuer Codex-/OpenAI-API-Produktionsweg.

## Dauerhafte Änderungen dieses Chats – WAS / WARUM

1. **Vollständige Schreibregel-Abdeckung fail-closed gebunden.**  
   `contracts/K9_WRITING_RULES.json`, `quality/k9_rule_guard.py`, `contracts/K9_WORKER_CONTRACTS.json` und der native Check wurden so gebunden, dass Writer/Repair den vollständigen Regelbestand verwenden und der Check denselben Regelbestand nachprüft.  
   **Warum:** Beim vorherigen Einzelartikel war die vorhandene H2-/Keyword-Stakkato-Regel dokumentiert, aber nicht als vollständige K9-Pflichtbindung mitgeführt worden. Neue oder entfernte Regelpfade dürfen künftig nicht still ignoriert werden.

2. **Mobile kompakte Tabellenregel verbindlich ergänzt.**  
   `contracts/K9_TABLE_RULE_V1.json` + `quality/k9_table_guard.py`: Kopfzeile und erste Spalte grundsätzlich kurze Begriffe, Mehrwort nur wenn fachlich nötig, keine Sätze/Fließtexte; Datenzellen knapp; Tabellenwörter dürfen die Artikel-Mindestwortzahl nicht auffüllen.  
   **Warum:** Tabellen sollen mobil scanbar bleiben und dürfen nicht als Wortzahl-Puffer missbraucht werden.

3. **Realer Einartikel-Bestätigungslauf mit neuer Regelbindung durchgeführt.**  
   Artikel: `Ist eine Reitplatzbewässerung von unten möglich?`  
   Ergebnis: LT 6.8 PASS, PPM 6.7.9 PASS, Schreib-/Tabellenregeln PASS, PSERC PASS, ENDSTEMPEL PASS, WordPress-Vertrag PASS, STOP.  
   Die dabei sichtbare Tabelle wurde bewusst knapp gehalten.

4. **STOP-Dateiübergabe dauerhaft in den K9-Startknopf aufgenommen.**  
   `hallo-netizen/text-start#46` verlangt jetzt bei STOP: `runtime/K9_STOP.json` live lesen, `final_ref`/`final_sha256` gegen Current prüfen und genau diese aktuelle Final-JSON automatisch an den Nutzer übergeben.  
   **Warum:** STOP ohne konkrete Dateiausgabe ist kein vollständiger Nutzerabschluss.

5. **Realer 16er-Paketlauf als STATION_ONLY begonnen.**  
   Paketprinzip: 16 Research gemeinsam → speichern → 16 Write gemeinsam → Check/Repair gemeinsam → Finalisierung. Kein Einartikel-AUTO_CHAIN als Ersatz.

6. **16er-Intake robust gemacht.**  
   Commit `f58efaa916299fda5a2145224789e4222d7b9258`: `.github/workflows/k9-intake.yml` legt fehlende leere Inbox-Verzeichnisse an.  
   **Warum:** Der manuelle Paketimport war fälschlich daran gescheitert, dass `inbox-auto` als leerer Ordner nicht existierte.

7. **STATION_ONLY-Persistenz von AUTO_CHAIN entkoppelt.**  
   Commit `2a415c5c2fbbcd7b2b00b1eaf16fcd5dfd05eaad`: Paketjob kann gespeichert werden, ohne eine nicht existente `runtime/AUTO_CHAIN.json` zwingend hinzuzufügen.  
   **Warum:** Paketmodus ist bewusst STATION_ONLY.

8. **16er-Research vollständig erzeugt, hashgebunden korrigiert und angenommen.**  
   Researchjob: `K9-RESEARCH-e053565c2857d4c0`; 16/16 DONE.  
   Erstsubmission `f4dd63...` wurde wegen `RESEARCH_CLAIM_EVIDENCE_HASH_INVALID:RPB_F2` abgelehnt; exakte Evidence-/Produkt-Hashes wurden in `adc973182ed7f8921a9c842321a67c73455d447f` korrigiert; Acceptance danach SUCCESS.

9. **Bestehenden Writer-Packager auf 1–16 Artikel generalisiert.**  
   Commit `4ea6a9dc263cd3294011b1fe6e42b531780a0215`.  
   **Warum:** Derselbe vorhandene Packager war technisch noch auf einen Artikel begrenzt (`REALTEST_PACKAGER_EXPECTS_ONE_ITEM`), obwohl der Stationsjob korrekt 16 Artikel enthielt. Keine neue Architektur, nur Generalisierung desselben Packagers.

10. **16er-Writing vollständig gespeichert und geprüft.**  
    Writejob `K9-WRITE-2932b06df177b8bf`: 16/16 DONE.  
    Package/Acceptance: `4dd0decbc4950392792cd8bb579d85889a368c65`.  
    Checkjob: `K9-CHECK-2261974bcecb8a68`; Ergebnis 16/16 REPAIR_REQUIRED.  
    Repairjob `K9-REPAIR-1e6b47713da62854` ist der aktuell offene Worker.

11. **Selftest an echten Paketmodus angepasst.**  
    - `33fb288097774dd4795098cab1837354bdaa2b20`: Syntaxfehler im aktiven Structural-Test behoben.
    - `2926dbbbadb87e0c57ee0ea84f0e5c572b7795d3`: Einartikel-Structural-Test wird bei 16er-Batch nicht fälschlich erzwungen.
    - Greenfield-Selftest Run `36775529468`: **SUCCESS**.

## Fehlerprotokoll – historisch behoben

- Schreibregelbestand nicht vollständig als K9-Pflichtinput/-prüfung gebunden → ursächlich mit kompletter Regelabdeckung + fail-closed Schema-/Gruppenbindung behoben.
- H2-Keyword-Stakkato konnte dadurch durchrutschen → durch vollständige Regelbindung und Heading-Guard behoben.
- Tabellen zu textlastig / Tabellen konnten Wortbudget auffüllen → mobile Tabellenregel + separater Guard, Wortbudget ohne Tabelle.
- STOP ohne automatische konkrete Finaldatei → Startknopf #46 ergänzt.
- 16er-Intake scheiterte an fehlendem leerem `inbox-auto` → behoben.
- Paket-Persistenz erwartete fälschlich `AUTO_CHAIN.json` → behoben.
- Researchsubmission mit falschem Evidence-Hash → abgelehnt, exakt korrigiert, danach angenommen.
- Writer-Packager nur für 1 Artikel → derselbe Packager auf 1–16 generalisiert.
- FAQ-Direct-Answer-Bindung im 16er-Draft erforderte Nachzug → Writer-/Packager-Bindung nachgezogen; Package danach erfolgreich.
- Selftest-Regex-Syntaxfehler → behoben.
- Einartikel-Selftest gegen 16er-Repairjob → als nicht anwendbar gebunden; aktueller Selftest SUCCESS.

## Aktuelle Repair-Evidence – NICHT Current, sondern gebundener Prüfnachweis

Autoritative Fehlerquelle für den jetzt offenen Repair:
`warehouse/check/K9-CHECK-2261974bcecb8a68.json`

| # | Artikel | LT 6.8 | PPM 6.7.9 | K9-Schreibregeln |
|---:|---|---|---|---|
| 1 | Das Wichtigste über Reitplatzplaner für Pferde | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_SHORT_CONCLUSION, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_INSUFFICIENT_TEXT_BETWEEN_HEADINGS, BLOCKED_WAVE2_CONCLUSION_BALANCE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 2 | Frieren Pferde unter Regendecken? | PASS | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE | PASS |
| 3 | Ist eine Reitplatzbewässerung von unten möglich? | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | PASS |
| 4 | Kann man mit Kappzaum spazieren gehen? | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | PASS |
| 5 | Longiergurte mit Bogen im Ratgeber | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_SHORT_CONCLUSION, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_INSUFFICIENT_TEXT_BETWEEN_HEADINGS, BLOCKED_WAVE2_CONCLUSION_BALANCE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 6 | Passende Kühlgamaschen für Pferde wählen | PASS | BLOCKED_CONTENT_WORD_FLOOR, BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_SHORT_CONCLUSION, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_CONCLUSION_BALANCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 7 | Pferdehaftpflicht mit Fremdreiterrisiko auswählen | PASS | BLOCKED_CONTENT_WORD_FLOOR, BLOCKED_CONTENT_PLACEHOLDER_SOURCE_TITLE, BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_SHORT_CONCLUSION, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_INSUFFICIENT_TEXT_BETWEEN_HEADINGS, BLOCKED_WAVE2_CONCLUSION_BALANCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 8 | So findest du ein optimales Kappzaum für Pferde | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_WORD_FLOOR, BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_SHORT_CONCLUSION, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_CONCLUSION_BALANCE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 9 | So wählst du passende Schermaschinen für Pferde | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_SHORT_CONCLUSION, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_CONCLUSION_BALANCE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 10 | Warum sagt man du alte Schabracke? | DE_REPEATEDWORDS_AUSSERDEM, PRAEP_DAT, UPPERCASE_SENTENCE_START | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_GENERIC_TECHNICAL_HEADING, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_INSUFFICIENT_TEXT_BETWEEN_HEADINGS, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | PASS |
| 11 | Was ist der Unterschied zwischen Schabracke und Satteldecke? | GERMAN_SPELLER_RULE, UPPERCASE_SENTENCE_START | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | PASS |
| 12 | Was ist ein Reitplatzplaner? | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_WORD_FLOOR, BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR |
| 13 | Welche Magnetfelddecke ist besser geeignet Bemer oder ActivoMed? | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | PASS |
| 14 | Wie lege ich einen Longiergurt an? | GERMAN_SPELLER_RULE | BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_FAQ_DIRECT_ANSWER, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | PASS |
| 15 | Wie oft muss ein Pferdeanhänger zum TÜV? | PRAEP_DAT, UPPERCASE_SENTENCE_START | BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED, BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_H2_SECTION_IMBALANCE, K9_RULE_TABLE_FIRST_COLUMN_TOO_LONG |
| 16 | Wie teuer ist der TÜV beim Pferdeanhänger? | DE_CASE, PRAEP_DAT, UPPERCASE_SENTENCE_START | BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED, BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO, BLOCKED_KNOWN_REQUIRED_LIST_MISSING, BLOCKED_WAVE2_INTRO_STRUCTURE, BLOCKED_WAVE2_HEADING_INTENT_MISMATCH, BLOCKED_WAVE2_REQUIRED_LIST, BLOCKED_WAVE2_TABLE_VALUE, BLOCKED_WAVE2_LANGUAGE_EVIDENCE | K9_RULE_H2_SECTION_WORD_RANGE, K9_RULE_H2_SECTION_IMBALANCE |

Alle 16 Checkresultate sind `REPAIR_REQUIRED`. Das ist **kein technischer Systemblocker**, sondern der normale aktuelle Repairzustand.

## Tests / Nachweise

- 16er-Research Acceptance: SUCCESS.
- 16er-Write Package/Acceptance: SUCCESS.
- 16er-Check: real ausgeführt; 16/16 bewusst fail-closed in Repair überführt.
- Combined Check Selftest Run `36770809541`: SUCCESS.
- Greenfield Selftest Run `36775529468`: SUCCESS.
- Current-Job-Validierung im Greenfield-Selftest: SUCCESS.
- Positive/negative PPM-/PSERC-Regressions im Greenfield-Selftest: SUCCESS.

## Nicht betroffen

- Plugins: NICHT BETROFFEN.
- Hobbyraum: NICHT BETROFFEN.
- Paul / fremde Parallelworker: NICHT BETROFFEN.
- Archiv: keine aktive Arbeit archiviert.
- Zielvertrag: unverändert.
- K4–K8: nicht als aktuelle Produktion reaktiviert.

## Eine Wahrheit

Dieses Dokument ist ausdrücklich **keine** Status-/NEXT-ACTION-Quelle.  
Für K9-Produktion gilt ausschließlich der statische Einstieg `hallo-netizen/text-start#46` und danach live root `CURRENT_STATE.json` auf `konzept9/greenfield-20260929`.

