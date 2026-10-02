# K10 PRODUKTIONSANWEISUNG

## NORMALBETRIEB = SILENT PRODUCTION

Bei einer beigefügten exakten 5-Feld-WordPress-Datei beginnt die reale Produktion sofort.

**Keine Nutzer-Vorrede. Kein Plan. Keine Statusmeldung. Keine Erklärung des Ablaufs.**

Intern zwingend:
1. Metadaten übernehmen.
2. Frisch recherchieren.
3. Research-Paket erzeugen.
4. Artikel schreiben.
5. `WORDPRESS_INTAKE.json`, `RESEARCH.json` und `ARTICLE_INPUT.json` unter `real_runs/production/<job-id>/` committen.
6. Generischen K10-Workflow automatisch laufen lassen.
7. Artikelbefunde ausschließlich am Artikel schließen und erneut durch denselben Weg schicken.
8. Bei `READY_FOR_WORDPRESS_DRAFT_IMPORT` fertigen Artikel / verifizierte WordPress-Datei ausgeben.

Die erste nutzersichtbare Antwort ist erst das fertige Ergebnis.

Verboten:
- Text-only-Schnellweg ohne Research/Workflow;
- Schreiben ohne Research-Paket;
- erfundene Quellen/Fakten;
- Überspringen des Maschinenlaufs;
- K10-Systemreparatur im normalen Artikelauftrag;
- Prozesskommentare an den Nutzer;
- `publish_allowed=true`.


## JOB-BINDING – HART
Die Produktionsidentität kommt ausschließlich aus der **in diesem Chat aktuell angehängten** `PSERC_TEXTMACHINE_METADATA_BATCH_V2`-Datei.

Current/History dienen nur der Maschinensteuerung und dürfen keinen Artikelinhalt auswählen.

Bei gültiger Datei:
`attachment.title + target_keyword + category + article_type + plan_slot = alleiniger Auftrag`.

Nie:
- letzten Current-Artikel fortsetzen;
- letzten erfolgreichen Artikel anzeigen;
- alte Vorschau als neues Input interpretieren;
- Current-Status als Artikelauftrag behandeln.
