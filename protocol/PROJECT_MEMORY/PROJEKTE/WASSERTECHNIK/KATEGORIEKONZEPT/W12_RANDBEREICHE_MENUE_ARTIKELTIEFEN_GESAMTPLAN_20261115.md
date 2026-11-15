# Wassertechnik W12 – echte Lücken und Randbereiche, kein neuer Blind-Import
Stand: 15.11.2026. **Fach-/Menü-Konzept, keine WP-/Plugin-/SEO-API-Schreibaktion.**

## 1. Ausgangspunkt und nachgewiesenes Problem
- Zielvertrag: 6–8 fachlich sinnvolle Hauptbereiche, letzte WordPress-Seitenebene ist **konkretes Produkt/System**, darunter genau diesem Produkt zugehörige frei benannte **WP-Beitragskategorien** mit **mindestens drei inhaltlich unterschiedlichen** plausiblen Einzelbeiträgen je Kategorie. Keine neue Kategorie nur für Menüästhetik.
- Der W4-Master hat **79 konkrete Produktseiten und 105 fachliche Inhaltskategorien**. 0 identisch benannte neue Produkte der W12-Kandidaten erscheinen bereits in der W4-Produktliste (automatischer Namensvergleich; **keine Aussage, dass es keine inhaltliche Überschneidung gibt**).
- Das echte im Chat vorliegende WT001-v0.1.7-Archiv `Wassertechnik-Plugin-0.1.7.zip` enthält in `assets/wassertechnik-w10-menu.json` sieben sichtbare Hauptbereiche. Die aus dem Code/JSON bestätigten Textdopplungen sind z. B. `Brunnen & Bewässerung → Bewässerungssysteme → Tropfbewässerungsset`, `Weitere Bewässerung → Gartenschlauch`, `Wasseraufbereitung → Osmoseanlagen → Untertisch-Osmoseanlage` sowie `Regenwasser & Wassertanks → Regenspeicher → Regenwasser-Erdtank`.
- **Menütext ist nicht SEO-Seitentitel:** Sichtbare, kurze Kontextbezeichnungen dürfen abweichen von H1, WordPress-Seitentitel, URL/Slug und SEO-Keyword. Kein Automatismus, der Produktnamen global verstümmelt.

## 2. Konkrete Bereinigungsregel für Doppelbezeichnungen
1. Behalte **sieben Hauptmenüpunkte** als aktuellen genehmigten sichtbaren Stand, bis ein tatsächlich tragfähiger achter Schwerpunkt beschlossen ist; keine Hauptkategorie »Smart Home«/»Umweltschutz«/»Technik«.
2. Nutze max. eine Gruppenüberschrift für fachlich nützliche Teilung; wenn eine einzelne Produktseite unter einer bloßen Zusatzüberschrift steht, diese **überschriftenlos** unter bestehende sachlich passende Gruppe einordnen, z. B. `Weitere Bewässerung` für genau einen Gartenschlauch entfernen.
3. In klar überschriebenen Gruppen sinnvolle Labels kürzen, **nur sichtbar**: `Osmoseanlagen: Auftisch / Untertisch / Direct Flow / Mit Drucktank`; `Regenspeicher: Regentonne / Erdtank / Kellertank`; `Labortests: Trinkwasser / Brunnenwasser / Schadstoffe`. **Jeder Link zeigt unverändert auf seine bestehende konkrete Produktseite.**
4. Vermeide falsche Kurzformen: `Manueller Rückspülfilter` und `Automatischer Rückspülfilter` unterscheiden tatsächlich technische Varianten; Unterscheidung erkennbar lassen. Bei `Tankarten` müssen Trink-/Nutzwasser sowie IBC/Mobil weiterhin klar sein.
5. Sichtbare Menügruppen sind keine zusätzlichen WP-Seiten oder Kategorien und keine doppelten SEO-Owner; eine strukturell echte WP-Gruppe bleibt vorhanden, auch wenn ihre Überschrift im Menü reduziert oder unterdrückt wird.
6. Nur einen neuen Menü-Plan innerhalb des **vorhandenen** WT001/Designsystems, später gebündelte Desktop/Mobil-Sichtprüfung; **keine** neue Pluginlinie oder Änderung des WP-Cores.

