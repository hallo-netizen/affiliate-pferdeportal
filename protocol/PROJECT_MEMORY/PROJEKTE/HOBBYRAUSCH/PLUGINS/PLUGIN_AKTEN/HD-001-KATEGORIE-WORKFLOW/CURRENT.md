# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-01
STATUS: V1.9.4 TERM-NAME READBACK FIX / LIVE-ROOT-CAUSE BEWIESEN / SOURCE+FRESH-INSTALLER POSITIV+NEGATIV HARD PASS / LIVE-RETEST OFFEN

## Harte Abnahmeregel

**Keine Abnahme ohne dokumentierte lokale Positiv- UND Negativsimulation.**

Ein synthetischer Einzeltest reicht nicht. Der echte Produktionspfad mit dem echten Buchbinden-Kandidaten muss simuliert sein.

## Live-Root-Cause – bewiesen

V1.9.3 Diagnose meldete live:

`DEPLOY_READBACK_MISMATCH @ node:hdc-21557545f2e7cc51 | Felder: name | Automatischer Rollback: PASS`

Der Knoten ist:
`Techniken & Praxis`.

WordPress Core speichert Taxonomie-Namen über `pre_term_name` und `_wp_specialchars`.
Damit wird der Klartextname

`Techniken & Praxis`

intern als

`Techniken &amp; Praxis`

gespeichert.

Der bisherige Readback verglich den rohen gespeicherten Termnamen bytegenau mit dem freigegebenen Klartextnamen. Dadurch entstand genau der Live-Mismatch.

## Exakte Reproduktion mit altem Code

V1.9.3 + echter Buchbinden-READ_ONLY_PREVIEW + echter 7-CREATE-Pfad + WordPress-Core-Term-Escaping:

`DEPLOY_READBACK_MISMATCH @ node:hdc-21557545f2e7cc51 | Felder: name | Automatischer Rollback: PASS`

Damit ist der Livefehler lokal wortgleich reproduziert.

## Fix V1.9.4

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.9.4`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.4_TERM_NAME_READBACK_FIX_HARD_PASS.zip`

Installer SHA-256:
`85990b87f0ef35530b616df7716547cb20974d1c77ca21aa7b3e0edec723f249`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.4_TERM_NAME_READBACK_FIX_HARD_PASS.zip`

Source SHA-256:
`12dcce406d842bd7b8a6cde5af6a54dff2a4bbff3e27528c04231898a8f02e01`

Änderung:
- nur Taxonomie-Termnamen werden beim Lesen von WordPress-Core-Sonderzeichen-Escaping zurück in Klartext normalisiert;
- Seiten-Titel bleiben unverändert;
- keine Struktur-/Research-/Ownership-Regel geändert;
- echte semantische Namensabweichungen bleiben fail-closed.

## Positiv-/Negativsimulation

Exakter Produktionspfad:
- echter Buchbinden-READ_ONLY_PREVIEW;
- echtes Research-Paket;
- 7 CREATE;
- WordPress-Core-Escaping aktiv.

Positiv V1.9.4:
- `Techniken & Praxis` → intern `Techniken &amp; Praxis`;
- Deploy + Readback PASS.

Negativ:
- echter falscher Kategoriename → `name` Mismatch + Rollback PASS;
- doppelt falsches `Techniken &amp;amp; Praxis` → `name` Mismatch + Rollback PASS;
- falscher Slug → BLOCKED + Rollback PASS;
- falscher Parent → BLOCKED + Rollback PASS;
- falsches concept_meta → BLOCKED + Rollback PASS;
- falsches logical_parent_meta → BLOCKED + Rollback PASS.

Regression:
- Source 251/251 PASS;
- Fresh-Installer 251/251 PASS;
- Source PHP-Lint 25/25 PASS;
- Fresh-Installer PHP-Lint 17/17 PASS;
- Source↔Installer Runtime-Parität 22/22 byteidentisch.

## Aktueller Live-Zustand

Der letzte V1.9.3-Diagnoselauf wurde **vollständig zurückgerollt**.

WordPress zeigt:
- `Testlauf vollständig zurückgerollt.`
- `Rollback abgeschlossen. Der technische Testbestand ist zurückgesetzt.`

Damit existiert **kein aktiver Dry-Run mehr**.

## NEXT ACTION

1. V1.9.4 über V1.9.3 installieren.
2. In `Kategorien` denselben bereits geprüften `HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_V1.json` erneut als neuen Arbeitsstand übernehmen.
3. `Finale Struktur freigeben`.
4. `WordPress-Vorschau erstellen`.
5. neuen 7-CREATE-Plan über `Geprüften Plan anwenden` ausführen.

Kein neuer Research-Lauf.
Keine neue fachliche Strukturdatei erzeugen.

Erwartung:
`Deployment abgeschlossen` + `Schreiben und Readback erfolgreich.`

Bei irgendeinem Fehler:
keine Abnahme; exakte Fehlermeldung auswerten.
