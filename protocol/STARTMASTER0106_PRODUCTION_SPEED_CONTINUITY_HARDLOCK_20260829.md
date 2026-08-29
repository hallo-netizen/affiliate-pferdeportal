# STARTMASTER0106 – Produktionsgeschwindigkeit / Kontinuität / Hardlock

Stand: 29.08.2026

## Ziel
Zeitverlust durch eigene Workflowentscheidungen des Modells, Rücksprünge, Seitensprünge, unnötige Wiederholungsprüfungen und Chatwechsel beseitigen. Bestehende Fach-/Inhalts-/Qualitäts-/Designlogik unverändert lassen.

## Nachgewiesener Sicherheitsstand
- Reales Codex-Cloud-Gate: Nutzer meldete exakt `CODEX_CLOUD_GATE_VERIFY_PASS`.
- GitHub Ruleset `Pferde Atelier Main Hardlock`, ID 21788951: aktiv, Ziel Default-Branch/main.
- Bypass-Liste leer; GitHub API: `current_user_can_bypass=never`.
- Aktiv: Delete-Schutz, Non-fast-forward/Force-push-Schutz, Pull Request Pflicht, Statuscheck `hardlock`, strict/up-to-date.
- Harte Negativprobe nach Aktivierung: direkter Create-File-Schreibversuch auf `main` wurde mit HTTP 409 abgewiesen: Änderungen müssen über Pull Request erfolgen; `hardlock` wird verlangt. Es entstand keine Testdatei.

## Harte Trennung
Die Eingangstür und Continuity-Schicht besitzen keine Fachautorität. Sie bewerten weder Beitragsart noch Titel, Keywords, Recherche, Text, Qualität, Design, PSTE, PSERC, PPM, LanguageTool, Dubletten-/Kannibalisierung oder Publish. Sie steuern ausschließlich Reihenfolge, Zustandsbindung, Batchfortschritt und Wiederaufnahme.

## Neu in STARTMASTER0106
1. verbindlicher Texterstellungs-Prompt;
2. Zielvertrag `Medium so weit wie möglich`, ohne irgendeinen Gate abzuschwächen;
3. NO-STOP-/Continuity-Hardlock;
4. Notfallübergabe für neuen Chat mitten im Batch;
5. Continuity-Guard mit Positiv-/Negativtests;
6. weiterhin kein Auto-Publish.

## NO-STOP
Ein aktiver Textbatch darf nicht wegen interner PASS/Hashes/Checkpoints unterbrochen werden. Checkpoints werden still gespeichert. Eine finale Batch-Freigabe ist nur zulässig, wenn alle gebundenen Item-IDs abgeschlossen sind. Chatgrenze führt zu Resume, nicht zu Neustart.

## Medium-Ziel
Medium ist Standard für Routine- und Textschritte, sofern derselbe unveränderte bestehende Workflow vollständig PASS bleibt. Höhere Stufe nur für bereits bindend höher eingestufte oder nachweislich bei Medium nicht sicher abschließbare Schritte. Kein Gate darf zur Erreichung von Medium verändert werden.

## Bestehender offene Schritt
Der 6er-Test ist veröffentlicht. Nächster bindender technischer Schritt bleibt `ROOTFIX_LIVE_40_40_MAX_FAMILIES_REACHED`; danach Sandbox AUTO_REENTRY -> retained backlog -> provider -> neuer Beitragsbatch.

## Keine fachliche Änderung
STARTMASTER0106 ändert keine aktuellen Installer und keine Fach-/Inhalts-/Qualitäts-/Designverträge. PSTE 0.56.25 und PSERC 0.28.14 bleiben unverändert. Textmaschine/Nullpunkt und geerbte Qualitätsartefakte bleiben unverändert.
