# Robotik V84 – Grundlagenrecherche abgeschlossen, 19 Fälle einmalig entschieden

**Stand 15.11.2026 · 16 eigenständige CORE-Typseiten, 3 Magazin/Registerfälle.** Kein weiterer breiter Recherchedurchlauf als Bedingung für den Start.

## Ergebnis

**Vorhandener Fachplan:** 188 WordPress-Seiten, 296 Inhaltskategorien im freigegebenen V62/V77-Soll. Der Nutzer meldete die Kategorien im Frontend als sichtbar; die exakten WordPress-Live-Zählungen und der Abschlussbericht des bisherigen Importes liegen im Chat nicht vor.

**19 neue Fälle:** 16 eigenständig fachlich vertretbare Robotertypen unter **ausschließlich vorhandenen Elternseiten** (keine 9. Hauptwelt, keine neue Zwischenseite), mit **32 getrennten Inhaltsrubriken** (je zwei Rubriken, jeweils mindestens drei verschiedene Artikelrichtungen). **3** Sonderthemen bleiben im Magazin bzw. Roboterregister und erhalten **keine** neue CORE-Kategorieseite.

## Alle 16 endgültigen Typseiten

| Nr. | Gewünschter Pfad unter vorhandener Elternseite | Fundstufe | Forschungs-ID |
|---:|---|---|---|
| 1 | Haushalt › Reinigung › Katzenkloroboter | Produkt | rf142 |
| 2 | Sport › Ballsport › Padel-Trainingsroboter | Produkt | rf148 |
| 3 | Sport › Ballsport › Pickleball-Trainingsroboter | Produkt | rf175 |
| 4 | Pflege › Handrehabilitationsroboter | Produkt | rf176 |
| 5 | Pflege › Zahnpflegeroboter | Produkt | rf177 |
| 6 | Sport › Wander-Exoskelette | Produkt | rf180 |
| 7 | Freizeit › Sandmalroboter | Produkt | rf181 |
| 8 | Sport › Ballsport › Baseball-Wurfroboter | Produkt | rf182 |
| 9 | Freizeit › Spielzeug › Transformationsroboter | Produkt | rf183 |
| 10 | Haushalt › Hausüberwachungsroboter | Produkt | rf143 |
| 11 | Freizeit › Robotische Teleskope | Produkt | rf184 |
| 12 | Sport › Ballsport › Volleyball-Ballmaschinen | Produkt | rf185 |
| 13 | Sport › Ballsport › Cricket-Ballmaschinen | Produkt | rf186 |
| 14 | Sport › Ballsport › Fußball-Trainingsroboter | Produkt | rf187 |
| 15 | Pflege › Massageroboter | Produkt | rf158 |
| 16 | Pflege › Nagelpflegeroboter | Produkt | rf159 |

*Die Kennzeichnung Produkt/Projekt/Idee bezieht sich auf die dokumentierte Gerätefunktion/den konkreten Herstellerfund, nicht auf eine dauerhafte, allgemeingültige Stufe sämtlicher Zukunftsmodelle. Teleskope und Ballmaschinen sind bewusst **Automatisierungs-Randbereiche**; im Text nicht als freifahrende autonome Roboter beschreiben.*

## Die drei bewusst nicht zusätzlich veröffentlichten CORE-Typen

| Fund | Fundstufe | Richtiger Owner | Warum keine weitere Typseite? |
|---|---|---|---|
| **Schminkroboter** | Projekt | Magazin > Forschung / Roboterregister | Ein universitärer Prototyp; keine ausreichend eigenständige etablierte Robotertyp-Landschaft für einen dauerhaft sinnvollen Kategorienzweig. |
| **Roboterkissen** | Produkt | Magazin > Ungewöhnliche Roboter / Roboterregister | Fufuly und motorisch verstellbare Kissen sind unterschiedliche Sondergeräte; keine belastbare gemeinsame Robotertyp-Funktion, um eine Kanonische CORE-Kategorie zu rechtfertigen. |
| **Baustein-Sortierroboter** | Projekt | Magazin > Forschung/Hobbyprojekte / Roboterregister | Reales Entwicklerprojekt, aber noch kein ausgereiftes, allgemein reproduzierbares Serien- oder Baukastenangebot; eine Typseite wäre im laufenden CORE-Baum überzogen. |

**Kein Fund wird gelöscht.** Quellen, Projektstatus, ID und bei Bedarf Magazin-/Registerverweise bleiben im bestehenden zentralen Fachmaster. Es gibt keine spätere automatische erneute Entscheidung über diese 19 Fälle.

## Der einzige endgültige gebündelte WordPress-Nachtrag

**Bestehende Pluginidentität** `robotik-kategorie-workflow`, aktuelle installierbare Version **0.4.14**. `PLUGIN/CURRENT.zip` und `PLUGIN/VERSIONEN/0.4.14.zip` sind identisch; keine zusätzlichen Pluginnamen, Tabellen, Cronjobs oder Google-URLs.

