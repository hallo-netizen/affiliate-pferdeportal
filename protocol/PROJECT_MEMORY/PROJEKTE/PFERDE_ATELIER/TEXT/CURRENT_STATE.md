# PFERDE ATELIER – TEXT – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

> **Einzige aktuelle Zustandsautorität dieses Scopes.** Status, erster offener Blocker und NEXT ACTION werden nur hier gepflegt.  
> `HOBBYRAUM.md` ist lediglich abgeleitete Ausführungsfläche.

STAND: 2026-09-18
STATUS: M39 HISTORY AUTHORITY MAINTENANCE

## EINE AKTUELLE WAHRHEIT

Current technical main:
`f9bc719efd0924a18ee876ee8581a566afa7ecda`

Letzter belastbarer Pre-Codex-Recovery-Stand:
`508f9dbb3650c99e5d41dbab83086af46945e225`

Aktueller erster Blocker:
`CURRENT_7ER_BATCH_ALREADY_HAS_DURABLE_RELEASE_IDENTITY_COLLISION`

Der 7er-Batch selbst bleibt unverändert. Die alte dauerhafte Ausgabe verwendet dieselbe Batch-ID als Release-ID. Ein frischer NEW-Lauf mit neuen Bytes würde dadurch später kollidieren.

## M39

M39 registriert ausschließlich diese technische Identitätskollision:
- logische Batch-ID bleibt unverändert;
- neue Ausgabe benötigt eine eigene technische Release-ID;
- alte Recovery-Artikel bleiben als Produktionsquelle verboten;
- keine Änderung von Artikelmetadaten oder Fach-/Qualitäts-/Designregeln;
- kein Publish.

History-Kandidat:
- Branch: `hobbyroom/m39-release-identity-history-20260918`
- Head: `5546adc61404437ac9de7ff35bba2d982b9d6266`
- erwarteter Beweis: current main M01–M38 PASS, M39 erster neuer FAIL.

Der bereits vorbereitete Produktfix bleibt bis zum erfolgreichen M39-History-Beweis getrennt und wird nicht in diesen History-Kandidaten gemischt.

## NEXT ACTION

M39-History-Kandidat mit bestehendem History-Maschinenweg, Hardlock und Hardlock-base beweisen und integrieren. Danach Produktfix neu auf dem resultierenden Main aufsetzen und vollständig prüfen.

## HARTE GRENZEN

- kein echter Codex;
- kein Artikelproduktionslauf;
- kein neuer Runner/Gate/Controller/Sidecar;
- keine Text-/SEO-/Design-/PPM-/PSERC-/PSTE-/WordPress-Regeländerung;
- kein Publish.
