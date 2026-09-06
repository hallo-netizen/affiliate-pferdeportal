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


## Büro-Zuständigkeit – Produktvergleich ↔ TEXT/SEO

Fachliche Autorität bleibt im Büro PRODUKTVERGLEICH:
- Definition der neuen Beitragsart `Produktvergleich`;
- Abgrenzung zum bestehenden allgemeinen Beitragsart-Typ `Vergleich` (Produktgruppen-/Bauartenvergleich);
- eigene Produktvergleichs-Textregeln;
- Kategorien-/Kategorieebenen-Anforderung für Produktvergleiche;
- Produktfindung und Pairing-Regeln;
- Recherche-/Quellen-/Faktenregeln;
- gewünschter Übergabevertrag;
- Abnahmekriterien für die spätere technische Anbindung.

TEXT/SEO ist nur technische Umsetzungsautorität für Änderungen innerhalb des bestehenden Text-/SEO-Produktionssystems:
- Article-Type-Extension registrieren;
- typbezogene Struktur-/Titel-/Textregeln technisch anbinden;
- PPM/PSERC/PSTE-/Plan-Slot-/Kategorie-Bridge nur soweit zwingend nötig;
- Regression beweisen: bestehende Typen unverändert.

AFFILIATE bleibt technische Autorität für Kaufquellen/Produktkarten.

Regel gegen Zuständigkeitskonflikte:
**Fachanforderung wird im PRODUKTVERGLEICH definiert; betroffener Fremdbereich implementiert ausschließlich gegen diesen klaren Vertrag in seinem eigenen Büro.**
Keine parallelen Writes desselben technischen Bereichs und keine Kopie fremder CURRENT_STATE-Wahrheit.

Aktuell wird TEXT/SEO nicht verändert: dessen Hobbyraum ist mit einem anderen aktiven Reparaturauftrag gebunden und Textmaschinen-/Fachregeländerungen sind dort derzeit gesperrt.


## Campus-Queraudit – bisherige Integrationsprobleme und Muster

Stand: 2026-09-06.

Für die Architekturentscheidung Produktvergleich wurde das Pferde-Atelier-Gebäude plus allgemeine Bausteine, TEXT-Fehlerquellen, Journal/Wissen-Rootcause und Kategoriemodell quer geprüft.

### Belastbare Muster

1. **Allgemeiner Kern + Projektkonfiguration** ist ein bereits mehrfach genutztes Campus-Prinzip:
   Bildzentrale, Universal Design und Universal Research & Fill trennen allgemeinen Modul-Kern von Pferde-Atelier-Konfiguration/Projektgeschichte.

2. **Single Writer / klare Fachgrenzen** sind eine zentrale Campus-Hardrule.
   Cross-Office-Lesen ist erlaubt; technische Änderungen gehören ausschließlich in den zuständigen Fachbereich.

3. **Tiefe Cross-Core-Integration war historisch risikoreich.**
   Die erste Journal/Wissen-Integration wurde direkt in PSTE, PSERC und PPM hart verdrahtet. Dokumentierte Folgen waren u. a. falsche Typ-/Kategoriezuordnung, selbstbestätigende Evidenz, globale Invalidierung großer Bestände, Rebuild-/Timeout-Probleme und falsche PASS-Zustände.

4. Die spätere **additive Article-Type-Extension** repariert diese Architekturverletzung.
   Sie ist aber kein trivialer Ein-Datei-Anschluss: PSTE, PSERC und PPM konsumieren ein gemeinsames signiertes Manifest; neue Typen benötigen eigene Scope-/Intent-/Kategorie-/Plan-Slot-Bindungen und vollständige Regression.

5. **Journal-Extension erzeugt keine WordPress-Kategorien.**
   Der PSTE-Extension-Router arbeitet read-only, sucht bereits existierende Kategorien via WordPress-Term-API und blockiert bei NOT_FOUND/AMBIGUOUS. PSERC prüft die reale Kategorie ebenfalls nur read-only und verlangt zusätzlich einen registrierten/signed Plan-Slot.
   Damit sind reale Kategorieanlage und Article-Type-/Redaktionsplan-Registrierung zwei getrennte Aufgaben.

