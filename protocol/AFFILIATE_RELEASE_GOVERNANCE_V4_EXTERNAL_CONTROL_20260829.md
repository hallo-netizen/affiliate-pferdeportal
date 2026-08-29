# Affiliate-Zentrale – Governance V4 / externe Kontrollinstanz

## Zweck

Die Kontrollinstanz sitzt **außerhalb des Plugin-Codes**. Sie soll verhindern, dass ein neuer Chat oder Worker im Kleinklein versinkt, eine zweite Wahrheit erzeugt, bereits bestandene Prüfungen wiederholt oder aus einem isolierten Symptom eine neue Version/Architektur baut.

## Drei Ebenen

1. **Maschinenvertrag:** `control/release-governance/CURRENT_RELEASE.json`
   - Gesamtziel (`objective_control.north_star`)
   - genau ein aktueller Meilenstein
   - genau ein autorisierter nächster Schritt
   - maximal ein Arbeitsstrang
   - genau ein Arbeitsbranch
   - erlaubter Änderungsscope
   - gebundene Source-/Baseline-Hashes
   - Pflichtgates und Evidence
2. **Prüfer:** `release_guard.py`
   - VERIFY ONLY
   - erzeugt keine Quelle
   - rekonstruiert keine Quelle
   - blockiert Scope-/Branch-/State-/Hash-/Evidence-/Release-Drift fail-closed
3. **GitHub-Enforcement:** Required Check + Hardlock
   - der Guard wird als Pflichtcheck gebunden
   - anschließend wird der Guard selbst durch `hardlock-base` immutable geschützt
   - keine Bypass-Akteure

## Entscheidender Architekturwechsel V3 → V4

V3 erklärte `CURRENT_WORKING_SOURCE.b64/` zur Autorität und der Guard dekodierte Chunk-/Base64-ZIP-Bytes. Damit reproduzierte die Governance genau das Problem, das sie verhindern sollte: Rekonstruktion.

V4 kennt für den aktuellen Stand nur noch:

`release/affiliate-zentrale/current/affiliate-portal-router/`

plus:

`release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`

Der 21-Dateien-Baum muss direkt committed sein. Der Guard vergleicht Dateiliste und SHA-256 hart gegen das Manifest. Er besitzt **keine** Materialisierungsfunktion.

## Anti-Kleinklein-Regeln

- `north_star` darf nicht durch einen Einzelbug ersetzt werden.
- maximal ein paralleler Arbeitsstrang.
- `authorized_next_action` ist bindend.
- neue Version nur, wenn der aktuell gebundene fehlgeschlagene Gate-Schritt eine Codeänderung erfordert.
- keine Zusatzanalyse außerhalb des aktuellen Gates oder expliziten Nutzerauftrags.
- bereits bestandene Evidence wird bei identischem Source-Manifest wiederverwendet statt erneut geprüft.
- ein Source-Change macht Evidence mit abweichender Source-Bindung ungültig.
- Release erst nach vollständigem Realpfad; Teil-PASS ist niemals Release-PASS.

## Aktueller gebundener Zustand

`WAITING_FOR_CANONICAL_SOURCE_BYTES`

Einziger autorisierter nächster Schritt:

`COMMIT_EXACT_V6638_21_FILE_SOURCE_TO_CANONICAL_ROOT`

Erlaubt sind dabei nur der direkte kanonische Source-Pfad und die gebundene State-Datei. **Nicht erlaubt:** historische Rekonstruktion, weitere Chunk-Reparatur, neue Plugin-Version, neuer Releasebranch, neue CI-Architektur oder irgendein Symptomfix.

Die 21 erwarteten Dateien und SHA-256 stehen bereits in `CURRENT_SOURCE_SHA256.txt`; deren Manifest-SHA ist `40972031c4e6ca2937bc3571de1b537950b8311e607c86d304b25c74ad3047d1`.

## Danach – ohne neue Planung

Nach 21/21 Hash-PASS wechselt der gebundene Zustand zu `RUNNING_BOUND_RELEASE_GATES`. Dann wird die vorhandene Gate-Kette in fester Reihenfolge abgearbeitet. PASS-Evidence bleibt bei identischem Source-Manifest gültig. Erst bei einem echten Gate-FAIL darf genau dieser Fehler zum Rootfix-Scope werden.

Final gilt weiterhin: Real-WordPress/MariaDB, Same-UUID/Recovery, Negativ-/Counterstates, Fresh-Unpack, gesamter Workflow gegen exakt die finale ZIP, Source↔ZIP und finaler SHA. Erst dann `release_allowed=true`.

## Einmalige Aktivierung

Der bestehende Main-Ruleset verlangt `hardlock` und `hardlock-base` und hat keinen Bypass. `hardlock-base` sperrt Änderungen an `.github/workflows/**`. Deshalb kann die neue Governance nicht seriös durch einen Trick in diese Workflows eingeschleust werden.

Nach Materialisierung der direkten Source ist genau **eine administrative GitHub-Aktivierung** nötig: den Governance-Check als Required Check binden bzw. den Hardlock einmalig so erweitern, dass dieser Check geschützt ausgeführt wird. Danach wird die Governance selbst immutable. Das ist Bootstrap, keine wiederkehrende Nutzeraktion.
