# STARTMASTER0107 — Teststrecke: reale Repair-Beweise und Textqualität getrennt

Stand: 18.09.2026

## Zweck

Die Teststrecke trennt ab jetzt drei Aussagen, die bisher zu leicht vermischt werden konnten:

1. **Textqualität**: Ein Text kann inhaltlich gut und nützlich sein, obwohl Struktur-/Formatregeln noch fehlschlagen.
2. **Repair-Routing**: Das System erkennt einen Befund, hält denselben Artikel fest, wählt den richtigen Repair-Owner und prüft erneut.
3. **Reale Codex-Reparatur**: Codex selbst erzeugt aus dem realen fehlerhaften Artikel eine neue Revision, die echte LT-/PPM-Prüfer besteht.

Keine dieser Aussagen darf die andere ersetzen.

## Positiver Qualitätsanker

Der vom Nutzer am 18.09.2026 bereitgestellte Codex-Artikel zu Putzplatzmatten wird hashgebunden als **inhaltlich positiver Referenztext** aufgenommen.

Verbindliche Bedeutung:
- Nutzer bestätigt die inhaltliche Textqualität.
- Strukturkonformität wird ausdrücklich **nicht** behauptet.
- Fullcheck-PASS wird ausdrücklich **nicht** behauptet.
- Der Text darf weder als vorbereitete Repair-Datei noch als PASS-Fixture noch als Produktionsartikel verwendet werden.

Referenzen:
- `isolated_system4/testdata/article_quality_reference_putzplatzmatten_20260918.txt`
- `isolated_system4/testdata/article_quality_reference_putzplatzmatten_20260918.json`

## Harte Repair-Beweisstufen

### REPAIR_ROUTING_PROVEN

Darf durch Unit-Tests, Mocks, deterministische Testworker oder vorbereitete End-Fixtures belegt werden. Aussage nur:
- Befund wird geroutet;
- derselbe Artikel bleibt gebunden;
- Recheck findet statt.

Diese Stufe darf **niemals** als reale Codex-Reparatur bezeichnet werden.

### REAL_CODEX_REPAIR_PROVEN

Nur zulässig, wenn gleichzeitig dauerhaft nachgewiesen sind:
- Worker = `CODEX_CLOUD`;
- `codex_used=true`;
- keine Mocks;
- keine vorbereitete `final`-Fixture;
- SHA-256 und dauerhafte Referenz des Artikels **vor** Repair;
- SHA-256 und dauerhafte Referenz des Artikels **nach** Repair;
- SHA-256 und dauerhafte Referenz der zugehörigen Findings;
- Revision vor/nach Repair;
- Same-Article-Routing;
- echter Recheck;
- finaler Fullcheck PASS;
- LanguageTool PASS;
- PPM PASS;
- PPM `CONTENT_QUALITY_CHECK_OK`.

Fehlt nur einer dieser Punkte, bleibt der Beweis höchstens `REPAIR_ROUTING_PROVEN`.

## Geänderte Testaussagen

- `full_local_acceptance.py` kennzeichnet seinen vorbereiteten Repair jetzt ausdrücklich nur als `REPAIR_ROUTING_PROVEN`.
- `real_known_regression_acceptance_v3.py` kennzeichnet die vorbereitete `final`-Fixture ausdrücklich nur als `REPAIR_ROUTING_PROVEN`.
- `live_parity_v2.py` kennzeichnet den deterministischen Testworker ausdrücklich mit `real_codex_repair_proven=false`.
- `test_repair_continuity.py` enthält Negativtests, die Mock, vorbereitete Enddatei und deterministischen Testworker als realen Codex-Beweis hart ablehnen.
- Derselbe Test bindet den Nutzer-Qualitätsanker und stellt sicher, dass dessen Inhaltsfreigabe keine Struktur-/Fullcheck-Freigabe erzeugt.

## Unverändert

Nicht geändert werden:
- PPM 6.7.9;
- LanguageTool 6.8;
- Qualitätsgrenzen;
- Textregeln;
- Designregeln;
- Produktionsarchitektur;
- Publish-Status.

## Nächste Freigabegrenze

Nach PASS dieser Teststrecke bleibt der Produktionslauf weiterhin gesperrt.

Der nächste reale Schritt ist erst nach neuer ausdrücklicher Nutzerfreigabe:
**genau ein realer Codex-Artikel als Repair-Abnahme mit dauerhaft gesicherten Vorher-/Nachher-/Findings-Artefakten.**
