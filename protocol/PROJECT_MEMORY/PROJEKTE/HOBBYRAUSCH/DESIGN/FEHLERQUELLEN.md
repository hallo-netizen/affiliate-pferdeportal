# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-056
Historie bleibt bestehen.

## HRD-057 – Navigation 1.50.627 gleichmäßig, aber insgesamt zu tief
STATUS: **LIVE CLOSED**
Navigation wurde danach korrigiert und vom Nutzer live als PASS bestätigt. Ab jetzt eingefroren.

## HRD-058 – Hub-Kartenbilder zu klein
STATUS: **LAYOUT LIVE CLOSED 1.50.628**
Die sichtbare Bildfläche bleibt Desktop 200×107, Tablet 165×88, Mobile 145×78.

## HRD-059 – Zu viele interne Links in Seitenendtexten
STATUS: **LIVE CLOSED 1.50.628**

## HRD-060 – Kategorie-/Link-Bilder zu eng / Lupeneindruck
STATUS: **1.50.629 LIVE FAIL / 1.50.634 LOCAL KORRIGIERT / LIVE OFFEN**

Anforderung:
- Szene weiter gefasst;
- klares Hauptmotiv;
- wenig konkurrierendes Drumherum;
- Thema sofort erkennbar;
- keine Hero-Änderung.

Fix 1.50.634:
- 65 aktive Kategorie-Vorschaubilder visuell geprüft;
- 48× v150629, 11× gezielt ausgewählte weitere v150623-Szenen, 6× v150616;
- keine globale Reaktivierung des alten v150623-Satzes;
- Hub1 bleibt designkontrolliert und fällt nicht auf alte Featured Images zurück.

## HRD-061 – 1.50.630 brachte Doppelbilder zurück
STATUS: **CLOSED / 1.50.630 VERWORFEN**

Root Cause:
- alter v150623-Satz wurde pauschal bevorzugt;
- dadurch wiederholten sich ganze Szenenfamilien.

Fix:
- keine pauschale alte Bildserie mehr;
- nur einzeln visuell geprüfte weitere Szenen werden verwendet.

## HRD-062 – Claim/Logo/Navigationslinie
STATUS: **LIVE CLOSED / EINGEFROREN**

Der Nutzer hat den aktuellen Navigations-/Headerstand live als PASS bestätigt.
Keine weitere Header-/Navigationsänderung in 1.50.634.

## HRD-063 – Kategorie-Vorschaubilder mit sichtbarem Rahmen/Passepartout
STATUS: **1.50.631/1.50.632 LIVE FAIL / 1.50.634 LOCAL KORRIGIERT / LIVE OFFEN**

Root Cause:
Die aktive Karten-CSS enthielt weiterhin eine eingerückte Bildbox, u. a. mit Margin, Hintergrund und Radius. Deshalb blieb trotz Bildwechsel ein sichtbarer Rahmen/Passepartout-Effekt.

Fehler 1.50.632:
Der Build wurde ausgegeben, ohne die endgültige berechnete Karten-CSS im gerenderten Zustand zu simulieren. Die Aussage "Rahmen weg" war damit unbelegt und falsch.

Fix 1.50.634:
- Kategorie-Vorschau füllt ihren Slot vollständig;
- Margin 0;
- Padding 0;
- Border 0;
- Border-Radius 0;
- transparenter Slot-Hintergrund;
- Bildgröße exakt gleich Slotgröße.

Simulation mit echten Assets:
- 1440 px: 200×107, Rahmengeometrie 0;
- 930 px: 165×88, Rahmengeometrie 0;
- 760 px: 145×78, Rahmengeometrie 0.

## Aktuell erster Blocker
**Live-Abnahme 1.50.634 ausschließlich Kategorie-Vorschaubilder.**

## Arbeitsfehlerprotokoll
Dauerhafte interne Fehler-/Lernakte:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/ARBEITSFEHLERPROTOKOLL_20261012.md`
