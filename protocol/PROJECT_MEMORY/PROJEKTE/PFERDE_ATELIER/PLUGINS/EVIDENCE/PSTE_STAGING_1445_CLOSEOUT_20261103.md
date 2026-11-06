# QA-Evidence – PSTE Staging, 03.11.2026

**Beweisart:** Sichtbare Nutzer-WordPress-Screenshots aus dieser Unterhaltung und tatsächlich zugängliches Chat-ZIP. Kein echter eigenständiger Server-/MySQL-Zugriff.

- Letzte sichtbare Staging-Version: PSTE 0.57.144.4 (15:42 Uhr Berlin), WordPress `oliver-beil.de`.
- Reset: Oberfläche `COMPLETE`, 5.016/5.016 nach UI gesichert/zurückgesetzt; nicht durch unabhängige Tabellenabfrage verifiziert.
- Neuer Prüflauf: Screenshot 320/5.014 `PSTE_FRESH_RECHECK_CONCURRENT_CHANGE_OR_WRITE_MISSING`; später `PSTE_EXISTING_ONLY_RESUME_STATE_INVALID`; letzter Stand `PSTE_BREADTH_QUEUE_STEP_ALREADY_RUNNING`. E2E **NICHT BESTANDEN**.
- Paket PSTE 0.57.144.5 wurde nach diesen Bildern bereitgestellt, aber seine Installation ist **nicht** bestätigt.
- Physisch geprüftes ZIP dieser Chatsitzung: `PFERDEATELIER_PSTE_0.57.144.5_SPEICHERUNG_KOORDINATION_NUR_TEST.zip`. SHA256 `9192ed966d3a89a43ff06df71ba08d521351ccad19ec53a3f7c312434fb892a0`; 607.947 Bytes; 120 Einträge; CRC PASS; 82/82 PHP-Lints PASS; Plugin-Header 0.57.144.5.
- Separater lokaler Bericht `PFERDEATELIER_PSTE_1445_NACHWEIS.txt` beschreibt PHPUnit-freie PHP-Stubs mit Originalklassen, 5.016 künstlichen Speicherfällen, Recovery-Test und Fehlersperren; es liegt KEIN E2E-Test mit echten 5.016 WP-Datensätzen vor.
- PSERC 0.28.53 und K0 nicht verändert; diese Aussage betrifft die Arbeit in diesem Chat, nicht eine aktuelle Live-Inspektion.
- Canonical Plugin-Artefakt `/Campus-Plugins/PFERDE_ATELIER/PPA-005/CURRENT.zip` im separaten Schrank wurde im Rahmen dieser Prüfung nicht physisch gelesen. **Keine Plugin-Current-/Release-Aussage aus dem Chat-ZIP ableiten.**

Dieses Dokument ist **nur statische Evidence**. Die aktuelle fachliche Wahrheit und GENAU EINE NEXT ACTION bleiben im zuständigen `PLUGINS/CURRENT_STATE.md`.
