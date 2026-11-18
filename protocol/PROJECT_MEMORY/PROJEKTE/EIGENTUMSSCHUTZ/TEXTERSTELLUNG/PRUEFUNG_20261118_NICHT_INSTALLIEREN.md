# Hab & Bewahr – Texterstellung: Quellen- und Konzeptprüfung vom 18.11.2026

**Status: NICHT INSTALLIEREN. Keine Livefreigabe.** Die im Chat zuvor ausgesprochene Testinstallations-Empfehlung für 0.4.24 ist fachlich zurückgezogen.

## Nachweis
- 0.4.24 wurde geöffnet: 88 Paketdateien, davon 78 PHP-Dateien; alle PHP-Syntaxprüfungen und alle 8 JSON-Parsingprüfungen bestanden. ZIP CRC bestanden. Das beweist nicht die Funktion des gesamten Artikelablaufs.
- Die angeblich portaleigene Kategoriezuordnung hat 0 Einträge und leeren Prüfhash. Der Originalcode meldet bei tatsächlichem Aufruf PSTE_PORTAL_CATEGORY_MAP_HASH_MISMATCH.
- Hab-&-Bewahr-Kategorievertrag: WP-Seite R1 > R2 > R3 > flache WP-category > Beitrag. Artikelart ist **separat**, keine im Kategorienamen enthaltene Kennung.
- Historischer verifizierter WordPress-Readback 13.10.2026: 285 Kategorien. 0/285 erfüllen den Artikelart-Prefix der Original-PSTE-Erkennung; 0/285 enthalten den R3-Seitennamen als exakte Anfangs-/Endwortfolge. Beispiele: Türen & Fenster -> Mechanik & Zugang, Alarm & Überwachung -> Alarm & Kamera, Camping & Wohnmobil -> Wohnmobil & Wohnwagen. Der tatsächliche PHP-Code erkennt in allen drei Beispielen keinen Typ. Kontrollfall FAQ Reitsattel -> Reitsattel funktioniert. Der Archivstand ist nicht automatisch der heutige WP-Stand.
- Ursprung 0.4.24 hatte Pferde-Gesundheitsregeln für Wurmkur/Tierarzt/Kolik; außerdem wurde PSERC-Originalfehlercode in der Diagnose abgeschnitten. Die getrennte QA-Quelle korrigiert das und meldet fehlende Kategoriezuordnung ausdrücklich; **keine fertige Hab-Kategorieerkennung vorhanden**.
- Zwei PFERDE_ATELIER_WORDPRESS_IMPORT_V1-Nennungen bleiben als historischer technischer Importvertrag in Hauptdatei und PSERC-Original. Nicht blind umbenennen, bevor die tatsächlich aktive K0-Ausgabe umgestellt ist. Die meisten PSTE-/PSERC-Treffer in älteren Rohzählungen sind interne Namen, keine inhaltlichen Pferde-Regeln.
- Unsig­nierte optionale Journal-Erweiterung meldet PSTE_EXTENSION_MANIFEST_MISSING. Das bekannte K0-Multiportal-Quellregister nennt Hab noch nicht. Hier überprüfte alte K0-Regeldatei enthält vier Artikelarten, Hab-Testkopie fünf; aktueller produktiver K0-Stand unbekannt.

## Abgeschlossene QA-Arbeit
Getrennte, NICHT INSTALLIERBARE QA-Quellkopie: genau drei PHP-Dateien geändert (bestehende Risiko-, Diagnose- und Kategoriefehler-Meldestelle), 78/78 PHP-Syntax, 8/8 JSON, 6 Website-Identitätsproben, Importvertragsprüfungen sowie negative/positive PHP-Beispiele. Keine Änderung an echtem WordPress, DataForSEO, K0, Pferdeatelier-Original oder vorhandenem Redaktionsplan. Keine automatische Veröffentlichung.

QA-ZIP und detaillierte Prüfberichte im Hab-Dateibüro: /hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_20261118/.

## Konkrete Weiterarbeit
Der aktuelle WordPress-Kategorie-/R3-Readback mit IDs, aktiver Revision und Besitzer-Zuordnung muss aus dem EINEN vorhandenen Kategorien-Workflow gelesen werden; reiner XML-Export ohne diese Bindung ist nicht sicher ausreichend. An der schon bestehenden Kategorien-/MINI-Entscheidungsstelle Kategorie und Artikelart voneinander trennen, ohne doppelte Entscheidungsstation. Danach vorhandene K0-Fünffeld-Ausgabe für Hab nach aktuell gültigem K0-Portalregister und WordPress-Entwurfsrückimport prüfen. Erst nach echtem Hab-E2E-Test Installations-ZIP. Arbeitszweig und PR #819 bleiben ungemergt.