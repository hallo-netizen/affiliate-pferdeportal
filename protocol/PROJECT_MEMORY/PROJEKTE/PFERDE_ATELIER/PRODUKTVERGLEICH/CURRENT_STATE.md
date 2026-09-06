# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-06
STATUS: PLANUNG AKTIV / ERSTE FACHBASIS EINGELESEN

## AUTORITÄT DIESER DATEI

Diese Datei ist die **einzige aktuelle Campus-Standzusammenfassung dieses Büros**.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- Änderungsgrund → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

Andere Campus-Dateien dürfen diesen dynamischen Bürostand nicht als zweite Wahrheit fortschreiben.

## Aktueller belastbarer Stand

Das Fachbüro **PRODUKTVERGLEICH** ist als eigenes Büro des Pferde-Ateliers eingerichtet.

Seine feste Zuständigkeit ist:
- Produktvergleichs-Konzept;
- konkrete Vergleichsdefinitionen;
- Vergleichseigenschaften;
- Recherche-/Faktendossiers;
- Quellenbindung;
- strukturierte Übergabe an TEXT zur eigentlichen Artikelproduktion.

## Eingelesene erste Fachbasis

Am 2026-09-06 wurden die vom Nutzer bereitgestellten Produktvergleichs-Arbeitsstände geprüft.

Wesentliche Belegbasis:
- `Produktvergleich_UEBERGABE_NACHBARCHAT_68_BEITRAEGE.xlsx`
- `Produktvergleich_Gesamtabschluss_alle_329_Kategorien_FAKTENBEFUELLT.xlsx`
- `Produktvergleich_Gesamtabschluss_alle_329_Kategorien_QUELLENAUDIT.xlsx`
- `Produktvergleich_Ausruestung_Decken_Marktrecherche(1).xlsx`
- `NACHBARCHAT_STARTPROMPT_PRODUKTVERGLEICHE.txt`

Belegt im 68-Beiträge-Paket:
- 17 freigegebene Produktvergleichskategorien;
- 68 konkrete Dossiers / geplante WordPress-Beiträge;
- 102 Produktidentitäten;
- 1.330 Hersteller-Merkmalswerte;
- 58 Dossiers mit deklarierten Lücken;
- 10 Dossiers mit Quellenkonflikten.

Die Recherchebasis trennt bereits sinnvoll:
**Vergleichsdefinition → Produkte → Merkmale → Herstellerfakten → Quellen → Konflikte/Lücken → Produktionsauftrag.**

## Planungsentscheidung V0

Für die weitere Entwicklung gilt als **reversibler Planungsstand**:

**Kein zweites vollständiges TEXT-/SEO-System bauen.**

Stattdessen:
1. eigenes Produktvergleichs-Fachmodul/Plugin für Auswahl, Vergleichslogik, Recherche, Faktenprüfung, Quellen, Konflikte und neutrales fachliches Fazit;
2. standardisierte Übergabe des geprüften Faktendossiers an die bestehende TEXT-/SEO-Produktion;
3. TEXT bleibt für Formulierung, redaktionelle Textregeln, SEO-Gesamtlogik, WordPress-Ausgabe und deren bestehende technische Gates zuständig.

Die Produktvergleichskategorien dürfen neu entwickelt werden. Ihre fachliche Definition kann im Produktvergleichsmodul entstehen; die Artikelproduktion bleibt trotzdem bei TEXT.

## Allgemeingültigkeit

Zielrichtung:
- ein projektunabhängiger Produktvergleichs-Kern;
- Pferde-Atelier nur als Konfiguration/Profil;
- keine Pferdebegriffe, festen Kategorien oder Herstellernamen im Kerncode;
- Quellen-, Merkmal- und Vergleichsregeln müssen konfigurierbar sein.

Allgemeingültigkeit ist **Ziel**, aber noch nicht technisch bewiesen. Bis zum belastbaren Prototyp bleibt die Modulklassifizierung UNGEKLÄRT.

## Fachgrenze

Dieses Büro besitzt keine zweite Textmaschine.

TEXT/STARTMASTER bleibt autoritativ für die eigentliche Artikel-/Textproduktion und deren technischen Produktionsweg.


## Kaufquellen-/Affiliate-Anbindung – Planungsstand

Der Produktvergleich selbst speichert **keine Händlerpreise, Verfügbarkeiten oder Affiliate-Links als dauerhafte Produktfakten**.

Geplante Rollen:
- PRODUKTVERGLEICH liefert die exakte Produktidentität der verglichenen Produkte, möglichst Hersteller + Modell + Variante + belastbare Kennung wie GTIN/EAN/MPN, soweit vorhanden;
- TEXT erstellt den Artikel und bewahrt diese Produktidentitäten als strukturierte Artikel-Metadaten/Übergabedaten;
- AFFILIATE bleibt alleinige Autorität für aktuelle Kaufangebote, Provider, Preis/Verfügbarkeit, Tracking, Disclosure und Produktkarten.

Bestehender Affiliate-Beleg:
Der kanonische Affiliate-Code besitzt bereits Artikelpläne für `post_bottom_products`, Qualitätsprüfung, Deduplizierung, bis zu drei Produktkarten, Tracking und Multi-Provider-Angebote. Für Produktvergleiche soll dieser Renderer wiederverwendet werden.

Geplante minimale Erweiterung:
Produktvergleichsartikel erhalten eine **explizite Exact-Product-Bindung** für Produkt A und Produkt B.
Die Affiliate-Zentrale versucht zuerst exakt diese Identitäten zu materialisieren.
Kein beliebiges ähnlich klingendes Ersatzprodukt darf an deren Stelle erscheinen.

Wenn für ein verglichenes Produkt keine belastbare Kaufquelle vorhanden ist:
- Artikel bleibt gültig;
- keine falsche Produktkarte;
- Kaufquelle für dieses Produkt wird ausgelassen bzw. als nicht verfügbar behandelt;
- Recherchefakten und Artikelinhalt bleiben davon unberührt.
