# STARTMASTER0107 – Immutable Base Hardlock / Produktionsgeschwindigkeit / Chat-Kontinuität

Stand: 29.08.2026

## Warum 0107 notwendig wurde
Nach dem erfolgreichen Merge von STARTMASTER0106 und dem aktiven GitHub-Ruleset wurde ein letzter theoretischer Umgehungspfad gefunden: Ein Pull Request konnte den bisherigen `hardlock`-Workflow selbst ändern und damit versuchen, seinen eigenen Check abzuschwächen. STARTMASTER0107 schließt genau diese Lücke.

## Neue unveränderliche Eingangstür
Der zusätzliche GitHub-Workflow `pferde-atelier-immutable-base-hardlock.yml` läuft mit `pull_request_target` aus dem bereits geschützten Base-Branch. Deshalb kann ein Pull Request nicht die für seine eigene Prüfung verwendete Workflowdefinition verändern.

Der Base-Hardlock blockiert Änderungen an:
- `.github/workflows/**`
- `AGENTS.md`
- `control/cloud-entry-gate/**`
- `control/deterministic-entrance-gate/**`
- `control/production-continuity/**`

Diese Schicht bleibt fachblind. Sie kennt keine Beitragsarten, Titel-, Keyword-, Text-, SEO-, Qualitäts-, Design-, PPM-, PSERC-, PSTE- oder Publish-Regeln.

## Zwangsnavigation
Jeder Wechsel des aktiven Workflow-States muss monoton sein und exakt dem bereits im aktuell gebundenen Step-Bundle hinterlegten `next_binding` entsprechen. Rücksprung, Seitensprung oder frei erfundener nächster Step wird vom Base-Hardlock abgewiesen.

Für die aktuelle Produktionsstrecke sind vorgebunden:
1. ROOTFIX_LIVE_40_40_MAX_FAMILIES_REACHED
2. SAFE_SANDBOX_AUTO_REENTRY_AFTER_40_40_ROOTFIX
3. RETAINED_BACKLOG_AFTER_SANDBOX_REENTRY
4. PROVIDER_AFTER_RETAINED_BACKLOG
5. PREPARE_NEW_ARTICLE_BATCH_AFTER_PROVIDER
6. BIND_NEW_ARTICLE_BATCH_FROM_READY_TOPICS
7. RUN_NEW_ARTICLE_BATCH_NO_STOP
8. FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH

## Texterstellung / Geschwindigkeit
- Reasoning `medium` ist Zielstandard für Routine- und Textschritte.
- Kein bestehender Gate wird für Medium geändert oder ausgelassen.
- Ein aktiver Textbatch läuft ohne Zwischenmeldung bis zum vorgesehenen Batch-Ende.
- Chatgrenze löst Checkpoint + Resume aus, niemals Neustart.
- Kein Auto-Publish.

## Zukunftsflexibilität
Neue Beitragsarten, Titelregeln, Keyword-/Suchlogik oder Inhaltsregeln liegen hinter der Eingangstür und können weiterhin geändert werden. Die unveränderliche Eingangstür enthält keinerlei fachliche Regel und muss dafür nicht angepasst werden.

## Sicherheitsgrenze
Die technische Produktionsautorität kann den geschützten Gate-/Workflowpfad nicht über einen normalen Pull Request verändern. Eine absichtliche Änderung der Eingangstür selbst erfordert eine bewusste manuelle Änderung des GitHub-Rulesets durch den Repository-Administrator. Das ist ausdrücklich ein Wartungs-/Adminvorgang, keine normale Produktionsfunktion.

## Aktivierung
Nach Merge dieses Stands muss im bestehenden Ruleset `Pferde Atelier Main Hardlock` zusätzlich der Required Status Check `hardlock-base` gesetzt werden. Erst danach ist STARTMASTER0107 vollständig aktiviert.

## Ausführungsledger 107001 – 29.08.2026
- Step: `107001 ROOTFIX_LIVE_40_40_MAX_FAMILIES_REACHED`
- Vorheriger identischer Codex-Durchlauf: `BLOCKED`, weil PSTE-0.56.25-Implementierungsquelle im Repository-Arbeitsbaum fehlte.
- Diese fehlende Arbeitsgrundlage ist jetzt auf dem bestehenden Branch `restore-107001-complete-inputs-20260829` materialisiert.
- Kanonischer Arbeitsbaum-Pfad: `portal-seo-topic-engine/includes/class-pste-breadth-research-queue.php`.
- Quelle stammt aus dem bereits gebundenen PSTE-0.56.25-Bestand; dokumentierter SHA-256: `b1db3df556ef0eafd5af4095a827bd5e91c52424b479d9470f69eb429f8285e8`.
- Bestehende 0.56.25-Regressionsergebnisse und 40/40-Kontext liegen zusätzlich unter `portal-seo-topic-engine/107001_BASELINES/` und `107001_INPUT/`.
- Status dieser Aktion: `ERLEDIGT`.
- NICHT WIEDERHOLEN: erneute Suche nach PSTE 0.56.25, erneute MASTER-/Library-Suche, erneuter identischer Evidence-only-Codex-Lauf.
- Nächster noch offener Punkt innerhalb 107001: Codex Cloud muss auf genau diesem materialisierten Arbeitsbaum den bereits gebundenen minimalen Fachrootfix implementieren und die dafür erforderlichen Positiv-/Negativ-/Regressionstests ausführen.
