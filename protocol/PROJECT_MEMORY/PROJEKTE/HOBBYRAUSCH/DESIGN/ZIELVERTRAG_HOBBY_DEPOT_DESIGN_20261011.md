# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV
FASSUNG: 4.4 / 2026-10-16

## Header / Navigation
- Logo unverändert und linksbündig.
- Header als 2-Spalten-System: links Logo; rechts Suchfeld + Navigation.
- Suchfeld auf Höhe der HOBBY-DEPOT-Wortmarke.
- `Hobbys. Ideen. Möglichkeiten.` steht exakt mittig unter der HOBBY-DEPOT-Wortmarke bzw. exakt in deren Breite; kein seitlicher Versatz.
- Die sichtbare Unterkante des Claims und die Unterkante/Baseline der Hauptnavigation bilden eine gemeinsame horizontale Linie.
- Für diese Linie wird das Logo vertikal positioniert; die Navigation wird nicht erneut nach unten verschoben.
- Ab 761 px: alle 8 Welten in exakt einer horizontalen Zeile und auf derselben Baseline, einschließlich Sammeln.
- <761 px: Mobilmenü.
- Navigationsicons entfallen; Text + Pfeil bleiben.
- Flyouts per Hover/Fokus/Klick und viewport-sicher.
- Der live bestätigte Header-/Navigationsstand ist eingefroren.

## Mega-Menü – verbindliche Darstellungsregel
- Grundprinzip wie bei den bewährten Pferdeatelier-/H&Parfume-Referenzen: grafisch einheitliche, begrenzte Linkmenge statt beliebig langer Spalten.
- Die Zahl der direkt sichtbaren Unterkategorien ist **keine starre 3er-/4er-/5er-Regel**. Sie richtet sich nach dem kleinsten sinnvollen Direktbestand der acht Hauptwelten und dem grafisch gleichmäßigen Gesamtbild.
- Ziel ist: alle geöffneten Mega-Menüs wirken gleichmäßig, ohne unnötige Leerflächen oder einzelne überlange Menüs. Beim aktuellen Zielbaum ist die gemeinsame sichtbare Zahl **5**, weil die kleinste Hauptwelt 5 direkte Unterbereiche besitzt.
- Existieren darüber hinaus weitere direkte Unterkategorien, folgt am Gruppenende ein klarer Link/Button `Mehr Kategorien`; wenn keine weiteren existieren, `Alle Kategorien`.
- Beim ersten Hover/Fokus wird neben den direkt sichtbaren Unterkategorien **genau eine weitere sinnvolle Ebene** kompakt als Orientierung gezeigt. Keine weitere Verschachtelung.
- Keine unbegrenzte Vollbaum-Ausgabe und keine vierte/weitere verschachtelte Ebene im Mega-Menü.
- Die Begrenzung betrifft nur die Anzeige im Mega-Menü, niemals die reale Kategorienstruktur oder Erreichbarkeit tieferer Kategorien.
- Pferdeatelier/H&Parfume dienen hier ausschließlich als Design-/Strukturreferenz, nicht als Hobby-Depot-Statusquelle.

## Acht Hauptwelten – Hero
- Jede Hauptwelt besitzt einen eigenen, natürlichen Hero-Text.
- direkte Ansprache mit `du`.
- keine Schablonensätze.
- Text sagt in einfachen Worten, was der Nutzer dort findet.
- alle acht Texte inhaltlich verschieden.
- kein `Mehr über <Welt> erfahren`-Accordion auf Hauptwelten.
- Hero-Bilder Ebene 1 bleiben unverändert.

## Acht Hauptwelten – Text am Seitenende
- jede Hauptwelt endet mit einem längeren eigenständigen redaktionellen Text;
- klare, natürliche Zwischenüberschriften;
- direkte Ansprache;
- keine Keyword-/SEO-Textwüste;
- interne Links sparsam: **maximal 3 pro Hauptwelt, maximal einer pro Abschnitt**;
- nur semantisch passende reale Zielkategorien.

