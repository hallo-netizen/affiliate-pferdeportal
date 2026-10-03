# K0 START

## Befehl

`K0:start`

## Sichtbares Chatverhalten — HARDLOCK

Bei gültigem angehängtem K0-Handoff + `K0:start`:

**NICHT ANTWORTEN. SOFORT INTERN PRODUZIEREN.**

Verboten:
- Vorrede;
- Statusmeldung;
- Prüfankündigung;
- Prozessbeschreibung;
- Routing-Erklärung;
- Verweis auf andere Wege oder Konzepte;
- Bitte um `weiter`;
- Zwischenmeldung irgendeiner Art.

Die erste sichtbare Antwort ist ausschließlich:

1. die **fertige verifizierte WordPress-Datei**, oder
2. ein **echter terminaler Blocker**, der intern nicht lösbar ist.


## Frische Ausführung — HARDLOCK

Jeder neue Nutzerauftrag mit angehängtem K0-Handoff + `K0:start` erzeugt **immer einen neuen K0-Produktionslauf**.

Verboten:
- vorhandene `WORDPRESS_SINGLE.json`, `WORDPRESS_BATCH.json` oder andere frühere K0-Ausgaben als Ergebnis des neuen Auftrags wiederzuverwenden;
- einen bestehenden Batch-Hash als Beweis für eine neue Ausführung zu behandeln;
- einen früheren PASS, Writer-Run, LT-PASS, PPM-PASS oder Export-PASS für den neuen Auftrag zu übernehmen;
- einen neuen Auftrag wegen identischem Upload-/Batch-Hash abzukürzen.

Pflicht vor sichtbarer Enddatei:
- neue Run-ID / neuer Run-Pfad für diesen Auftrag;
- frische Recherche/Fact-Pack-Bindung;
- frischer Writer-Lauf;
- frische vollständige Regelprüfung vor LT;
- frisches LanguageTool 6.8;
- frische finale Regelprüfung;
- frischer SYSTEM4_WORDPRESS_HANDOFF_V1;
- frische Verifikation dieses neuen Outputs.

Frühere Runs dürfen ausschließlich als Historie/Evidence gelesen werden, niemals als Produktionsersatz.

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

Interne Links: exakt 3; `parent_category` und `semantic_related` liegen in zwei verschiedenen Haupttextblöcken, `further_information` ausschließlich im Block `further_information`. Intro, Fazit und Tabelle zählen nicht als Haupttext.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
