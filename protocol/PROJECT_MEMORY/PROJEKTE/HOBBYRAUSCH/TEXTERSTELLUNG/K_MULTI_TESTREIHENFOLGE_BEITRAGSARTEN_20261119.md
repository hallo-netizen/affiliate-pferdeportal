# Hobbydepot – Gesamtworkflow, K-Multi, Kategorieanalyse, Beitragsarten (19.11.2026)

**Status: KONZEPT- UND QUELLENABGLEICH, NOCH KEINE ÄNDERUNG AM PLUGIN.** Nutzer verlangt kurze, verständliche, geordnete Reihenfolge, möglichst wenige Artikelarten, KISS und nur einmalige Entscheidung/Prüfung.

## 1. Verifizierter Bestand
- Aktuelle Hobby-Texterstellung: `0.4.24.5`; aktuelle ZIP bereits im zentralen Büro `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip`; unverändert.
- Sichtbarer aktueller WP-Recherche-Screenshot 19.11. 09:45: **379 offene Themenbereiche**, **2241 Artikelkategorien** (alle zugeordnet), **3520 WP-Kategorien insgesamt**, **0 Recherchen/0 gespeicherte Themen**, Recherche ausdrücklich GESTOPPT (manueller Start nötig). Die Zahlen im Screenshot sind KEIN vollständiger Kategorieexport; keine Fake-Analyse von 3520 Einzelknoten.
- Projektkonzept `SEO_KATEGORIEN/KONZEPT_3_SAEULEN_ZIELBAUM_20261007.md` nennt acht CORE-Hobbywelten: **Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**. Fachliche Content-Leaves: Einstieg/Grundlagen, Ausrüstung/Kosten, Techniken/Praxis, Material, FAQ/Probleme, ggf. Vergleich/Pflege/Sicherheit/Projekte – nur wenn konkret vorhanden, KEINE festen Blätter erzwingen.
- Konzept-Magazin nach `.../HD001_V1_14_4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS_20261009.json`: **vier Blöcke**: Hobby finden (Hobbyfinder/Hobbywelten sind Seiten/Funktionen), Nach Situation (Zuhause, Draußen, Alleine, Zu zweit, Wenig Platz, Wenig Zeit), Nach Jahreszeit (Winter, Sommer), Entdecken (Ungewöhnliche Hobbys, Verrückte Hobbys, Neue Hobbys, Trends). Die darunter liegenden realen `journal_cat` sind von der CORE-Taxonomie getrennt; früheres Oktober-Manifest nennt **13 journal_cat**, aktuellen Livebestand nicht vollständig exportiert. **Magazin-Ziel ist stets eine konkrete Magazin-Unterrubrik, niemals pauschal „Magazin“.**
- Ältere Fachprofile sind nicht mit aktueller Live-WordPress-Einzelkategorie-Inventur gleichzusetzen; verbindliche Quelle ist allein der read-only **HD-004**-Snapshot `apkw_target_tree_active_snapshot_v1`. **Der komplette aktuelle HD-004-Readback inklusive Magazin ist vor endgültiger Einzelzuordnung noch ausstehend.** Kein zweiter Baum, keine Neuanlage.

