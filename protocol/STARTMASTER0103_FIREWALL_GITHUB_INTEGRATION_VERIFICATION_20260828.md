# STARTMASTER0103 – Firewall GitHub Integration Verification

Stand: 28.08.2026

## Ergebnis
PASS.

GitHub-Workflow: `.github/workflows/pferde-atelier-ai-tool-firewall.yml`

Verifizierter Push-Run:
- Run ID: `33215079905`
- Job ID: `98996786653`
- Commit: `a4084afd2b22cdbab2e7c6141885760adedc8f4b`
- Checkout: PASS
- Controller-Runtime-Assemble: PASS
- Hardlock-Preflight: PASS
- Modellaufruf: auf Push absichtlich SKIPPED; nur manuell per `workflow_dispatch` zulässig.

Der Controller verwendet `tool_choice.allowed_tools`, eine lokale step-spezifische Allowlist, `parallel_tool_calls=false`, ein festes Ergebnis-Schema, `CONTROLLER_ONLY` für State-Write und Default DENY für unbekannte Schritte.

Aktuelles API-Modell: `gpt-5.6-sol` (explizit übersteuerbar über `PFERDE_ATELIER_MODEL`/`--model`).

## Lokale harte Regression
`ALL_POSITIVE_NEGATIVE_TESTS_PASS` einschließlich:
- korrigiertes Paket PASS;
- wiederholter Kategorie-Identitätsfehler BLOCKED;
- Scope-Mismatch BLOCKED;
- STARTMASTER0039-Boundary-Verstoß BLOCKED;
- fehlende Release-Bindung BLOCKED;
- falscher State-Hash BLOCKED;
- falscher Step BLOCKED;
- nicht erlaubtes Tool BLOCKED;
- Modell-State-Write BLOCKED;
- falsches Result-Step BLOCKED.

## Schutzparität
PSTE 0.56.25, PSERC 0.28.14, PPM 6.7.9, Textmaschine, LanguageTool, Artikelinhalte, Design, Dubletten-/Kannibalisierungsschutz und Publish-Logik unverändert. Kein Auto-Publish.

MASTER STARTMASTER0103 SHA-256: `d9e132a9786f6413741ff7e9969413b518c4d992f64e7ca79f9d69681e0fe7fd`.

Hinweis: Der echte API-Modellaufruf benötigt einmalig das GitHub Repository Secret `OPENAI_API_KEY`. Der Hardlock-/Preflight-Pfad selbst ist bereits live in GitHub Actions erfolgreich ausgeführt.
