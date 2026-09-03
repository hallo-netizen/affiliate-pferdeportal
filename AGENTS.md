# TEMPORÄRE CODEX-MAINTENANCE-AUTORISIERUNG – NUR DIESER REPARATUR-BRANCH

Diese Anweisung gilt ausschließlich auf `rootfix-107007-fachworkflow-proofs-20260903` und darf NICHT nach `main` übernommen werden.

## Einziger Auftrag
Repariere ausschließlich die technische Ursache, warum der bestehende unveränderte Fachworkflow in `107007` zwar echte `FACHWORKFLOW_PASS`-/Stage-Proofs liefern muss, aber die aktuelle Worker-Aktion keinen produktiv ausführbaren, gebundenen Proof-Handoff bereitstellt.

## Maintenance-Einstieg
Für diesen isolierten Reparatur-Task NICHT `cloud_entry.py start` ausführen und NICHT den aktuell gebundenen Produktionsbatch starten. Der aktuelle Produktions-State darf weder verändert noch abgeschlossen werden. Diese Maintenance-Ausnahme ist notwendig, weil die normale repositoryweite Eingangstür sonst jeden Reparatur-Task sofort in den produktiven Step `107007` bindet.

Zuerst den aktuellen `main`-Stand und die Historie der früher funktionierenden 107007-Artikelausführung sowie der später eingeführten Dual-Rootfix-/Fachworkflow-Proof-Pflicht prüfen. Danach nur den kleinsten technischen Adapter-/Proof-Handoff-Fix implementieren.

## HARDLOCK
- Textmaschine unverändert.
- PPM, PSERC, PSTE, Redaktionsplan, Artikelregeln, SEO-/Qualitätsregeln und WordPress-Importer unverändert.
- Keine Prüfung abschalten oder abschwächen.
- Keine Proofs faken oder bloße PASS-Dateien ohne reale Ausführung erzeugen.
- Keine alten Artikel-/Produktions-JSONs oder alten Artikelkörper für neue Produktion wiederverwenden.
- Keine Sonderlösung für den aktuellen 7er-Batch.
- Keine Parallelarchitektur und keine neue Fachlogik.
- Kein Auto-Publish.

## Ziel
`gebundener Artikel -> bestehender unveränderter Fach-/Textprozess -> reale Stage-Ausführung -> echte hashgebundene Stage-Proofs -> FACHWORKFLOW_PASS.json -> 107007 akzeptiert PASS -> nächster Artikel`

Der Mechanismus muss artikel- und batchneutral sein.

## Tests
Positiv und negativ testen. Fehlender, falscher oder nachträglich veränderter Stage-Proof muss fail-closed blockieren. Soweit im Reparatur-Branch ohne produktive externe Abhängigkeiten möglich, zwei verschiedene synthetische Batch-/Item-Identitäten durch denselben technischen Adapter testen, damit keine aktuelle 7er-Sonderbindung entsteht.

Ein echter Produktions-End-to-End-Test darf erst NACH Merge über den normalen Dispatcher auf `main` erfolgen; auf diesem Maintenance-Branch niemals den produktiven State verändern.

## Vor Abschluss zwingend
`AGENTS.md` byte-identisch auf den aktuellen `main`-Inhalt zurücksetzen. Die temporäre Maintenance-Autorisierung darf im finalen PR-Diff NICHT enthalten sein.

Im finalen PR dürfen ausschließlich technisch notwendige Adapter-/Proof-Handoff-Dateien, deren Tests und technisch zwingende Hashbindungen enthalten sein. Keine Fachdatei verändern.