## 3. Randbereiche – Eignung und klare Schnittmengen
| Umfeld | Zulässige WASSERTECHNIK-Produktarten | Bewusst außerhalb des Produktbaums |
|---|---|---|
| **Smart Home** | Leckageschutz-Absperrventil, Bewässerungs-Magnetventil, vorhandener Bewässerungscomputer, vernetzte Zisternenüberwachung | Allgemeine Smart-Home-Zentralen und App-Vergleiche ohne Wassertechnik – Magazin oder andere Portale |
| **Wassersparen / Umweltschutz** | Strahlregler, Ablaufdrosseln, Regenwasser-Sedimentationsanlage, Duschwasser-Wärmetauscher, vorhandene Grauwasseranlage | Politik, Klimaanpassung, Gewässerschutz, Schwammstadt als **Magazin**; keine »Umweltschutz«-Fake-Produktseite |
| **Haus-/Gebäudetechnik** | Trinkwasser-Druckminderer, Zirkulationspumpe, Hygienespülstation; wassertechnisches Leckageschutzventil | Komplettes Heizungs-/Sanitärportal oder allgemeine Elektrotechnik |
| **Garten/Brunnen** | Brunnenköpfe, Brunnen-Vollwandrohre, Tropfrohre, Regner, Ventile, autarke Bewässerung | Allgemeiner Gartenbau/Pflanzenpflege, Mähroboter |
| **Abwasser kleiner Betriebe** | Fettabscheider, Leichtflüssigkeitsabscheider, weitere tatsächliche Rückhalte-/Behandlungsanlagen | Allgemeine Gewerbeversicherung oder Abfallrecht |
| **Pool/Teich** | Sandfilter, Pumpen, Dosiergeräte, Salzelektrolyse, Teichfilter/UVC/Belüftung | Poolmöbel, Planschbecken, Fischfutter, Aquaristik als Hobby |
| **Camping/Selbstversorgung** | Nur echte tragfähige Wasseraufbereitungs- oder Versorgungstechnik, nach eigenem Geräte-/Anwendungsabgleich | Wohnmobil-Zubehör allgemein / Prepper-Gadgets ohne wassertechnische Funktion |

**Portfolio-Grenze:** Hab & Bewahr kann zum Wasser-Leckageschutz auf **eine** fachliche Produktseite im Wassertechnik-Portal verlinken; eigener Schutz-/Schadensartikel ist anderes Informationsziel. Hobby Depot kann aus dem Gartenteich-Hobby auf die technische Filter-/Pumpproduktseite verweisen. Nicht denselben Produkt-SEO-Owner sinnlos mehrfach kopieren.

## 4. Echter zusätzlicher Produktbestand
`W12_PRODUKTLUECKEN_26_MIT_BEITRAGSTIEFEN_20261115.json` enthält **26 recherchierte Produkttypen** mit mindestens einem Hersteller-/Fachquellenlink je Produkttyp und zugeordneter existierender W10-Hauptwelt bzw. ausdrücklich optionalem achten Bereich. Sie wurden **noch nicht** als WP-Owner oder SEO-Ziele freigegeben.
- **6** Brunnen & Bewässerung: Brunnenkopf, Brunnen-Vollwandrohr, Viereckregner, Bewässerungs-Magnetventil, Tropfrohr, Solar-Bewässerungsset.
- **3** Pumpen & Druck: Trinkwasser-Druckminderer, Warmwasser-Zirkulationspumpe, automatisches Leckageschutzventil.
- **2** Wasseraufbereitung: Trinkwasser-Hygienespülstation, Wasserspar-Strahlregler.
- **2** Wasseranalyse: Gelöstsauerstoff-Messgerät, Leitfähigkeitsmessgerät (zweites mit ausdrücklich hoher SEO-Überschneidungsgefahr zu Multimessgerät).
- **2** Regenwasser & Wassertanks: Ablaufdrossel, Sedimentationsanlage.
- **3** Abwassertechnik: Duschwasser-Wärmetauscher, Fettabscheider, Leichtflüssigkeitsabscheider.
- **8** Pool & Teich: Pool-Sandfilteranlage, Pool-Dosieranlage, Pool-Salzelektrolyseanlage, Pool-Umwälzpumpe, Teichfilter, Teich-UVC-Klärer, Teichpumpe, Teichbelüfter.

