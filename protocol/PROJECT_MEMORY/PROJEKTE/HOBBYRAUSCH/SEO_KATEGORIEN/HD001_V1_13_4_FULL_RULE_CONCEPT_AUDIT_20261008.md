# HD-001 V1.13.4 – VOLLSTÄNDIGER REGEL-/KONZEPTAUDIT NACH FRONTEND-SICHTPRÜFUNG

STAND: 2026-10-08
STATUS: FAIL / LIVE-STRUKTUR NICHT ABGENOMMEN

## AUTORITÄTEN
- Zielvertrag 2.5
- Assessment Rules 1.5
- KONZEPT_3_SAEULEN_ZIELBAUM_20261007.md
- V1.13.4 Zielprofil / Live-Dry-Run 20261008-113205

## 1. EBENENMODELL
Verbindlich:
SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE.

Aktuelles Zielprofil:
- 8 Weltseiten;
- 52 fachliche Zwischenbereiche;
- 340 CORE-Hobbyseiten als dritte Seitenebene;
- 4 WordPress-Kategorien ausschließlich unter Buchbinden.

Befund:
Die dritte Seitenebene fehlt im Zielprofil NICHT. Alle 340 CORE-Hobbys hängen unter einem fachlichen Zwischenbereich.
Was im Frontend fehlt bzw. falsch wirkt, ist die korrekte Navigation auf diesen Zielbaum.

## 2. WORDPRESS-CONTENT-KATEGORIEN
Zielvertrag 2.5 erlaubt ausdrücklich, dass ein CORE-Hobby Beiträge zunächst direkt enthält.
3–6 Unterkategorien sind kein Startzwang.
Neue Content-Kategorien sollen erst entstehen, wenn reale Inhalte stabile Cluster von ungefähr 5–12 eigenständigen Beitragsintents bilden.

Daher ist der Umstand, dass derzeit nur Buchbinden die vier Kategorien
Einstieg / Ausrüstung / Material / Techniken & Praxis
besitzt, nach dem AKTUELLEN Zielvertrag kein Regelverstoß.

Wenn künftig jedes bzw. fast jedes CORE-Hobby zwingend eine Content-Kategorieebene bekommen soll, ist das eine bewusste Regeländerung und muss vor einem neuen Zielprofil festgelegt werden.

## 3. SICHTBARE NAVIGATION – FAIL
Zielvertrag:
großer interner Bestand, kleine sichtbare Navigation.

Real sichtbares Frontend:
alte/legacy Hobbyseiten werden zusammen mit den neuen Zwischenbereichen im WordPress-/Theme-Menü angezeigt.
Beispiele aus Screenshot:
Betonmöbel, Dorodango usw. direkt unter Fertigen.

Zielprofil:
Betonmöbel = Editorial / Ungewöhnliche Hobbys.
Dorodango = Editorial / Ungewöhnliche Hobbys.

Ursache:
HD-001 rendert den kanonischen Zielbaum als Seiteninhalt/Portal-Hub/Footer, kontrolliert aber die aktive Theme-/Header-Navigation nicht.
Gleichzeitig archiviert der Final-Sync absichtlich nur bereits per _apkw_target_node_id gebundene Altobjekte.
Ungebundene Legacy-Seiten bleiben daher veröffentlicht und können von einer Page-List-/Theme-Navigation weiter angezeigt werden.

Entscheidung:
Header-/Hauptnavigation darf künftig ausschließlich aus dem aktiven Target-Snapshot aufgebaut werden.
Ungebundene Altseiten dürfen die Navigation nicht mehr bestimmen.
Kein Hard-Delete notwendig.

## 4. MAGAZIN – TARGET PASS / HEADER FAIL
Zielprofil besitzt:
- Magazin-Hub;
- Hobby finden;
- Nach Situation;
- Nach Jahreszeit;
- Entdecken;
- insgesamt 15 journal_cat-Terme;
- feste Gruppen laut Konzept.

Konzept:
Magazin
→ Hobby finden → Hobbyfinder / Hobbywelten
→ Nach Situation → Zuhause / Draußen / Alleine / Zu zweit / Wenig Platz / Wenig Zeit
→ Nach Jahreszeit → Winter / Sommer
→ Entdecken → Ungewöhnliche Hobbys / Verrückte Hobbys / Neue Hobbys / Trends

Befund:
Die Magazinstruktur existiert im Zielprofil, wird aber nicht in die aktive Header-Navigation projiziert.
Damit ist die sichtbare Magazin-Navigation unvollständig.

## 5. TREIBHOLZ – FAIL IM LIVE-FRONTEND
Konzept:
Treibholz + Treibholz sammeln = eine hobby_id.
Ohne DIRECT/ASSISTED-Fit nicht als Hauptportal-Hobby unter Sammeln.

Aktuelles Profil:
canonical = Treibholz sammeln;
alias = Treibholz;
monetization_fit = UNKNOWN;
Placement = Editorial / Ungewöhnliche Hobbys.

Folge:
Im kanonischen Zielbaum gibt es keinen CORE-Treibholz-Knoten.
Jede sichtbare Treibholz-Seite unter Sammeln ist Legacy-Bestand.
Zwei sichtbare Varianten verletzen zusätzlich die Alias-/Dublettenregel.

