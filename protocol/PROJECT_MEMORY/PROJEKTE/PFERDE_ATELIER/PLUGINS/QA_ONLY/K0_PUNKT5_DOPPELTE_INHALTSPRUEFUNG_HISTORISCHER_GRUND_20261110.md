# K0 – Punkt 5: Warum vor und nach LanguageTool geprüft wird (historisch und im laufenden Code belegt)
**10.11.2026 – Quellengeprüfte Rücknahme der vorzeitigen „Doppelprüfung beseitigen“-Freigabe. Keine Codeänderung.**

## Quellen und belegte Ursache

- **01.10.2026**, GitHub-Commit `3ee2684f56e2c325156e72ad030db44f6fb99206`, `ARCHITECTURE.md`, `K10_GOAL_CONTRACT.json`: Gewünschte zentrale Qualitätsarchitektur `ONE_HARD_RULE_ONE_OWNER_ONE_CONTENT_CHECK_ONE_RECEIPT`. Nachfolgeprüfer **überprüfen die unveränderte Bindung und Prüfnachweise**, nicht nochmals den Inhalt. Bei Textänderung gelten alte Nachweise nicht mehr; betroffene Regeln neu prüfen. `TEXTMACHINE_SCOPE_REFERENCE.json`: `FINAL_STAGE_DOES_NOT_RECHECK_PASSED_CONTENT_RULES`.
- **02.10.2026**, Commit `4135fab77e9f258be435acafe66d240f7ce6d1b1`: Getrennte **Vorprüfung der inhaltlichen Regeln ohne LT** (`run_article_content_checks` plus `verify_article_pre_lt68`) und anschließende **finale Gesamtfreigabe mit LT**. Der Grund ist die korrekte zeitliche Abhängigkeit: Eine Sprachprüfung darf die anderen Qualitätssperren nicht ersetzen; ohne Sprach-PASS keine Exportfreigabe.
- **03.10.2026**, Commit `5dc172f9233cc0d576030632eb380906574ceae7`: Implementiert die K0-Regelbindung und die beiden Funktionen `verify_pre_lt68` / `verify_final`; `1ae6c6924f03473b45c60d054880e471a5f8e59a`: In `.github/workflows/k0-writer-accept.yml` eingefügt: erst `K0_ALL_RULES_PRE_LT68_PASS`, dann `K0_LT68_PASS`, danach `K0_ALL_RULES_FINAL_PASS`. Die WordPress-Exportfunktion verlangt alle drei PASS und überprüft die zur selben Textversion gehörenden Hashes.

## Was genau zweimal passiert und was nicht
- `engine/k0_production_gate.py` ruft `verify_full_rules_pre_lt68` auf. `engine/k0_full_rules.py::verify_pre_lt68` führt für den Artikel **84 / 85** inhaltliche/strukturelle Regeln aus. `::verify_final` führt `run_article_checks` mit **denselben 84 Prüfungen + der LT-Statusregel** aus.
- Der Workflow gibt **dieselbe unveränderte** `/tmp/K0_SEALED_WRITER_PRODUCT.json` vor und nach LT weiter.
- `engine/lt68_external.py` **analysiert** den sichtbaren Text; es **korrigiert und verändert Artikel-HTML nicht automatisch**. Ist die Grammatik nicht bestanden, stoppt der Lauf bei LT; ein korrigierter Text wird als neuer Draft/Writer-Durchlauf eingereicht und muss dann wieder vollständig geprüft werden.
- `engine/k0_wordpress_export.py` verlangt das bestandene Vor-Gate, LT-Status sowie die finale Freigabe mit identischer `html_sha256`; dort existiert ein tatsächlicher Sicherheitsnutzen der getrennten Etappen.
- Im K0-Zweig werden **die detaillierten 84 Vorprüf-Receipts aktuell nicht für eine finale Hash-gesicherte Wiederverwendung persistiert**; nur die Vorprüf-Zusammenfassung wird zurückgegeben. Einfach die zweite Berechnung zu entfernen würde die erwarteten 85 aktuellen finalen Einzelbelege verletzen oder neue, unbewiesene Lücken erzeugen.
- **Original K10 hat einen Nachweis der Zielarchitektur:** `engine/preflight.py` speichert `ARTICLE_RECEIPTS_PRE_LT68.json`; `engine/real_proof.py` kann `pre_receipts` laden, mit `verify_article_pre_lt68` prüfen, **nur LT-Receipt ergänzen** und anschließend `verify_article` ausführen. Das ist ausdrücklich der historische Sinn von „einmalig prüfen“, **nicht** die doppelte Kontrollstufe abzuschaffen.

## Bewertung und verbindliche Änderung der geplanten Freigabeliste
- **Zwei Freigabestufen bleiben zwingend:** umfassende Qualitätsprüfung vor LanguageTool; nach LT vollständiger finaler Nachweis für **denselben** unveränderten Artikel.
- **Bei repariertem/verändertem Artikel**: Qualitätsregeln erneut ausführen – nicht über die alte Freigabe hinwegschreiben; bestehende Reparaturschleife unverändert.
- **Nur bei nachgewiesener identischer Text-/Daten-/Regelversion** darf eine spätere KISS-Optimierung dieselben inhaltlichen Prüfergebnisse durch **gültige, vollständige, bindende Einzelbelege** erneut verwenden. Das wäre eine Optimierung der Rechenarbeit, keine Qualitäts-/Sicherheitsabsenkung.
- **Punkt 5 ist NICHT zur Umsetzung freigegeben**. Erst einen vollständig isolierten K0-Proof mit positiven und gezielten Negativtests durchführen, bevor überhaupt ein Code-Change erwogen wird. Wort-/Absatz-/H2-/Fazit-/Link-/Fakten-/Tabellen-/Wiederholungs-/LT-Schutz bleibt unangetastet. K0 Live-/Produktionsbranch hier nicht verändert.

**RESULTAT: Historische Schutzabsicht BELEGT; redundante Rechenarbeit BESTÄTIGT; tatsächliche Laufzeit-/Lastvorteile NICHT gemessen; sofortige Entfernung NICHT freigabefähig.**
