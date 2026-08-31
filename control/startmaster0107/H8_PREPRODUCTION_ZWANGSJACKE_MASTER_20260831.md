# STARTMASTER0107 – H8 PREPRODUCTION-ZWANGSJACKE MASTER

Stand: 2026-08-31

## Oberste Massgabe
Ab der ersten Sekunde keine freie Workflowentscheidung des Chats. Der Wächter bleibt fachblind: keine Inhalts-, Qualitäts-, SEO-, Titel-, Keyword-, LanguageTool-, PPM-, PSERC-, PSTE-, Design- oder Publish-Bewertung.

## Hart geprüfte Optionen
1. Nur härterer Prompt: VERWORFEN. Ein Prompt ist keine technische Akzeptanzsperre.
2. Nur bestehende Pakettür `R_PRE_001`: VERWORFEN. Das Paket müsste weiterhin vor dieser Tür entstehen.
3. Neue Tür davor ohne kryptographisch gebundene Herkunft: VERWORFEN. Ein frei erzeugtes Paket könnte theoretisch eingeschleust werden.
4. Gewählt: `R_BOOT_001` vor `R_PRE_001` plus signierte H8-Herkunftsbindung und erneute Herkunftsprüfung vor `R_001`.

## Zielkette
`Sekunde 1 -> R_BOOT_001 -> signiert H8-gebundenes Produktionspaket -> R_PRE_001 -> H8 Runtime-Provenance-PASS -> R_001 -> unveränderter bestehender Fachworkflow`

Der Wächter prüft dabei nur mechanisch Tür, Bindung, Hash/Signatur und Herkunft. Er bewertet niemals Artikelqualität.

## Technische Umsetzung
- `control/CURRENT_STARTMASTER.json` zeigt auf `project_single_door_entry_v2.py`.
- `project_single_door_entry_v2.py` validiert zuerst die hashgebundene H8-Grenze und wählt ausschließlich den aktuellen gebundenen Raum.
- `R_BOOT_001` exponiert genau eine erzwungene parameterlose Capability `execute_bound_action`.
- `single_door_bootstrap.py` bindet den aktuellen Runtime-Batch/Snapshot und akzeptiert als Ergebnis nur ein Paket, dessen Workflow-Release die H8-Bindung kryptographisch mitsigniert.
- `preproduction_provenance_guard.py` verlangt exakt die aktuelle Generation, Batch-ID, Snapshot-Hashes, `R_BOOT_001`, `P_BOOT_001` und `SINGLE_DOOR_BOOTSTRAP_ONLY` innerhalb des signierten Workflow-Releases.
- `runtime_batch_slot_guard_h8.py` lässt `RUNTIME_INPUTS_BOUND` nur mit gültiger H8-Herkunft weiterlaufen.
- 107007 ist auf die H8-Grenze hashgebunden und muss zuerst `project_single_door_entry_v2.py status` ausführen.
- Der Textproduktionsprompt und die Notfall-Übergabe beginnen ebenfalls unmittelbar mit der ersten Tür.

## Alte Umgehungsroute
Ein altes oder frei erzeugtes Produktionspaket ohne signiertes `h8_bootstrap_binding` erreicht `R_001` nicht mehr. Selbst wenn der alte Runtime-Lifecycle technisch aufgerufen würde, blockiert der autoritative H8-Runtime-Guard vor produktiver Weiterleitung.

## Tests
Temporärer, ausdrücklich nicht gemergter CI-Prüf-PR #57 wurde nur verwendet, um den neuen H8-Test auf GitHub Actions auszuführen.

Deterministic Entrance Gate Run 102: PASS.
- Legacy deterministic gate regression: PASS
- Codex Cloud entrance positive-negative CI: PASS
- Production continuity positive-negative CI: PASS
- H8 preproduction bootstrap positive-negative CI: PASS
- H8-Testfälle: 8/8 PASS
- realer aktueller Raum: `R_BOOT_001`
- `quality_authority`: `NONE`
- `content_semantics_inspected`: `false`
- API-Abhängigkeit der aktiven Eingangsschicht: keine

## Wichtige externe Restbindung
Die private Workflow-Signatur bleibt absichtlich ausserhalb des Repositorys. Deshalb darf das Repository selbst kein Ersatzpaket signieren.

Die serverseitig an `R_BOOT_001` gebundene Producer-/Signer-Capability MUSS die H8-Bindung im signierten Workflow-Release erzeugen. Solange diese externe Capability nicht verfügbar/gebunden ist, bleibt `R_BOOT_001` fail-closed. Es gibt ausdrücklich keinen Chat-Fallback.

Diese Restbindung ist keine Fach- oder Qualitätsänderung, sondern die letzte technische Anbindung der neuen ersten Tür an den bereits vorhandenen externen Producer/Signer.

## Nicht verändert
- keine Artikelregeln
- keine Qualitätsgates
- keine Recherche-/Fact-Pack-Regeln
- kein LanguageTool/PPM/PSERC/PSTE-Fachverhalten
- keine Titel-/Keyword-/SEO-/Designregeln
- kein Auto-Publish

## Prototyp-Bewertung
Repository-seitig ist die Lücke vor `R_PRE_001` geschlossen und negativ abgesichert. Für einen vollständigen echten Produktions-PASS fehlt nur die serverseitige Bindung des vorhandenen Producers/Signers an `R_BOOT_001`; bis dahin blockiert das System statt frei weiterzuarbeiten.
