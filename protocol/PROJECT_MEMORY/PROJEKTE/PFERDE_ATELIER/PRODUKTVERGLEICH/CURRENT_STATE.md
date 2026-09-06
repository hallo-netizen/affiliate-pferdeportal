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


## Architekturprüfung STARTMASTER/TEXT – Revision 2026-09-06

Neue Belege aus dem bestehenden Produktionssystem:
- der aktuelle STARTMASTER0107 ist nur die äußere Steuer-/Sicherheitskette um einen wesentlich größeren Fachworkflow;
- allein unter `control/startmaster0107/` wurden zwischen 2026-08-29 und 2026-09-05 306 Commits gezählt;
- die aktuelle Hobbyraum-Regressionmatrix führt M01–M33 als bekannte historische Fehlerklassen;
- der produktive Ablauf bindet SEO-Metadaten, Plan-Slots, Fachworkflow, Fact-Pack, Textmaschine, PPM 6.7.9, PSERC, PSTE, Duplicate-/Cannibalization-, SEO-, Design- und Publish-Safety-Stufen;
- die aktuelle saubere Vorproduktionsschnittstelle ist absichtlich auf exakt fünf Metadatenfelder beschränkt: title, target_keyword, category, article_type, plan_slot;
- ein historischer Liveversuch vom 2026-08-02 zeigte bereits, dass extern vorbereiteter Artikelinhalt/Fact-Pack in der bestehenden Produktionskette eine Architekturverletzung und Format-/Designfehler verursachen kann;
- plan_slot und article_type sind im bestehenden PPM-/Redaktionsplan fest gebunden; neue freie Produktvergleichsartikel würden daher keine wirklich lose Übergabe darstellen, sondern erneut tief in PSERC/PPM/PSTE/SEO eingreifen.

### Revidierte KISS-Empfehlung

**Produktvergleich soll vorerst NICHT an STARTMASTER/TEXT als Laufzeit-Abhängigkeit gekoppelt werden.**

Stattdessen wird als bevorzugte V1-Architektur geplant:

**eigenständige Produktvergleichsstraße**
1. Produktkandidaten finden;
2. sinnvolle Vergleichspaare prüfen;
3. Hersteller-/Primärquellen recherchieren;
4. Faktendossier bilden;
5. eigener kleiner Product-Compare-Writer erzeugt Artikel;
6. eigene produktspezifische Qualitätsprüfung;
7. WordPress-DRAFT erzeugen;
8. exakte Produktidentitäten als strukturierte Post-Metadaten speichern;
9. vorhandene AFFILIATE-Zentrale liest diese Identitäten für Kaufquellen.

### Textmaschinen-Wiederverwendung

Nicht den kompletten STARTMASTER-/PSERC-/PPM-/PSTE-Workflow klonen.

Zulässig und zu prüfen:
- bewährte Schreib-/Struktur-/Formatregeln der vorhandenen Textmaschine als Referenz übernehmen;
- falls technisch sauber isolierbar, nur einen kleinen stabilen Schreibkern forken/einfrieren;
- falls der vorhandene Code zu stark gekoppelt ist, Verhalten/Regeln neu und klein implementieren statt Abhängigkeiten mitzuschleppen.

Ziel: **Verhalten wiederverwenden, Altarchitektur nicht duplizieren.**

### Kategorien

Das allgemeine Kategoriemodul ist für dieses Vorhaben ausdrücklich NICHT vorgesehen.

Die Produktvergleichs-Engine bekommt eine eigene minimale Kategorie-Konfiguration:
- projektunabhängiger Kern kennt nur category_path/category_key;
- Pferde-Atelier-Profil definiert die konkrete Produktvergleichsstruktur;
- Einrichtung/Import der eigenen Produktvergleichskategorien ist Teil des einmaligen Produktvergleichs-Setups, keine dauerhafte externe Kategorie-Schnittstelle.

### SEO

SEO ist für die fachliche Vergleichsrecherche **keine Pflichtabhängigkeit**.

