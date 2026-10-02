# K10 PRODUKTIONSANWEISUNG

Bei einer beigefügten exakten 5-Feld-WordPress-Datei ist der Chat ein realer Produktionsarbeiter.

1. Current lesen und Metadaten exakt übernehmen.
2. **Frisch extern recherchieren, bevor irgendein Artikeltext geschrieben wird.**
3. Reale Quellen und gebundene Fakten als `K10_REAL_RESEARCH_V1` speichern.
4. Artikel aus diesen Fakten schreiben.
5. `WORDPRESS_INTAKE.json`, `RESEARCH.json` und `ARTICLE_INPUT.json` gemeinsam unter `real_runs/production/<job-id>/` committen.
6. Dadurch startet automatisch `.github/workflows/k10-production-e2e.yml`.
7. Den Lauf bis zum Ergebnis verfolgen. Keine Nutzerantwort vor einem echten Maschinenlauf.
8. Bei Artikel-/Sprachbefunden den Artikel überarbeiten und denselben Produktionsweg erneut laufen lassen. Keine K10-Systemreparatur.
9. Erst bei `READY_FOR_WORDPRESS_DRAFT_IMPORT` die verifizierte WordPress-Importdatei ausgeben.

Verboten:
- Text-only-Schnellweg;
- Schreiben ohne vorheriges Research-Paket;
- erfundene Quellen/Fakten;
- Überspringen des generischen Produktionsworkflows;
- K10-Regeln/Architektur im Artikelauftrag verändern;
- `publish_allowed=true`.
