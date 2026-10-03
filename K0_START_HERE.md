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

1. die **fertige verifizierte WordPress-Datei als echte Datei/Download im Chat**, oder
2. ein **echter terminaler Blocker**, der intern nicht lösbar ist.

**Nicht zulässig als Endausgabe:** GitHub-Link, Raw-Link, Actions-Link, Artifact-Link oder bloßer Repository-Pfad. Kann die exakte verifizierte Datei nicht in den Chat materialisiert/angehängt werden, lautet der terminale Blocker `K0_CHAT_FILE_DELIVERY_REQUIRED`.


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

Frühere Runs dürfen ausschließlich von technischen Guards für Hash-/Gate-/Negativtest-Evidence betrachtet werden. **Recherche, Writer und Repair dürfen alte Artikeltexte oder alte Produktionsinhalte weder lesen noch als Quelle erhalten.**

## Inhaltsisolation — HARDLOCK

Für jeden neuen Artikel gilt: **inhaltlich neu von Null.**

Maßgebliche Auftrags-/Artikelidentität:
- ausschließlich der aktuelle hochgeladene K0-Handoff.

Zusätzlich zulässige Inputs:
- frische externe Recherche dieses neuen Runs;
- aktuelle K0-Regeln;
- aktuelle WordPress-Kategorieauflösung;
- aktuelle interne Link-Bindungen.

Als Inhalts-, Fakten-, Struktur- oder Formulierungsquelle strikt verboten:
- frühere Artikel;
- frühere Writer-Drafts;
- frühere Repair-Texte;
- frühere Fact-Packs und Research-Pakete;
- frühere `AUTHORING_CONTEXT.json`, `SEALED_WRITER_PRODUCT.json`, `WORDPRESS_SINGLE.json` oder `WORDPRESS_BATCH.json`;
- Inhalte aus `real_runs/**`, `recovery/**`, `archive/**` oder `writer_drafts/**`;
- bestehende Artikel auf `pferde-atelier.de` als Recherchequelle;
- Repository-/GitHub-Dateien mit alten Artikelinhalten als Recherchequelle.

Vor Export muss der K0-Historical-Content-Guard PASS sein. Er blockiert erkannte Textübernahme aus historischen Artikelbeständen.

## Chat-Dateiausgabe — HARDLOCK

Nach erfolgreicher Verifikation:
1. die **exakten Bytes** der frisch verifizierten WordPress-Datei dieses Runs laden;
2. den Hash gegen den verifizierten Output dieses Runs prüfen;
3. diese exakte Datei in den Chat-Arbeitsbereich materialisieren/ablegen;
4. dem Nutzer **diese Chat-Datei als Download** ausgeben.

Ein Repository-/GitHub-/Raw-/Actions-/Artifact-Link darf weder die Datei ersetzen noch als alleinige Endausgabe erscheinen.

Wenn Schritt 1–3 technisch nicht möglich ist: **keinen GitHub-Link ausgeben**, sondern fail-closed mit `K0_CHAT_FILE_DELIVERY_REQUIRED`.

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

Interne Links: exakt 3; `parent_category` und `semantic_related` liegen in zwei verschiedenen Haupttextblöcken, `further_information` ausschließlich im Block `further_information`. Intro, Fazit und Tabelle zählen nicht als Haupttext.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
