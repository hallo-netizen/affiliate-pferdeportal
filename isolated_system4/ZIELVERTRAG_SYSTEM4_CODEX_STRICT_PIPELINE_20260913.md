# ZIELVERTRAG — SYSTEM 4 / CODEX STRICT PIPELINE

Status: **VERBINDLICHER ZIELVERTRAG DES ISOLIERTEN SYSTEM-4-PROTOTYPS**

Dieser Zielvertrag beschreibt ausschließlich das Ziel von System 4 unter `isolated_system4/**`. Er ändert weder den offiziellen STARTMASTER0107 noch die bestehende Textmaschine, PPM 6.7.9, WordPress, Theme/CSS oder andere produktive Fachkomponenten.

## 1. Ziel
Das nachweislich funktionierende fachliche Arbeitsprinzip der früheren Chat-Texterstellung wird auf Codex übertragen, ohne die alte fehleranfällige Orchestrierung mitzunehmen.

Die fachliche Kette lautet unverändert:

`Thema/Metadaten -> Codex recherchiert -> Codex bildet Fakten/Fact-Pack -> Codex schreibt -> unveränderte echte Prüfer -> gezielte Reparatur desselben Artikels -> Batchprüfung -> exakter Chat-/WordPress-Handoff`

Codex bleibt der **eine fachliche Arbeiter**. Es gibt keinen zweiten Chat-Schreiber, keinen externen Faktenlieferanten und keinen Legacy-Worker.

## 2. Unverhandelbare Grenze: Textmaschine
Die bestehende Textmaschine und ihre fachlichen Regeln sind **READ-ONLY**.

System 4 darf keine bestehende Textregel:
- ändern;
- abschwächen;
- ergänzen;
- neu interpretieren;
- normalisieren;
- ersetzen;
- durch eine eigene Schreibregel überschatten.

System 4 darf nur Eingaben und Ergebnisse gegen die bereits bestehende fachliche Wahrheit prüfen und danach PASS oder BLOCK liefern.

Wenn ein gewünschter System-4-Fix eine Änderung an der Textmaschine voraussetzen würde, ist das Ergebnis `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE`.

## 3. Unverhandelbare Grenze: Design
Das bestehende Artikel-/WordPress-Design ist **READ-ONLY**.

System 4 darf weder direkt noch indirekt:
- CSS oder Theme-Dateien verändern;
- Inline-Styles erzeugen;
- Designklassen erfinden oder ersetzen;
- Überschriftenebenen umstellen;
- Tabellenklassen oder Tabellenformatierung verändern;
- Plugin-/Theme-Dateien verändern;
- nach dem fachlich geprüften Artikel eine HTML-Normalisierung, Dekoration oder Umgestaltung vornehmen.

Der bestehende Produktions-/Designvertrag wird nur fail-closed geprüft. Der aktuell gebundene Beratungspfad erwartet insbesondere die bereits etablierte Produktionshülle und Selektoren (`ppm-generated`, `ppm-type-beratung`, passendes `data-article-type`, `system-129-table comparison-table`, Beratung-Zwischenüberschriften auf H2-Ebene). System 4 darf diese Elemente nicht nachträglich erzeugen oder reparieren, sondern muss einen abweichenden Artikel blockieren.

## 4. Recherche- und Faktenbindung
Codex recherchiert selbst. Der Controller darf den nächsten Schritt aber erst freigeben, wenn die Recherche strukturell belegt ist.

Pflichtkette:
1. `SYSTEM4_RESEARCH_EVIDENCE_V1` mit realer URL, Titel, Retrieval-Zeit, gespeicherter Evidence und SHA-256 dieser Evidence.
2. `SYSTEM4_FACTS_EVIDENCE_V1` mit konkreten Claims, die auf akzeptierte `source_id` zeigen; `evidence_text` muss tatsächlich im gespeicherten Quellenausschnitt vorkommen und der Hash muss stimmen.
3. `canonical_fact_pack_v1` muss dieselben akzeptierten Quellen und Kernclaims enthalten.
4. Erst danach darf der Produktionskontext gebunden und der Artikel für FULL-Produktion angenommen werden.

