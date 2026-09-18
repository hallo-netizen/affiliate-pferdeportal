# STARTMASTER0107 – Preproduction Entry Reconcile – 2026-09-18

## Zweck
Technische Vorstufe vor dem nächsten realen Einzelartikel reparieren. Kein Codex-Lauf, keine Artikelproduktion, kein Publish.

## Reparaturen
- HTTP-403-Ursache im Environment-Setup beseitigt: Wenn der lokale Checkout bereits exakt dem frisch über GitHub ermittelten main-SHA entspricht, wird kein unnötiger git-fetch mehr ausgeführt. Die Main-Identität bleibt geprüft und lokal materialisiert.
- V1/V2-Doppelwahrheit beseitigt: output_release_gate.py liest den gültigen Preflight-Vertrag jetzt aus demselben Producer wie worker_freshness_guard.py. Keine zweite fest codierte Vertragsversion.
- Die auf PR #275 bewiesene Block-Semantik wurde auf den aktuellen System-4-Reparaturweg portiert. Der alte divergierte PR275-Unterbau wurde nicht übernommen.
- Der aktuelle Reparaturweg bleibt Same-Article über DRAFT_WORKER und controller.py fullcheck/repair. Kein Legacy-Repairpfad wurde reaktiviert.

## Nachweise
- System 4A Real LT68 PPM679 Acceptance Run 35335734559: PASS.
- Pferde Atelier Immutable Base Hardlock Run 35336072555: PASS.
- Pferde Atelier Deterministic Entrance Gate Run 35336074403: PASS.
- Vorherige rote Hardlock-/Entrance-Runs waren ausschließlich Folge der absichtlich noch alten Hashbindungen und wurden durch die reguläre Bindungskette behoben.

## Sicherheitsgrenzen
- Codex wurde nicht aufgerufen.
- Kein Produktionsartikel wurde gestartet.
- Kein advance, Batch-Collect, Release oder Publish.
- CURRENT bleibt bis zur ausdrücklichen Freigabe des nächsten realen Einzelartikel-Laufs BLOCKED.

## Warum
Die technische Eingangskette musste wieder eine einzige Vertragswahrheit und konsistente Hashbindungen besitzen, bevor ein realer Artikeltest zulässig ist. Die PR275-Arbeit durfte dabei nicht als alter Parallelstand übernommen werden, sondern nur in den heutigen System-4-Weg integriert werden.
