# Texterstellung 0.4.16 — NUR isolierte TESTseite oliver-beil.de

Stand: 2026-11-15. Nutzer hat Version 0.4.15 wegen RUNNING ohne sichtbare Ergebnisse deaktiviert.

## Nachgewiesene Ursachen
- Version 0.4.15: TXE_Workshop::deactivate() leer.
- PSTE_Research_Driver::maybeKickExisting() kann gespeicherte RUNNING-Aufträge auf WordPress-Aufrufen erneut anstoßen.
- Fortschritt wurde zuvor aus einer Signatur mit auch ohne neue Suchergebnisse veränderlichen Zeitstempeln gelesen.
- Plugin-UI lud sich alle 15 Sekunden automatisch neu. Der bestätigte Start ist kein bestätigtes Rechercheergebnis.

## KISS-Änderungen 0.4.16
- Eine persistente Halt-Sperre im ursprünglichen PSTE-Recherchetreiber. Manueller Stopp, Plugin-Deaktivierung/Reaktivierung und Zeitgrenzen nutzen denselben Zustand, nicht drei Systeme.
- Originale native PSTE-Breadth-Research-Queue::requestCancel bzw. PSTE-Research-Job::parkCurrent für den verlustarmen Abbruch; keine zweiten Keyword-/Kategorieentscheidungen. Eine schon laufende Einzelanfrage nicht unsicher beenden; bei Sperre Halt behalten, bis sicher abschließbar.
- Keine automatische Wiederaufnahme aus einem gestoppten Zustand; auch verzögerte Cron-/Loopback-Aufrufe starten nichts. Neuanlauf nur nach ausdrücklicher Auswahl und Kostenbestätigung.
- Anzeige: echte Phase, Daten-Schritt, bereits empfangene Keyword-Rohzeilen, letzte echte Ergebnisänderung, Stoppgrund; nur manuelles Aktualisieren, kein Reload alle 15 s.
- Ohne echte Ergebnisänderung nach 60 s Warnung, nach 120 s Stopp; spätestens nach 300 s pro Kategorie Stopp. Bei Kategorienwechsel startet neues Zeitbudget. Reine Zeitstempel sind kein Fortschritt.
- Originale MINI-/K0-Produktion, übrige bestehende Daten/Entscheidungen unberührt.

## Lokale Tests
- Original PSTE_Research_Driver PHP gegen simuliertes WordPress/Provider/Queue: 21/21 PASS.
- Original PSTE_Breadth_Research_Queue PHP gegen simulierten WordPress-Datenspeicher: 12/12 PASS (persistentes CANCELLED, Ergebniserhalt, paralleler Lock, spätere Stornoauflösung).
- 77/77 PHP-Syntaxprüfungen PASS; ZIP-CRC PASS.
- 86 Dateien; nur 4 verändert: Hauptdatei, originaler PSTE Research Driver, originaler PSTE Research Job (additiver Zähler), README.
- **Kein echter WordPress/MySQL/DataForSEO-Lauf**. Nicht als Live-getestet oder live-freigegeben ausgeben.

## Installierbare Test-ZIP + vollständiger QA-Bericht im Plugin-Büro (Library)
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_KISS_0.4.16_TEST_Stop_Fortschritt_Zeitgrenzen.zip`
SHA256 c44d946cd1ec7d682eb6e2bd19801d550c82536efdc7615229b4dab55ba5c38e
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/TEXTERSTELLUNG_KISS_0.4.16_STAND_UND_SIMULATION_20261115.md`

## Nächster Schritt
Bestehendes Plugin auf isolierter oliver-beil.de-Testseite nach Backup durch neue ZIP **ersetzen, niemals löschen**. Beim Aktivieren kein Auto-Neustart der bestehenden Jobs; zunächst Stopp/Status des alten Windschutz-Jobs prüfen, dann höchstens eine neue kostenpflichtige Recherche ausdrücklich starten. Erst danach MINI, K0 und Draft-End-to-End-Test. Nicht auf Live-Seite installieren.