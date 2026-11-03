# PFERDE-ATELIER – PLUGINS – FEHLERQUELLEN

## PSTE-STAGING-20261103 (nicht als CURRENT oder NEXT-ACTION-Quelle verwenden)

Bereich: Portal SEO Topic Engine, PPA-005, **TEST** `oliver-beil.de`, keine Live-Freigabe.

### Tatsächlich durch Nutzer-Screenshots belegte Fehler

- **PSTE-CLEAN-20261103-01**: PSTE 0.57.144.3, kontrollierter Themenneustart bei FINALIZE abgebrochen mit `PSTE_CLEAN_RESET_HISTORY_KEY_INVALID`. Der im lokalen Quellcode geprüfte Schlusscheck erwartete 64 Zeichen; das Plugin erzeugt auch 36-stellige UUID-Schlüssel. 0.57.144.4 änderte die lokale Prüfung; WordPress-Screenshot 15:29 zeigte danach **COMPLETE**.
- **PSTE-RECHECK-20261103-02**: Mit PSTE **0.57.144.4** schlug anschließender Bestandslauf bei **320/5014** fehl, `PSTE_FRESH_RECHECK_CONCURRENT_CHANGE_OR_WRITE_MISSING`. Nicht bewiesen, ob auf dem echten WordPress-Server eine unveränderte Speicherung, ein echter Konflikt oder ein Fehler vorlag. Der Code in 0.57.144.4 wertete Datenbank-UPDATE=0 ohne strikte Rückleseprobe als Fehler.
- **PSTE-REENTRY-20261103-03**: Nachfolgender Screenshot zeigte `PSTE_EXISTING_ONLY_RESUME_STATE_INVALID`; letzter sichtbarer Stand 15:42 zeigte bei PSTE **0.57.144.4** `PSTE_BREADTH_QUEUE_STEP_ALREADY_RUNNING` und Status GESTOPPT. Kein nachgewiesener erfolgreicher Staging-Endlauf.
- **PSTE-DIAG-20261103-04**: Große Diagnose-Downloads waren zuvor mehrfach nicht erfolgreich; ein vollständig frischer Diagnoseexport des finalen abgebrochenen Laufs liegt nicht vor.

### Nachgestellte Korrektur, NICHT live abgenommen

Testpaket `PFERDEATELIER_PSTE_0.57.144.5_SPEICHERUNG_KOORDINATION_NUR_TEST.zip`, SHA256 `9192ed966d3a89a43ff06df71ba08d521351ccad19ec53a3f7c312434fb892a0`; 120 ZIP-Einträge, 82 PHP. ZIP-CRC und alle 82 PHP-Lints im Abschlusslauf vom 03.11. unabhängig PASS. Der vorhandene lokale QA-Bericht beschreibt WordPress-Stub-Gegenläufe für idempotente Persistenz und Queue-Koordination. Das beweist **nicht** den Erfolg auf WordPress. Eine Installation von 0.57.144.5 ist nicht belegt.

**Grenzen:** Dies ist die autoritative Fehlerdetailsammlung des Staging-Incidents, KEINE zweite dynamische Current-/NEXT-ACTION-Wahrheit. Aktueller Status und der einzige Arbeitsschritt liegen ausschließlich im vom Autoritätsplan genannten `PLUGINS/CURRENT_STATE.md`. Live/K0 unverändert im Verlauf dieser Reihe; nicht als frisch geprüfte Live-Version ausgeben.
