# Codex-Auftrag – Generation 1 / 7 bestehende Artikel bis 107008

## Einzige Aufgabe

Führe die **bereits vorhandenen sieben Generation-1-Artikel** über den **bestehenden STARTMASTER0107-/H7-/Single-Door-Workflow** bis zum vorgesehenen Endzustand **107008 FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH**.

Dies ist **kein neuer Workflow** und **keine neue Artikelproduktion**. Es ist ausschließlich die Fertigstellung des bereits gebundenen Generation-1-Batches.

## Verbindlicher Einstieg

1. Arbeite auf aktuellem `main`.
2. Lies zuerst `control/CURRENT_STARTMASTER.json`.
3. Führe danach ausschließlich den dort gebundenen `gate_ref` aus.
4. Freie Navigation aus Chat-Historie ist verboten.
5. `free_chat_execution_authority=false` bleibt unverändert.

## Einzige externe Nutzdatei

Im Codex-Task ist genau eine JSON-Datei beigefügt. Verwende sie nur, wenn ihre Eigenschaften exakt sind:

- SHA-256: `0535129cb98fd78e1167007870eb628bee16e34e844d2fc91588a987c3465334`
- Größe: `114929` Bytes
- Top-Level-Contract: `production_plan_v4`
- Generation: `1`
- Item count: `7`
- Batch SHA-256: `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`

Bei Abweichung: fail-closed, nichts rekonstruieren und keine Ersatzdatei erzeugen.

## Recovery-Lock zuerst

Bevor irgendeine Fachstufe weiterläuft, erzeuge aus genau dieser Datei den Recovery-Lock ausschließlich mit dem bereits vorhandenen Tool:

```bash
python3 control/startmaster0107/production-package-release/production_package_release_gate.py recovery-manifest <EXAKTER_PFAD_DER_BEIFUEGTEN_JSON> control/startmaster0107/production-package-release/GENERATION1_7_ARTIKEL_RECOVERY_LOCK.json
python3 control/startmaster0107/production-package-release/production_package_release_gate.py verify-recovery control/startmaster0107/production-package-release/GENERATION1_7_ARTIKEL_RECOVERY_LOCK.json <EXAKTER_PFAD_DER_BEIFUEGTEN_JSON>
```

Nur bei `EXISTING_TEXT_RECOVERY_LOCK_PASS` weiterarbeiten.

Der Recovery-Lock bedeutet zwingend:

- vorhandene Artikeltexte nicht verändern,
- Titel nicht neu erzeugen,
- Keywords nicht neu auswählen,
- Kategorien nicht neu auswählen,
- Artikeltypen nicht neu auswählen,
- keine neue Themenrecherche,
- keinen neuen Batch erzeugen.

## Unveränderliche Grenzen

Nicht ändern, abschwächen oder umgehen:

- H7 / Project Single-Door / CURRENT_STARTMASTER,
- Hardlocks und Entrance Gate,
- Recherche- und Fact-Pack-Regeln,
- Text-/Inhalts-/Fachregeln,
- LanguageTool,
- PPM,
- PSERC,
- PSTE,
- Qualitätsprüfungen,
- Dubletten-/Kannibalisierungsregeln,
- SEO-/Titel-/Keyword-Regeln,
- Design-/Formatregeln,
- Publish-Regeln.

Kein Auto-Publish. `publish_allowed` muss immer `false` bleiben.

## Fertigstellung der sieben vorhandenen Texte

Die sieben Texte stammen aus einer Produktion vor der späteren H7-Nachschärfung. Deshalb dürfen die Texte selbst erhalten bleiben, aber **keine heute verpflichtende Sicherheits- oder Qualitätsstufe darf übersprungen werden**.

Arbeite die für diese sieben noch fehlenden **bereits vorhandenen** Pflichtstufen ausschließlich mit den im Repository und der autorisierten Laufzeit vorhandenen Werkzeugen/Autoritäten ab. Insbesondere bleiben erforderlich:

1. Fact-Pack-Bindung,
2. Language-/Quality-Bindung,
3. bestehende Workflow-Supervisor-Freigabe,
4. bestehende ED25519-Signatur durch die vorhandene autorisierte Signierinstanz,
5. vollständiges `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`,
6. bestehender Production-Package-Preflight,
7. neuer rein technischer Release-Gate-Check,
8. H7 `R_PRE_001`-Handoff,
9. bestehender unveränderter 107007-Lauf,
10. 107008 Final Review.

**Keine private Signatur erfinden, keine Testsignatur verwenden, keinen Signierschutz umgehen.** Wenn die autorisierte Signierinstanz in der Laufzeit nicht erreichbar ist, exakt dort fail-closed stoppen und den fehlenden bestehenden Autoritätszugang benennen. Keine Ersatzarchitektur bauen.

## Produktionspaket-Regel

Ein `production_plan_v4` ist niemals die Benutzer-Upload-Datei.

Nur ein bereits vollständiges, korrekt signiertes `PSERC_APPROVED_PRODUCTION_PACKAGE_V1` darf als Upload-Datei ausgegeben werden.

Vor Ausgabe müssen alle drei Prüfungen PASS sein:

```bash
python3 control/production-package-preflight/PRODUCTION_PACKAGE_PREFLIGHT_GUARD_STARTMASTER0103.py <PAKET.json>
python3 control/startmaster0107/production-package-release/production_package_release_gate.py validate <PAKET.json>
python3 control/single-door-boundary/project_single_door_entry.py status
```

Das Paket darf nur über den bestehenden H7-Single-Door-Weg an den Runtime-Slot gebunden werden. Runtime-State niemals manuell editieren.

## Keine Zwischenstopps

Solange der bestehende Workflow keinen echten technisch zwingenden `USER_ACTION_REQUIRED`- oder fail-closed-Zustand liefert, ohne Rückfrage bis zum nächsten gebundenen Schritt weiterarbeiten.

Keine Wiederholung von 107001–107006. Keine neue Recherche. Keine eigene Reparatur außerhalb des gebundenen Fehlers.

## Zulässige Endausgabe

### Bei vollständigem PASS

Nur kurz ausgeben:

- `GENERATION1_107008_READY_FOR_USER_REVIEW`
- Item count `7`
- Batch SHA-256
- Package-ID / Package-SHA
- `publish_allowed=false`
- den **exakten Pfad der einen fertigen `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`-JSON**, die der Nutzer in WordPress verwenden soll
- Review-Ergebnis 107008

### Bei echtem BLOCKED

Nur ausgeben:

- exakter gebundener Blocker,
- welche bestehende Pflichtstufe ihn erzeugt hat,
- konkreter Beleg,
- **keine** neue Architektur, keine Alternativroute, keine neue Titel-/Recherche-/Textproduktion.