## Hub-/Unterkategorie-Bilder Ebene 1
- alle 65 direkten Unterkategorien besitzen kontrollierte Motive;
- die Kategorievorschau wird aus dem jeweils aktuellen Hub2-Hero derselben Kategorie abgeleitet; Hero und Vorschau dürfen nicht aus unterschiedlichen Bildständen stammen;
- Thema auf den ersten Blick verständlich;
- kein unnötiger Lupen-/Makroeindruck;
- ruhiges Bildumfeld;
- keine wiederverwendeten Szenenfamilien;
- kein Rückfall auf alte mehrfach verwendete Featured Images;
- kein Passepartout/Bild-im-Bild.
- Stand 1.50.634 wird vorerst akzeptiert und nicht weiter verändert.
- Für Hub2 gilt ab WIP 1.50.653 verbindlich: **Kategorievorschau und zugehöriges Hub2-Hero stammen aus derselben Bildquelle**; aus der Heroquelle wird zusätzlich die 200×107-Kategorievorschau abgeleitet. Keine zweite unabhängige Bildzuordnung für dieselbe Kategorie.

## Kategorieebene 2 / Hub2
- Der akzeptierte Buch-&-Papier-Stand **1.50.645** bleibt die visuelle Referenz für Karten, Claim-Stil und Grundcharakter.
- Der in 1.50.650 live bestätigte **Textinhalt** und die dort bestätigte **Grundaufteilung** sind eingefroren; Bild- und Hero-Fehler dürfen diese Bereiche nicht erneut verändern.
- Breadcrumb oben.

### Hero – Aufbau
- **Desktop >1100 px:** links Schreibschrift-Claim + H1 + kurzer direkter Einsteigertext; rechts ein breites, klar erkennbares Hero-Bild.
- **Tablet / mittlere Breiten <=1100 px:** Claim + H1 + kurzer Einsteigertext oben; Hero-Bild darunter; längerer Kategorietext erst danach.
- **Mobil:** dieselbe gestapelte Logik, kompakter.
- Der Hero darf die Seite nicht dominieren. Ein vollbreites 600×320-Bild darf auf Tablet/Mobil **nicht ungeprüft hochskaliert** werden, wenn dadurch ein übergroßer Hero entsteht.
- Hero-Bilder müssen als **breite Landschafts-/Stilleben-Szene** funktionieren: Thema sofort erkennbar, Hauptmotiv vollständig sichtbar, genügend Abstand, kein Makro-/Detailcrop.
- Keine unscharfen oder sichtbar hochskalierten Quellen. Ein Bild darf nur verwendet werden, wenn seine reale Auflösung für die tatsächliche Ausgabefläche ausreicht.
- Wenn kein geeignetes vorhandenes Motiv existiert: **kein falscher Fallback**. Dann bleibt der Bildslot für die Arbeitsfreigabe als fehlend markiert bzw. es wird gezielt ein neues, optimiertes Motiv erzeugt; niemals thematisch falsches Bild nur zum Füllen.
- Der linke Weißverlauf darf das Motiv nicht zerstören und darf keine zusätzliche Unschärfe vortäuschen.
- Hero-Rundung zurückhaltend, maximal wie im akzeptierten Buch-&-Papier-Stand.

### Hero – Claim
- Über der H1 steht pro Hub2 ein kurzer individueller, natürlicher, leicht frecher Claim.
- Schreibschrift und beige Pinselkurve orientieren sich **exakt am akzeptierten Buch-&-Papier-Stand**.
- Pinselstrich bleibt unter dem Claim, mit sauberem Abstand; nicht nach oben verrutschen.
- Pinselstrich darf nicht deutlich über den sichtbaren Claim hinauslaufen; keine überlange Vollbreiten-Linie.
- Claim-Größe und -Position nicht pro Kategorie willkürlich skalieren.

### Hero – kurzer Einstieg
- Pro Hub2 ein kurzer, eigener Einsteigertext.
- direkte **du**-Ansprache;
- locker, pfiffig, nicht förmlich;
- themenspezifisch;
- keine austauschbare Schablone;
- kurz genug, damit der Hero unabhängig von Kategorie und Bildschirmbreite stabil bleibt.

