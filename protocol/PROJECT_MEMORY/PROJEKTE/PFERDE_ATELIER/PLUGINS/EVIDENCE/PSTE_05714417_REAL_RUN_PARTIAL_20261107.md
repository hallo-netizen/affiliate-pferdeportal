# 07.11.2026 PSTE 0.57.144.17 – echter MINI-Stapel-Zwischenstand

Quelle: vom Nutzer hochgeladener `pste-stapelbericht-2026-11-07 (1).json`, Zeitstempel **2026-11-07T09:35:13Z**, Version **0.57.144.17**. Bei Auslesung war der Lauf noch **RUNNING 29/87**, **58 PENDING**, **26 zurückgehalten** (davon 25 HELD + 1 BLOCKED), **3 PASS**, kein Transportfehler. Nicht als 87er-Endergebnis ausgeben!

Vier der bisher 29 geprüften Fälle tragen weiterhin `PSTE_PORTAL_RELEVANCE_NOT_PROVEN`:
1. Horseware-Regendecken und ihre Unterschiede bei Schnitt und Ausstattung
2. Regendecken für Ponys mit der richtigen Größe und Passform finden
3. Regendecken von Krämer nach Passform und Ausstattung auswählen
4. Gut sitzende Regendecken für Shetlandponys finden

Drei weitere Wassertrog-Fälle sind noch **PENDING** und dürfen nicht als schon erneut blockiert mitgezählt werden.

**Neue festgestellte gemeinsame Code-Hürde der v17-Fassung:** Der MINI-JA-Beleg wird in `includes/class-pste-repository.php::reanalyzeRetainedBacklogBatch` trotz „eine Relevanzquelle“ **nur** dann gelesen, wenn `$isStoredTitleCandidate` und `title_candidate_evidence.source === LANGUAGE_TITLE_DESK_IMPORT` gelten. Damit ist der Relevanzbeleg weiterhin **an den Zustand der Titelmetadaten gebunden** – genau entgegen dem KISS-Ziel. Die v17-Simulation prüfte isoliert `PSTE_Mini_Workflow::approvedRelevanceFor` und das Relevanz-Gate, nicht hinreichend die aufrufende Repository-Kette. Der reale Bericht belegt Fortbestand der 4 Sperren; der Bericht allein enthält nicht den gespeicherten Payload, daher nicht auf Einzelfallursachen schließen. Code-Hürde an EINER Stelle entfernen, echte DB-Eingaben/Kopplungen negativ prüfen und keine vorzeitige Installer-Freigabe.

Offen: 87/87 Abschluss, Zuordnung/Kategorie/echte Dubletten und K0-Schutz. Keine Live-Daten oder PSERC ändern.
