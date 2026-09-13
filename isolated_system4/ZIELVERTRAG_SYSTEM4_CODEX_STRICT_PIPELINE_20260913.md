# ZIELVERTRAG — SYSTEM 4 / CODEX STRICT PIPELINE

Status: **VERBINDLICHER ZIELVERTRAG DES ISOLIERTEN SYSTEM-4-PROTOTYPS**

Dieser Zielvertrag beschreibt ausschließlich das Ziel von System 4 unter `isolated_system4/**`. Er ändert weder den offiziellen STARTMASTER0107 noch die bestehende Textmaschine, PPM 6.7.9, WordPress, Theme/CSS oder andere produktive Fachkomponenten.

## 1. Ziel
Das nachweislich funktionierende fachliche Arbeitsprinzip der früheren Chat-Texterstellung wird auf Codex übertragen, ohne die alte fehleranfällige Orchestrierung mitzunehmen.

Die fachliche Kette lautet:

`gebundene Metadaten -> Codex recherchiert -> Codex bildet Fakten/Fact-Pack -> gebundener Production-Context -> aus denselben unveränderten Autoritäten abgeleiteter Authoring Contract -> Codex schreibt -> unveränderte echte Prüfer -> gezielte Reparatur desselben Artikels -> Batchprüfung -> exakter Chat-/WordPress-Handoff`

Codex bleibt der **eine fachliche Arbeiter**. Es gibt keinen zweiten Chat-Schreiber, keinen externen Faktenlieferanten und keinen Legacy-Worker.

## 2. Universelle Mengen- und Beitragsartbindung
System 4 hat **keine feste Artikelzahl**. Ein gebundener Produktionslauf verarbeitet exakt die nichtleere Menge aus dem Eingabe-Snapshot: `1..N` ohne künstliche System-4-Obergrenze. Zahlen wie 1, 7, 25 oder 1000 sind ausschließlich Regressionstests und niemals Produktionsvertrag.

System 4 hat **keine feste Beitragsart**. `article_type` kommt ausschließlich aus den gebundenen Metadaten. `Beratung` ist ein vorhandener Typ mit bekannten typspezifischen Regeln, aber keine System-4-Zulassungsliste. Neue Beitragsarten müssen ohne Änderung an Controller, Batch-Gate oder Handoff durch denselben generischen Weg laufen können. Ob ein konkreter Typ fachlich gültig ist, entscheiden die unveränderten autoritativen Textmaschine-/PPM-/Designregeln, nicht eine System-4-Whitelist.

## 3. Unverhandelbare Grenze: Textmaschine
Die bestehende Textmaschine und ihre fachlichen Regeln sind **READ-ONLY**.

System 4 darf keine bestehende Textregel ändern, abschwächen, ergänzen, neu interpretieren, normalisieren, ersetzen oder durch eine eigene Schreibregel überschatten. System 4 darf nur Eingaben und Ergebnisse gegen die bereits bestehende fachliche Wahrheit prüfen und danach PASS oder BLOCK liefern.

Wenn ein gewünschter System-4-Fix eine Änderung an der Textmaschine voraussetzen würde, ist das Ergebnis `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE`.

## 4. Unverhandelbare Grenze: Design
Das bestehende Artikel-/WordPress-Design ist **READ-ONLY**.

System 4 darf weder direkt noch indirekt CSS oder Theme-Dateien verändern, Inline-Styles erzeugen, Designklassen erfinden/ersetzen, Überschriftenebenen umstellen, Tabellenklassen/-formatierung verändern, Plugin-/Theme-Dateien verändern oder nach dem fachlich geprüften Artikel HTML normalisieren/dekorieren/umgestalten.

Der Design-Guard bindet den übergebenen `article_type` generisch an die bestehende `ppm-type-*`-Konvention. Bereits autoritativ bekannte typspezifische Regeln dürfen für ihren Typ geprüft werden; sie dürfen nicht als Grund benutzt werden, unbekannte/neue Beitragsarten pauschal abzulehnen.

## 5. Recherche- und Faktenbindung
Codex recherchiert selbst. Der Controller darf den nächsten Schritt aber erst freigeben, wenn die Recherche strukturell belegt ist.