## 2. K-Multi-Status – Quellen widerspruchsfrei getrennt
- Nutzer-Nachbarchat meldete K-Multi/KISS 1.2 **48/48 lokale Tests**, originaler Pferdeatelier-K0-Prüfer eingebunden, keine zweite Textprüfung. Dies war ein **Simulations-/Entwicklungsstand** und kein freigegebener WordPress-Endlauf.
- Direkt verifiziert `hallo-netizen/k0-multiportal`, `main/README.md`: **QUARANTÄNE – KEINE AUSFÜHRUNG, KEIN WORDPRESS-ANSCHLUSS**. Offline-Branch `k0-offline-rule-bindings-20261027`: 121 gemeinsame Katalogregeln, 114 HARD insgesamt, vier Pferdeatelier-Typen (Beratung, FAQ, Pflege, Vergleich), Hobby `state=NO_VALUES_BLOCKED`, **keine eigene Wertetabelle, keine Artikeltypfreigabe/Kategoriebindung/WordPress-Ziel**, `production_enabled=false`. Also **kein produktiver Multi-Switch jetzt**.
- Separat im derzeit aktiven Pferdeatelier-K0-Zweig `konzept0-portal-neutral-20261002`: K0 `READY_FOR_FRESH_K0_START`, `ARTIKELTYPEN/Anleitung.json` ist READY und vier in `RULE_VALUES.json`; **dieser K0-Status überträgt sich nicht automatisch auf Multi**. `K0_PORTAL_REGISTRY.json` nennt Hobby lediglich mit `category_exact=["discgolf-beratung"]` (keine breite Registrierung). Direktes Ankoppeln wäre nicht belastbar.
- Vorhandener MINI-Weg entscheidet **Kategorie, Suchabsicht, Titel, Artikelart EINMAL vor K0**; K0/Multi muss diese Werte unverändert übernehmen und **nur ein einziges Mal** mit dem vorhandenen Qualitätsprüfer prüfen; Import nur als Entwurf. Kategorienamen dürfen **keine** Schreibart automatisch erzwingen.
- Für einen späteren Multi-Wechsel: (a) produktiven, ausführbaren Multi-Runner nachweisen, (b) alle aktuellen CORE- und konkreten Magazin-Slugs eindeutig einem Portal zuordnen, (c) Portal-Textregelwerte/Schreibarten autorisieren (inkl. Prüfung Anleitung und eventuell Inspiration), (d) Original-Übergabeformat und Rückimport aus dem aktuellen WordPress-Plugin unverändert halten oder an **einer** einzigen Brückenstelle minimal anpassen, (e) echter WP→MINI→Multi→Entwurfsimport-Endtest, keine Publikation.

## 3. Kleine und vollständige Artikelarten-Shortlist – fachlicher Vorschlag, noch NICHT freigegeben
**Fünf bewährte Basisarten:** 
1. **Beratung**: Einstieg, Hobby auswählen, Ausrüstung/Kosten, Kauf-/Einstiegsentscheidungen, passende Hobbys für eine Situation.
2. **Anleitung**: Techniken, Materialien anwenden, Projekte/Bauen/Schritte; klare machbare Reihenfolge, benötigte Dinge und relevante Vorsicht.
3. **Vergleich**: echte Alternativen von Material, Methoden oder Ausrüstung anhand einheitlicher Kriterien.
4. **Pflege**: Erhaltung, Wartung, Pflanzen-/Tierhaltung nur fachlich passende regelmäßige Maßnahmen; nicht generisch auf alle Hobbys ausrollen.
5. **FAQ**: eine klar abgrenzbare konkrete Frage/Problemlösung, kein Ersatz für jede schwache Leaf-Kategorie.

**Ein einziger möglicher Zusatztyp für Magazin: „Inspiration“** für ungewöhnliche/neue Hobbys, Entdecken, Trends, Situations-/Saisonideen, mehrere Hobbytipps und echte journalistische Auswahl. Muss erst mit vorhandenen Regelblöcken auf **eindeutige Absicht** und Überschneidung zu Beratung geprüft werden. Die Inspirationsartikel sind nicht automatisch nötig, wenn eine Beratung den Suchintent bereits vollständig erfüllt. Keine neue Typ-Freigabe aus Konzepttext allein.

