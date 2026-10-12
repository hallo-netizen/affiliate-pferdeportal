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
STATUS: **VORERST AKZEPTIERT 1.50.634 / KEINE WEITERE BILDRUNDE JETZT**

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
STATUS: **VORERST AKZEPTIERT 1.50.634 / KEINE WEITERE BILDRUNDE JETZT**

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


**Live-Abnahme 1.50.635 auf einer realen Kategorieebene-2-/Hub2-Seite.**

## Arbeitsfehlerprotokoll
Dauerhafte interne Fehler-/Lernakte:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/ARBEITSFEHLERPROTOKOLL_20261012.md`

## HRD-064 – Testbeiträge in 1.50.636 angelegt, aber auf Hub2 nicht sichtbar
STATUS: **LOCAL CLOSED 1.50.637 / LIVE OFFEN**

LIVE-BEFUND:
Auf `Druck & Fotografie` blieb die Beitragsvorschau leer und zeigte den Hinweis, dass keine gleichnamige Beitragskategorie gebunden sei.

ROOT CAUSE:
`render_post_previews()` brach bei Seiten ohne gleichnamige WordPress-Beitragskategorie ab, bevor die vier Testbeiträge überhaupt abgefragt wurden. Die Zuordnung der Testbeiträge zu allen vorhandenen Beitragskategorien konnte dieses Gate daher nicht überwinden.

FIX 1.50.637:
- Testposts werden robust bei erstem eingeloggten Admin-/Frontend-Aufruf angelegt bzw. wiederverwendet;
- sie sind privat, klar mit `[TEST]` markiert und besitzen Beitragsbilder;
- für eingeloggte Hub2-Designprüfung existiert ein gezielter Demo-Fallback über Meta `_hd_demo_post_v150637=1`;
- reale öffentliche Beitragslogik bleibt unverändert.

TEST:
PHP-Harness ohne gleichnamige Beitragskategorie → 4 Demo-Karten PASS.

## HRD-065 – Hub2-Bildkarten 1.50.641–1.50.643 nicht 1:1 aus Ebene 1 übernommen
STATUS: **LOCAL CLOSED 1.50.644 / LIVE OFFEN**

LIVE-BEFUND:
Trotz mehrfacher Teilfixes blieben Buch-&-Papier-Karten optisch falsch; 1.50.643 änderte zusätzlich die gewünschte 3er-Struktur in der realen Ansicht.

ROOT CAUSE:
Es wurde weiter ein eigener `hd-bp-card`-/`hd-bp-photo`-Sonderweg gepflegt, obwohl die bereits korrekte Ebene-1-Lösung vollständig vorhanden war. Dadurch kollidierten Pilotregeln mit der bestehenden Kartenkaskade.

FIX 1.50.644:
Der Pilot-Sonderweg für Karten/Bilder ist im aktiven Markup entfernt. Buch & Papier nutzt jetzt exakt `hd-next-grid`, `hd-next-card has-photo`, `hd-next-photo`, `hd-next-card-body`, `hd-next-copy` und `hd-row-size-*` wie Ebene 1.

BEWEIS:
Browser-Simulation mit echter CSS-Kaskade und echten Bildern:
- 1440: 3+2;
- 900: 2+2+1;
- 760: 1-spaltig;
- Bildslot/Card-Border-Geometrie flush 0;
- Bild/Slot Δ 0;
- kein Overflow.


## Aktuell erster Blocker
**Live-Abnahme 1.50.644: Header-Claim-Dicke + Buch-&-Papier-Unterkategoriekarten.**

