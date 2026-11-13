# Hobby Depot – Fehlerregister und laufender Stand, 13.11.2026

## Stand 01 – bestätigt durch Betreiber-Screenshot 11:32
- Die Airbrush-Seite zeigt unter **Empfehlungen** drei große, leere Kacheln mit „Nur eingeloggt sichtbar / Affiliate-Produkt / Platz aktuell nicht belegt“.
- Die bisherigen unpassenden Kleidungs- und Garnprodukte werden dort nicht mehr angezeigt.
- Weil keine Produktkarten angezeigt werden, sind die gewünschten Produktbilder, Stichpunkte, Farben und Anbieterbuttons auf der Seite **nicht sichtbar**.
- **Nicht behaupten**, dass HD009 0.1.37 + HD003 1.50.813 den Gesamtworkflow erfolgreich umgesetzt haben.
- Exakte tatsächliche installierte WordPress-Versionen und interne Produktbestände sind durch einen Screenshot allein nicht bewiesen.

## Meine bisherigen Fehler
1. Einzelne synthetische PHP- und CSS-Tests als reale End-to-End-Freigabe dargestellt.
2. Falsche Produkte über restriktive Ausgabesperren unterdrückt, ohne zuvor genügend echte passende Idealo-/Amazon-Daten zu beschaffen.
3. Bestehende HD003-Leerplatzhalter auf der Produktseite nicht in den Funktionstests berücksichtigt.
4. Den Nutzer wiederholt zu Installationen und Screenshots aufgefordert, obwohl kein kompletter Beweis für funktionierende echte Produktkarten vorlag.
5. Testfälle mit selbst erfundenen Beispielartikeln nicht ausreichend als synthetische Tests eingeordnet.

## Zielvertrag
- Keine thematisch falschen Produkte.
- Bei nachweislich fehlenden passenden, echten Produktangeboten: keine leeren Kästen; den leeren Empfehlungsbereich vollständig auslassen, sofern keine anderen Provider dort Angebote besitzen.
- Echte Produkte: Bild, belegbare Kurzmerkmale und tatsächliche mehrere Anbieterbuttons in einer Karte.
- Keine Veränderung an bestehenden fremden Portalen, WordPress-Core, unnötiger Architektur oder zusätzlichen Live-Abfragen.
- Keine Freigabe ohne nachvollziehbaren Test des vollständigen Kategorie-Outputs inklusive **null**, einem und mehreren passenden Produkten.

## Aktuelle Aufgabe
**Erst den PHP-Ausgabe- und Leerplatzhalter-Pfad der bestehenden Design-/Affiliate-Plugins untersuchen; die Stelle finden, die die drei leeren Boxen erzeugt; anschließend minimal korrigieren und dieselbe Quelle mit Null-/Ein-/Drei-Produkt-Ausgaben prüfen.** Danach gesondert die reale Produktabdeckung mit 2747/2901 klären; 2901 nicht ohne echten Feedvergleich als Lösung bezeichnen.

## Änderungslog
- 2026-11-13, Stand 01: Dokumentation eröffnet. **Noch kein Plugin geändert oder installiert.**
