# PSTE 0.57.143.2 – NEGATIVPROBE: alte Prüfwerte sind keine aktuelle Freigabe (02.11.2026)

**Kein neues WordPress-Plugin. Kein Release.** Die sichere Teilkorrektur aus PR #608 ist weiterhin nur ein unverändertes QA-Delta (SHA256 `e9c66d3d76a4afd0bebf6c3cfba7cbb14291eff37be2cc0e3753343bb9b04577`).

Eine **neue isolierte, nicht freigegebene** Phase-3-Variante entfernte die Kontext-Zweitentscheidung `ANSWER_EQUIVALENT_PLANNED`/ `ANSWER_EQUIVALENT_EXISTING`, ließ die vorhandene zentrale Planung die Keyword-/Plankollision entscheiden und fügte gespeicherte WordPress-/Plan-Prüfsummen hinzu.

**Gegenprobe mit den tatsächlichen vorhandenen PHP-Klassen:**
1. Plan alt: leer. Zentrale Prüfung des Themas „Wie viel Heu braucht mein Pferd?“ PASS, beide gespeicherten Prüfbelege stimmen überein.
2. Plan neu: derselbe Artikel wird inzwischen geplant. Eine *wirklich neu ausgeführte* zentrale Prüfung ergibt **BLOCKED**.
3. Die isolierte Testvariante verglich aber nur zwei *alte gespeicherte Prüfwerte*. Damit lieferte `currentSnapshotMatches=true` und `planningSuitability=YES`, obwohl der neue aktuelle Plan das Thema blockieren müsste.

**Ergebnis:** Negativtest endet absichtlich mit Status 17 / `FAIL_UNSAFE_STALE_SNAPSHOT_ACCEPTED`; `previous_source_is_bound=true`, `prior_suitability=YES`, `new_central_decision=BLOCKED`. Damit ist der Versuch **beweisbar UNSICHER und wurde verworfen**. All 78 PHP-Dateien Syntax-PASS genügt gerade NICHT als Freigabe. Die Testvariante blieb separat und wird weder als PR-Quelldelta noch als Installations-ZIP übernommen.

**Zusätzliche echte Quellbefunde:**
- `PSTE_Repository::compilerPlanningTopicPage` benutzt gespeicherte `planning_suitability='YES'` und `context_state=CURRENT`, ohne selbst die aktuelle redaktionelle Plan-Quelle gegen die gespeicherte Freigabe zu prüfen.
- `PSTE_Repository::refreshPortalContextForKeysUsingBinding` liest den früher gebundenen Index, nicht automatisch einen inzwischen neuen Plan.
- `PSTE_Article_Ownership_Gate` schützt einen *separaten eindeutigen importierten Eigentümer* anhand `owner_concept_id`/ `semantic_intent_key`, enthält jedoch zusätzlich einen Legacy-Keyword-/Titeläquivalenzvergleich, der fachlich mit der zentralen Dublettenentscheidung überschneiden kann. Nie pauschal aushebeln.

**Nächste KISS-Arbeit:** Die tatsächlich aktuelle Plan-Quelle **an der bestehenden abschließenden Compiler-/PSERC-Übergabe einmal pro begrenztem Paket** gegen das gespeicherte Freigabe-Receipt verifizieren, bei Änderung STOP und erneuten zentralen Planungsowner-Lauf verlangen; auch WordPress-Bestandsänderungen müssen mit einem aktuellen Beleg behandelt werden. Keine zweite redaktionelle Prüfung an der Übergabe, nur der vorhandene Freigabebeleg wird gültig/ungültig. Erst wenn diese Race-Kante und der optionale Upstream-Legacy-Überlapp sauber erledigt sind, die Kontext-Zweitentscheidung entfernen und alle Worker/JSON-Reentry-/5.014er/PSERC→K0-Grenzen gemeinsam testen. **Erst dann genau ein kumuliertes Test-ZIP; Live 0.57.120 unangetastet.**

Vollständiger ausführlicher Bericht in bestehender Library `/Pferdeatelier/TempVerify/PFERDEATELIER_1432_NEGATIVPROBE_ALTER_PLAN_NEUER_DOPPELARTIKEL_20261102.md`, SHA256 `866f34a10fc20724b0992fe99e917925081f6a6c7da244c3732a6926d9a1b74f`.