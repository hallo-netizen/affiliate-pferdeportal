# Pferde Atelier – Parent-Topic-Gap Umsetzung

Stand: 2026-09-22

## Ziel
Fünf bestätigte kaufnahe Parent-Topic-Gaps ohne Architekturumbau schließen:

1. Sattel -> Hub sichtbar: "Sattel & Zubehör" -> neuer Knoten: "Pferdesättel"
2. Trensen & Gebisse -> Hub bleibt -> neuer Knoten: "Trensen"
3. Offenstall -> Hub bleibt -> neuer Knoten: "Offenstallbau"
4. Paddock -> Hub bleibt -> neuer Knoten: "Paddockbau"
5. Reitplatz -> Hub bleibt -> neuer Knoten: "Reitplatzbau"

Boxen & Türen ausdrücklich ausgeschlossen.

## Harte Regeln
- KISS, kein neuer Architekturpfad.
- Bestehende IDs, Inhalte und URLs möglichst erhalten.
- Keine Blindänderung an Slugs.
- Keine Änderung bestehender Artikel.
- Keine Änderung der aktuell exportierten 16 Artikel.
- Keine automatische Massenvermehrung von Artikeltypen.
- Nur neue Artikeltypen, die je neuer Familie fachlich sinnvoll sind.
- Keine Freigabe eines Redaktionsplans gegen einen alten Portalstruktur-Hash.

## To-do / Prüfliste

### 1. Ist-Bestand und Kollisionsprüfung
- [ ] exakte Parent-ID und Parent-Slug je der fünf Fälle bestätigen
- [ ] vorhandene direkte Kinder je Parent bestätigen
- [ ] vorgeschlagene neue Namen gegen bestehende Seiten/Kategorien prüfen
- [ ] vorgeschlagene Slugs gegen bestehende Seiten/Kategorien prüfen
- [ ] bestehende Links/Artikelzuordnungen der Parents prüfen
- [ ] festlegen, welche Parent-Namen sichtbar geändert werden und welche nicht

### 2. Allgemeingültige Kategorie-Workflow-Regel
- [ ] PARENT_TOPIC_GAP als echte Prüfregel in den Kategorie-Workflow integrieren
- [ ] Positivfälle testen
- [ ] Negativfälle testen: Decken, Hufe, Boxen & Türen, Halfter & Stricke
- [ ] kein automatisches Schreiben allein aufgrund der Erkennung

### 3. Delta für Pferde Atelier
- [ ] exakt fünf neue Produkt-/Themenknoten planen
- [ ] bestehende Kinder unangetastet lassen
- [ ] benötigte Artikeltypen je neuem Knoten festlegen
- [ ] Delta gegen Live-Bestand prüfen
- [ ] Rollback-/Readback-Nachweis vorbereiten

### 4. Design / Kacheln
- [ ] prüfen, dass neue direkte Unterseite automatisch als Hub-Kachel erscheint
- [ ] prüfen, dass neue Artikelkategorien auf der neuen Produktseite automatisch als Kacheln erscheinen
- [ ] keine Sonderlogik im Template-Kit nötig
- [ ] visueller Positiv-/Negativtest

### 5. Kategorietexte
- [ ] für jede neue Seite Kategorietext über vorhandenen PFTK-Kategorietextpfad erzeugen
- [ ] Parent-Hubtext nach neuer Struktur neu erzeugen/prüfen
- [ ] keine manuellen Alttexte überschreiben
- [ ] fachliche/SEO-Prüfung

### 6. Affiliate-Zentrale / Portalstruktur
- [ ] Portalstruktur-Katalog um fünf neue Produktziele ergänzen
- [ ] Sollzahlen/Hashes neu erzeugen
- [ ] Affiliate-Klassifizierung gegen neue Ziele testen
- [ ] keine bestehenden Produktziele umleiten

### 7. PSTE / Themenengine
- [ ] frischen Portalstruktur-Snapshot erzeugen
- [ ] neue topic_family/head_intent-Ziele erkennen
- [ ] bisherige STRUCTURE_GAP-Kandidaten erneut gegen neue Struktur prüfen
- [ ] positive und negative Routingtests je Familie

### 8. PSERC / Redaktionsplan
- [ ] Redaktionsplan aus frischer Struktur neu erzeugen
- [ ] portal_structure_registry_sha256 muss aktuellem Struktur-Hash entsprechen
- [ ] alter Hash -> BLOCKED
- [ ] neue Keywords/Themen müssen in neue Familien routbar sein
- [ ] bestehende plan_slots/Artikel nicht verändern

### 9. Endtest
- [ ] kompletter lokaler Positiv-/Negativlauf
- [ ] Einzelfalltest
- [ ] Mehrfach-/Batchtest
- [ ] WordPress-Readback
- [ ] Design/Kacheln/Text/SEO/Redaktionsplan zusammen prüfen
- [ ] erst danach Live-Freigabe
