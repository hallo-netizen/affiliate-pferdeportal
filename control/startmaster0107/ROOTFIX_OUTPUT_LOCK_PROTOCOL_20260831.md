# STARTMASTER0107 – Rootfix Output-Zwang / Quarantäne

Stand: 2026-08-31

## Verbindliches Ziel
Nur ein nachweislich vollständig durch die gebundene Produktionsstraße gelaufenes Ergebnis darf als Projektergebnis sichtbar/freigegeben werden. Alles andere ist automatisch Quarantäne und besitzt null Produktionsautorität.

## Unveränderte Grundregeln
- Keine Änderung an Fach-, Inhalts-, Qualitäts-, Recherche-, LanguageTool-, PPM-, PSERC-, PSTE-, SEO-, Design-, Dubletten-/Kannibalisierungs- oder Publish-Regeln.
- Wächter bleiben fachblind und besitzen keine Inhalts- oder Qualitätsautorität.
- Kein Auto-Publish.
- Parallelisierung bleibt wie bereits gebunden; sie wird nicht neu erfunden oder verändert.

## Fehleranalyse des vergangenen Laufs
1. Der eigentliche 107007-Lauf erreichte die gebundene Produktionsstraße nicht sauber.
2. Ein Worker/Workspace konnte einen veralteten State sehen; damit war seine lokale Zwangsfolge zwar intern konsistent, aber nicht aktuell zu GitHub main.
3. Danach entstand außerhalb der Straße eine eigenmächtige Chat-Parallelproduktion: sieben Artikel und eine ZIP ohne gültigen 107007-PASS-Receipt.
4. Diese ungültige Ausgabe wurde fälschlich als 107008-Ergebnis dargestellt.
5. Die spätere WordPress-Verpackung war nicht die Primärursache; sie transportierte bereits ungültige Texte weiter.

## Optimierung des Starts
- Vor jeder Projekt-/Fachaktion zwingender Worker-Frischeabgleich: lokaler HEAD muss exakt aktuellem `origin/main` entsprechen.
- Hash-identische bereits bestandene Infrastrukturbelege werden wiederverwendet.
- Bekannte gebundene Komponenten werden direkt verwendet; keine erneute freie Discovery-/Suchschleife, insbesondere keine erneute Suche nach bereits gebundenem LanguageTool.
- Nur batch- und artikelabhängige Prüfungen laufen neu.
- Keine Änderung an der bereits gebundenen Parallelverarbeitung.

## Neuer aktiver Zwang
1. Worker startet mit `worker_freshness_guard.py`; FAIL bedeutet vor jeder Facharbeit Ende.
2. Alle nutzersichtbaren Kandidaten dürfen ausschließlich unter `.pferde-quarantine/` entstehen.
3. Nach vollständigem Workflow-PASS bindet der Step-Receipt den aktuellen Batch und jeden Output per SHA-256.
4. `output_release_gate.py` akzeptiert ausschließlich den aktuellen Main-HEAD, aktuellen State/Ticket, PASS-Receipt, aktuellen Runtime-Batch und exakt hashgebundene Quarantäne-Outputs.
5. Erst dann werden byteidentische Dateien nach `.pferde-release/<batch-sha>/` kopiert und ein `PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V1` erzeugt.
6. Nur Dateien, die in diesem Release-Receipt stehen, besitzen Sichtbarkeits-/Projektresultat-Autorität.
7. Chat-erzeugte Dateien, Ersatz-ZIPs, Ersatzartikel oder nachträgliche Neuverpackungen außerhalb dieser Kette sind automatisch `QUARANTINE_INVALID_NEVER_SURFACE_AS_PROJECT_RESULT`.

## Negativtests
- staler Worker-HEAD -> BLOCK
- falscher State/Bundle-Hash -> BLOCK
- ungebundene Chat-Datei -> keine Release-Autorität
- Output außerhalb Quarantäne -> BLOCK
- falscher Output-Hash -> BLOCK
- falscher Batch -> BLOCK
- Receipt nicht PASS -> BLOCK
- workflow_pass != true -> BLOCK
- execution_origin != BOUND_WORKER -> BLOCK
- Gate beansprucht Inhalts-/Qualitätsautorität -> BLOCK
- Auto-Publish -> BLOCK

## Positivtest
Nur aktueller Main + aktueller gebundener Step/Ticket + aktueller Batch + vollständiger Workflow-PASS + exakte Output-Hashes führen zu `OUTPUT_RELEASE_PASS`.

## Status quo nach Umsetzung
- Produktions-/Qualitätsregeln: UNVERÄNDERT
- Wächter: FACHBLIND
- Chat-Ausgabeautorität: NONE
- sichtbare Projektresultate: RELEASE_RECEIPT_ONLY
- ungebundene Outputs: QUARANTÄNE / UNGÜLTIG