**Fachlicher Artikeltiefen-Check über die 26 Kandidaten:** **37** frei und fachbezogen benannte, nicht starr vorgeschriebene Beitragskategorien; **111** konkrete unterschiedliche Artikelrichtungen. Jede der 37 Kategorien hat **genau drei** durchdachte Ansätze (Minimum nachgewiesen). Das ist eine **redaktionelle Plausibilitätsprüfung**, keine Google-SERP-, Suchvolumen- oder echte Textqualität-Garantie. Produkte brauchen nicht automatisch genau eine oder genau zwei Kategorien.

**Rechenobergrenze:** 79 vorhandene + 26 Vorschläge = **105 denkbare Produktseiten**, ABER keine Prognose, dass alle die endgültige eigenständige SEO-/WP-Ownerprüfung bestehen. Insbesondere: Leitfähigkeitsmessgerät vs vorhandenes Multimessgerät, Pool-Dosieranlage vs allgemeine Wasser-Dosieranlage, Pool-Salzelektrolyse vs Pool-Dosieranlage, Brunnen-Vollwandrohr vs Brunnenfilterrohr, Teich-UVC vs vorhandene UV-Desinfektion. Nicht alle Varianten automatisch getrennt publizieren.

### Priorität: was tatsächlich neue kaufnahe Tiefe bringt
**Zuerst**: Brunnenkopf, Viereckregner, Bewässerungs-Magnetventil, Solar-Bewässerungsset, Trinkwasser-Druckminderer, Hygienespülstation, Warmwasser-Zirkulationspumpe, Wasserspar-Strahlregler, Fettabscheider, Duschwasser-Wärmetauscher, Regenwasser-Ablaufdrossel. Bei diesen sind Geräte/Funktionen und unterscheidbare Nutzungsfragen aus offiziellen Quellen klar.
**Danach gezielt:** weitere Komponenten und Messgeräte, Leckageschutz mit Portfolio-Abgrenzung, qualifizierte Lösungen für Pool & Teich.

### Pool & Teich = realer Vorschlag für achte Hauptkategorie
Acht eigenständige kaufbare Produktfamilien und unterschiedliche Technikaufgaben sind bei BAYROL, Steinbach und Sera belegt; also nicht nur »Menüauffüllen«. **Als achter Hauptbereich plausibel**, aber **noch nicht entschieden**: Heterogenität und Hobby-Depot-Abgrenzung beachten. Die bestehende siebte `Industrie & Großanlagen` bleibt Informationszugang, kein zweites vollständiges Produktportal. Alternativ Pool/Teich als wenige sachliche Querzugänge zu vorhandenen Wasseraufbereitungs-/Pumpen-Inhaltsbereichen, **keine** zweite SEO-Kopie.