Pflichtkette:
1. `SYSTEM4_RESEARCH_EVIDENCE_V1` mit realer URL, Titel, Retrieval-Zeit, gespeicherter Evidence und SHA-256 dieser Evidence.
2. `SYSTEM4_FACTS_EVIDENCE_V1` mit konkreten Claims, die auf akzeptierte `source_id` zeigen; `evidence_text` muss tatsächlich im gespeicherten Quellenausschnitt vorkommen und der Hash muss stimmen.
3. `canonical_fact_pack_v1` muss dieselben akzeptierten Quellen und Kernclaims enthalten.
4. Erst danach darf der Produktionskontext gebunden werden.
5. Erst nach gebundenem Produktionskontext und gültigem Authoring Contract darf der Artikel für FULL-Produktion angenommen werden.

Ein selbstzertifizierter, quellenloser oder synthetisch belegter Fact-Pack darf nicht bis zum Artikel gelangen.

## 6. Schreiben und Reparatur
Codex schreibt jeden Artikel selbst unter den unveränderten bestehenden Regeln des jeweils gebundenen `article_type`.

Eine Reparatur darf nur denselben gebundenen Artikel für den konkret gemeldeten Fehler korrigieren. Ein großflächiger Austausch des Artikels im Reparaturpfad ist verboten und wird über Kontinuitätsprüfung fail-closed blockiert.

### 6A. Vorab-Autoritätsbindung — Ursache statt Symptom
Nach `facts` darf **nicht** unmittelbar geschrieben werden.

Pflichtweg:

`FACTS -> CONTEXT_REQUIRED -> gebundener Production-Context -> maschinell abgeleiteter hashgebundener Authoring Contract -> DRAFT_REQUIRED`

Der Authoring Contract darf ausschließlich aus den bereits bestehenden, unveränderten autoritativen Quellen abgeleitet werden. Chat, Codex, Nutzertext oder andere externe Inputs dürfen **keine neue Fach-/Schreibregel** einspeisen, lockern oder überschreiben.

Alle Pflichten, die aus den gebundenen unveränderten Autoritäten bereits **vor** dem Schreiben bekannt und maschinell prüfbar sind, müssen vor Draft-Annahme gebunden und geprüft werden. Dazu gehören je nach gebundenem Typ/Context insbesondere Struktur-, Wortmengen-, Tabellen-, Link-, Metadaten-, Typ- und Designpflichten, soweit sie bereits aus den bestehenden Autoritäten hervorgehen.

Dynamische Befunde, die sinnvoll erst am fertigen Text ermittelt werden können, bleiben Aufgabe des normalen FULL-Checks und Same-Article-Repair-Wegs.

Ein späterer Prüfer darf nicht erstmals als normaler Repair-Fall eine Pflicht melden, die bereits vor Draft bindbar war. Geschieht das, gilt dies als Fehler der Vorab-Autoritätsbindung und muss fail-closed sichtbar werden.

Eine Sonderausnahme wie „bei Wortmengenfehlern darf der Repair-Guard pauschal größere Änderungen zulassen“ ist **nicht** die Zielarchitektur. Die Ursache muss vor dem Schreiben geschlossen werden; die allgemeine Same-Article-Kontinuität bleibt bestehen.

## 7. Prüfer
`controller.py fullcheck` ist der einzige System-4-Orchestrator für die produktionsnahen Prüfer.

Pflicht bleiben unverändert:
- reale PPM 6.7.9-Prüfung;
- reales LanguageTool 6.8 / Bestand 43;
- bestehende SEO/PSERC/PSTE-/Artikeltyp-/Tabellen-/Link-/Metadaten-/Publish-Regeln;
- NO-LEGACY;
- `publish_allowed=false`.

Kein System-4-Guard darf einen bestehenden Prüfer ersetzen oder dessen PASS simulieren. Ein Vorab-Gate darf nur dieselben bereits vorhandenen Autoritäten lesen/binden; es ist keine neue Textmaschine.

## 8. Artikelübergreifende Kontrolle
Bei Batches mit mehr als einem Artikel werden zusätzlich starke Textähnlichkeit und wiederholte lange Satz-/Absatzschablonen geprüft. Bei genau einem Artikel ist der Batch gültig; nur logisch unmögliche Paarvergleiche entfallen.

