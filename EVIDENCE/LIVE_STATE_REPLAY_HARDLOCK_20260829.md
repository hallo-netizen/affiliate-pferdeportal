# LIVE-STATE-REPLAY-HARDLOCK – verbindlich ab 2026-08-29

## Zweck
Verhindern, dass ein Plugin-Kandidat trotz vieler grüner Einzel-/Proxytests erst nach einem stundenlangen Live-Lauf an einem bereits bekannten oder nicht vollständig nachgebildeten Endzustand scheitert.

## 1. Kein Live-Test auf Basis synthetischer Zwischenzustände
Vor jedem weiteren Live-Installationslauf MUSS der exakte zuletzt beobachtete Produktionszustand als Fixture/Replaysnapshot vorliegen. Dazu gehören mindestens: Run-ID, Phase, Checkpoint, Selection-Status/-Phase, Recovery-Historie/-Grund, Kandidaten-/Gewinnerzahlen, PRIVATE/BUSINESS-Coverage, relevante Freshness-/Timestampdaten und der terminale Fehlercode.

## 2. NEGATIV muss den echten Live-Fehler terminal reproduzieren
Der vorherige Kandidat muss mit genau diesem Fixture bis zum selben terminalen Fehler laufen. Ein Test, der nur prüft, dass eine Recovery startet oder eine Zwischenphase erreicht wird, ist UNGÜLTIG.

## 3. POSITIV muss denselben Zustand bis TERMINAL PASS durchlaufen
Der Fix muss aus demselben Fixture durch die echte State-Machine bis zum finalen Public-/Coverage-Gate und terminalen PASS laufen. Keine Shortcuts, keine direkte Manipulation des Zielzustands, kein Überspringen von Materialisierung, Freshness, Public-Gate, Coverage oder Cleanup.

## 4. Zeitabhängige Fehler werden mit beschleunigter Uhr getestet
Live-Wartezeit ist kein Testinstrument. Der lokale Prüfstand muss virtuelle/beschleunigte Zeit unterstützen und mindestens die realen Zeitgrenzen überschreiten. Für den aktuellen eBay-Fall zwingend: Quelle frisch vor Auswahl, Ablauf während eines mehrstündigen simulierten Runs, stale bei Public-Gate; zusätzlich Grenzfälle knapp vor/auf/nach Ablauf.

## 5. Selektor UND finales Gate müssen dieselbe Frische-Invariante beweisen
Für PRIVATE und BUSINESS gilt: Ein Kandidat, der beim finalen Public-Gate wegen source_stale/source_hash_mismatch/etc. scheitern würde, darf entweder nicht Gewinner werden oder muss vor Veröffentlichung deterministisch ersetzt/neu validiert werden. Der Test muss beides beweisen: Auswahlverhalten und finales Gate.

## 6. Jeder Produktions-Fehlercode erhält einen vollständigen E2E-Regressionsfall
Ein Fehlercode gilt erst als behoben, wenn der Test alte Version = terminal FAIL und neue Version = terminal PASS aus demselben Live-State beweist. Reines 'Recovery wurde gestartet' ist kein PASS.

## 7. Test-Adequacy-Gate vor Installer
Vor dem Packen eines Installers muss maschinell geprüft werden, dass für jeden Fix mindestens vorhanden sind:
- exact-live-state fixture
- old-version terminal negative
- fixed-version terminal positive
- boundary/time test, falls zeitabhängig
- protected-area regressions
- fresh-unpack replay bis terminal
Fehlt einer dieser Punkte: BUILD BLOCKED / NOT RELEASED.

## 8. Mutationsnachweis
Mindestens ein Mutations-/Sabotagetest pro Rootfix: die korrigierte Invariante gezielt wieder brechen; der neue E2E-Test MUSS dann rot werden. Bleibt er grün, ist der Test ungeeignet und der Kandidat gesperrt.

## 9. Keine erneute mehrstündige Live-Runde ohne lokalen terminalen Replay-PASS
Ein weiterer Live-Lauf ist verboten, solange der exakte letzte Live-State lokal nicht vollständig bis terminal PASS durchlaufen wurde. Live dient nur noch als Bestätigung, nicht als Fehlerfindung.

## 10. Freigabe
Pluginfreigabe nur bei: NEGATIV echter Live-State reproduziert + POSITIV gleicher Live-State terminal PASS + Gesamtworkflow-Regressions-PASS + Fresh-Unpack terminal PASS + Mutationsnachweis PASS + lückenlose Protokollierung.

## Aktueller konkreter Fehlerfall
V6.63.4 ist FAIL. Der aktuelle Rootfix muss mindestens den realen PRIVATE-Freshness-Fall abdecken: stale/ablaufende PRIVATE-Quelle über Auswahl -> Materialisierung -> finales PRIVATE-Public-Gate. Die alte Version muss dort terminal scheitern; der Fix muss denselben Fall terminal bestehen. Erst dann darf erneut live installiert werden.
