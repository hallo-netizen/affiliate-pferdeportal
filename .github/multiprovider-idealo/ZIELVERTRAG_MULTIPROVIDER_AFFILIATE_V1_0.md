# ZIELVERTRAG MULTI-PROVIDER-AFFILIATE V1.0

Stand: 27.08.2026
Status: VERBINDLICH für die weitere Affiliate-Zentrale-Entwicklung

## 1. Leitprinzip
Die Affiliate-Zentrale muss mehrere Produktprovider unabhängig voneinander betreiben können. eBay bleibt bestehender produktiver Provider. idealo wird als nächster Provider angebunden. Amazon folgt erst danach. Weitere Provider müssen grundsätzlich ergänzbar bleiben.

KEEP IT SIMPLE ist verbindliches Architekturprinzip. Kein Provider darf technisch voraussetzen, dass ein anderer Provider vorhanden oder funktionsfähig ist.

## 2. Zwei gleichberechtigte Ausgabemodi
### A. Getrennte Provider-Ausgabe
Produkte können getrennt nach Provider ausgegeben werden, z. B. nur eBay, nur idealo, nur Amazon oder mehrere Provider als getrennte Karten. Diese Betriebsart benötigt kein providerübergreifendes Produktmatching.

### B. Gemeinsame Produktkarte
Ein zweifelsfrei identisches Produkt kann eine gemeinsame Karte mit mehreren Bezugsquellen erhalten, z. B. eBay, idealo und Amazon. Eine Provider-Schaltfläche wird nur angezeigt, wenn für genau diesen Provider ein gültiges Angebot bzw. ein gültiger Affiliate-Link vorhanden ist. Keine leeren oder ausgegrauten Platzhalter.

## 3. Providertrennung
Jeder Provider besitzt einen eigenen Adapter. Der Adapter kapselt Datenaufnahme, Normalisierung, Trackinglink, Status, Preis soweit vorhanden, Bild, Produktschlüssel und Aktualisierung. Ein Fehler in einem Adapter darf andere Provider nicht stoppen.

## 4. Neutrales Produktformat
Mindestens: Provider, Provider-Produkt-ID, Titel, Marke, Modell, EAN/GTIN falls vorhanden, weitere eindeutige Produktkennung falls vorhanden, Bild, Preis falls vorhanden, Ziel-/Affiliate-Link, Status, Zeitpunkt der letzten Aktualisierung. Provider-spezifische Zusatzdaten dürfen separat erhalten bleiben.

## 5. Reihenfolge der Umsetzung
1. Bestehenden eBay-Stand unverändert lassen.
2. Reale idealo-Feedstruktur und Zugang prüfen.
3. Eigenständigen idealo-Adapter bauen.
4. idealo isoliert positiv/negativ testen.
5. eBay + idealo parallel betreiben.
6. Getrennte Provider-Ausgabe fertigstellen.
7. Erst danach optionales Matching eBay ↔ idealo.
8. Gemeinsame Produktkarte mit dynamischen Providerbuttons.
9. Amazon als dritten unabhängigen Provider anbinden.

## 6. Matching-Hardlock
Providerangebote dürfen nur zusammengeführt werden, wenn Produktidentität ausreichend sicher ist. Bevorzugt EAN/GTIN, eindeutige Hersteller-/Modellnummer oder andere belastbare IDs. Nicht ausreichend sind ähnliche Titel, gleiche Kategorie, ähnliche Bilder oder KI-Vermutung. Bei Zweifel getrennt anzeigen.

## 7. idealo-Start
Für idealo wird zuerst der im iPN dokumentierte Product Data Feed geprüft und genutzt, sofern er die benötigten Produktdaten liefert. Keine künstliche API-Konstruktion, solange der Feed die Aufgabe einfacher und belastbar erfüllt. Der Quick Setup Guide dokumentiert außerdem Deeplink-Generator, Creatives und Tracking-Check.

Vor produktiver Implementierung sind anhand des echten iPN-Zugangs zu verifizieren: exakte Feed-Spalten, EAN/GTIN-Abdeckung, automatisierbarer Abrufweg/URL, Authentifizierung, Abruflimits falls vorhanden, Bildnutzungsregeln sowie Tracking-/Deeplinkparameter. Nichts davon darf geraten werden.

## 8. Fehlerprinzip
Ein Providerfehler darf niemals die komplette Produktausgabe stoppen. Kandidaten-/Produktfehler werden lokal protokolliert und übersprungen, sofern dadurch keine falschen Affiliate-Daten veröffentlicht werden. System-, Speicher-, Vertrags- und Identitätsfehler bleiben fail-closed.

## 9. Portalweite Ausgabeoptionen
Die bestehenden Affiliate-Einsatzorte in Beiträgen und Kategorien bleiben erhalten. Später muss je Einsatzbereich konfigurierbar sein: automatisch, nur eBay, nur idealo, nur Amazon, mehrere getrennt oder gemeinsame Produktkarten.

## 10. Drei Produkte sind nicht drei Provider
Die Zielanzahl der Produktkarten und die Zahl der Provider sind getrennte Dinge. Eine Karte darf 1, 2 oder 3 Providerbuttons haben. Es gibt keinen Zwang, pro Produkt alle Provider zu finden. Relevanz und korrekte Zuordnung haben Vorrang.

## 11. Hardlocks
Unzulässig: Umbau des funktionierenden eBay-Providers nur wegen idealo; Monolith aus eBay/idealo/Amazon; zwingende Drei-Provider-Abhängigkeit; falsches Matching; leere Buttons; Gesamtstopp wegen eines einzelnen Providers; Annahmen über nicht dokumentierte idealo-Schnittstellen; unnötige API-Komplexität; Änderungen am Designplugin.

## 12. Zielzustand
Produktquelle → Provideradapter → neutrales Produkt → Ausgabe. Optional darüber: zweifelsfrei identisches Produkt aus mehreren Quellen → eine Karte → nur verfügbare Providerbuttons. Getrennte und gemeinsame Ausgabe müssen dauerhaft parallel möglich sein.