Korrektur:
beide Legacy-CORE-Navigationseinträge aus der Hauptnavigation entfernen;
keine zweite Hobbyidentität anlegen;
kanonische Identität bleibt Editorial.
Kein Hard-Delete ohne Inhaltsprüfung.

## 6. MONETARISIERUNG
Aktuelles V1.13.4-CORE-Profil:
- 298 DIRECT;
- 42 ASSISTED;
- 0 NONE/UNKNOWN im CORE.

Damit erfüllt der eigentliche Zielbaum das strengere Konzept-Gate bereits.
Die sichtbaren UNKNOWN-Themen unter CORE stammen aus Legacy-/Navigation-Leakage, nicht aus dem neuen Zielprofil.

Dokumentkonflikt:
Zielvertrag 2.5 sagt Monetarisierung beeinflusst CORE-Priorität, entscheidet aber nicht allein über Behalten/Löschen.
Das ältere 3-Säulen-Konzept sagt strenger: NONE/UNKNOWN nicht ins Hauptportal.
Beides ist für Erhalt kompatibel, aber nicht für CORE-Promotion.
Für den aktuellen Zielbaum wurde faktisch das strengere Gate verwendet.
Dieser Widerspruch muss vor der nächsten Revision bereinigt werden.

## 7. ZWISCHENBEREICHE / VERTEILUNG
Aktuelles Zielprofil, direkte Zwischenbereiche je Welt:
- Gestalten 5
- Fertigen 7
- Technik 7
- Forschen 5
- Pflanzen 7
- Tiere 5
- Bewegen 8
- Sammeln 8
= 52.

Konzept-Arbeitsstruktur:
- Gestalten 7
- Fertigen 9
- Technik 9
- Forschen 6
- Pflanzen 9
- Tiere 7
- Bewegen 8
- Sammeln 8
= 63.

V1.13.4 hat damit 11 konzeptionelle Trennungen zusammengezogen/entfallen lassen.
Nicht alle 11 dürfen blind wieder angelegt werden, weil leere Ebenen verboten sind.

Klar überbreite aktuelle Zwischenbereiche nach realem CORE-Bestand:
- RC & Drohnen: 16 Hobbys;
- Leder & Textil: 13;
- Genuss: 12;
- Elektronik & Funk: 11;
- Holz & Naturmaterial: 10;
- Metall & Schmuck: 9.

KISS-Korrektur nach bestehendem Konzept:
- Fertigen: Leder und Textil wieder trennen;
- Fertigen: Metall und Schmuck wieder trennen;
- Technik: Elektronik und Funk wieder trennen;
- Technik: Robotik und Smart Home wieder trennen;
- Gestalten: Schrift & Lettering und Papierkunst wieder trennen;
- Pflanzen: Bonsai und Moos/Miniaturgärten trennen, soweit reale Hobbys vorhanden;
- Tiere: Insekten und Wirbellose nur dann trennen, wenn beide Seiten fachlich tragfähig sind;
- keine leere Citizen-Science-, Gehegegestaltung-, Essbare-Pflanzen- oder sonstige Symmetrie-Kategorie erfinden.

RC & Drohnen (16), Genuss (12) und Holz & Naturmaterial (10) bleiben anschließend separate Split-Reviews; keine automatische Zusatzebene, weil die maximale Seitenebene sonst überschritten würde.

## 8. UNTERSTE CONTENT-KATEGORIE – OFFENE KONZEPTENTSCHEIDUNG
Aktueller Pilot Buchbinden:
Fertigen → Buch & Papier → Buchbinden → Einstieg/Ausrüstung/Material/Techniken & Praxis → Beiträge.

Sinnvolle Kandidaten für die allgemeine Regel:
- Einstieg (deckt Anfänger ab);
- Ausrüstung;
- Material;
- Techniken & Praxis;
- Probleme & Lösungen / FAQ nur bei echter Kapazität;
- Lernen & Kurse optional;
- Fortgeschritten/Profi nur dann als eigene Kategorie, wenn dafür 5–12 eigenständige Beitragsintents existieren.

Nicht sinnvoll:
Für Anfänger / Für Profis pauschal unter jedes Hobby setzen.
Das erzeugt bei vielen Hobbys leere oder dünne Ebenen und verletzt den bestehenden Capacity-Vertrag.

## 9. ENTSCHEIDUNG
V1.13.4 ist technisch nicht als finaler Portalzustand abgenommen.

Kein weiterer Live-Sync.

Nächster Arbeitsblock:
1. kanonische Header-/Frontend-Navigation ausschließlich aus Target-Snapshot;
2. Legacy-Seiten aus sichtbarer Navigation ausschließen;
3. Treibholz-/Alias-Leakage schließen;
4. Magazin-Navigation vollständig projizieren;
5. klar zusammengezogene Zwischenbereiche gegen das Konzept korrigieren;
6. erst danach gemeinsam die allgemeine WordPress-Content-Kategorieebene festlegen;
7. neues Zielprofil vollständig lokal POS/NEG inklusive Navigation, Altbestand, Dubletten, Magazin und Rollback testen;
8. erst dann neuer Live-Kandidat.