### Längerer Kategorietext
Verbindliche Textregel:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`

Es werden **nur die redaktionellen Textregeln** aus Pferdeatelier übernommen:
- ca. 150–200 Wörter;
- natürliches normales Deutsch;
- themenspezifische Substanz;
- keine Generator-/Padding-Sprache;
- keine generische Schlussformel;
- fachliche, praktische Orientierung;
- nur reale vorhandene Unterthemen nennen.

Hobby-Depot-Darstellung:
**sichtbarer Lead → `Mehr zu <Kategorie> erfahren` → restlicher Text im Aufklapper.**
- kein zusätzlicher zweiter Erklärungstext;
- der Text steht unter dem Hero;
- beim Öffnen darf sich die Hero-Bildgröße nicht verändern;
- ausreichend echter Text bleibt bereits ohne Aufklappen sichtbar.

### Hero-Bildregeln – semantisch
Für jede der 65 Hub2-Seiten:
- eigenes thematisch passendes Hero-Motiv;
- Szene weiter herausgezoomt;
- klare Szenerie / Stilleben statt angeschnittenem Detail;
- Hauptthema auf den ersten Blick erkennbar;
- wenige konkurrierende Objekte;
- keine inhaltlich fremden Motive;
- keine Duplikat-/Universalbilder für fachlich verschiedene Kategorien;
- keine Kakteen bei Genuss oder Essbare Pflanzen, wenn das konkrete Thema nicht Kakteen ist;
- keine Blumen als Hauptmotiv für Ameisen & Insekten;
- keine Münzen-/Globusmotive für Papier-/Postkarten-Unterthemen ohne echten fachlichen Bezug.

### Unterkategoriekarten
- jede tatsächlich vorhandene direkte Unterkategorie erhält eine **Fotokarte**;
- kein Icon-Rückfall;
- jede Karte erhält unter dem Titel eine kurze sinnvolle Orientierungszeile wie bei Buch & Papier;
- jedes Bild muss inhaltlich **zur konkreten Unterkategorie** passen;
- kein generischer Welt-Pool-Fallback;
- innerhalb derselben Hub2-Seite keine doppelten Bilddateien und keine offensichtlich identischen Motive;
- klare, einfache Szene, Hauptmotiv sofort erkennbar;
- **Zoom raus:** kein Makro-/Detailbild, wenn dadurch das Thema nicht mehr erkennbar ist;
- möglichst wenig störender Hintergrund / keine überfüllte Szene;
- keine eingebrannten weißen Rahmen, Passepartouts, Vignetten oder Bild-im-Bild-Ränder;
- keine unscharfen/upgescalten Quellen;
- wenn kein geeignetes vorhandenes Bild existiert: als fehlend behandeln und gezielt ersetzen, nicht semantisch falsch füllen;
- Bilder exakt im vorhandenen Ebene-1-Kartenrahmen: Margin 0, Padding 0, Foto-Radius 0, Overflow hidden, Object-fit cover;
- Desktop 3 Karten nebeneinander; unvollständige letzte Reihe linksbündig;
- Affiliate-Banner darf den freien Restplatz der letzten 3er-Reihe füllen; bei voller Reihe eigene Bannerzeile.

### Reihenfolge darunter
- konkrete `category_product_1..3`-Produkte;
- **3** passende Beiträge mit Beitragsbild;
- genau ein direkt verkaufbarer Werbeplatz;
- **kein** zusätzlicher redaktioneller Seitenendtext auf Hub2;
- öffentlich leere Affiliate-Flächen unsichtbar; eingeloggte Arbeitsvorschau erlaubt;
- je tiefer die Seite, desto konkreter die Produktbelegung; nicht einfach mehr Produkte.

### Harte Abnahme für Bild-/Hero-Änderungen
Kein neuer Kandidat ohne lokale Sichtprüfung der realen gerenderten Ausschnitte:
1. semantische Passung;
2. Zoom/Szenerie;
3. Schärfe / keine Hochskalierung;
4. Duplikatfreiheit;
5. keine eingebrannten Rahmen;
6. Hero-Höhe und Proportionen;
7. Responsive Desktop/Tablet/Mobil;
8. Claim-Unterstrich;
9. Regression der live bestätigten Text-/Grundaufteilung.

## Karten
- natürliche Überschrift `Weiter in <Thema>` / `Weitere Kategorien`.
- Kartentitel 15 px.
- Untertitel nur mit echtem Orientierungswert.
- kein generischer Fülltext.

## Monetarisierung
- Affiliate-Produkte nie zwischen Unterkategorie-Reihen.
- Banner und Affiliate-Produkte sind getrennte Slottypen.
- Direktwerbung ist ebenfalls getrennt und maximal ein Platz pro Seite.
- Affiliate-Zentrale bleibt Monetarisierungsautorität.

## Bestehende Bindungen
- keine Taxonomie-/Workflow-/Provideränderung durch Design.
- HD-001/HD-004 bleiben Kategorie-/Runtime-Autorität.
- keine neue Architektur.

## PASS
Kein Live-PASS ohne echten WordPress-Readback.\n