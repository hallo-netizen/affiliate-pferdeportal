# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.9 LIVE BIS SPEZIALISIERUNGS-TIEFENPRÜFUNG PASS / READ_ONLY_PREVIEW LOKAL PASS / LIVE-FINALPRÜFUNG OFFEN

## Live-Teststand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.9 Hobby Depot Guided Resume`

Live erfolgreich:
- persistenter Arbeitsstand;
- DataForSEO-PASS persistent;
- signierter Initial-Draft übernommen;
- Global-Coverage gespeichert und wiederverwendet;
- korrigierter Global-Stand freigegeben;
- Detailresearch abgeschlossen;
- Spezialisierungs-Tiefenprüfung abgeschlossen.

Aktuelles Research-Paket:
`kategorie-research-hobby-depot-testlabor-aktuell.json.gz`

Research-Befund:
- specialization_depth_research.completed = true;
- 15/15 Content-Knoten exakt abgedeckt;
- remaining_unattempted_estimate = 0;
- 15 Paid-Calls in der Spezialisierungsstufe;
- Spezialisierungskosten 0.225 USD;
- kein WordPress-Write.

## READ_ONLY_PREVIEW vorbereitet

Datei:
`kategorie-read-only-preview-hobby-depot-testlabor-20260928.json`

SHA-256:
`93c72578bfaed4c4600e5b375535619c8a8b2bd55b28f5e5b24cdbac2b64fd00`

Lokale Prüfung gegen exakt V1.8.9:
- Kategorie-Schema PASS;
- Research-Bindung PASS;
- Research-Evidenz PASS;
- Comparator PASS_READ_ONLY_PREVIEW;
- 0 blockierende Evidenzfehler.

Nicht blockierende Warnungen:
- 182 Cross-Cluster-Overlap-Review-Signale aus bewusst überlappenden Dummy-Seeds;
- 6 Sparse-Longtail-Review-Signale.

Negativtests:
- eine erforderliche Cluster-Coverage-Entscheidung entfernt → BLOCKED;
- Research-Bindung manipuliert → BLOCKED;
- unrecherchiertes Primärkeyword eingesetzt → BLOCKED.

Wichtig:
Die Live-HMAC-Signaturen des Research-Pakets sind an den geheimen WordPress-Salt gebunden und werden deshalb erst auf derselben Live-Installation kryptographisch verifiziert. Der deklarierte Inhalts-Hash des Research-Pakets stimmt lokal exakt.

## NEXT ACTION

READ_ONLY_PREVIEW einmal als neuen Arbeitsstand übernehmen. Erwartung: direkte finale Read-only-Gesamtprüfung PASS und sichtbare Aktion `Finale Struktur freigeben`. Erst nach diesem Live-PASS weiter zum Deployment-Dry-Run.
