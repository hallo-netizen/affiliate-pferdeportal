# HOBBYRAUSCH – HRD SCOPE13 IMAGE REPAIR

STAND: 2026-10-16
STATUS: **13/13 REPAIR PASS / HARD SCOPE / KEINE ANDEREN KATEGORIEN ANGEFASST**

## Harte HRD-Regel
Ausschließlich diese 13 Kategorien durften geändert werden:
1. Druck & Fotografie
2. Oberfläche & Dekoration
3. Genuss
4. Metall
5. Schmuck
6. Funk
7. Smart Home
8. Zucht & Futtertiere
9. Gehegegestaltung
10. Geschick & Tricks
11. Team & Wettkampf
12. Rollen & Balance
13. Wurf & Ziel

Alle anderen Kategorien: **FINGER WEG**.

## Vorgehen
Vor Neugenerierung wurden die älteren Bildstände geprüft. Ergebnis: keine neue Bildgeneration nötig.

Wiederverwendete frühere gute Vollquellen:
- Druck & Fotografie
- Oberfläche & Dekoration
- Genuss
- Metall
- Schmuck
- Funk
- Smart Home

Gezielt auf ältere bessere 1.50.625-Bilder zurückgesetzt:
- Zucht & Futtertiere: Futterinsekten/Mehlwürmer statt Bienen-/Waben-Dopplung
- Gehegegestaltung: eigener Habitat-Ausschnitt, nicht identisch mit Terraristik

Gezielt auf den besseren WIP-1.50.653-Bildstand zurückgesetzt:
- Geschick & Tricks
- Team & Wettkampf
- Rollen & Balance
- Wurf & Ziel

Keine Collage als Releasequelle verwendet.

## Visuelle Prüfung
Hero- und Preview-Ableitungen aller 13 Kategorien geprüft:
- Hero: 600×320
- Preview: 200×107
- semantisch passend;
- kein falsches Technikbild bei Metall;
- Schmuck wieder Schmuckwerkstatt;
- Funk wieder Funkstation;
- Smart Home wieder Smart-Home-Szene;
- Genuss wieder Brot/Käse/Küche;
- Zucht & Futtertiere nicht mehr Bienenbild;
- Gehegegestaltung nicht identisch mit Terraristik;
- Geschick/Team/Rollen/Wurf wieder passende Bewegungs-/Zielmotive.

Perzeptive Kollisionskontrolle:
- Zucht & Futtertiere ↔ Imkerei/Bestäuber: dHash-Distanz 128
- Gehegegestaltung ↔ Terraristik: dHash-Distanz 134
- keine exakten Scope13-Hero-Dubletten.

## Plugin-Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HRD_SCOPE13_REPAIR_LOCALPASS.zip`

SHA-256:
`d32805e2747f9df25e722efc7242f4df820bd273f19db2e2b8b97e5b249e1bf4`

Basis:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_NEW_IMAGES_30_VISUALPASS.zip`
SHA-256:
`cbc9789925660ada90a32e1d9726c4b6086c9d8308a8d097009573afab66ddc8`

## 1:1-Simulation
PASS:
- exakt **26 Dateien geändert** = 13 Heroes + 13 Previews;
- **0** Dateien hinzugefügt;
- **0** Dateien entfernt;
- alle übrigen Dateien byte-identisch;
- damit auch der komplette neue 30er-Bildstand unverändert erhalten;
- Mapping byte-identisch;
- **55/55 PHP-Dateien byte-identisch**;
- **55/55 PHP-Syntax PASS**;
- ZIP-Roundtrip PASS.

QA:
`/hobby rausch/releases/HOBBY_DEPOT_HRD_SCOPE13_REPAIR_QA.json`

Release:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HRD_SCOPE13_REPAIR_LOCALPASS.zip`

## NEXT ACTION
Nur Live-Readback dieser 13 Kategorien. Bei einem sichtbaren Fehler ausschließlich die betroffene Kategorie innerhalb dieses HRD-Scope ändern. Alle anderen Kategorien bleiben gesperrt.