Diese Prüfung ist ausschließlich ein Release-/Batch-Integritätsguard. Sie schreibt keine Texte um und fügt der Textmaschine keine Autorenregel hinzu.

## 9. Handoff
Nach FULL PASS aller gebundenen Input-Artikel darf kein Artikeltext mehr verändert werden.

Zielkette:
`1..N FULL PASS -> batch_gate -> SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json -> V2 inline-pack (1..M Transportteile) -> Elternchat -> inline-unpack -> SHA/Schema/Bytegleichheit -> genau diese JSON-Datei zum direkten WordPress-Import`

Der Handoff enthält exakt alle Artikel des gebundenen Input-Snapshots in dessen Reihenfolge. Er kennt weder eine feste Artikelzahl noch eine Beitragsart-Whitelist. Die Aufteilung in Transportteile dient nur der sicheren Übertragung großer Dateien und verändert weder Artikelzahl noch Artikelbytes.

Kein Repository-Handoff, keine Zwischenkopie durch den Nutzer, keine nachträgliche HTML-/Designtransformation.

Aktuell gebundener direkter Importer: `Portal SEO Editorial Plan Compiler 0.28.23`. Die Signaturprüfung ist für diesen aktuellen Pfad ausgeschaltet; daher kein ENDSTEMPEL/Signing-Schritt. `publish_allowed=false` bleibt zwingend.

## 10. Altlastenverbot
System 4 darf alte Systeme nur als Fehler-/Regressionsevidenz lesen. Verboten ist das Übernehmen von Legacy-Orchestrierung, alten Runnern/Gates, alten State Machines, alten Handoffs, alten Artikeln/Fact-Packs/Research als Produktionsinhalt oder alten Fehlerverbindungen als neue Laufzeitabhängigkeit.

## 11. Freigabekriterium und Testpflicht
System 4 ist erst für einen neuen Codex-Produktionsversuch freigegeben, wenn auf **dem exakt aktuellen PR-Head** ohne Codex nachweislich PASS vorliegt für:
- kompletten `isolated_system4`-Unittestbestand;
- NO-LEGACY;
- lokalen positiven End-to-End-Weg vom Root-/Codex-Einstieg bis zur rekonstruierten Chat-/WordPress-JSON;
- **jeden bekannten Workflow-Schritt mindestens einmal positiv und einmal negativ gegen den vollständigen Gesamtworkflow**, nicht nur als isolierten Einzeltest;
- Mengenregression mindestens für 1, mehrere, 25 und einen großen Batch (aktuell 1000) ohne Produktions-Hardlimit;
- mindestens einen gemischten Beitragsart-Batch sowie einen neuen/unbekannten Typ ohne System-4-Whitelist;
- relevante Negativfälle: 0 Artikel, falsche/erfundene Fakten, Design-Drift, Text-/Template-Wiederholung, breiter Repair, Metadaten-/Hash-/Publish-Manipulation, Handoff-/Part-Manipulation, externe Regel-Injektion und Authoring-Contract-Manipulation;
- unveränderte hashgebundene PPM-/LanguageTool-Autorität.

Ein isolierter Einzeltest darf niemals als „komplett positiv/negativ gegen den Gesamtworkflow“ bezeichnet werden.

Erst danach und nur nach ausdrücklicher Nutzerfreigabe darf ein echter Codex-Lauf für den **konkret gebundenen Input-Batch** gestartet werden. Dessen Anzahl und Beitragsarten kommen ausschließlich aus diesem Input.

## 12. Codex-Nutzung
Codex ist ausschließlich für einen **konkreten real gebundenen Artikel-/Batch-Produktionslauf** vorgesehen und nur nach ausdrücklicher Nutzerfreigabe.

Codex darf nicht für Diagnose, Architektur-/Codearbeit, Patch/Commit/Push, Preflight, lokale Regressionstests, Dokumentation, Handoff-Experimente oder WordPress-Arbeit verwendet werden.

Diese Arbeiten müssen ohne Codex erfolgen. Ein Codex-Produktionslauf darf nur die bereits vollständig vorgeprüfte gebundene Arbeit ausführen und nicht gleichzeitig das System umbauen oder vorbereiten.
