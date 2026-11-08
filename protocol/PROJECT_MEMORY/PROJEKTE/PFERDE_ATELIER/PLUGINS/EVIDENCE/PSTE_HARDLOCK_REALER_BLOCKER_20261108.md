# Pferdeatelier – tatsächlicher GitHub-Hardlock-Blocker, 08.11.2026

**Festgestellter Fehler, keine Vermutung:**

- Fehlgeschlagener ursprünglicher Workflow `Pferde Atelier Immutable Base Hardlock`, [GitHub Actions Lauf 42466410773](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42466410773), Job `hardlock-base`.
- Genau fehlgeschlagener Aufruf: `python3 control/paul-scope-gate/paul_scope_gate.py verify-pr "$HEAD_REF" "$HEAD_SHA" "$BASE_SHA"`.
- Tatsächlicher GitHub-Runner-Befund: `python3: can't open file '.../control/paul-scope-gate/paul_scope_gate.py': [Errno 2] No such file or directory` (Exit 2).
- **Exakt dieselbe Datei ist auf beiden über GitHub API geprüften Branches nicht vorhanden:** `fix/pste-mini-workflow-kiss-20261107` (**PR-Ausgangsstand**) und `fix/pste-kisten-einmalige-pruefung-20261107` (**aktueller QA-Stand**): beide GitHub `fetch_file` = **404 Not Found**. Der fehlende Pfad wurde durch das aktuelle QA-Diff nicht gelöscht.
- Der GitHub-PR-Gesamtvergleich enthält nach Entfernung der temporären QA-Testworkflows **keine** Änderungen unter `.github/`, `control/` und an Original-Plugin-ZIPs. Die eigene technische QA belegt weiterhin nicht, dass diese gesonderte Sicherheitsprüfung bestanden wäre.

**Schluss:** Die immutable Hardlock-Prüfung ist derzeit wegen ihrer **fehlenden, vom Workflow erwarteten Prüfdatei** nicht ausführbar. Das ist ein konkreter eigenständiger Sicherheits-/Baseline-Blocker, **keine** WordPress-Semantik-, PSERC- oder K0-Ursache.

**Verbindliche sichere Behandlung:** Nicht im Plugin-Branch eine Attrappe erzeugen, den Test überspringen oder Hardlock-Regeln lockern. Die zuständige autorisierte **Sicherheits-/Basisverwaltung** muss den Workflowpfad und die erwartete vertrauenswürdige Datei am geschützten Ausgangsstand wieder zur Deckung bringen und danach den Original-Hardlock mit PASS ausführen. Bis dahin **kein Merge, keine Installationsfreigabe** des Testpaares.

**Technischer QA-Stand bleibt getrennt:** `EVIDENCE/PSTE_PSERC_TESTPAAR_QUELLABNAHME_20261108.md`. PSTE und PSERC Paket-/Quelltest PASS, aber echte WordPress-Testinstallation und externe SEO-Arbeit weiterhin offen.