Ablauf nur **nach** gespeichertem, vollständigem alten Gesamtabschluss: WordPress Admin **Robotik Kategorie → Gesamtabschluss (einmalig) → Einmalige 16 Robotertypen + 32 Rubriken**. Dann **eine** explizite Sammelfreigabe für **48** neue Objekte. Der vorhandene V63-Writer erstellt 16 neue Typseiten als Entwürfe und 32 dazugehörige flache WP-Kategorien; im selben Lauf werden die 16 Typseiten **veröffentlicht**. Die drei ausgeschlossenen Magazinthemen werden technisch nicht mitimportiert.

- Originale **188/296** Seiten-/Kategoriekennungen müssen im realen WordPress vorliegen; das Plugin liest den Bestand vor dem Schreiben, ignoriert keine echten Identitätskonflikte und darf nicht einfach die alte Importliste erneut starten.
- Ein unterbrochener Schreibauftrag behält seinen Index; Wiederaufnahme mit **derselben gespeicherten Freigabe**, kein Doppelimport. Falls echte WP-Kollision, sicherer Stopp statt raten.
- Einmalige zusätzliche Änderung statt 16 Einzelläufen. Nach tatsächlichem WordPress-Erfolg theoretisch **204 Seiten und 328 WP-Inhaltskategorien** im Soll. **Diese Zahlen sind keine von ChatGPT gemessenen Live-Zählungen.**
- **Keine Artikeltexte** von diesem Kategorienplugin: K0 bleibt der einzige Textworkflow. Die aus V81 stammenden acht Briefings der beiden ausgeschlossen V80-Typen gehören nicht in die CORE-Artikelproduktion.

## Echte technische Abnahme und Grenze

[GitHub Actions 0.4.14 – SUCCESS](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43712225606) verifizierte:
- Gleichheit der beiden Installations-ZIP-Dateien und **11 PHP-Dateien ohne Syntaxfehler**.
- Erhalt des bisherigen Programms: 227er Originalimport, 104 alte Seiten, 68 neue Seiten, 16+48 alte Fachnachtragsobjekte.
- Der neue 48er Ablauf im **WordPress-Simulationslauf**: **16/16 veröffentlichte neue Seiten und 32/32 eigene Rubriken**, exakte Eltern-/Identitäts-/Slug-Zuordnung, keine Dopplung, alte IDs erhalten, geändertes Manifest stoppt sicher.
- Paketgröße **233147 Bytes**, `sha256=4ef443b7c04cf3abc1f22ab9fd5d2ce675008f30180ddd46896d8b67bd38daa5`.
- **Kein** echtes WordPress-Livestatus- oder Frontend-Test-PASS; das erfordert die Installation durch den Administrator. Eine vorab gemeldete Live-Ansicht der Kategorien ersetzt die technische Einzelabnahme der neuen 48 Objekte nicht.

Die CI-Datei war ein **einmaliger Testauftrag** und wurde wieder entfernt. Das Release-Paket bleibt im GitHub-Büro. Es wurde im aktuellen Chat zusätzlich als direkte ZIP-Datei bereitgestellt.

## Danach Magazin/Glossar/Register/Finder/Anzeigenmarkt

- Magazin **ein gemeinsamer Bereich** mit sechs redaktionellen Rubriken, kein Privat-/Industrie-Doppelmagazin, die drei zurückgestellten Sonderfunde dort behandeln.
- Roboterregister **ein aktueller Modellpilot V2 mit 19 unterschiedlichen Modellen/Projekten** (4 historisch, 15 ergänzt), keine doppelte Typdatenbank.
- Glossar behält seinen bestehenden **558er Begriffs-Pool**, 14 Begriffe genauer klassifiziert: 5 Alias-Owner, 9 eigene Kurzdefinitionen; kein 558-seitiger Leerimport.
- Roboterfinder bleibt **ein gemeinsamer Finder**; 14 Aufgabenfelder als Ideen und 16 quellenbasierte, aber bislang unvollständige Merkmalsprofile, daher keine vorgetäuschte Live-Eignungsprüfung.
- Anzeigenmarkt hat **sieben einfache HivePress-Anbieter-/Angebotskategorien** als Fachkonzept, siehe `../ANZEIGENMARKT/START_HERE.md`, kein zweiter Firmen-/Produktbaum.

Die weiteren Arbeiten sind **Konzept-/Datenarbeit** und wurden nicht direkt in WordPress veröffentlicht. Der nächste technische Gesamtblock sollte zuerst die tatsächlich vorhandenen Module und HivePress-Kategorien live auslesen, bevor irgendeine neue Oberfläche gebaut wird. Kein neues Plugin auf Verdacht.

**Einziger Kategorie-Datenowner:** `RECHERCHE/PRODUKTE_V2_20261108.json`, Feld `category_release_v84`, Rev20. Das Installer-Asset `PLUGIN/V84_SOURCE/assets/robotik-v84-delta.json` ist lediglich die unveränderliche ausführbare Momentaufnahme dieser einen fachlichen Entscheidung.