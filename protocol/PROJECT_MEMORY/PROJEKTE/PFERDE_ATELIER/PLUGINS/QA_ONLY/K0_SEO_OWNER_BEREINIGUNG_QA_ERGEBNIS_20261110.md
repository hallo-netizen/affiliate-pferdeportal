# K0 – freigegebene SEO-/Titelbereinigung auf isolierter QA-Kopie umgesetzt

**Wichtig für Folgechat:** Die Änderungen befinden sich **ausschließlich** auf GitHub-Branch `qa/k0-editorial-owner-only-20261110`. Aktiver K0-Branch `konzept0-portal-neutral-20261002` sowie WordPress-Plugins und DataForSEO-Workflow sind unberührt.

**Freigegebene und bereits im QA-Branch implementierte Änderungen:**
1. Exakte Keyword-Reihenfolge im Titel aus K0-Hardrules gestrichen.
2. Pflicht zur exakten Keyword-Phrase in H2 aus K0 gestrichen. Keyword-Stakkato-Schutz max. 2 H2 bleibt.
3. K0-Titelregeln Doppelpunkt und FAQ-Fragezeichen gestrichen; **bestehender** PSERC-Titel-Gate prüft beides bereits vor Handoff.
4. Zweite K0-Suchintent-Entscheidung aus Artikelart und Titel nachweislich beseitigt. K0 übernimmt vorhandenen `content_profile.search_intent` und prüft den Text weiterhin auf vorhandene verbotene Floskeln.
5. Vor-/Nach-LanguageTool-Prüfungen und Reparaturschleifen vollständig unverändert.
6. WordPress-Export-, Writer-, LanguageTool- und produktive Workflows exakt unverändert. PSTE/DataForSEO `KEYWORD_SUGGESTIONS`, `RELATED_KEYWORDS`, `KEYWORD_IDEAS` unverändert; kein fest hinterlegter Keywordstamm erzwungen.

**QA-Beweis:** [GitHub Actions Run 42837580167 – PASS, 58/58 Tests](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42837580167). Regelkatalog 85→81 nur genau 4 freigegebene; 117 restliche Katalogobjekte, alle übrigen Regelwerte und 101 geschützte PPM-Mappings originalgleich; 104 PPM-Einträge bleiben abgedeckt. Originale 3er-Handoff-Datei technisch gültig. Code in TEST/Live noch nicht installiert.

**Vollständiger Quell-/Änderungs-/Rollback- und Grenzbericht:** [`qa/k0-editorial-owner-only-20261110:protocol/K0_QA_EDITORIAL_OWNER_ONLY_20261110.md`](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/qa/k0-editorial-owner-only-20261110/protocol/K0_QA_EDITORIAL_OWNER_ONLY_20261110.md)

**Nicht als fertig melden:** Fünf-Felder-Handoff trägt **kein eigenes Suchintentfeld**. Der durchgehende Identitätsnachweis von externer PSTE/PSERC-SEO-Entscheidung in `K0_AUTHORING_CONTEXT.content_profile.search_intent` ist noch nicht end-to-end gesichert. Bestehende K0-Writer-Jobs sind an alte Regelhashes gebunden; keine rückwirkende Änderung. Erst nach echtem QA-E2E kontrollierte Aktivierung; keine stillschweigende Änderung des K0-Produktionsbranches.

Separater, noch **nicht** behobener alter Textschutzfehler: `FORBIDDEN_BOILERPLATE`-Fingerprint mit `ß` kann beim `.casefold()`-Vergleich entgehen. Die vorgegebenen Textregeln durften hier nicht geändert werden. **K0 aktiv unverändert, TEST/LIVE unverändert.**
