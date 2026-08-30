# Codex-Auftrag – Generation 1 / 7 bestehende Artikel bis 107008

## Einzige Aufgabe
Führe die bereits vorhandenen sieben Generation-1-Artikel im bestehenden STARTMASTER0107-/H7-/Single-Door-Workflow bis zum vorgesehenen Endzustand 107008 `FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Dies ist keine neue Artikelproduktion und kein neuer Workflow.

## Verbindlicher Einstieg
- Bleibe auf dem vom Nutzer ausgewählten Branch. Nicht auf einen anderen Branch wechseln.
- Lies zuerst `control/CURRENT_STARTMASTER.json`.
- Der dort gebundene `gate_ref` ist die einzige Ablaufautorität.
- Keine freie Navigation aus Chat-Historie.
- `free_chat_execution_authority=false` bleibt unverändert.

## Quelle – kein Upload, keine externe Datei
Die exakte Generation-1-Quelle liegt bereits in diesem Branch. Rekonstruiere sie ausschließlich mit:

```bash
python3 control/startmaster0107/production-package-release/reconstruct_gen1_source.py /tmp/GENERATION1_7_ARTIKEL_PRODUKTIONSPLAN.json
```

Nur bei `GENERATION1_SOURCE_RECONSTRUCTED_EXACT` weiterarbeiten.

Die Rekonstruktion muss zwingend ergeben:
- SHA-256 `0535129cb98fd78e1167007870eb628bee16e34e844d2fc91588a987c3465334`
- 114929 Bytes
- Contract `production_plan_v4`
- Generation 1
- 7 Items
- Batch SHA-256 `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`

Bei Abweichung fail-closed stoppen. Nichts rekonstruieren, ersetzen oder neu erzeugen.

## Recovery-Lock
Danach exakt:

```bash
python3 control/startmaster0107/production-package-release/production_package_release_gate.py recovery-manifest /tmp/GENERATION1_7_ARTIKEL_PRODUKTIONSPLAN.json /tmp/GENERATION1_7_ARTIKEL_RECOVERY_LOCK.json
python3 control/startmaster0107/production-package-release/production_package_release_gate.py verify-recovery /tmp/GENERATION1_7_ARTIKEL_RECOVERY_LOCK.json /tmp/GENERATION1_7_ARTIKEL_PRODUKTIONSPLAN.json
```

Nur bei `EXISTING_TEXT_RECOVERY_LOCK_PASS` weiterarbeiten.

Damit sind für diese sieben Artikel gesperrt:
- Textänderungen,
- neue Titel,
- neue Keywords,
- neue Kategorien,
- neue Artikeltypen,
- neue Themenrecherche,
- neuer Batch.

## Danach nur der bestehende Wächterweg
Führe aus:

```bash
python3 control/single-door-boundary/project_single_door_entry.py status
```

Danach ausschließlich die dort gebundene Aktion ausführen. Keine eigene Route, keine Ersatzaktion und keine manuelle Änderung des Runtime-State.

Nicht ändern, abschwächen oder umgehen:
- H7 / Project Single-Door / CURRENT_STARTMASTER,
- Hardlocks und Entrance Gate,
- Recherche-/Fact-Pack-Regeln,
- Inhalts-/Fach-/Qualitätsregeln,
- LanguageTool,
- PPM,
- PSERC,
- PSTE,
- Dubletten-/Kannibalisierungsregeln,
- SEO-/Titel-/Keyword-Regeln,
- Design-/Formatregeln,
- Publish-Regeln.

Keine Wiederholung von 107001–107006. Kein Auto-Publish. `publish_allowed=false` bleibt zwingend.

## Fehlende Pflichtstufen der alten sieben Texte
Die Texte stammen aus der Zeit vor der späteren H7-Nachschärfung. Die Texte bleiben erhalten, aber alle heute bestehenden Pflichtstufen bleiben zwingend, insbesondere:
1. Fact-Pack-Bindung,
2. Language-/Quality-Bindung,
3. bestehende Workflow-Supervisor-Freigabe,
4. echte autorisierte ED25519-Signatur,
5. vollständiges `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`,
6. bestehender Production-Package-Preflight,
7. technischer Release-Gate-Check,
8. H7 `R_PRE_001`-Handoff,
9. bestehender 107007-Lauf,
10. 107008 Final Review.

Keine private Signatur erfinden, keine Testsignatur verwenden und keinen Signierschutz umgehen. Ist die echte autorisierte Signierinstanz nicht erreichbar, exakt dort fail-closed stoppen.

## Produktionspaket
Ein `production_plan_v4` ist niemals die WordPress-Upload-Datei.

Nur ein vollständiges und korrekt signiertes `PSERC_APPROVED_PRODUCTION_PACKAGE_V1` darf ausgegeben werden. Vor Ausgabe müssen die bestehenden Paketprüfungen PASS sein.

## Endausgabe
Bei vollständigem PASS nur kurz ausgeben:
- `GENERATION1_107008_READY_FOR_USER_REVIEW`
- Item count 7
- Batch SHA-256
- Package-ID / Package-SHA
- `publish_allowed=false`
- exakten Pfad der einen fertigen `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`-JSON
- Review-Ergebnis 107008

Bei echtem BLOCKED nur ausgeben:
- exakter Blocker,
- welche bestehende Pflichtstufe ihn erzeugt hat,
- konkreter Beleg,
- keine Alternativroute und keine neue Titel-/Recherche-/Textproduktion.