Ein selbstzertifizierter, quellenloser oder synthetisch belegter Fact-Pack darf nicht bis zum Artikel gelangen.

## 5. Schreiben und Reparatur
Codex schreibt den Artikel selbst unter den unveränderten bestehenden Textregeln.

Eine Reparatur darf nur denselben gebundenen Artikel für den konkret gemeldeten Fehler korrigieren. Ein großflächiger Austausch des Artikels im Reparaturpfad ist verboten und wird über Kontinuitätsprüfung fail-closed blockiert.

## 6. Prüfer
`controller.py fullcheck` ist der einzige System-4-Orchestrator für die produktionsnahen Prüfer.

Pflicht bleiben unverändert:
- reale PPM 6.7.9-Prüfung;
- reales LanguageTool 6.8 / Bestand 43;
- bestehende SEO/PSERC/PSTE-/Artikeltyp-/Tabellen-/Link-/Metadaten-/Publish-Regeln;
- NO-LEGACY;
- `publish_allowed=false`.

Kein System-4-Guard darf einen bestehenden Prüfer ersetzen oder dessen PASS simulieren.

## 7. Artikelübergreifende Kontrolle
Die Einzelartikelprüfung allein reicht nicht aus, weil der historische schlechte 7er-Lauf artikelübergreifende Schablonenwiederholung gezeigt hat.

Deshalb wird nach den Einzelprüfungen zusätzlich geprüft:
- starke Textähnlichkeit zwischen Artikeln;
- wiederholte lange Sätze/Schablonen über mehrere Artikel.

Diese Prüfung ist ausschließlich ein Release-/Batch-Integritätsguard. Sie schreibt keine Texte um und fügt der Textmaschine keine Autorenregel hinzu.

## 8. Handoff
Nach 7/7 FULL PASS darf der Artikeltext nicht mehr verändert werden.

Zielkette:
`7/7 FULL PASS -> batch_gate -> exaktes kanonisches SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json -> inline-pack -> Elternchat -> inline-unpack -> SHA/Schema/Bytegleichheit -> genau diese JSON-Datei zum direkten WordPress-Import`

Kein Repository-Handoff, keine Zwischenkopie durch den Nutzer, keine nachträgliche HTML-/Designtransformation.

Aktuell gebundener direkter Importer: `Portal SEO Editorial Plan Compiler 0.28.23`.

Die Signaturprüfung ist für diesen aktuellen Pfad ausgeschaltet; daher kein ENDSTEMPEL/Signing-Schritt. `publish_allowed=false` bleibt zwingend.

## 9. Altlastenverbot
System 4 darf alte Systeme nur als Fehler-/Regressionsevidenz lesen. Verboten ist das Übernehmen von:
- Legacy-Orchestrierung;
- alten Runnern/Gates;
- alten State Machines;
- alten Handoffs;
- alten Artikeln/Fact-Packs/Research als Produktionsinhalt;
- alten Fehlerverbindungen als neue Laufzeitabhängigkeit.

## 10. Freigabekriterium
System 4 ist erst für einen neuen Codex-Produktionsversuch freigegeben, wenn auf **dem exakt aktuellen PR-Head** ohne Codex nachweislich PASS vorliegt für:
- kompletten `isolated_system4`-Unittestbestand;
- NO-LEGACY;
- lokalen positiven End-to-End-Weg vom Codex-Einstieg bis zur rekonstruierten Chat-/WordPress-JSON;
- relevante Negativfälle: falsche/erfundene Fakten, Design-Drift, Text-/Template-Wiederholung, breiter Repair, Metadaten-/Hash-/Publish-Manipulation, Handoff-Manipulation;
- unveränderte hashgebundene PPM-/LanguageTool-Autorität.

Erst danach und nur nach ausdrücklicher Nutzerfreigabe darf ein neuer echter Codex-7/7-Lauf gestartet werden.
