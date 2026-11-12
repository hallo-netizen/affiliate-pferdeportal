# 08.11.2026, 16:29:19 UTC: ECHTER WordPress-PSTE-v24-Export – 55 lokale Tests, 9 exakte Datenruinen und 3 verwaiste Referenzen

**Stand:** TEST-only; die vom Betreiber installierte PSTE 0.57.144.24 hat tatsächlich alle sechs vorhandenen Quellen in einer JSON ausgegeben. **Die Quellqualität ist wegen beschädigter Altbestände weiterhin nicht für eine externe SEO-FREI-Entscheidung nachgewiesen.** Keine neue Pluginversion, kein erneuter WP-Gesamtlauf, kein WordPress-Schreibzugriff, kein K0-/Live-Änderung.

## Echte Eingangsdatei, privat gesichert

- Original-Datei vom Nutzer `pferdeatelier-mini-ergebnisse-20261108-162920.json`, 1.094.709 Bytes, SHA256 `ddeadf12b0a84e215e534172ee70f6d3f11c5f1289fc9e6e6d00deed7a278125`. Private Library `/pferdeatelier/pferdeatelier-mini-ergebnisse-20261108-162920(1).json` (ID `libfile_be945aff6430819180f6b844c0a2441f`). Nicht in GitHub als Rohdatei kopiert.
- `contract=PSTE_MINI_RESULTS_FOR_EDITORIAL_V1`, 100 MINI-Stichwörter: 87 JA, 9 VIELLEICHT, 4 NEIN; 87 SEO-Subjekte. Snapshot 1.179 **vollständige technische Datenzeilen**: WORDPRESS 1.024, PSTE_PLAN 1, EDITORIAL_PLAN 9, PSERC_ACTIVE_PLAN 1, PPM679_EXISTING_EDITORIAL_RUNTIME 144, MINI_RESERVED 0.
- PSERC-Quelle `complete=true`, 144 PPM679-Belegungen mit eindeutigem `canonical_article_id` und eindeutigem `plan_slot`. 141 PPM-Titel aus vorhandenem WP-Artikel übernommen. Kein technisch abgebrochener Export mehr.
- Snapshot `complete=false`, `parkhaus_complete=false`, leerer **Freigabe-Hash** und Grund **`EDITORIAL_PLAN_UNRESOLVED:9;PPM679_RUNTIME_TITLE_UNRESOLVED:3`**. Der vorhandene `diagnostic_sha256` ist nur eine Diagnosekennung, ausdrücklich keine Besitzerfreigabe. **Keinen externen FREI-Rückimport erzeugen oder importieren.**

## Wichtiger neuer Wurzelbefund: neun vollständig identische Alt-Platzhalter

Alle 9 von WordPress ausgelesenen `EDITORIAL_PLAN`-Einträge haben **exakt denselben** `raw_record_sha256=6a7d9b77e6d0cf54455eb98d76c6b11b3c1258ae369724b995744f41df3dffe9`. Der tatsächliche gespeicherte Sechs-Felder-Inhalt wurde **verlustfrei durch vollständige SHA256-Rekonstruktion** aus den im echten Export enthaltenen Feldnamen/-Titeln bestätigt:

```json
{"title":"Array","primary_longtail_query":"Array","category_name":"","intent_cluster_id":"","headings":[],"source_reference":""}
```

Es gibt darin **weder echte Themenbezeichnung noch Kategorie, Überschrift, belegten Planplatz, Referenz oder Artikelidentität**. Alle neun sind **bytegleich inhaltlich identische Platzhalter**, NICHT neun unterschiedlich identifizierbare Artikel. Der Export hat keine verborgenen Titel ausgelassen, die man aus diesen gespeicherten sechs Feldern sinnvoll rekonstruieren könnte. **Wichtig:** Der Quellcode liest zuerst einen externen WP-Filter und sonst die gespeicherte PSTE-Option; aus der exportierten Datei allein ist daher noch NICHT beweisbar, welche dieser beiden Quellen die neun Zeilen geliefert hat. Deshalb **weder pauschal die WP-Option löschen noch behaupten, ein Filter sei sicher verantwortlich**.