SEO kann optional verwendet werden für:
- Nachfrage/Priorisierung von Vergleichsideen;
- Keyword-/Titelwahl;
- Dubletten-/Kannibalisierungsprüfung;
- spätere Optimierung.

Ausfall oder Nichtverfügbarkeit des SEO-Tools darf die faktische Recherche und Artikelerstellung nicht blockieren.

### Externe Laufzeitschnittstellen V1

Ziel: maximal eine zwingende fachliche Laufzeitschnittstelle.

1. **AFFILIATE** – Exact-Product-Kaufquellen über stabile Produktidentitäten.

Alle anderen Aufgaben sollen innerhalb des Produktvergleichsmoduls liegen oder optional/offline angebunden werden.


## Nachprüfung WISSEN/JOURNAL-Erweiterungsarchitektur – 2026-09-06

Der frühere Journal-Umbau verändert die Architekturentscheidung wesentlich.

Belegt:
- Journal/Wissen verursachte im August reale Rootcause-Arbeit.
- Danach wurde eine allgemeine additive Article-Type-Extension-Schnittstelle aufgebaut.
- PSERC 0.28.2 dokumentiert ausdrücklich: bestehender Workflow und Textmaschine bleiben tabu; Journal darf nur additiv über eine signierte/versionierte Extension-Schnittstelle angebunden werden.
- Core-Typen FAQ/Beratung/Vergleich/Pflege und Extension-Typen wurden nach einem Journal-bedingten Global-Gate-Fehler wieder allgemein getrennt.
- Eine zusätzliche synthetische Beitragsart (`SyntheticProbe`) wurde als additive Extension positiv geprüft, ohne Core-Support zu verändern.
- Aktuelle Metadaten-Snapshots führen weiterhin `article-type-extension-registry.php`, ein signiertes `article-type-extension-manifest-v1` und einen separaten Journal-Release.
- Journal wird aktuell extern als `Journal` geführt und intern über die bestehende Legacy-Art `Wissen` gebridged.
- Der produktive Übergabevertrag bleibt exakt fünf Felder breit: title, target_keyword, category, article_type, plan_slot. Die Textmaschine bleibt alleinige Content-/Format-Autorität.

### Konsequenz für Produktvergleich

Die Aussage aus PV-PLAN-003, eine STARTMASTER/TEXT-Laufzeitkopplung grundsätzlich zu vermeiden, ist nach diesem neuen Beleg **nicht mehr als bevorzugte Endentscheidung belastbar**.

Neuer Stand:
**ARCHITEKTURWEG OFFEN – EXTENSION-FIRST-FEASIBILITY-TEST.**

Zu prüfen ist zuerst, ob `Produktvergleich` als vollständig additive Beitragsart über die vorhandene Extension-Tür aufgenommen werden kann:
- keine Änderung der Core-Textmaschine;
- keine Erweiterung des 5-Felder-Handoffs;
- keine Änderung bestehender Typen;
- keine neue Runner-/Gate-/Signer-Architektur;
- idealerweise Bridge auf vorhandene interne Vergleichsstruktur, falls fachlich passend;
- bestehende FAQ/Beratung/Vergleich/Pflege/Journal müssen byte-/verhaltensgleich bleiben.

Nur wenn dieser Test klein und isoliert PASS ist, wird die gemeinsame Textproduktion wieder bevorzugt.
Wenn dafür Core-Umbauten, zusätzliche Handoff-Felder oder breite PSERC/PPM/PSTE-Eingriffe nötig werden, fällt die Entscheidung zurück auf die eigenständige Produktvergleichsstraße.

### Noch offene Kernfrage

Die Extension-Schnittstelle löst noch nicht automatisch die Frage, wie die **exakten Produktidentitäten A/B und ihre geprüften Herstellerfakten** ohne neue gefährliche Payload-Schnittstelle in die bestehende Recherche-/Textproduktion gelangen.

Genau diese Datenfrage ist der nächste Architekturprüfpunkt.