6. Das allgemeine **Kategoriemodell** ist technisch eigenständig und umfangreich.
   Es besitzt einen 14-stufigen Research-/Freigabeworkflow und eine lange R2–R10-Fehler-/Rootfixhistorie. Sein aktueller V1.8.0-Stand ist lokal/fresh stark geprüft, echter Live-WordPress-Deployment-PASS aber ausdrücklich noch nicht belegt.
   Für eine einzelne Produktvergleichs-Kategorie-/Ast-Aufgabe wäre seine vollständige Einbindung deshalb nicht automatisch KISS.

7. Der heutige TEXT-Produktionsweg zeigt weiterhin hohe Kopplungsempfindlichkeit an Übergaben:
   Kategorieidentität, Plan-Slot, Exact-Five-Handoff, PPM-Reihenfolge und Worker-/Context-Bindung waren reale wiederkehrende Fehlerquellen.
   Diese Probleme entstanden nicht primär in der Textformulierung, sondern an technischen Übergabe-/Kontrollgrenzen.

### Konsequenz für die Entscheidung

Die frühere Hypothese `Produktvergleich -> interner Vergleich` wird nicht als bevorzugter Shortcut behandelt.
Der bestehende Typ `Vergleich` bleibt fachlich der allgemeine/symmetrische Vergleichspfad; Produktvergleich benötigt eigene, strengere Herstellerfakten-/Quellen-/Neutralitätsregeln.

Wenn eine TEXT-Integration später gewählt wird, dann ausschließlich als **eigene additive Beitragsart mit eigenem Vertrag**, nicht als stilles Umdeuten des bestehenden Typs `Vergleich`.

Parallel bleibt die eigenständige universelle Engine eine starke KISS-Option:
allgemeiner Produktvergleichs-Kern + Pferde-Konfiguration + eigener begrenzter Kategorieast + optionale SEO-Schnittstelle + Affiliate-Schnittstelle.


## Eingefrorene Bild-/Grafikregel für Produktvergleiche – 2026-09-06

Für Produktvergleichsartikel gilt als verbindlicher Konzeptstand:

1. **Kein echtes Produktfoto als automatisch erzeugtes Beitrags-/Teaserbild.**
   Herstellerbilder, Google-Bilder, Screenshots oder nachgebildete konkrete Produktfotos werden dafür nicht manuell übernommen.

2. **Beitragsbild = eigene neutrale Vergleichsgrafik.**
   Sie wird automatisch aus einem festen, projektkonfigurierbaren Grafikvertrag erzeugt, z. B. Vergleichssymbol, Produkt-A-/Produkt-B-Bezeichnung, neutrale Produkttyp-Symbole sowie Portal-Farben/-Typografie. Keine Herstellerlogos und keine markengetreuen Produktabbildungen als notwendiger Bestandteil.

3. **Echte Produktbilder bleiben Aufgabe der AFFILIATE-Ausgabe.**
   Sie dürfen im Artikel nur aus der dafür vorgesehenen Affiliate-/Produktquelle erscheinen. Produktvergleich kopiert oder speichert dafür keine fremden Produktbilder als eigenen dauerhaften Bildbestand.

4. **Prozessmuster aus DESIGN wird übernommen, nicht dessen Inhalte.**
   Der geprüfte DESIGN-Stand zeigt einen zentralen strukturgebundenen Iconkatalog mit 329 Zuordnungen, eigenem Asset-Ordner, deterministischer Zuordnung und Fail-closed-Verhalten bei fehlender/ungültiger Zuordnung. Dieses Produktionsprinzip ist Referenz für den Produktvergleich.

5. **Keine Übernahme bestehender Pferde-Icons/-SVG-Geometrien.**
   Weder Motive noch konkrete Icon-Dateien oder deren inhaltliche Zuordnungen werden kopiert. Wiederverwendet wird ausschließlich das technische Prinzip: standardisierte Erzeugung → eigener Asset-Bestand → eindeutiger Schlüssel → deterministische Ausgabe → Fail-closed.

6. **Produktvergleichs-Zuordnung:**
   Jeder Vergleich erhält eine stabile `comparison_id`. Die erzeugte Grafik wird genau dieser ID zugeordnet, z. B. `PV-00017 -> pv-00017.svg`.

7. **Fail-closed:**
   Fehlt die korrekte Vergleichsgrafik oder stimmt ihre Bindung nicht, wird keine Grafik eines anderen Vergleichs und kein nur ungefähr passendes Ersatzmotiv eingesetzt. Im Zweifel erscheint kein Beitragsbild, bis die korrekte Grafik erzeugt ist.