## 5. Verwendete Hersteller-/Fachbelege, nachprüfbar
- STÜWA Brunnenkopf und Vollwandrohr: https://www.stuewa.de/de/produkte/brunnenabschluesse/brunnenkoepfe und https://www.stuewa.de/de/produkte/pvc-brunnenfilter-und-aufsatzrohre/pvc-filter/vollwandrohre
- GARDENA Regner, Smart-Ventile, Tropfrohr und Solar-Set: https://www.gardena.com/de/produkte/bewaesserung/regner ; https://www.gardena.com/de/produkte/bewaesserung/bewaesserungssteuerung ; https://www.gardena.com/de/produkte/bewaesserung/micro-drip-system ; https://www.gardena.com/de/produkte/bewaesserung/bewaesserung-ohne-wasseranschluss-urlaubsbewaesserung/solar-bewaesserungs-aquabloom-set/967999001.html
- SYR Leckageschutz: https://www.syr.de/de/Produkte/BB120F93-73D2-4AD2-B362-5307DCC3866A/ISI-Home-Connect-System
- KEMPER Hygienespülstation: https://www.kemper-group.com/de-de/gebaeudetechnik/produkte/hygienesystem-khs/khs-hygienespuelungen/index.html
- DVGW Trinkwasserinstallation/Druckminderer/Fachbetrieb: https://www.dvgw.de/themen/wasser/verbraucherinformationen/trinkwasser-installation/
- Grundfos Warmwasser-Zirkulationspumpen: https://www.grundfos.com/de/support/faq/what-are-the-requirements-for-the-hot-water-recirculation-pump
- Neoperl Wasserspar-Strahlregler: https://www.neoperl.com/de/de/handel/produkte/strahlregler/wasserspartechnologien
- co2online Duschwasser-Wärmerückgewinnung: https://www.co2online.de/energie-sparen/wasser-sparen/warmwasserbereitung/warmwasser-waermerueckgewinnung/
- INTEWA Regenwasser-Drosseln: https://www.intewa.com/de/intewa-produkte/ablaufdrosseln/
- ACO Regenwasservorreinigung, Fettabscheider, Leichtflüssigkeitsabscheider: https://www.aco.de/anwendungen/regenwasserbewirtschaftung/regenwasserbehandlung ; https://www.aco.de/anwendungen/gewaesserschutz/fetthaltiges-abwasser ; https://www.aco.de/produktfinderuebersicht/leichtfluessigkeitsabscheider
- Xylem/WTW Gelöstsauerstoff und Leitfähigkeit: https://www.xylemanalytics.com/de/produkte/messgeraete/sauerstoff-messgeraete ; https://www.xylemanalytics.com/de/produkte/messgeraete/leitfaehigkeits-messgeraete
- Steinbach Poolfilter/Pumpen: https://www.steinbach-group.com/de/040385-filteranlage-classic-250n-de/ ; https://www.steinbach-group.com/de/041063-filterpumpe-wp-7000-de/
- BAYROL Pool-Dosierung und Salzelektrolyse: https://www.bayrol.de/bayrol-technik-dosieranlagen ; https://www.bayrol.de/produkte/automatische-wasserpflege/salt-relax-power
- Sera Teichfilter/UVC/Pumpen/Belüfter: https://www.sera.de/de/gartenteich/Produkte/gartenteich-technik

## 6. Einziger sinnvoller nächster Hauptblock – **noch keine WP-Aktion**
1. Die 26 Kandidaten gegen bereits publizierte W4-Owner und reale Suchabsicht **einmal zusammen** nach eigener technischer Funktion und Konkurrenz in W4 prüfen; nicht jede Produktvariante blind als neue Seite anlegen. Keine bezahlte DataForSEO-Abfrage ohne gesonderte Freigabe.
2. Fachlich tragfähige Kandidaten und mögliche 8. Hauptkategorie `Pool & Teich` als **eine Strukturentscheidung** abnehmen, in demselben Zuge redundante Menülabels entschlacken. **Keine neue feste Pflicht-Kategoriesystematik**.
3. Erst mit freigegebenem Endbaum eine einzige synchronisierte, ADD-only-Erweiterung in **bestehender** WT001-Pluginidentität vorbereiten, Site-/Bestandsabgleich und ausdrückliche Schreibfreigabe. Keine neue zusätzliche Pluginlinie, keine unbegründete URL-Änderung, keine vorhandenen SEO-Owner neu erzeugen.
4. **Eine** Desktop-/Mobil-Abnahme des Menübilds und ein echtes WP-Readback. Bis dahin im Frontend nichts automatisch umbenennen.

**Status: W12 recherchiert und als Fachvorschlag dokumentiert; WordPress, SEO-API, Plugin, Design und Fremdportale unverändert.**
