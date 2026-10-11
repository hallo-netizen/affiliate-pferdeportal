# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Autoritative Fehlerhistorie dieses Design-Scopes.  
Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-017
Bisherige abgeschlossene/unter Regression stehende Fehler bleiben unverändert in der Historie.

## HRD-018 – Hauptnavigation bei mittlerer Breite abgeschnitten

STATUS: LOCAL CLOSED IN 1.50.616 / LIVE OFFEN

Korrektur:
- Vollnavigation erst >1560 px;
- 761–1560 px Dropdown;
- <980 px 2-spaltig;
- kein rechter Cutoff.

## HRD-019 – Unterkategorie-Bilder wiederholen dasselbe Weltmotiv

STATUS: LOCAL CLOSED IN 1.50.616 / LIVE OFFEN

Befund:
1.50.615 fiel ohne Child-Featured-Image auf das Parent-Weltbild zurück. Dadurch erschien in Gestalten mehrfach dieselbe Person/dasselbe Bild.

Korrektur:
- generischer Parent-Weltbild-Fallback entfernt;
- echtes Child-Bild gewinnt;
- Gestalten besitzt 7 unterschiedliche Fallbackmotive;
- andere Hubs ohne echtes Bild bleiben vorerst bildfrei statt falsch/dupliziert.

## HRD-020 – Navigation zu weit unten / Berührung mit Trennlinie

STATUS: LOCAL CLOSED IN 1.50.616 / LIVE OFFEN

Korrektur:
Desktop-Transform von 22 px auf 8 px reduziert.

## HRD-021 – Verdacht auf verkleinerte Typografie

STATUS: GEPRÜFT / KEIN GLOBALER TYPO-FEHLER

Vergleich 1.50.614 ↔ 1.50.616:
relevante Schriftgrößen unverändert.

## HRD-022 – Hub1 zeigt Text doppelt offen

STATUS: LOCAL CLOSED IN 1.50.616 / LIVE OFFEN

Korrektur:
Hero behält sichtbaren Kurztext; Zusatztext darunter nur noch geschlossen unter `Mehr über <Welt> erfahren`. Volltext bleibt im HTML.

## HRD-023 – Verkaufbarer Werbeplatz mit 4 Bildern statt einem starken Motiv

STATUS: LOCAL CLOSED IN 1.50.616 / LIVE OFFEN

Korrektur:
- exakt 1 Foto;
- Textoverlay auf dem Foto;
- auffälliger heller Pinselstrich hinter der Headline;
- CTA zu Werbemöglichkeiten & Preisen.

## Aktuell erster Fehler-/Abnahmeblocker

**Live-Abnahme 1.50.616 auf Gestalten bei Desktop / Side-by-Side / Mobile.**
