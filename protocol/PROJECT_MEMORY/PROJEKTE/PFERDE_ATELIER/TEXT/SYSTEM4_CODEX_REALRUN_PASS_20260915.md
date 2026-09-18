# PFERDE ATELIER – TEXT – SYSTEM 4 – REALER CODEX-LAUF – 2026-09-15

## STATUS

**REALER EIN-ARTIKEL-CODEX-LAUF: PASS**

PR: `#259`
Produktions-Head: `a9cb5e3a7500cf4ba5e4551591ffd79cae57e36e`
Codex-Auftrag: Kommentar `5675455629`
Codex-Ergebnis: Kommentar `5675516766`

Es wurde exakt ein gebundener Artikel verarbeitet. `publish_allowed=false` blieb verbindlich. Kein Merge, kein Publish, kein zweiter Artikel.

## REPARATURVERLAUF

1. Realer Start über `parent_start.py start-bound`: PASS.
2. Worker-Start, Research, Facts, Context, Draft: PASS.
3. Erster Fullcheck: reparierbare LanguageTool-Befunde.
4. Same-Article-Repair: PASS.
5. Nächster Fullcheck: `BLOCKED_CONTENT_TITLE_COLON`.
6. Fehler wurde korrekt an `PARENT_METADATA/TITLE_BINDING` zurückgeroutet.
7. Derselbe Artikel wurde mit unverändertem Plan-Slot, Keyword, Kategorie und Artikeltyp neu gebunden und erneut durch Research → Facts → Context → Draft geführt.
8. Danach reparierbarer Befund `BLOCKED_WAVE2_CONCLUSION_BALANCE`.
9. Dieser wurde korrekt über `DRAFT_BODY/SAME_ARTICLE_BODY_REPAIR` repariert.
10. Erneuter Fullcheck: `SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED`.
11. Batch Gate: PASS.
12. V2-Handoff: PASS.
13. Inline-Pack/Unpack: PASS.
14. Bytegleiche Rekonstruktion: PASS.

## FINALER HANDOFF

- Artikelanzahl: `1`
- Canonical plaintext SHA256: `5e6a537315cb6610c300f0772f5bddcccc670f8dcadb3d816203652bf8603c7c`
- Byte length: `29660`
- Relay parts: `1`
- Runtime-Datei: `/tmp/system4-parent-runtime/SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json`
- Rekonstruierte Datei: `/tmp/system4-parent-runtime/parent-chat/SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json`
- Bytegleichheitsprüfung via `cmp -s`: PASS.

## BEDEUTUNG

Der reale Codex-Lauf hat erstmals die neue Rückrouting-Logik im echten Produktionslauf erfolgreich bewiesen:
- reparierbarer Metadatenfehler -> zuständige Parent-Metadaten-Stufe -> Neubindung -> erneuter Weiterlauf;
- reparierbarer Textfehler -> Same-Article-Repair -> erneute Vollprüfung;
- anschließend echter LT-6.8-/PPM-6.7.9-PASS bis zur bytegleichen finalen Datei.

## REPOSITORY-STATUS

Codex benötigte keine Repository-Änderung. Working Tree am Ende sauber. Kein Commit durch Codex, kein neuer Pull Request, kein Merge, kein Publish.

## NEXT ACTION

Dieser reale Ein-Artikel-Lauf ist als **PASS-Nachweis** festzuhalten. Weitere Produktionsfreigaben bleiben davon getrennt und benötigen ihre eigenen Freigaben/Nachweise.
