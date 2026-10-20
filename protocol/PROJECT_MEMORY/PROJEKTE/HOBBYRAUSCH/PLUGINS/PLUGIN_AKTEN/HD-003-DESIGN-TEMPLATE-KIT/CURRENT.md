# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.705 HOBBYFINDER DESIGN LOCAL HARD PASS / LIVE-DESIGN-READBACK OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.705_HOBBYFINDER_DESIGN_LOCALPASS.zip`

SHA-256:
`e56a3b170a888c876ece8e60969be52746a4245b464946d7af1912bc7eb067e5`

Größe:
58,685,530 Bytes.

## Basis

- direkte Basis: **1.50.704**;
- stabile Klasse bleibt `Hobby_Depot_Profile_V150699`;
- Finder-Datenlogik und Ranking unverändert;
- HD-007 bleibt einzige read-only Hobbyregister-Laufzeitquelle;
- keine zweite Hobby-Datenhaltung;
- Kategorie-/Affiliate-/Footer-/SEO-Struktur unverändert.

## Live-Baseline 1.50.704

Nutzer-Readback 2026-10-20:
- HD-007 + HD-003 1.50.704 installiert;
- ursprüngliche WordPress-Seite lag unter `/magazin/hobbyfinder/` und wurde deshalb nicht als Finder-Route gerendert;
- Seite auf die vorgesehene Route `/hobbyfinder/` gestellt;
- Finder erschien danach im Frontend;
- kompletter 8-Schritte-Durchlauf inklusive Ergebnisse funktionierte laut Nutzer.

Damit ist die 1.50.704-Funktionalität live grundsätzlich bestätigt. Der nachfolgende Stand 1.50.705 ist ausschließlich Design-/Bildverbesserung.

## Neu 1.50.705

- Finder-Akzent nutzt die bestehende Portal-Farbvariable Grün/Petrol statt der separaten blauen Finder-Farbe;
- aktive Auswahlkarten grün markiert;
- jede Antwortkachel besitzt ein schlichtes semantisches Linien-Icon;
- erster Schritt erhält kompaktes Hero-Bild;
- Hauptüberschrift gekürzt auf **„Finde dein Hobby“**;
- auf allen Finder-Zuständen stehen **„Zur Startseite“** und **„Neu starten“** zur Verfügung;
- Ergebniskarten verwenden vorhandene echte Ziel-/Kategorie-Bilder, wenn über das bestehende Zielobjekt auflösbar;
- fehlt ein reales Bild, wird keine Bild-URL erfunden; neutraler vorhandener Welt-Icon-Fallback;
- echte Ziel-URLs weiterhin ausschließlich über `hd_category_registry_resolve()`.

## Lokale QA 1.50.705

- PHP-Lint: **135/135 PASS**;
- JavaScript Syntax: **PASS**;
- Finder-Runtime-Datensätze: **862/862 PASS**;
- Score-/Ranking-Funktion gegenüber 1.50.704 byte-identisch: **PASS**;
- Antwortoptionen mit Icon-Zuordnung: **41/41 PASS**;
- Kategorie-Bildauflösung Positivtest: **3/3 PASS**;
- nicht auflösbares Ziel: keine erfundene URL und kein erfundenes Bild: **PASS**;
- ZIP-Integrität: **PASS**;
- gegenüber 1.50.704 geändert: Hauptplugin-Version, stabile Profilklasse/Finderbereich, Evidence-Datei.

## ISOLIERTE CAMPUS-ABLAGE

Das Manifest wird auf 1.50.705 aktualisiert.
Eine echte `CURRENT.zip` ist im GitHub-Campus weiterhin nicht vorhanden; keine Pointerdatei als Ersatz anlegen.

## ERSTER OFFENER BLOCKER

**Echter WordPress-/Frontend-Readback von HD-003 1.50.705.**

## EXAKT EINE NEXT ACTION

**HD-003 1.50.705 über die installierte 1.50.704-Version installieren/aktualisieren und danach `/hobbyfinder/` visuell prüfen. HD-007 nicht ändern.**
