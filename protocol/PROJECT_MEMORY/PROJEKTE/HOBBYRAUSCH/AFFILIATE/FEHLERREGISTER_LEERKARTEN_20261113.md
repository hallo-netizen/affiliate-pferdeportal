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

## Stand 02 – Ursache im echten Quellcode bewiesen
- Quellarchiv **HD003 1.50.813** vollständig geprüft (1291 Dateien, CRC ok, Original-SHA256 `5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73`).
- `class-hobby-depot-profile-v150709.php`, Zeile 3219: Bei fehlendem Affiliate-HTML wird für eingeloggte Personen bewusst `affiliate_preview_placeholder('Affiliate-Produkt',...)` erzeugt, bis zu drei Stück. Zeile 1827 ist der **wörtlich zum Screenshot passende Text** „Nur eingeloggt sichtbar / Affiliate-Produkt / Platz aktuell nicht belegt“.
- Zeilen 3654–3661 bauen aus diesen erzeugten Vorschauen drei große **Empfehlungen-Karten**. Die zuletzt vergrößerten HD003-Produktkarten-CSS-Regeln machen daraus besonders auffällige leere Boxen.
- Damit ist der Fehler **nicht nur fehlender Import**, sondern zusätzlich ein unberechtigter Admin-Platzhalter im öffentlichen Seitenlayout, sobald der Betreiber angemeldet ist.
- Der Screenshot wurde zu Recht nicht durch die vorherigen CSS-/PHP-Simulationen erkannt, weil es dort immer künstliche Beispielprodukte gab.
- Geplanter minimaler Eingriff: Vorhandene **Produkt**-Vorschau im HD003-Ausgabepfad entfernen; Banner-/Redaktionsvorschauen nicht verändern; echte vorhandene Produkt-HTML unverändert durchlassen. Bei 0 Produkten ganze Empfehlungen-Sektion weglassen.
- Prüfung braucht ausdrücklich eingeloggte **und** ausgeloggte Darstellung bei 0/1/3 echten Produkt-Slots; keine künstlichen Produktbeschreibungen.
- Quelle: `AFFILIATE/EVIDENCE/HD003_HD009_LEERKARTEN_CODE_20261113.txt` (exakte Quellenzeilen aus GitHub-Actions-Abgleich). 
- **Noch keine neue Version in WordPress installiert.**