8. **Allgemeingültigkeit:**
   Der Grafikgenerator soll nach Möglichkeit als kleiner allgemeingültiger Baustein konzipiert werden. Pferde-Atelier liefert nur Stil-/Projektkonfiguration; der Kern darf nicht auf Pferdeprodukte fest verdrahtet sein.

Ziel: copyright-arm, reproduzierbar, einheitlich, automatisierbar und unabhängig von der Lebensdauer fremder Produktbilder.


## Eingefrorenes Vergleichs-Kategorie-/Archivkonzept – 2026-09-06

Für jede konkrete Produktgruppe gilt als verbindlicher Konzeptstand:

1. **Nur eine sichtbare Vergleichskategorie.**
   Beispiel: `Reitstiefel -> Vergleich`, `Pferdeanhänger -> Vergleich`.

2. **Drei fachlich getrennte Vergleichstypen leben unter diesem einen Dach:**
   - Produktgruppenvergleich;
   - Produktvergleich;
   - Variantenvergleich.
   Jeder einzelne Vergleich ist ein eigener WordPress-Beitrag.

3. **Technisch bleiben die Typen strikt unterscheidbar.**
   Gemeinsame Kategorie bedeutet keine gemeinsame Text-/Faktenlogik. Der Beitrag trägt einen eindeutigen Vergleichstyp, sodass Darstellung, Textregeln, Suche, Verlinkung und Monetarisierung getrennt steuerbar bleiben.

4. **Eigenes universelles Vergleichs-Archivtemplate.**
   Die normale WordPress-Kategorieausgabe wird für diese Vergleichskategorien durch eine eigens definierte Vergleichsdarstellung ersetzt.

5. **Prominente Hauptfilter oben:**
   `Alle | Produktgruppenvergleiche | Produktvergleiche`.
   Variantenvergleiche gehören zur konkreten Produktentscheidungswelt und werden innerhalb der Produktvergleichsansicht klar als `Variantenvergleich` gekennzeichnet bzw. über einen zusätzlichen Unterfilter `Produkte | Varianten` erreichbar gemacht.

6. **Produktnavigation nur aus real vorhandenen Vergleichsinhalten.**
   Seitlich auf Desktop werden nur konkrete Produkte aufgeführt, zu denen mindestens ein Produkt- oder Variantenvergleich vorhanden ist. Bei vielen Produkten: `Weitere anzeigen` und/oder ein eigenes AJAX-Produktsuchfeld.

7. **Produktsuche durchsucht beide konkreten Welten.**
   Suche nach einem Produkt liefert sowohl Produktvergleiche als auch Variantenvergleiche, in denen dieses Produkt vorkommt. Treffer werden sichtbar nach Typ gekennzeichnet.

8. **Mobil andere Navigation statt Sidebar-Zwang.**
   Desktop darf eine Shop-artige Produktnavigation links oder rechts erhalten. Mobil wird diese nicht als lange Seitenleiste übernommen, sondern kompakt über Suchfeld und aufklappbare Produktliste/Drawer zugänglich gemacht.

9. **Verlinkungs-Hardrule Produkt <-> Variante.**
   Existiert zu einem Produkt in einem Produktvergleich ein passender Variantenvergleich, muss der Produktvergleich im Text ausdrücklich darauf hinweisen und intern darauf verlinken. Der Variantenvergleich verlinkt zurück auf den passenden Produktvergleich, sofern vorhanden.

10. **Keine zusätzliche Varianten-Kategorieebene.**
    Variantenvergleich bleibt eigener Beitrag unter derselben Vergleichskategorie. Die optische Trennung erfolgt im Template, nicht durch noch tiefere WordPress-Kategorien.

Zielbild: eine zentrale, shopartig nutzbare Vergleichswelt pro Produktgruppe, ohne die fachlichen Vergleichstypen technisch zu vermischen.


## Gemeinsame Produktrecherche als Faktenbasis für Vergleich und Beratung – 2026-09-06

Verbindlicher Konzeptstand:

1. **Produktrecherche ist keine Beitragsart.**
   Sie erzeugt belastbare, quellengebundene Produktfakten zu konkreten Produkten und Varianten.

