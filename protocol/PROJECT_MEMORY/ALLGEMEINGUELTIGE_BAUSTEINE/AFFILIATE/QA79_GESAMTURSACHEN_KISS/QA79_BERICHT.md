# QA79 – eBay KISS Gesamtursache und echte Freigabegrenze
**Stand 15.11.2026. NICHT INSTALLIEREN, KEINE LIVE-ABNAHME.**

## Zielvertrag
QA69 unverändert: eine gespeicherte 283er-Familienzuordnung; Suche/gezielter Ersatz nur vom fachlichen Besitzer; laufende Verfügbarkeit nur als Quellenstatus ohne erneute Zuordnung; ein öffentlicher SAFE-Bestand; eine Schlussbereinigung; EIN GitHub-Arbeiter; nachweislicher terminaler Gesamtabschluss.

## An Originaldaten und PHP nachgewiesene Grundursachen
1. **Unnötiger Wiedereintritt in Suche/Ranking:** Vor QA77 wurde eine Vollrecherche nach 3h fällig und auch ein als `refresh` gestarteter Lauf ging durch die Fachauswahl und Gapfill. QA77 hat das lokal getrennt und die Fälligkeit auf wöchentlich ab echtem Gesamtabschluss umgestellt; live NICHT verifiziert.
2. **Zwei Zeitanstöße für dieselbe Frischefunktion:** Der Original-Hauptcode registriert unter `init` sowohl das Entfernen alter Canonical-Crons als auch `ensure_ebay_refresh_schedule`; letztere legt zusätzlich einen 2h-WordPress-Cron an. Die kurze GitHub-Kette prüft ebenfalls Quellenfrische. Das sind **zwei Takte**, aber nicht zwei fachliche Produktentscheidungen (QA78 direkter Original-PHP-Test 17/17).
3. **Zu geringe nachgewiesene Quellenprüfkapazität:** Im eBay-Quellcode werden fällige veröffentlichte Artikel 2h vor `fresh_until` in Paketen zu maximal 5 geprüft. Die echten drei GitHub-Läufe (Jobs `132854576005`, `132864326218`, `132874229982`) hatten 70,37/70,44/72,41 Sekunden zwischen Heartbeats. Für **eine konservative Lastprobe mit 634 gleichzeitig fälligen Kampagnen** wären 127 Pakete und bei abwechselnder Suche/Frische 254 Heartbeats nötig = **4,96–5,11 Stunden** (ohne zusätzliche Anbieter-Latenz). Auch der alte WP-Cron benötigte in diesem Fall 3,17h. Die 634 stammen aus einer BESTANDS-Anzeige; dass 634 tatsächlich gültig und gleichzeitig fällig wären, ist ausdrücklich **nicht belegt**. **Die lokale QA79-Zusammenlegung kann die 2h-Frist im Worst-Case NICHT garantieren und darf daher nicht installiert werden.**
4. **Keine echte 283er-Regal-Abnahme:** Ältere 161/298 waren real, die 5/283 sind ein historischer Zwischenstand; 634 Freigaben sind nicht 634 geprüfte Familien. CSVs enthalten keine vollständigen heutigen originalen WP-Quell-/Creative-/Zielseiten-/SAFE-Daten zu den echten Provider-Antworten. Das grüne GitHub-`completed` am 15.11. 15:31:54 MEZ beweist technischen Abschluss, NICHT öffentlichen 283er-Endbestand.
5. **GitHub-Wecker nicht zuverlässig abgenommen:** Main arbeitet mit nomineller 15m-Schedule und 30-facher Selbstkette; PR #759 ist weiterhin Hardlock-geschützt/unmerged. Keine Umgehung der Sicherheit.

## QA79 – eine gebündelte nur lokale Testvariante
NUR die beiden **bestehenden** Dateien `includes/trait-ppar-ebay-run.php` und `includes/trait-ppar-ebay.php` auf der QA77-Quelle verändert:
- GitHub-Heartbeat erledigt einen begrenzten Verfügbarkeitsbatch ODER das nächste kanonische Suchpaket; dieselbe gespeicherte Lauf-/Quellenfrische, kein neuer Worker/Entscheider.
- `ensure_ebay_refresh_schedule` entfernt alle alten WP-Cron-Termine einschließlich Fortsetzungen; die echte vorhandene Plugin-Hauptdatei ruft die Methode schon unter `init` auf.
- Bei manuellem Stop keine Quellenarbeit. Bei fehlendem Nachweis eines Speicher-Fehlers sichtbarer Systemstopp statt endloser Stummwiederholung. SAFE-Checkpoint unverändert.
- **Kein anderer Partner, K0, WP Core oder GitHub Workflow verändert.**

**Lokal ausgeführt:** 11/11 Heartbeat/Stop-/Fallback-Fälle, 13/13 Frische-/Cursor-/WP-Cron-Fälle (11 explizite Modellquellen genau einmal), 17/17 originale Quellenentscheidungsfälle (95 echte historische IDs mit MODELLANTWORTEN), 26.967/26.967 bestehende QA77-Regressionen (hauptsächlich Audit-Konsistenz, keine 26k echten Produkttests), acht vollständige PHP-Controller-Modellläufe; 23/23 PHP syntaktisch gültig, 66 Original-Paketdateien, genau zwei abweichend, 64 identisch.

**Freigabebedingung / nächster zusammengefasster Nachweis:** EINE unveränderte reale Momentaufnahme vom bestehenden WordPress-Bestand (aktive veröffentlichte Kampagnen, Frische-/Fälligkeitsverteilung, Quellen-, Creative-, Zielseiten- und SAFE-Zuordnung) plus tatsächliche Provider-Laufzeit unter bestehendem GitHub-Takt. Damit denselben 283er-Abschluss und 6h-Frischebudget im vollen Ablauf kontrollieren. Erst wenn die eine Uhr mindestens die wirkliche Frischekapazität erreicht, darf der bisherige WP-Cron überhaupt entfallen. Keine neue Pluginversion auf Verdacht. **QA69 NICHT BESTANDEN.**

Reproduzierbares lokales Archiv in der Chat-Datei: `QA79_GESAMTURSACHEN_KISS_NUR_LOKALER_BEWEIS_KEIN_PLUGIN.zip` (kein WordPress-Installationsarchiv), SHA256 `4df85f567e350a58cbc32b8da3279ee894f9fd78280a2f21e1aa091bd83fa14c`.