## Drei verwaiste PPM679-Artikelverweise, weiterhin belegt lassen

Die Post-IDs 972356, 972414 und 972560 stehen noch in der gespeicherten PPM679-Planbelegung mit **je eigener, gültiger Artikelkennung und eigenem Plan-Slot** und historischem `status=DRAFT_CREATED_READBACK_PASS`. Weder der WordPress-Inventar-Export noch der v24-`get_post`-Rückgriff fanden den aktuellen Beitrag oder seinen Titel. Die drei Zuordnungen dürfen **nicht** stillschweigend als FREI gelten. Drei andere WP-Beiträge mit unabhängigen Artikelkennungen sind kein Ersatz. Alle 144 PPM679-Kennungen und Slots bleiben einzigartig/belegt.

## ECHTE lokale Nachprüfung mit den frisch gelieferten v24-Daten

- Bestehende QA für die tatsächliche neue Datei angepasst, **nicht** bloß den alten .22-Export wiederholt: 55 einzelne lokale PHP-Checks **PASS**. 9 von 9 echte Alt-Quellzeilen bis auf alle sechs Originalfelder und ihren Hash vollständig nachgerechnet; aus echten 1.179 Einträgen WordPress + PSTE + PSERC + PPM wieder mit den originalen Methoden nachgebaut; echte 141 Posttitel und 3 Negativverweise bestätigt. Beim defekten Quellbestand keine Schreibaktion und Import korrekt **abgelehnt**; positiver Vollständigkeitstest kennzeichnet ausschließlich 9+3 künstliche Ersatzwerte als **synthetisch**, keine WordPress-Freigabe. PSERC 0.28.55-Leseweg positiv/negativ geprüft, K0 nicht benutzt.
- Quellskript/Log/Audit als Text in `PLUGINS/QA_ONLY/PSTE_05714424_QUELLFIX/LIVE_WP_20261108_162920/` eingecheckt; außerdem privat `/pferdeatelier/PLUGINS/QA/`. Das vollständige v24-Original-ZIP bleibt bereits unverändert privat gespeichert; **kein neues Plugin gebaut**, weil der aktuelle Fehler nachweislich **Alt-Datenqualität**, nicht Exportvollständigkeit, betrifft.
- Automatisierte Textähnlichkeits-Suche dient höchstens zur **Kandidatenfindung**, NICHT zur Freigabe, nicht als zweiter SEO-Owner. Der externe einmalige fachliche Vergleich steht aus.

## Nächster technischer Quellenabgleich vor jeder Löschung

1. Herausfinden, ob die identischen `EDITORIAL_PLAN`-Platzhalter aus einer alten gespeicherten Importoption oder aus dem externen WP-Filter kommen. Die neun Identitätslosen sind nachweislich kein nutzbarer *Artikelplan*, sollen aber ohne Herkunftsklärung nicht verändert werden.
2. Die drei **alten** PPM679-Referenzen gegen ursprüngliche gespeicherte Produktionsprotokolle/Backups und aktuelle Post-ID-Migration abgleichen. Alle drei Planplätze so lange belegt lassen.
3. **Nur nach belegtem Quellenabgleich** veraltete Phantomdaten reversibel von der aktiven SEO-Inhaltsquelle trennen. Kein einfaches `complete=true` über ungeklärten Einträgen, keine blind neu erfundenen Titel, kein stiller Aufbau einer zweiten Datenquelle.
4. EIN externer SEO-Owner für 87 JA-Subjekte mit allen wirklich gültigen Titeln/Belegungen, dann bestehender atomarer Import und technischer PSERC-Handoff. K0 bleibt unverändert.

**GitHub-Autorität:** Branch `fix/pste-kisten-einmalige-pruefung-20261107`, Draft-PR #682, kein Merge/Release.
