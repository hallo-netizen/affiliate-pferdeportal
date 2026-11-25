# VERBINDLICHE PERFORMANCE-FREIGABEREGEL

Stand: 25.11.2026

Ab jetzt darf KEIN neues Performance-Plugin an den Nutzer ausgegeben werden, nur weil ein Teilabschnitt oder Mikrobenchmark schneller ist.

Freigabe nur wenn ALLE Punkte erfüllt sind:

1. Vollständige relevante Seitenstrecke lokal simuliert
- echte WordPress-/WXR-Daten
- vollständiger Kandidatenpool
- vollständige Produktplätze
- Rendering bis zur tatsächlichen HTML-Ausgabe
- gleiche Eingaben Alt/Neu
- mehrere alternierende Alt/Neu-Läufe, nicht nur Einzelmessung
- Gesamtpfad muss außerhalb der Messstreuung schneller sein

2. Kausalitätsbeweis je Einzelmaßnahme
- jede Maßnahme separat Alt/Neu messen
- jede Maßnahme muss im direkt betroffenen Produktionsabschnitt schneller sein
- Maßnahme ohne stabilen Zeitgewinn wird verworfen
- mehrere bewiesene Maßnahmen erst danach bündeln
- Bündelung muss erneut als Gesamtpfad schneller sein

3. Kein Funktionsrückbau – inhaltlicher Beweis
Byte-/Dateigrößenvergleich allein zählt ausdrücklich NICHT.
Alt und Neu müssen inhaltlich gleich sein für:
- Kandidatenmenge und Reihenfolge
- Ranking und Auswahl
- Provider und Strategien
- Post-/Kampagnen-IDs
- Titel, URL, Bild, CTA, Preis, Währung, Verfügbarkeit
- Fallbacks
- Tracking/Links
- dynamische Metadaten-/Optionsänderungen während desselben Ablaufs
- Providerpause / Emergency-Stop / Filter
- externer Objektcache
- vollständiges gerendertes HTML der betroffenen Ausgabe

4. Vollständiger Funktionsbestand
- keine bestehende Fachfunktion entfernen
- keine bestehende Entscheidung überspringen, außer ihr Ergebnis wird beweisbar identisch wiederverwendet
- Schreibwege, Hooks, Filter, Shortcodes und Fallbacks müssen erhalten bleiben
- Struktur-/Bytevergleich ist nur Zusatzbeweis, niemals Hauptbeweis

5. Release-Schwelle
- kein Plugin für einzelne kleine Fixes
- erst mehrere kausal bewiesene Maßnahmen bündeln
- vor Ausgabe: kompletter Re-Extract-Test des finalen ZIP
- finaler ZIP-Quellstand nochmals gegen Baseline messen
- wenn Gesamtpfad nicht klar schneller ist: NICHT AUSGEBEN

6. Live-Messung
- Live dient nur noch als Bestätigung des vorher bereits lokal bewiesenen Gesamtgewinns.
- Live ist nicht mehr der Ort, an dem erst festgestellt wird, ob das Plugin überhaupt schneller ist.

6.72.379:
- lokal waren Teilpfade und der isolierte Realpfad schneller.
- der nachträgliche Live-Gesamtlauf bestätigte keinen Gesamt-Speedup.
- nach der hiermit verschärften Freigaberegel wäre 6.72.379 NICHT mehr als neuer Release ausgegeben worden.
- 6.72.379 bleibt aktuell installiert, weil kein kausaler Funktions- oder Performance-Rückschritt durch H+I bewiesen ist.
- nächstes Plugin erst nach vollständigem Bestehen dieser Freigaberegel.