## 4. Fachregeln NUR als Ergänzung, gemeinsame K0-Regeln unangetastet
- **Hobby-Einstieg**: für unbekannte Begriffe zuerst konkret erklären, was man tatsächlich macht; keine künstlichen Floskeln.
- **Praxis/Ausrüstung**: echte Materialien/Schritte, Voraussetzungen, Schwierigkeitsgrad, ggf. Kosten/Sicherheit soweit relevant, keine erfundenen Produkte/Aussagen.
- **Magazin-Inspiration**: welchen konkreten Menschen bzw. welcher Situation/Hobbyauswahl hilft der Beitrag? Nenne reale Hobbys, wann/wo/voraussetzungen, mit belegten Linkzielen; Trends mit zeitlich überprüfbaren Fakten. Kein Werbetext.
- **Eindeutige Zielrubrik**: Magazinartikel in echte Magazin-Unterrubrik, keine Root-Magazin-Ablage. Gemeinsame interne Linkregeln verwenden, nicht neu erfinden.
- **Unterscheidung Artikel vs. Seiten-Text**: bestehende Hobby-SEO-Kategorieleads 45–60 Wörter plus 150–200 Wörter Aufklapptext (`DESIGN/TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`) sind **keine K0-Artikeltypen- oder Artikel-Wortzahlregeln**. Nicht vermischen.
- **Original-K0-Qualitäts-/Recherche-/Sprach-/Linkregeln und Original-Pferdeatelier nicht ändern**; je Portal nur fachlich sinnvolle Zusatzregelwerte, ein Prüfer.

## 5. Ein verbindlicher gestaffelter Testplan
A. **Kategorie-Komplettinventar lesen** (HD-004 read-only, exakt aktueller live Revision-Snapshot mit CORE + Magazin); jedes echte produktive Ziel genau einmal nach Rolle/Schreibintent klassifizieren, keine Kategorien neu erzeugen. Ergebnis: bewiesene Abdeckung der 5(+1) Arten, Lücken sichtbar.
B. **Eine kostenlose Rechercheprobe** in Texterstellung: `Texterstellung → Recherche`, Anzahl **1**, kostenpflichtige DataForSEO-Checkbox **AUS**, bestehender Button `Nächste offene Kategorien recherchieren` (aktuell 3D-Bogenschießen). Auftrags-/Kategorie-/Titel-/Suchbegriff-Abgleich; Ergebnis und Fehler im vorhandenen Bestand kontrollieren. **Nicht jetzt alle 379/2241 starten; keine Kosten ohne Freigabe**.
C. **Eine getrennte Magazinprobe** auf eine real vorhandene Magazin-Unterrubrik, zunächst kostenlos: richtige Fachrubrik und kein generisches „Magazin“ als Ziel.
D. **MINI-/Redaktionsentscheidung prüfen** mit 1 CORE + 1 Magazin, genau eine Fachentscheidung pro Auftragsdatensatz: Suchbegriff, Überschrift, Artikeltyp, Kategorie. K0-/Multi-Schreibproduktionssperre bleibt bis Freigabe.
E. **K-Multi aus eigenem Büro fertig und offline nachweisen:** mindestens 5 bestehende Typen (+ Inspiration nur wenn nötig), Source- und Sprachregeln, eindeutiger Portal/Kategorieschlüssel, unveränderte Endformatierung. Negative Cases inkl. falsche Kategorie, Typkonflikte und Mehrfachprüfung.
F. **Echter End-to-End-Pilot:** vorhandene WP-Texterstellung → MINI → K-Multi → K0-Qualitätsprüfer **einmal** → Original-Rückimport → **WordPress-Entwurf**. Nach bestandener CORE- und Magazinprobe batchweise ausweiten. Keine automatische Veröffentlichung.
**Keine neue Pluginversion als Voraussetzung dieses Konzeptbeschlusses.** Reihenfolge A+B+C+D, dann E, zuletzt F. Alte Pferdeatelier-K0 bleibt in Betrieb und unangetastet.

## Nächster konkreter Nutzerklick (nur bei bewusst gewünschtem Test)
`Texterstellung → Recherche`: Anzahl **1**, Haken „Kostenpflichtige DataForSEO-Recherche“ **aus**, `Nächste offene Kategorien recherchieren` klicken; Rückmeldung muss zunächst gelesen werden. Alternativ zunächst nur **read-only** vollständiges HD004- und Magazin-Inventar als Datenbasis aus dem vorhandenen Kategorie-Plugin ziehen; kein zusätzliches Plugin installieren.