2. **Dieselbe Produktfaktenbasis darf mehrfach genutzt werden.**
   Sie kann insbesondere Produktvergleich, Variantenvergleich und Beratungsbeiträge versorgen, damit Herstellerdaten nicht mehrfach unabhängig recherchiert werden müssen.

3. **Beratung beantwortet Bedarfsfragen, nicht Modellfragen.**
   Beispiel: `Welche Reitstiefel eignen sich für breite Waden?` Die Beratung darf aus verifizierten Produktmerkmalen passende konkrete Modelle als Beispiele bzw. passende Optionen ableiten. Ein konkretes Modell wird dadurch nicht selbst zur Beratungsart.

4. **AFFILIATE bleibt Commerce-Schicht, nicht fachliche Eignungsautorität.**
   AFFILIATE darf verfügbare Kaufangebote/Produktkarten zu bereits fachlich passend bestimmten Produkten liefern. Es soll nicht allein aus Händlerdaten entscheiden, welches Produkt für einen Bedarf wie `breite Waden` fachlich geeignet ist.

5. **Saubere Aufgabenverteilung:**
   - Produktrecherche: Was ist das Produkt, welche belastbaren Eigenschaften hat es?
   - Beratung: Welche Eigenschaften/Produkte passen zu welchem Bedarf?
   - Produktvergleich: Welche konkreten Konkurrenzprodukte unterscheiden sich für eine Kaufentscheidung wie?
   - Variantenvergleich: Welche kaufrelevanten Ausführungen desselben Modells unterscheiden sich wie?
   - Affiliate: Wo ist das exakt bestimmte Produkt aktuell kaufbar und wie wird es korrekt monetarisiert?

6. **Mögliche Kopplung ohne Vermischung:**
   Ein verifiziertes Bedarfsmerkmal wie `für breite Waden geeignet` darf als strukturierte fachliche Zuordnung aus Produktrecherche/Beratung an AFFILIATE weitergereicht werden. AFFILIATE materialisiert daraus nur passende aktuelle Kaufangebote; es erfindet die fachliche Eignung nicht selbst.

Ziel: einmal sauber recherchieren, mehrfach nutzen; Fachentscheidung und Kaufquelle bleiben getrennt.


## Eingefrorene Richtung Produktregal ↔ Affiliate – 2026-09-06

Verbindlicher Konzeptstand:

1. **Zentrale fachliche Hauptquelle ist das Produktregal / Produktwissen.**
   Dort liegen eindeutig identifizierte, recherchierte und quellengebundene Produkte/Varianten mit ihren belastbaren Herstellerfakten.

2. **Inhalte werden aus dem Produktregal abgeleitet.**
   Beratung, Produktvergleich und Variantenvergleich wählen ihre fachlich passenden Produkte aus dieser Faktenbasis aus.

3. **Affiliate bestimmt nicht die fachliche Vergleichsauswahl.**
   Amazon, eBay, idealo, Awin und andere Commerce-Quellen dürfen nicht allein entscheiden, welche Produkte verglichen oder als passend empfohlen werden. Händlerbestand und Monetarisierbarkeit sind keine fachliche Eignung.

4. **Hauptrichtung:**
   `Produktregal/Faktenbasis -> Inhalt -> Affiliate-Exact-Match -> Kaufangebote`.

5. **Affiliate gleicht anschließend exakt ab.**
   Für die im Artikel fachlich ausgewählten Produktidentitäten prüft die Affiliate-Zentrale, ob exakt passende Angebote in ihren angeschlossenen Quellen vorhanden sind. Exact Match vorhanden = Kaufangebot möglich. Kein Exact Match = kein Ersatzprodukt; der fachliche Artikel bleibt gültig.

6. **Affiliate darf Kandidaten entdecken, aber nicht freigeben.**
   Neue Produkte aus Affiliate-Feeds/-Quellen dürfen als Recherchekandidaten in das Produktregal gemeldet werden. Erst nach eindeutiger Identifikation und Hersteller-/Primärquellenrecherche werden sie für Beratung oder Vergleiche freigegeben.

7. **Kein stiller Rückwärtsfluss.**
   Kurzfristige Händlerverfügbarkeit, Provision oder Angebotsdichte darf nicht nachträglich Fakten, Eignung oder Vergleichspaarung verändern.

Kurzform: **Affiliate darf entdecken. Produktrecherche entscheidet. Affiliate monetarisiert.**
