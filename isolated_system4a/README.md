# SYSTEM 4A — CURRENT STATE

STATUS: **TEST ONLY / PRODUKTION BLOCKED / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die eine aktuelle 4A-Statuswahrheit.

## Aktueller Remote-Stand

PR #255, Branch `hobbyroom/system4a-capsule-v1-20260913`.

Der letzte reale Ein-Artikel-Codexlauf am früheren Head `78bf4ae2fb2be0afd7ddc590afc4c481f4e1c0ee` erreichte:

`ROOT_ENTRY_PASS -> PRODUCTION_INGRESS_BOUND -> RESEARCH_PASS -> FACTS_PASS -> CONTEXT_PASS -> DRAFT_PASS -> LT PASS -> BLOCK`

Erster echter Blocker:

`FULLCHECK_PRODUCTION_HARD_BLOCK:PPM679_QUALITY_BINDING_MISSING`

PPM selbst wurde noch nicht ausgeführt. Kein `ARTICLE_PASS`, kein Batch, kein V2-Handoff.

## Rootcause

Der frühere lokale Volltest war **keine gültige Produktionsabnahme**: Er übernahm bereits vorbereitete `quality_binding`-/Link-Felder aus einem Fixture. Der reale Codexweg erzeugte diese Bindung nicht. Deshalb war lokal grün möglich, obwohl der reale Weg blockierte.

Alle historischen Fixture-/Goldplan-PASS gelten ab jetzt nur noch als historische Architektur-/Diagnosebelege, **nicht als Produktionsabnahme**.

## Harte Realfall-Abnahmeregel

Eine Produktionsabnahme ist nur erlaubt, wenn exakt nachgewiesen ist:

- `REALINPUT = TESTINPUT`
- `REALER EINSTIEG = TESTEINSTIEG`
- `REALER PLANERZEUGUNGSWEG = TESTPLANERZEUGUNGSWEG`
- `REALER WORKER-AUFRUF = TEST-WORKER-AUFRUF`
- `REALE PRÜFER = TESTPRÜFER`
- `REALE ABHÄNGIGKEITEN = TESTABHÄNGIGKEITEN`
- `REALER HANDOFF = TESTHANDOFF`

Verboten als Abnahme: vorbereitete Pflichtfelder, künstlich vollständige Pläne, Mocks, Ersatzinputs, manuell ergänzte Bindungen, andere Aufrufwege oder nur äquivalente Tests.

Der Test beginnt vor der ersten automatischen Erzeugung/Bindung. Wenn ein Teil nicht 1:1 real geprüft werden kann: **BLOCKED**.

## Technische Sperren gegen die alte Testlücke

- Worker darf `quality_binding`, `quality_binding_hash`, `category_binding`, `category_binding_hash` nicht vorgeben.
- Worker darf keine fertigen `runtime_order.links` vorgeben.
- Alte vorgebundene Fixture-Kontexte werden am echten Context-Pfad hart geblockt.
- Rohinput-Kategorie wird bereits im Produktions-Ingress gegen das exakt gepinnte PPM-6.7.9-Kategorie-Contract geprüft.
- Der im letzten Codexlauf verwendete falsche Slug `pferdeanhaenger-beratung` blockiert jetzt **vor Research**.
- Ein kanonischer Beratung-Slug wie `checklisten-fuer-pferdeanhaenger-beratung` passiert den Ingress.

## Neuer Supervisor-Binder

`isolated_system4a/production_plan_binding.py` bindet den nackten Produktionsplan **nach verifiziertem Fact-Pack und vor dem Draft** supervisorseitig.

Die Bindung stammt aus:

- exakt gepinntem PPM 6.7.9;
- signiertem `complete-portal-category-source-v1.json`;
- signiertem `article-type-templates.json`;
- realem Fact-Pack;
- deterministischer Portal-Hierarchie für die drei internen Links.

Der Worker erhält erst danach den gebundenen Produktionskontext für den Draft. State/Route/PASS bleiben beim Supervisor.

## Link-Nachweis

Gegen den realen Portal-Audit-Snapshot vom 30.08.2026, SHA256
`456ee43cb2d7d3ccde8b73047d83c27a055d50961c478b310d5fe7b25e3c2ece`,
wurde die aus dem signierten PPM-Hierarchiepfad abgeleitete URL-Regel geprüft:

- 1124 PPM-Kategorien;
- 3 Linkrollen pro Kategorie;
- **3372 / 3372** berechnete URLs stimmen exakt mit den realen Portal-URLs überein;
- 0 fehlend;
- 0 mehrdeutig.

Es wird keine neue frei gepflegte Linkdatenbank eingeführt.

## Aktuelle lokale Beweise — ausdrücklich KEINE Produktionsabnahme

Nach dem aktuellen Binder-/Ingress-Stand:

- fokussierte Ingress/Binder/Context-Prüfungen: **9/9 PASS**;
- gesamter im rekonstruierten lokalen Testordner vorhandener 4A-Testbestand: **23/23 PASS**;
- alter vorgebundener Fixture-Volltest wird jetzt korrekt geblockt;
- diagnostischer Vollkettenlauf mit entfernten Fixture-Bindings erreicht real LT, Same-Article-Repair und anschließend PPM-Linkprüfung; alte Diagnose-Links werden erwartungsgemäß gegen die neue Supervisor-Bindung abgelehnt.

Diese Ergebnisse sind **keine Abnahme**, weil der exakt gleiche frische Codex-Web-Recherche-/Worker-Produktionsweg lokal noch nicht 1:1 ausgeführt ist.

## NEXT ACTION

Kein weiterer Codexlauf.

Zuerst muss ein **einziger kanonischer Realfall-Produktions-Einstieg** geschaffen werden, den lokaler Realtest und Codex unverändert gemeinsam benutzen. Erst wenn genau dieser Einstieg vom echten Rohinput über frische Research/Facts/Context/Draft, echten Cross-UID-Worker, echten LT 6.8, echten PPM 6.7.9, Same-Article-Repair, Batch, V2 und Parent-Chat vollständig 1:1 PASS ist, darf eine Produktionsabnahme oder ein weiterer Codexlauf erfolgen.

Bis dahin: **BLOCKED**.

## Codex-Regel

Kein Codex-Lauf ohne ausdrückliche vorherige Freigabe des Users. Kein Merge. Kein Publish.
