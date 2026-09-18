# PFERDE ATELIER – TEXT – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

> **Einzige aktuelle Zustandsautorität dieses Scopes.** Status, erster offener Blocker und NEXT ACTION werden nur hier gepflegt.  
> `HOBBYRAUM.md` ist lediglich abgeleitete Ausführungsfläche.

STAND: 2026-09-18
STATUS: PRE-CODEX FULL SIMULATION PASS / INTEGRATION PENDING

## EINE AKTUELLE WAHRHEIT

Current technical main:
`508f9dbb3650c99e5d41dbab83086af46945e225`

Aktueller Pre-Codex-Kandidat:
- Branch: `hobbyroom/full-e2e-simulation-before-codex-20260918`
- Head: `b1c33ee8e800ccc5b542c077ffe825bd20871581`
- Acceptance-Run: `35356394787`
- Ergebnis: **40/40 PASS**

## WAS DAMIT BEWIESEN IST

- Chat-/Startweg bis Point-0 und Root: PASS.
- fehlende externe Point-0-Datei: fail-closed BLOCKED.
- Worker-Anbindung wird im Test über den echten `codex_entry.py worker-start`-Weg simuliert.
- kompletter 1-Artikel-Lauf: PASS.
- kompletter 3-Artikel-Lauf mit isoliertem Repair: PASS.
- LanguageTool 6.8: PASS.
- PPM 6.7.9: PASS.
- Batch-/Handoff-/Dateiausgabe: PASS.
- 1..N-Downstream-Vertrag: 1 / 3 / 25 / 1000 PASS.
- Negativfälle bleiben fail-closed.
- vor `advance` muss die Artikelidentität jetzt exakt über `title / target_keyword / category / article_type / plan_slot` übereinstimmen.
- kein echter Codex-Lauf und kein Publish sind Teil dieses Beweises.

M38 ist im produktiven `control/startmaster0107/CURRENT_STATE.json` bereits als gelöst gebunden; die alte Campus-M38-Blockerbeschreibung war stale und ist hiermit ersetzt.

## ERSTER NOCH OFFENER PUNKT

Der funktional grüne Kandidat muss noch gegen Hardlock und Deterministic Entrance auf exakt demselben Head bewiesen und danach integriert werden. Anschließend ist derselbe vollständige Acceptance-Lauf auf dem resultierenden exakten `main` zu wiederholen.

## NEXT ACTION

1. Hardlock + Deterministic Entrance für Kandidat `b1c33ee8e800ccc5b542c077ffe825bd20871581` ausführen.
2. Nur bei PASS auf `main` integrieren.
3. Vollständigen 1-/Mehrartikel-Acceptance-Lauf erneut auf dem exakten neuen `main` ausführen.
4. Danach **STOP direkt vor echtem Codex**.

## HARTE GRENZEN

- **Kein echter Codex ohne ausdrückliche Freigabe des Nutzers.**
- kein Artikel 2 vor echtem Artikel-1-PASS im späteren Produktionslauf.
- kein neuer Runner/Gate/Controller/Sidecar.
- keine PPM-/PSERC-/PSTE-/Textmaschinen-/Fachregeländerung.
- kein WordPress-Write.
- kein Publish.
