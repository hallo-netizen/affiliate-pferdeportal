# K0-Handoff 10.11.2026: zwei vorab erkennbare Titel-/Keyword-Sperren

Status: Beweis aus tatsächlichen GitHub-Dateien der laufenden Produktion und Original-K0-Quellregel; keine Programmmodifikation, keine Pluginversion, keine Datenänderung.

## Reale Datei
K0-Branch `konzept0-portal-neutral-20261002`:
- `real_runs/k0/batch-20261110-42619ca7/BATCH_INTAKE.json`: echte 3er-Übergabedatei aus WordPress-TEST, 5 Felder pro Thema, korrekte SHA256, gültiger PSERC_METADATA_BATCH_V2-Vertrag. Alle drei sind **formal gültig**, nicht kaputte JSON-Dateien.
- Artikel 1: `Horseware regendecken` → `Horseware-Regendecken und ihre Unterschiede bei Schnitt und Ausstattung` => **PASS** bei originaler Titelregel. `real_runs/k0/k0-20261110-42619ca7-01-r2/WORDPRESS_VERIFY.json` hat Status PASS.
- Artikel 2: `Fliegen regendecke pferd` → `Kombinierte Fliegen- und Regendecken für Pferde sinnvoll nutzen` => **BLOCK** bei originaler Titelregel: `regendecke` ist nicht `regendecken`, `pferd` nicht `pferde`.
- Artikel 3: `Regendecke pferd 0g` → `Regendecken ohne Füllung für Pferde richtig einsetzen` => **BLOCK**: `regendecke` und `pferd` sind nicht wörtlich gleich, `0g` fehlt im Titel.

## Prüfer und spät angewendete Regel
- `engine/checkers.py` Funktion `_keyword_tokens_in_order(keyword,title)` normalisiert nur Groß-/Kleinschreibung, Satzzeichen, ß, und verlangt **alle Keyword-Wörter in derselben Reihenfolge als exakte Tokens**. Keine Plural-/Singular- oder Synonymtoleranz. Aufgerufen als `title.keyword_required` in `structural_receipts()` ca. Zeile 205.
- `engine/k0_full_rules.py::verify_pre_lt68` bereitet **erst mit schon vorhandenem Artikel-HTML** `build_check_article(package,...)` vor und ruft `run_article_content_checks` / `verify_article_pre_lt68`. Deshalb fällt `title.keyword_required` erst **nach** Recherche/Texterstellung auf.
- `engine/k0_portal_resolver.py::validate_intake` prüft zuvor nur Vertragsnamen, Status, exakt 5 nichtleere Textfelder pro Artikel und den Datei-Hash; **keine** Titel-/Keyword-Wortregel. Die `.github/workflows/k0-authoring-context.yml` ruft diesen Intake-Validator beim Erstellen des Writer-Auftrags bereits auf, zieht aber `title.keyword_required` nicht vor.
- In ursprünglichen `...-02/WRITER_JOB.json` und `...-03/WRITER_JOB.json` wurden beide identischen Titel und Keywords **unverändert** an Writer durchgereicht. Ihre `-r2`-Versionen ändern nur den Recherche-Suchintent `COMMERCIAL_INVESTIGATION` → `DECISION_SUPPORT`, aber behalten die beiden Literal-Titel-Konflikte. Eine Suchintent-Korrektur löst den Titel-/Keyword-Konflikt **nicht**.

## Ursache
Der PSERC-Originalexport ist **formal korrekt**, aber das nachgelagerte K0-Qualitätskriterium `title.keyword_required` ist **strenger** als die fachlich akzeptierten externen SEO-Titel. Die zwei Übergabeeinträge entsprechen dem K0-Titelvertrag nicht. Die Fehlprüfung kam nicht erst durch einen fertigen Artikel zustande; alle zum Erkennen nötigen Werte lagen bereits beim ursprünglichen Metadatenexport vor.

## KISS-Maßnahme (noch nicht umgesetzt)
1. **Exakt die schon vorhandene K0-Funktion** `_keyword_tokens_in_order` aus `engine.checkers` im bestehenden K0-Intake-Prüfer `validate_intake` **vor** Recherche, Job-Erzeugung und Writer verwenden; kein neuer Titelowner, kein zweites fachliches Gate, keine Datenbank, kein Plugin erforderlich. Nur den bestehenden Prüfzeitpunkt verschieben/ergänzen und die nachgeschaltete Qualitätsprüfung unverändert lassen.
2. Auf PSERC/PSTE-Seite die vorhandene externe Titel-Freigabe **nicht blind** als vollständig K0-kompatibel bezeichnen. Vor künftigem Produktionsdownload muss die Schnittstelle gegen die K0-Originalregel abgeglichen sein (idealerweise ein gemeinsam verbindlicher Abnahmevertrag, keine neu erfundene Titelregel).
3. K0-Ingest-Regression: Originaldreierdatei muss **vor Writer** für Position 2 und 3 mit konkreten Gründen stoppen, Position 1 PASS; manipulierte Hashes weiterhin BLOCKED. Ein syntaktisch korrekter, K0-kompatibler Titel muss durchgehen. Keine automatischen Änderungen von Originaltitel, Keyword, Plan-Slot oder Hash; Korrektur ausschließlich durch den bestehenden externen Titelowner, neue gebundene Übergabedatei.
4. K0-Artikel, Writer und komplette alte Qualitätsregel bleiben unverändert; keine zusätzlichen fachlichen Checks nachgelagert.
5. Der separate Nutzerverweis auf ein bereits geschriebenes *Prüfprotokoll* konnte im K0-Branch unter `protocol/` nicht als heutiger neuer Bericht verifiziert werden. Die hier genannten Originaldateien und Regeln sind aber physisch auf GitHub nachgewiesen. Dieser QA-Bericht ist ausdrücklich eine neue Dokumentation, nicht als gefundenes altes Protokoll ausgegeben.

HINWEIS: Dieser Bericht ist eine geprüfte Ursachenanalyse und **KEIN** schon ausgeführter Early-Guard-Test; keine Live-/K0-Änderung behaupten.
