# HOBBYRAUSCH – DESIGN – ARBEITSFEHLERPROTOKOLL 2026-10-12

ROLLE: Dauerhafte Fehler-/Lernakte für die Designarbeit am Hobby-Depot-Template-Kit.
Autoritative aktuelle Fehlerlage bleibt `FEHLERQUELLEN.md`.
Aktueller Stand/NEXT ACTION bleibt ausschließlich `CURRENT_STATE.md`.

## Zweck
Dieses Protokoll dokumentiert ausdrücklich die Arbeitsfehler, die im Designlauf 1.50.629–1.50.631 gemacht wurden. Es darf nicht als zweite Current-Wahrheit benutzt werden.

## AF-001 – Falscher Repository-Kontext beim ersten Campus-Check
FEHLER:
Zu Beginn wurde ein GitHub-Pfad zunächst gegen den falschen Repository-Kontext geprüft. Dadurch entstand ein 404, der für die eigentliche Hobbyrausch-Designprüfung keine Aussagekraft hatte.

URSACHE:
Repo-Kontext nicht zuerst aus der realen Campus-Bindung bestätigt.

KORREKTUR:
Der richtige Bestand wurde danach im Repository `hallo-netizen/affiliate-pferdeportal`, Branch `hobbyroom/project-memory-campus-v1-20260905`, geprüft.

VERMEIDUNGSREGEL:
Vor jedem Status-/Pfadbefund zuerst Repository + Branch + Head aus der autoritativen Bindung bestätigen.

## AF-002 – 1.50.629 als Bildkorrektur ausgegeben, obwohl die sichtbare Änderung nicht belastbar bewiesen war
FEHLER:
1.50.629 wurde als fertige Bildkorrektur ausgegeben. Der Nutzer stellte live fest, dass die Kategorie-Vorschaubilder praktisch unverändert wirkten.

URSACHE:
Die Prüfung konzentrierte sich auf Dateibindung, Version, SHA-Eindeutigkeit und Paketstruktur. Es wurde nicht ausreichend bewiesen, dass die sichtbare Bildwirkung tatsächlich dem gewünschten "weiter raus / weniger Detail / klareres Gesamtmotiv" entsprach.

ZUSÄTZLICHER FEHLER:
Die Aussage, die Bildkorrektur sei "umgesetzt", war zu stark. Lokal war nur technisch belegt, dass ein anderer/gebundener Bildbestand vorhanden war, nicht dass die visuelle Anforderung erfüllt war.

VERMEIDUNGSREGEL:
Bildänderung niemals nur per Dateihash/Versionspfad als PASS erklären. Vor Ausgabe zwingend visueller Gesamtvergleich des aktiven 65er-Satzes und Stichproben in realer Karten-Geometrie.

## AF-003 – 1.50.629 ließ eine bereits akzeptierte Navigation sichtbar wieder absinken
FEHLER:
Obwohl die Navigation zuvor vom Nutzer als PASS bestätigt und "nicht mehr anfassen" markiert war, erschien sie nach dem folgenden Build wieder tiefer.

URSACHE:
Regression der Header-/Releasebindung wurde vor Ausgabe nicht gegen den letzten live akzeptierten Stand geometrisch gegengeprüft.

VERMEIDUNGSREGEL:
Jeder neue Build muss für alle bereits live akzeptierten Bereiche einen Negativ-Regressionscheck enthalten: keine Änderung an Navigation, Texten, Headergeometrie oder Monetarisierung, sofern nicht ausdrücklich beauftragt.

## AF-004 – 1.50.630 aktivierte den falschen alten Bildsatz
FEHLER:
Um den Zoom-out schnell zu korrigieren, wurde in 1.50.630 der alte `v150623`-Bildsatz im aktiven Hub1-Pfad bevorzugt.

FOLGE:
Mehrere visuell gleiche bzw. sehr ähnliche Szenenfamilien wurden wieder aktiv. Der Nutzer sah erneut Doppelbilder.

URSACHE:
Die Annahme "älter = weiter gefasst = besser" wurde aus früherer Dokumentation abgeleitet, ohne den vollständigen 65er-Satz visuell auf Szenenwiederholungen zu prüfen.

VERMEIDUNGSREGEL:
Keinen alten Bildsatz blind reaktivieren. Vor Aktivierung kompletter Contact-Sheet-/visueller Duplikatcheck aller 65 Motive plus aktiver Pfadprüfung.

## AF-005 – Byte-Eindeutigkeit mit visueller Eindeutigkeit verwechselt
FEHLER:
Mehrfach wurde "65/65 SHA-eindeutig" als starke Qualitätsaussage verwendet.

PROBLEM:
Unterschiedliche Dateien können trotzdem dieselbe oder nahezu dieselbe Szene zeigen. Genau das trat beim alten Satz auf.

URSACHE:
Technische Dateieindeutigkeit wurde zu stark als Ersatz für visuelle Eindeutigkeit gewertet.

VERMEIDUNGSREGEL:
Für Bildsätze sind mindestens drei getrennte Prüfungen nötig:
1. Datei-/SHA-Eindeutigkeit,
2. visueller/perzeptueller Duplikatcheck,
3. menschlicher Gesamtcheck auf wiederkehrende Szenen, Motivfamilien und unklare Themenabbildung.

## AF-006 – 1.50.630 als Fix ausgegeben, bevor Header und Bilder vollständig simuliert waren
FEHLER:
Das ZIP 1.50.630 wurde als korrigierter Stand ausgegeben, obwohl erst danach vollständig nachgewiesen wurde, dass der alte Bildsatz Doppelungen enthält und die Headergeometrie nicht stimmt.

URSACHE:
Zu frühe Freigabe nach Codeänderung statt nach vollständigem Positiv-/Negativtest.

VERMEIDUNGSREGEL:
Kein Downloadkandidat mehr vor abgeschlossener Simulation. Reihenfolge verbindlich:
Änderung → aktive Pfade prüfen → visueller Bildcheck → Headergeometrie → Regression bereits abgenommener Bereiche → erst dann ZIP ausgeben.

## AF-007 – Claim künstlich verbreitert und dadurch nicht mittig
FEHLER:
Im Header blieb die CSS-Regel `.hd-logo-claim-v150622{transform:scaleX(1.06)}` aktiv.

FOLGE:
"Hobbys. Ideen. Möglichkeiten." war gegenüber der HOBBY-DEPOT-Wortmarke nach rechts verbreitert und nicht sauber mittig/gleich breit.

URSACHE:
Vorhandene Altregel wurde beim Headerumbau nicht als Konflikt erkannt.

VERMEIDUNGSREGEL:
Bei Logo-/Claim-Ausrichtung keine optische Stretch-/Translate-Korrektur ohne geometrischen Nachweis. Wortmarke und Claim müssen über gemessene Breite/Mitte ausgerichtet werden.

## AF-008 – Logo-Unterkante und Navigation wurden nicht vor Freigabe auf eine gemeinsame Linie gemessen
FEHLER:
Die Nutzeranforderung "Logo/Claim-Unterkante und Navigation eine Linie" wurde zunächst nur optisch/CSS-seitig umgesetzt.

NACHWEIS DES FEHLERS:
Vor 1.50.631 ergab die lokale Geometrie:
- Desktop: 7 px Abweichung;
- 761–1000 px: 38 px Abweichung.

URSACHE:
Kein verpflichtender Koordinatenvergleich der echten gerenderten Elemente vor Ausgabe.

VERMEIDUNGSREGEL:
Bei Headerausrichtung an allen Pflichtbreiten die tatsächlichen Bounding-Box-Koordinaten messen. PASS nur bei definierter Toleranz; für diese Anforderung: 0 px Zielabweichung.

## AF-009 – Bereits akzeptierte Bereiche wurden bei Korrekturen nicht strikt genug eingefroren
FEHLER:
Navigation und andere Headerteile wurden in Folgekorrekturen erneut beeinflusst, obwohl sie zuvor live als PASS bestätigt waren.

URSACHE:
"Nicht anfassen" war dokumentiert, aber nicht als technische Regression-Sperre behandelt.

VERMEIDUNGSREGEL:
Live akzeptierte Teilbereiche erhalten ab sofort eine harte Freeze-Liste im jeweiligen Buildtest. Eine Änderung daran ist nur zulässig, wenn der Nutzer genau diesen Bereich erneut beauftragt.

## AF-010 – Dokumentation war zeitweise stärker als der tatsächliche Beweis
FEHLER:
Campus-Texte beschrieben 1.50.629 bereits als belastbare Bildkorrektur, obwohl der reale Liveeffekt später als unzureichend/falsch bestätigt wurde.

URSACHE:
Lokaler Technik-PASS und visuelle Live-Abnahme wurden sprachlich nicht sauber genug getrennt.

KORREKTUR:
Die aktuelle Design-Current und `FEHLERQUELLEN.md` führen 1.50.629 als Live-Fail und 1.50.630 als verworfen.

VERMEIDUNGSREGEL:
Dokumentation muss immer unterscheiden:
- technisch lokal vorhanden,
- visuell lokal simuliert,
- WordPress live bestätigt.
Kein "behoben"/"PASS" ohne die jeweils erforderliche Stufe.

## Verbindliche Schutzregeln ab diesem Fehlerlauf
1. Keine Bildfreigabe nur auf Basis von SHA/Dateinamen.
2. Vor Bildrelease kompletter 65er-Gesamtcheck auf Motivklarheit und Szenendoppelungen.
3. Kein Rückgriff auf alte Bildserien ohne vollständige visuelle Prüfung.
4. Keine Änderung an bereits live akzeptierten Bereichen ohne ausdrücklichen Auftrag.
5. Headeränderungen müssen vor ZIP-Ausgabe bei 1600/1440/1200/1024/900/800/761 px geometrisch simuliert werden.
6. Claim/Wortmarke nicht per Stretching "optisch passend" machen.
7. Downloadkandidat erst nach Positiv-, Negativ- und Regressionstest ausgeben.
8. Lokalen Technik-PASS niemals als Live-PASS formulieren.
9. Bei Nutzerforderung "nicht raten" keine Annahme aus früheren Versionstexten als Ersatz für eine reale Prüfung verwenden.

## AF-011 – 1.50.632 ohne echte Karten-CSS-Simulation freigegeben
FEHLER:
1.50.632 wurde mit der Aussage ausgegeben, der Rahmen sei entfernt. Im tatsächlich wirksamen CSS blieb jedoch die eingerückte Kategorie-Bildbox aktiv, unter anderem mit `margin:9px 0 9px 9px`, Hintergrund und Radius.

FOLGE:
Live blieb der sichtbare Rahmen/Passepartout-Effekt bestehen.

URSACHE:
Nur die Bildbindung wurde geprüft; die endgültig berechnete CSS-Kaskade der Kategoriekarte wurde vor Ausgabe nicht im Browser simuliert.

VERMEIDUNGSREGEL:
Kein Karten-/Layout-Fix ohne Render-Simulation der finalen CSS-Kaskade. Pflichtprüfung: Slot-Rechteck gegen Bild-Rechteck; Margin/Padding/Border müssen bei "kein Rahmen" tatsächlich 0 sein.

## AF-012 – Trotz ausdrücklicher Forderung erneut einen zu schnell geprüften Build ausgegeben
FEHLER:
Nach der ausdrücklichen Vorgabe, keine ungetesteten Schnellschuss-ZIPs mehr auszugeben, wurde 1.50.632 dennoch vor vollständiger Karten-Simulation freigegeben.

URSACHE:
Die gewünschte sichtbare Wirkung wurde erneut aus Quelltextänderungen abgeleitet statt vollständig im gerenderten Ergebnis geprüft.

VERMEIDUNGSREGEL:
Bei Designänderungen gilt verbindlich:
Änderung → echte Assets laden → finale CSS-Kaskade rendern → Pflicht-Viewports simulieren → bereits akzeptierte Bereiche regressionsprüfen → erst dann ZIP erzeugen/ausgeben.

## AF-013 – Bildanforderung zu lange mit technischen Ersatzmaßnahmen statt echter Motivprüfung behandelt
FEHLER:
Die Anforderung "Szenerie weiter raus, Hauptmotiv klar, wenig Zeug drumherum" wurde zeitweise mit Crops, alten Bildserien oder künstlicher Bildumfelderweiterung beantwortet, statt jedes aktive Kategorie-Vorschaubild auf die eigentliche visuelle Anforderung zu prüfen.

VERMEIDUNGSREGEL:
Für Kategorie-Vorschaubilder ist der visuelle Zweck die Autorität:
- klare Szene;
- erkennbares Hauptmotiv;
- weiter gefasst;
- wenig konkurrierende Elemente;
- keine künstliche Rahmung;
- Hero-Bilder unberührt.
Technische Dateieindeutigkeit allein ist kein Qualitäts-PASS.

## AF-014 – Testbeiträge angelegt, aber Vorschau-Gate nicht gegen reale Seitenstruktur geprüft
FEHLER:
1.50.636 enthielt Seed-Code für vier Testbeiträge und die Aussage, damit könne die Hub2-Beitragsvorschau live beurteilt werden. Auf der realen Seite blieb die Vorschau trotzdem leer.

URSACHE:
Die lokale Prüfung betrachtete Seed und Kartenrendering getrennt. Nicht vollständig simuliert wurde der reale Hub2-Zugriffspfad: Seite ohne gleichnamige WordPress-Beitragskategorie → früher Abbruch in `render_post_previews()` → Testposts werden gar nicht abgefragt.

VERMEIDUNGSREGEL:
Bei Vorschau-/Fallbacklogik muss künftig der komplette reale Gate-Pfad simuliert werden, einschließlich des Negativfalls „keine gleichnamige Beitragskategorie vorhanden“. Seed-Erfolg allein ist kein Frontend-PASS.

## AF-015 – Vorhandene korrekte Ebene-1-Lösung nicht kopiert, sondern erneut Sonderregeln gebaut
FEHLER:
Bei 1.50.641–1.50.643 wurden für Buch & Papier wiederholt eigene Karten-/Bildregeln ergänzt, obwohl die nächsthöhere Kategorieebene bereits die richtige Bildwrapper-, Cropping- und Rasterlogik enthielt.

FOLGE:
Mehrere Live-Runden mit weiterhin falscher Bildrahmung; 1.50.643 verschlechterte zusätzlich die reale Kartenanordnung.

URSACHE:
Die vorhandene Ebene-1-Implementierung wurde nicht als einzige technische Vorlage behandelt. Stattdessen wurden parallele Pilotselektoren weitergeführt und nur teilweise überschrieben.

VERMEIDUNGSREGEL:
Wenn der Nutzer ausdrücklich eine bestehende korrekte Darstellung als Vorlage nennt, wird künftig zuerst deren **Markup + Klassen + finale CSS-Kaskade vollständig wiederverwendet**. Keine nachgebaute Annäherung. Vor Freigabe Browser-Render mit echter Kaskade und Geometriemessung.


## AF-016 – Header-Claim 1.50.642/1.50.643 als „kräftiger“ bezeichnet, obwohl die sichtbare Änderung live nicht nachgewiesen war
FEHLER:
Die Claim-Verstärkung wurde als erledigt ausgegeben, obwohl die lokale Regel nur eine sehr schwache optische Manipulation verwendete und kein belastbarer visueller Dicken-Nachweis vorlag.

FIX 1.50.644:
Gleicher Sprite-Ausschnitt wird ohne Größenänderung mit zwei zusätzlichen ±0,75-px-Lagen überlagert. Browser-Readback bestätigt beide Lagen als aktiv.

VERMEIDUNGSREGEL:
Bei sichtbarer Strichstärkenänderung nicht nur CSS-Vorhandensein, sondern gerenderte Wirkung bzw. eindeutig wirksame Mehrfachlage prüfen.

## AF-017 – Bilddatei selbst nicht geprüft; CSS fälschlich als alleinige Ursache behandelt
FEHLER:
Bei mehreren Korrekturen wurde geprüft, ob Wrapper und IMG Radius/Margin/Padding 0 haben. Nicht geprüft wurde früh genug, ob die sichtbare Rundung bereits in den Pixeln der fünf Pilotbilder steckt.

FOLGE:
Mehrere lokal technisch korrekte CSS-Aussagen führten live weiterhin zu sichtbar gerundeten/weiß gerahmten Bildern.

VERMEIDUNGSREGEL:
Bei sichtbaren Bildrändern immer getrennt prüfen:
1. Quelldatei/Pixelecken,
2. IMG,
3. Wrapper,
4. Karten-Clipping.
Ein CSS-PASS reicht nicht, wenn das Artefakt im Bild selbst eingebrannt ist.

## AF-018 – Wiederkehrender Release-Ketten-Fehler vor Ausgabe 1.50.646 nicht geprüft
FEHLER:
Beim Hochziehen der Profilklasse auf V150646 wurden die gerouteten Owned-Templates nicht ebenfalls auf dieselbe Release-Version umgestellt. Die Templates blieben v150645 und riefen V150645 auf.

FOLGE:
WordPress-Runtime-Fatal / kritischer Fehler unmittelbar nach Installation.

URSACHE:
Es wurde PHP-Syntax geprüft, aber nicht die komplette aktive Release-Kette Mainplugin → Profilklasse → geroutete Templates → Template-Klassenaufruf.

VERMEIDUNGSREGEL:
Vor jedem neuen Template-Kit-ZIP zwingender Release-Chain-Test:
1. Plugin-Header/Plugin-VERSION;
2. require_once aktive Profilklasse;
3. class_exists-/Init-Bindung;
4. Profil-RELEASE;
5. route_template-Pfade;
6. Klassenaufrufe innerhalb beider Owned-Templates;
7. aktiver Stale-Reference-Scan auf die vorherigen Releaseklassen.
Kein ZIP-PASS ohne diese sieben Punkte.

## AF-019 – Beim Rollout 1.50.646/1.50.647 den akzeptierten Pilot neu implementiert statt unverändert zu vervielfältigen
FEHLER:
Nach akzeptiertem 1.50.645 wurde für den portalweiten Hub2-Rollout eine neue allgemeine Renderlogik gebaut. Dadurch gingen genau die zuvor abgenommenen Eigenschaften wieder verloren.

FOLGE:
1.50.647 war technisch lauffähig, aber visuell ein Rückschritt: Icons, andere Aufteilung und abweichender Hero-/Claim-/Textpfad.

VERMEIDUNGSREGEL:
Ein ausdrücklich akzeptierter Pilot ist beim Rollout künftig eine **harte Vorlage**:
- Markup und CSS nicht neu entwerfen;
- dieselben Klassen und dieselbe Reihenfolge wiederverwenden;
- nur Daten/Assets pro Zielseite austauschen;
- Regression gegen den Pilot vor Freigabe visuell messen;
- erst danach paketieren.

## AF-020 – „Textregeln kopieren“ fälschlich als „Pferdeatelier-Darstellung kopieren“ umgesetzt
FEHLER:
Beim Hub2-Rollout 1.50.648 wurden neben den gewünschten redaktionellen Pferdeatelier-Regeln auch Teile der Pferdeatelier-Accordion-Darstellung übernommen. Gleichzeitig durfte ein Parentbild als Kartenfallback mehrfach verwendet werden.

FOLGE:
Der akzeptierte Buch-&-Papier-Aufbau wurde erneut sichtbar verändert: zusätzlicher Textblock, gleiche Bilder in mehreren Karten und verlorene Karten-Unterzeilen.

VERMEIDUNGSREGEL:
Anforderungen künftig strikt in **Inhalt/Textregel** und **Darstellung/UI-Regel** trennen.
Wenn nur Textregeln kopiert werden sollen:
- Wortzahl, Ton, Substanz, Tabus und redaktionelle Qualitätsregel übernehmen;
- vorhandene Ziel-UI vollständig unangetastet lassen.
Bei Fotokarten:
- jede sichtbare Kindkarte braucht ein Foto;
- innerhalb derselben Seite keine wiederholte Foto-URL;
- Parent-/Hero-Bild niemals als Universalbild für alle Kinder;
- Untertitel ist Bestandteil des akzeptierten Kartenlayouts und darf beim Rollout nicht verloren gehen.

## AF-021 – Bild-URL-Eindeutigkeit erneut mit Bildqualität verwechselt
FEHLER:
1.50.649 wurde mit 328/328 Fotokarten und ohne doppelte URL lokal als Bild-Rollout freigegeben. Das bewies nur Belegung und Eindeutigkeit, nicht aber Motivpassung, Ruhe der Szene oder sinnvollen Bildausschnitt.

FOLGE:
Live waren mehrere Bilder zwar technisch verschieden, aber zu voll, zu nah, teilweise thematisch falsch oder durch ungeeignete Quellvarianten optisch gerahmt.

VERMEIDUNGSREGEL:
Für jede Bildfreigabe sind getrennt zu prüfen:
1. Slot/Geometrie;
2. Quelle ohne eingebrannten Rahmen;
3. semantische Motivpassung;
4. gewünschte Distanz/Zoom;
5. visuelle Ruhe/Klarheit;
6. Duplikatfreiheit.
Ein PASS in Punkt 1 oder 6 darf nie als Gesamt-Bild-PASS ausgegeben werden.

## AF-022 – Hero und Langtext bei mittleren Breiten zu lange gekoppelt
FEHLER:
Die Hub2-Darstellung hielt den langen Kategorietext bis zu zu kleinen Bildschirmbreiten im selben zweispaltigen Hero wie das Bild. Dadurch wurde auf Tablet/kleineren Desktopbreiten weder Text noch Bild sauber präsentiert.

FOLGE:
Der Text wurde schmal und hoch, das Bild daneben wirkte gedrängt; die Gestaltung war abhängig von Textlänge und Bildschirmbreite.

VERMEIDUNGSREGEL:
Responsive Hero-Komponenten dürfen nur kurze, höhenstabile Inhalte neben einem Bild tragen.
- Hero: Claim + H1 + kurzer Einstieger;
- Langtext: eigener Block unterhalb;
- klarer Breakpoint, bevor die Textspalte unruhig wird;
- Pflichtsimulation mindestens 1440/1200/1100/1024/900/760/600.

## AF-023 – Karten-Duplikatprüfung zunächst nur Karte↔Karte statt zusätzlich Hero↔Karte

FEHLER:
Ein Teil der bereits als Karten-PASS behandelten Motive verwendete dieselbe Ausgangsquelle wie das Hero derselben Hub2-Seite. Die frühere Duplikatprüfung hatte diesen Hero↔Karte-Fall nicht vollständig als eigene Sperre behandelt.

FOLGE:
13 Hero↔Karte-Gleichquellen wurden nachträglich gefunden. 11 konnten mit vorhandenen eigenständigen Motiven ersetzt werden; 2 wurden mangels sauberem Ersatz wieder als fehlend markiert.

VERMEIDUNGSREGEL:
Vor jedem Karten-PASS pro Hub2-Seite gemeinsam prüfen:
1. Karte↔Karte;
2. Hero↔Karte;
3. offensichtliche Motiv-Nahduplikate.
Nur ein eigener, fachlich eindeutiger Karten-Crop darf PASS erhalten.

## AF-024 – Karten als aktiv gezählt, obwohl Quellenkennung vom Renderer nicht akzeptiert wurde

FEHLER:
Zwei ergänzte Karten (`3d-druck`, `wandern`) waren als Dateien vorhanden und im Mapping gezählt, verwendeten aber zunächst eine Quellenkennung, die der aktive Renderer nicht akzeptierte.

FOLGE:
Die Karten hätten trotz vorhandener Datei im realen Pfad nicht zuverlässig gerendert.

FIX:
Quellenkennung auf den aktiven WIP-Vertrag `v150653` korrigiert und Assetpfade normalisiert.

VERMEIDUNGSREGEL:
Eine Karte zählt erst als aktiv, wenn gleichzeitig gilt:
- Mapping vorhanden;
- Quellenkennung vom aktiven Renderer akzeptiert;
- Datei real vorhanden;
- Zielcrop korrekt;
- semantischer Sichttest PASS.



## AF-025 – Arbeitscheckpoint hatte veraltete interne Karten-Metadaten

FEHLER:
Der persistente Arbeitscheckpoint `WIP_1.50.653_WORKING_75CARDS_NOT_RELEASE.zip` enthielt real 75 verschachtelte Karten-Mappings und alle 75 Dateien, führte im internen `meta.card_count` aber noch 73 und im protokollierten Neublock nur 5 statt 7 Einträge.

FOLGE:
Der reale Asset-/Mappingstand war korrekt, aber die interne Checkpoint-Metadatenlage widersprach der Current-Autorität und hätte spätere Prüfungen oder Rekonstruktionen irreführen können.

FIX:
ZIP direkt geprüft; `meta.card_count` auf 75 gesetzt und `pilze-kulturen/speisepilzzucht` sowie `audio-hifi/lautsprecherbau` im vollständigen 7er-Neublock ergänzt. Keine Assets und keine aktiven Mappings verändert.

VERMEIDUNGSREGEL:
Ein Checkpoint zählt erst als konsistent, wenn neben Mapping, Quelle, Datei und Crop auch seine internen Zähl-/Blockmetadaten gegen den realen Inhalt geprüft wurden.


## AF-026 – AF-018 trotz vorhandener Schutzregel bei 1.50.653 wiederholt

FEHLER:
Beim neuen Pluginstand 1.50.653 wurde derselbe Release-Ketten-Fehler wie bereits bei 1.50.646 erneut eingebaut. Das Main-Plugin lud die neue Profilklasse, während die aktiven gerouteten Templates noch die alte Releaseklasse aufriefen.

FOLGE:
WordPress-Fatal / kritischer Fehler unmittelbar nach Aktivierung bzw. beim Aufruf der gerouteten Hobby-Depot-Seiten.

URSACHE:
Die bereits seit AF-018 dokumentierte Release-Chain-Prüfung wurde vor Ausgabe des ZIPs nicht als harter automatischer Blocker durchgesetzt. Syntax-PASS und ZIP-Struktur wurden erneut fälschlich als ausreichend behandelt.

KORREKTUR:
1.50.653 ist als Installationspaket verworfen. 1.50.654 wurde so korrigiert, dass Main-Plugin, aktive Profilklasse, geroutete Templates und Klassenaufrufe dieselbe Releaseversion verwenden.

VERMEIDUNGSREGEL – AB SOFORT HARTE SPERRE:
Kein neues Hobby-Depot-Plugin-ZIP darf ausgegeben werden, solange nicht alle sieben AF-018-Punkte als ein gemeinsamer Release-Chain-Test PASS sind:
1. Plugin-Header/Plugin-VERSION;
2. require_once aktive Profilklasse;
3. class_exists-/Init-Bindung;
4. Profil-RELEASE;
5. route_template-Pfade;
6. Klassenaufrufe in beiden Owned-Templates;
7. Stale-Reference-Scan auf vorherige Releaseklassen.

Zusätzlich zwingend:
- Hauptplugin unter WordPress-Hook-Stubs laden;
- beide aktiven Templates mit der tatsächlich geladenen Profilklasse ausführen;
- bei irgendeiner alten Releaseklassen-Referenz: BUILD FAIL, kein ZIP, keine Freigabe.


## AF-027 – 1.50.654 live zurück auf generisches Theme gefallen; Bildvorschauen waren trotz vorhandener Dateien nicht verdrahtet

FEHLER:
1.50.654 wurde nach lokalen Syntax-/Klassenprüfungen ausgegeben, obwohl zwei reale Funktionspfade nicht ausreichend geprüft waren:
1. Der Live-Aufruf `/gestalten/druck-foto/` zeigte nach Installation nicht mehr das eigene Hobby-Depot-Template, sondern den generischen Theme-/Seitenstand.
2. Die 65 neuen 200×107-Kategorievorschauen lagen im Assetbaum, aber `next_level_card_photo()` für Ebene 1 verwendete weiterhin den alten `v150617/subcategories/*-v150634.webp`-Pfad.

ZUSÄTZLICHER SICHTFEHLER:
Seit der 1.50.651-Hero-Architektur ist die Hero-Copy ein Flex-Container. Der Claim blieb ohne `align-self:flex-start` und wurde deshalb horizontal gestreckt; dadurch wurde auch der Pinselstrich viel zu lang.

KORREKTUR:
1.50.654 verworfen. 1.50.655 wird vom funktionierenden 1.50.651-Code abgeleitet, ohne neue Profilklasse und ohne neue aktive Templates. Routing und aktive Templates bleiben byte-identisch zu 1.50.651. Nur Bildbindung, Ebene-1-Vorschaubilder, Unterstrich-Stretch und Hero-Seitenverhältnis werden korrigiert.

VERMEIDUNGSREGEL:
Bei reinen Bild-/Designänderungen keine neue Profilklasse und keine neuen gerouteten Template-Dateien erzeugen, solange Routing/Architektur nicht beauftragt sind.
Vor Ausgabe zwingend zusätzlich testen:
- Ebene-1-Vorschaubild-Resolver zeigt real auf den neuen Preview-Assetbaum;
- Hub2-Hero-Resolver zeigt real auf den neuen Hero-Assetbaum;
- mindestens ein kompletter bekannter Seitenpfad wird als `hub2` erkannt und auf das aktive Owned-Template geroutet;
- Flex-Claims werden auf tatsächliche Textbreite begrenzt;
- Bilddateimaß und CSS-Anzeigeverhältnis müssen zusammenpassen.


## AF-028 – Falsche Ausgangsbasis 1.50.651 trotz dokumentiertem LIVE FAIL weiterverwendet

FEHLER:
Nach den ersten 1.50.653-Fatals wurde mehrfach 1.50.651 als „funktionierender Runtime-Code“ behandelt und daraus 1.50.654–1.50.656 abgeleitet.

DAS WAR FALSCH:
Die autoritative Fehlerhistorie führt 1.50.651 ausdrücklich als **LIVE FAIL / verworfen**. Der letzte bestätigte Stand mit **Text PASS + Grundaufteilung PASS** war 1.50.650.

FOLGE:
Mehrere Reparaturpakete wurden auf einer bereits verworfenen Basis aufgebaut und verschlechterten den realen Zustand weiter.

KORREKTUR:
Historischer damaliger Reparaturansatz: direkt aus dem originalen 1.50.650-Paket, 55 PHP-Dateien und alle Nicht-Bild-Dateien byte-identisch, ausschließlich Bilddateien ersetzt. **Der damals hier verwendete Hero-Wert 600×220 wurde später durch AF-038 als falsch nachgewiesen und ist nicht mehr gültig; aktuell gilt 600×320.**

VERMEIDUNGSREGEL:
Bei einem bereits dokumentierten LIVE FAIL darf die betroffene Version niemals wieder als „funktionierende Basis“ bezeichnet oder als technische Ausgangsbasis verwendet werden. Basiswahl künftig ausschließlich aus dem letzten explizit live bestätigten PASS-Stand.


## AF-029 – Normale Plugin-Überschreibung weiterverwendet, obwohl der Restore-PHP-Code bereits byte-identisch zu 1.50.650 war

FEHLER:
Nach 1.50.653–1.50.656 wurde noch ein weiterer normaler Replace-Build ausgegeben:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_RUNTIME_RESTORE_NEW_IMAGES.zip`.
Dessen 55 PHP-Dateien waren byte-identisch zum originalen 1.50.650-Stand; geändert waren ausschließlich 130 WebP-Dateien. Trotzdem zeigte der reale Frontend-Aufruf erneut den WordPress-kritischen Fehler.

BEDEUTUNG:
Der konkrete Live-Fatal darf damit nicht weiter durch erfundene neue PHP-Codeursachen dieses Restore-ZIPs erklärt werden. Ohne Server-Fatal-Log ist die exakte Live-Zeile unbekannt.

ARBEITSFEHLER:
Trotz der Abweichung „lokal grün / live fatal“ wurde der gleiche normale Überschreibungsweg erneut verwendet, anstatt den realen Updatezustand selbst – alter Pluginordner, stale Dateien, PHP-/Object-/Page-Caches und Request-Grenze – als eigenen E2E-Fall zu simulieren.

KORREKTUR 1.50.657:
Kein weiterer normaler Replace-Build. Ein eigenständiger Repair Installer wurde gebaut, der:
1. Payload vorab vollständig per SHA-256 prüft;
2. das alte Template Kit deaktiviert;
3. den kompletten alten Pluginordner rekursiv entfernt;
4. den bekannten 1.50.650-Runtime-Payload sauber neu kopiert;
5. alle 981 Ziel-Dateien erneut per SHA-256 prüft;
6. Statcache, OPcache und verfügbare WP/Page-Caches leert;
7. das Template Kit erst im nächsten Admin-Request aktiviert;
8. sich nach erfolgreicher Zielaktivierung selbst deaktiviert.

E2E-NACHWEIS:
Der Repair-Ablauf wurde jeweils aus vier verschmutzten Ausgangsständen 1.50.653, 1.50.654, 1.50.655 und 1.50.656 über drei getrennte Request-Grenzen simuliert.
Alle vier: Repair PASS → Aktivierung PASS → `/gestalten/druck-foto/` Routing/Render PASS → Negativroute bleibt Theme.
Zusätzlich Negativtests:
- beschädigter Payload stoppt vor Eingriff in den alten Pluginordner;
- manipuliertes Ziel nach Kopie wird nicht aktiviert.

VERMEIDUNGSREGEL:
Wenn ein Restore-Paket codegleich zum letzten bestätigten Runtime-Stand lokal PASS ist, live aber weiter fatal läuft, darf nicht erneut nur ein weiteres normales Replace-ZIP gebaut werden. Dann muss zuerst der komplette Installations-/Cache-/Request-Zustand als E2E-Szenario reproduziert und bereinigt werden.


## AF-030 – Reparaturserie wirkte im realen Frontend nicht; lokale Teiltests wurden zu früh als ausreichende Freigabe behandelt

FEHLER:
Nach 1.50.653 wurden mehrere Reparaturpakete ausgegeben, obwohl der reale Nutzer-Screenshot weiterhin denselben kritischen Fehler zeigte.

BELASTBARER NACHWEIS:
Der zentrale Seitenbereich der Screenshots 17:21, 18:05 und 18:34 ist pixelidentisch. Damit ist belegt, dass die späteren Reparaturversuche den sichtbar gerenderten Frontendzustand nicht verändert haben.

URSACHE DER ARBEITSWEISE:
Lokale Syntax-, Routing-, Stub- und Dateibaumtests wurden wiederholt als ausreichende Grundlage für ein neues Installationspaket behandelt. Nach der ersten Abweichung „lokal PASS / live weiterhin kritisch“ hätte keine weitere normale Überschreibungsrunde stattfinden dürfen.

KORREKTUR:
1.50.658 ist kein weiterer blinder Template-Kit-Build. Der Recovery-Prozess prüft den realen WordPress-Server per Loopback vor und nach jeder Kandidatenaktivierung und behält einen Kandidaten nur bei echtem Frontend-PASS. Andernfalls wird der nächste Kandidat getestet bzw. automatisch auf den vorherigen exakten Plugin-Snapshot zurückgerollt.

LOKALE SCHUTZPRÜFUNG:
11/11 Positiv-/Negativ-/Rollback-Szenarien PASS, einschließlich:
- vier reale kaputte Ausgangsbäume 1.50.653–1.50.656;
- 1.50.652-Backup bevorzugt;
- 1.50.652 Frontend-/Aktivierungs-Fail → 1.50.650-Fallback;
- alle Kandidaten fail → exaktes Rollback;
- korrupter Payload → exaktes Rollback;
- doppelte aktive Kit-Kopie → Deaktivierung;
- gesundes Frontend → keinerlei Ersetzung.

VERMEIDUNGSREGEL:
Sobald lokaler Test und reales Livebild auseinanderlaufen, ist jeder weitere normale Release-/Replace-Build gesperrt. Der nächste Schritt muss den realen Serverpfad selbst als Gate prüfen und bei Nicht-PASS automatisch rückrollen. Kein weiterer Kandidat darf allein wegen lokaler Stub-/Syntax-/Dateiprüfung empfohlen werden.


## AF-031 – Hero-Only 1.50.659 änderte entgegen der Vorgabe zusätzlich das Mapping

FEHLER:
1.50.659 wurde als „nur Heroes“ ausgegeben, änderte aber zusätzlich den `heroes`-Block in `assets/hobby-depot-v150650/hub2-image-map.json`.

FOLGE:
Die ausdrückliche Vorgabe „nur vorhandene Fotos austauschen, Finger weg von Architektur/System“ wurde erneut unnötig erweitert.

KORREKTUR:
1.50.659 verworfen.
1.50.660 liest das bestehende aktive Mapping nur aus und überschreibt ausschließlich die 65 dort bereits referenzierten Hero-WebP-Dateien. Mapping, PHP, Templates, Routing, CSS, Karten und Architektur bleiben unverändert.

LOKALER NACHWEIS:
- pristine 1.50.650: exakt 65 Datei-Diffs, ausschließlich die 65 gemappten Hero-WebPs;
- Mapping byte-identisch;
- 0 PHP-Dateien geändert;
- zusätzlich gegen einen bereits mit 1.50.659 veränderten Zustand simuliert: 65/65 aktuell gemappte Hero-Zieldateien korrekt ersetzt.

VERMEIDUNGSREGEL:
Bei Auftrag „nur Bilder austauschen“ dürfen keine Mapping-, PHP-, Template-, Routing-, CSS- oder Versionslogikänderungen vorgenommen werden. Es werden ausschließlich die bereits aktiven Bilddateien an ihren bestehenden Zielpfaden ersetzt.


## AF-032 – Technischer 65er-Dateiaustausch 1.50.660 ohne ausreichende visuelle Motivfreigabe

FEHLER:
1.50.660 erfüllte technisch die Vorgabe „nur bestehende Bilddateien ersetzen“, wurde aber ausgegeben, obwohl der 65er-Bildsatz visuell nicht ausreichend auf Distanz, Schärfe, Motivpassung und Wiederholungen freigegeben war.

LIVE-BEFUND:
Der Nutzer verwarf 30 Heroes ausdrücklich. Grundsätzlich: unscharf und/oder zu klein bzw. viel zu dicht rangezoomt. Zusätzlich wurden bei mehreren Kategorien falsche Motive und Doppelungen benannt.

KORREKTUR:
1.50.660 ist für diese 30 Heroes verworfen. 1.50.661 ersetzt ausschließlich diese 30 aktuell gemappten Bilddateien. Mapping, Runtime, Templates, Routing, CSS, Karten und Architektur bleiben unangetastet.

SCHUTZPRÜFUNG 1.50.661:
- historisch exakt 30 Payload-Dateien; **der damalige 600×220-Wert ist durch AF-038 verworfen, aktuell gilt 600×320**;
- 30 SHA-eindeutig;
- lokaler Schärfecheck;
- perzeptueller Duplikatcheck;
- echte PHP-Aktivierung E2E auf pristine 1.50.650;
- echte PHP-Aktivierung E2E auf simuliertem Nach-1.50.659+1.50.660-Zustand;
- in beiden Fällen exakt 30 Datei-Diffs, Mapping unverändert, übrige 35 Heroes unverändert, 0 PHP-Diffs.

VERMEIDUNGSREGEL:
Bei Bildaufträgen ist die visuelle Prüfung vor dem Release gleichrangig mit der technischen Dateiprüfung. Kein Bildsatz wird wegen korrekter Maße/Hashes/Pfade als fertig bezeichnet. Distanz, Motiv, Schärfe und sichtbare Wiederholungen müssen separat geprüft werden; Live-Abnahme bleibt bis zur Sichtprüfung offen.


## AF-033 – 1.50.661 hatte den falschen Pluginordner und war deshalb keine Überinstallation

FEHLER:
1.50.661 wurde als Nachfolger des bereits installierten Hero-Replace-Plugins ausgegeben, verwendete aber den neuen Ordner `hobby-depot-hero-replace-30-only-150661`.

FOLGE:
WordPress behandelte 1.50.661 als separates Plugin statt als Überinstallation/Ersetzung von 1.50.660.

KORREKTUR:
1.50.662 verwendet exakt den bestehenden 1.50.660-Pfad:
- `hobby-depot-hero-replace-only-150660/`
- `hobby-depot-hero-replace-only-150660.php`

Zusätzlich wurde der reale In-Place-Overwrite-Fall lokal simuliert, bei dem das Plugin bereits aktiv ist und der Activation Hook deshalb nicht als Ausführungsgrundlage vorausgesetzt werden darf. 1.50.662 führt den Bildaustausch in diesem Fall einmalig beim nächsten Admin-Request aus.

LOKALER NACHWEIS:
- aktive Plugin-Dateireferenz vor/nach Overwrite identisch;
- 1.50.660 zunächst real ausgeführt;
- Pluginordner anschließend durch 1.50.662 ersetzt;
- kein erneuter Activation Hook;
- 1.50.662 trotzdem PASS über one-shot admin_init;
- exakt 30 Hero-Diffs, 35 unverändert, Mapping unverändert, 0 Template-Kit-PHP-Diffs.

VERMEIDUNGSREGEL:
Ein Plugin-Update, das ausdrücklich „überinstalliert“ werden soll, muss vor Ausgabe denselben Top-Level-Pluginordner und dieselbe Main-Plugin-Datei wie die installierte Vorgängerversion besitzen. Zusätzlich muss der Updatepfad bei bereits aktivem Plugin ohne erneuten Activation Hook getestet werden.


## AF-034 – 1.50.662 lief nach Überinstallation nur im Admin und konnte bei direkter Frontend-Prüfung wirkungslos bleiben

FEHLER:
Der 1.50.662-In-Place-Updatepfad setzte voraus, dass nach der Überinstallation ein weiterer Admin-Request mit `admin_init` stattfindet.

FOLGE:
Bei direktem Wechsel vom Upload/Replace-Vorgang zur Frontend-Prüfung wurde der 30er-Bildaustausch nicht ausgeführt. Die sichtbaren Heroes blieben daher unverändert. Die danach genannte Cache-Erklärung war nicht belastbar und ist verworfen.

KORREKTUR:
1.50.663 behält exakt denselben Pluginordner und dieselbe Hauptdatei, hängt den einmaligen Austausch aber an `plugins_loaded`. Dadurch läuft er auf dem ersten folgenden WordPress-Request – Admin oder Frontend.

LOKALER NACHWEIS:
In-Place-Overwrite eines aktiven Vorgängers simuliert; Activation Hook nicht aufgerufen; admin_init nicht aufgerufen; nur plugins_loaded ausgelöst:
- PASS;
- APPLIED=1;
- exakt 30 Zielbilder geändert;
- 35 unverändert;
- Mapping byte-identisch;
- 0 Template-Kit-PHP-Diffs.

VERMEIDUNGSREGEL:
Bei In-Place-Updates aktiver Helper-Plugins darf die eigentliche Migration nicht an einen Admin-only-Hook gebunden sein, wenn der Nutzer unmittelbar im Frontend prüft. Der reale nächste Requestpfad muss E2E simuliert werden.


## AF-035 – 1.50.663 recycelte Grundszenen und erzeugte Bild-in-Bild statt echter kategoriespezifischer Heroes

FEHLER:
Obwohl bereits verbindlich festgelegt war, pro Kategorie ein eigenständiges, semantisch klares, weit gefasstes Motiv zu verwenden, wurde für 1.50.663 ein kleiner Bestand an Grundszenen mehrfach wiederverwendet. Teilweise wurden nur andere Ausschnitte derselben Szene benutzt; zusätzlich entstanden sichtbare Bild-in-Bild-/Collage-Kompositionen.

LIVE-BEFUND:
Der Nutzer hat 1.50.663 visuell verworfen. Besonders bestätigt:
- Papierkunst: Bild in Bild;
- Schrift & Lettering: Bild in Bild;
- Holz: falsches Motiv;
- Leder: falsches Motiv;
- Keramik & Glas: Bild in Bild;
- Mechanik & Uhren: falsches Motiv + Bild in Bild;
- Astronomie: falsches Motiv + Bild in Bild;
- Messen & Analysieren: falsches Motiv;
- Mikroskopie: falsches Motiv + Bild in Bild;
- Wetter & Umwelt: falsches Motiv + Bild in Bild;
- Gärtnern: doppelt;
- Moos & Miniaturgärten: falsches Motiv + doppelt;
- Pilze & Kulturen: falsches Motiv;
- Ameisen & Insekten: falsches Motiv;
- Wirbellose: falsches Motiv + dreifach;
- Naturfunde: verworfen;
- Spielzeug & Spiele: falsches Motiv;
- Technik & Medien: falsches Motiv + Bild in Bild.

URSACHE:
Technische Positiv-/Negativtests prüften Dateiaustausch, Mapping, Hooks und Integrität, aber nicht ausreichend die semantische Einzigartigkeit der **Ausgangsquelle**. Unterschiedliche Dateien/Crops wurden erneut fälschlich als unterschiedliche Motive behandelt.

KORREKTUR:
1.50.663 ist vollständig verworfen. Seine Ausgangsszenen dürfen für die verworfenen Kategorien weder direkt noch als Crop/Teilbild/Collage erneut verwendet werden.

VERMEIDUNGSREGEL:
Vor jedem nächsten Hero-Release muss für jede Kategorie eine Quellen-ID geführt werden. PASS nur wenn:
1. Quelle fachlich eindeutig passt;
2. Quellen-ID innerhalb des freizugebenden Satzes einzigartig ist;
3. kein Crop derselben Quelle als zweite Kategorie vorkommt;
4. kein Bild-in-Bild/Compositing verwendet wird;
5. Hero als breite Szene mit erkennbarem Hauptmotiv funktioniert;
6. menschlicher Sichtcheck vor ZIP-Bau erfolgt.


## AF-036 – Nach erfolgreichem Einzelmotiv-Start wieder in Sammel-/Collage-Generierung abgerutscht

FEHLER:
Nach dem vollständigen Verwerfen von 1.50.663 wurde korrekt mit neuen eigenständigen Einzelmotiven begonnen. Der Nutzer bewertete diesen Ansatz ausdrücklich positiv. Danach wurden jedoch wieder Sammelbilder/Collagen mit mehreren Themen erzeugt.

FOLGE:
- Themen wurden erneut mehrfach besetzt;
- verschiedene Kategorien waren nicht mehr sauber 1:1 einer Quelle zuordenbar;
- mindestens Mechanik & Uhren tauchte erneut mehrfach auf;
- die bereits festgelegte Regel „eine Kategorie = eine eigenständige Quelle“ wurde dadurch wieder verletzt.

BELASTBARER POSITIVER ZWISCHENSTAND:
Die neuen Einzelmotiv-Richtungen für Astronomie, Papierkunst, Miniaturen & Szenen, Textilgestaltung, Malen & Zeichnen und Schrift & Lettering wurden vom Nutzer positiv beurteilt.
Dies ist **kein Release-/Live-PASS**. Bei Miniaturen & Szenen existieren mehrere Kandidaten; kein einzelner ist final festgelegt.

KORREKTUR:
- Sammel-/Collage-/Montageausgaben werden nicht als fertige Heroes gewertet;
- vor jeder weiteren Generierung wird der vorhandene Bestand auf 30 Kategorien auditierbar gemacht;
- pro Kategorie exakt eine Quelle oder FEHLEND;
- neue Generierung nur für tatsächlich fehlende Kategorien;
- Pluginbau erst nach abgeschlossenem 30/30-Quellenaudit.

VERMEIDUNGSREGEL:
Bildproduktion und Pluginbau strikt trennen:
1. Quellen auswählen/generieren;
2. 1:1-Zuordnung;
3. semantischer/visueller Audit;
4. Duplikat-/Quellenidentitätscheck;
5. erst danach Assets ableiten und einmalig paketieren.


## AF-037 – Einzelbild-Fortsetzung erzeugte erneut generische 24er-Collagen

FEHLER:
Nach der Nachprüfung des Vorschau-/Quellenstands wurde die Fortsetzung ausdrücklich als einzelnes Holz-Hero bzw. als getrennte Einzelbilder ohne Collage angewiesen. Die Bildgenerierung lieferte trotzdem generische 24er-Hobby-Raster mit Beschriftungen und fachfremden Themen.

FOLGE:
- die Ausgaben verletzen die harte Regel `1 Kategorie = 1 eigenständige Ausgangsquelle`;
- sie enthalten Beschriftungen, Raster und zahlreiche fachfremde Motive;
- sie sind für den Hero-Bestand vollständig unbrauchbar;
- sie zählen als Quelle/Kandidat **0** und dürfen nicht paketiert oder gemappt werden.

KORREKTUR:
- diese Fehlbilder nicht wiederverwenden;
- keine weitere Sammel-/Mehrfachgenerierung aus diesem fehlerhaften Lauf;
- die 23 offenen Kategorien sind jetzt einzeln mit eindeutigen Motivvorgaben in `HERO_EINZELQUELLEN_WORKLIST_23_20261015.md` gebunden;
- bestehende Vorschau-Sammelbilder bleiben nur Richtungsreferenz, niemals Quelle.

VERMEIDUNGSREGEL:
Eine neue Quelle darf nur als PASS gelten, wenn das erzeugte Ergebnis tatsächlich **ein einziges unbeschriftetes Motiv für genau die angeforderte Kategorie** enthält. Jede Raster-/Poster-/Collage-Ausgabe wird sofort verworfen und nicht weiterverarbeitet.


## AF-038 – Hero-Zwischenmaß 600×220 ohne Prüfung der eingefrorenen 1.50.650-CSS übernommen

FEHLER:
Im technischen 7er-WIP wurde zunächst ein Hero-Dateimaß von 600×220 abgeleitet, ohne vorher das tatsächlich aktive Seitenverhältnis der eingefrorenen 1.50.650-Basis direkt zu prüfen.

NACHPRÜFUNG:
Die echte 1.50.650-Laufzeit verwendet für den Hub2-Hero `aspect-ratio:600/320` und `object-fit:cover`. Der Zielvertrag verlangt keinen 600×220-Dateistandard.

KORREKTUR:
- der 600×220-Zwischenstand ist verworfen;
- Hero-Dateien neu als **600×320** abgeleitet;
- Previews bleiben **200×107**;
- reale 1.50.650-Basis erneut als reiner Bildersatz simuliert;
- exakt 14 Bilddateien geändert, 0 Code-/CSS-/Mapping-/JSON-Änderungen;
- Mapping byte-identisch;
- ZIP-Roundtrip 981/981 PASS;
- kein Plugin/Release wurde aus dem falschen Zwischenmaß freigegeben.

VERMEIDUNGSREGEL:
Vor jeder Asset-Ableitung zuerst das aktive Render-Seitenverhältnis der eingefrorenen Basis prüfen. Ein Bildmaß darf nicht aus Erinnerung oder aus einem früheren Reparaturstand übernommen werden.


## AF-039 – Geplanter neuer 8er-Fotoblock wurde von der Sammelgenerierung inhaltlich nicht geliefert

FEHLER:
Im Nachbarchat war am 2026-10-15 gegen 08:08–08:09 UTC ausdrücklich ein neuer 8er-Fotoblock festgelegt:
Guss & Formen; Heimwerken; Robotik & Automation; Ameisen & Insekten; Wirbellose; Wind & Drachen; Klettern & Seil; Wasser.

Die unmittelbar danach gespeicherten Sammelbilder lieferten jedoch nicht diesen 8er-Satz. Stattdessen wurden bereits vorher verwendete Themen wie Töpferei, Uhren, Mikroskopie, Wetter, Garten und Pilze erneut dargestellt.

FOLGE:
Für Heimwerken, Robotik & Automation, Wirbellose, Wind & Drachen, Klettern & Seil und Wasser ist die neue Produktionsabsicht belegt, aber keine gültige neue Einzelquelle aus diesem Lauf vorhanden. Die fehlerhaften Sammelbilder dürfen für diese sechs Kategorien nicht als Quelle umgedeutet werden.

KORREKTUR:
- Guss & Formen bleibt durch die separat vorhandene neue Einzelquelle abgedeckt.
- Ameisen & Insekten besitzt eine andere neu gebundene Vorschau-Richtung.
- Die sechs übrigen Kategorien werden nur als **Bestandteil des vom Nutzer akzeptierten neuen 8er-Blocks belegt** geführt. Eine konkrete Motivrichtung ist daraus nicht rekonstruierbar und darf nicht erfunden werden.
- Keine alte 1.50.653-/1.50.663-Datei wird als Ersatz verwendet.

VERMEIDUNGSREGEL:
Nach jeder Mehrfachgenerierung muss das tatsächliche Bildresultat gegen die angeforderten Kategorien geprüft werden. Ein angekündigter 8er-Block zählt nicht als produziert, wenn die Ausgabebilder andere oder wiederholte Themen enthalten.


## AF-040 – Bildgenerator ignorierte Einzelmotiv-Auftrag und erzeugte Plugin-/Statusgrafiken

FEHLER:
Beim Versuch, aus der exakt gebundenen Holz-Referenz eine neue eigenständige Einzelquelle zu erzeugen, lieferte der Bildgenerator zweimal fachfremde Plugin-/Statusinfografiken statt eines Holzmotivs.

Betroffene Ausgaben:
- `file_00000000d654820aa38cee0e4660af0f`
- `file_00000000d49481f69adc2b2223a606a2`

FOLGE:
Beide Ausgaben sind vollständig ungültig und zählen als Bildquelle **0**.

KORREKTUR:
- keine der beiden Dateien wird in Current, Manifest, Queue, Mapping oder Plugin übernommen;
- Bildgenerierung über diesen fehlerhaften Pfad wurde abgebrochen;
- bestehender Stand 7 echte Quellen + 13 exakt gebundene Richtungen + 10 BLOCKED bleibt unverändert.

VERMEIDUNGSREGEL:
Nach einer fachfremden Bildgenerator-Ausgabe nicht erneut blind denselben Pfad benutzen. Eine Ausgabe zählt nur, wenn das tatsächliche Bild die angeforderte Kategorie als einzelnes Motiv zeigt.


## AF-041 – Münzen-&-Geld-Preview-Zielpfad in 30er-Plan falsch geschrieben

FEHLER:
Der 30er-Zielplan führte für die Kategorie `Münzen & Geld` den Preview-Pfad
`subcategories/sammeln/munzen-geld-v150634.webp`.
Dieser Pfad existiert in der eingefrorenen 1.50.650-Basis nicht.

URSACHE:
Der Hero-Map-Pfad verwendet historisch `munzen-geld-v150623.webp`, während die Hub1-Preview-Auflösung im aktiven Renderer über den Alias
`munzen-geld => muenzen-geld`
auf `muenzen-geld-v150634.webp` zeigt.

NACHWEIS:
Der vollständige synthetische 30er-Overlay-Test fand exakt diesen einen fehlenden Zielpfad; alle übrigen 59 Zielpfade waren vorhanden.

KORREKTUR:
- Hero bleibt: `subcategories/sammeln/munzen-geld-v150623.webp`.
- Preview korrigiert auf: `subcategories/sammeln/muenzen-geld-v150634.webp`.
- Manifest und Zielpfad-Dokument korrigiert.
- vollständiger 30er-Overlay-Test danach erneut ausführen.

VERMEIDUNGSREGEL:
Bei Hero und Preview nicht aus Dateinamenssymmetrie schließen. Preview-Pfade immer gegen die aktive Alias-Auflösung des eingefrorenen 1.50.650-Renderers plus reale Datei-Existenz prüfen.


## AF-042 – Plugin angeboten, obwohl nur technische und keine vollständige visuelle Abnahme vorlag

FEHLER:
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.660.zip` wurde als fertiges Plugin angeboten, nachdem lediglich Struktur/Dateimengen/Mapping technisch geprüft worden waren.

Nach vollständiger Sichtprüfung der 65 Bilder zeigte sich der Bildsatz als VISUAL FAIL mit mehreren semantisch falschen Motiven und Wiederholungen.

URSACHE:
Technischer PASS wurde fälschlich wie Bild-/Release-PASS behandelt.

KORREKTUR:
- 1.50.660 nicht installieren / nicht verwenden;
- temporär erneut erzeugter Downloadlink entfernt;
- spätere Arbeitskopien von 1.50.660–1.50.663 aus `_working` wieder entfernt;
- neuerer Bildarbeitsstand bleibt erhalten;
- Current und Plugin-Current auf harte Vorab-Abnahmeregel korrigiert.

VERMEIDUNGSREGEL:
**Niemals ein Bild-Plugin anbieten, bevor jedes reale Bild visuell geprüft UND der vollständige Plugin-Einbau lokal simuliert wurde. Technische Dateiprüfung allein ist ausdrücklich unzureichend.**
## AF-043 – AF-026 in 1.50.671 erneut wiederholt: neue Profilklasse, alte aktive Templates

FEHLER:
1.50.671 lud Hobby_Depot_Profile_V150671, routete aber weiterhin auf die aktiven 1.50.670-Templates. Diese riefen Hobby_Depot_Profile_V150670 auf, obwohl diese Klasse im Paket nicht vorhanden war.

FOLGE:
WordPress-Fatal / kritischer Fehler auf den gerouteten Hobby-Depot-Seiten.

BELASTBARER NACHWEIS:
- Fronttemplate: Class "Hobby_Depot_Profile_V150670" not found;
- Contenttemplate: derselbe Fehler.

URSACHE DER ARBEITSWEISE:
Der seit AF-026 verbindliche siebenstufige Release-Chain-Test wurde bei 1.50.671 erneut nicht als tatsächlicher Blocker ausgeführt. PHP-Lint und ZIP-Prüfung konnten diesen Klassenkettenfehler nicht erkennen.

KORREKTUR:
1.50.671 verworfen. 1.50.672 bindet alle sieben aktiven Punkte auf dieselbe Releaseversion und wurde zusätzlich durch reales Ausführen beider aktiven Templates geprüft.

VERMEIDUNGSREGEL – HART:
Kein Designplugin-ZIP mehr freigeben, bevor der AF-026-Test tatsächlich ausgeführt und protokolliert ist. Beide von route_template() gelieferten Owned-Templates müssen mit der tatsächlich geladenen Profilklasse ausgeführt werden. Zusätzlich muss der vorherige kaputte Release als Negativtest exakt scheitern und der neue Release im Dirty-Overlay-Fall bestehen.

## AF-044 – 1.50.674 nur auf breitem Desktop simuliert; responsive Altpfad und Textableitung übersehen

FEHLER:
1.50.674 wurde als Fullbleed-Hero-Kandidat freigegeben, obwohl die neue Regel nur oberhalb 1100 px wirkte. Darunter blieb die alte Hub2-Regel mit begrenzter Bildbreite aktiv. Gleichzeitig wurde der Hero-Einstieg weiterhin aus dem ersten Satz des langen Kategorietextes erzeugt.

FOLGE:
- bei bestimmten Fensterbreiten rechter Leerraum / nicht vollbreites Bild;
- Text/Claim wirkten wieder wie alter Stand;
- freigegebene Kurzzeile erschien nicht;
- Nutzer musste denselben Responsive-/Renderfehler erneut live finden.

KORREKTUR:
1.50.674 verworfen.
1.50.675 trennt Hero-Kurztext und Langtext technisch, führt eine zentrale Fullbleed-Klasse ein und simuliert den Hero bei 1440, 1180, 1024, 901, 900, 800, 760, 600 und 390 px.

VERMEIDUNGSREGEL – HART:
Kein Hub2-Hero-Release mehr nur mit einem Desktop-Screenshot oder reinem CSS-Stringcheck. Vor Release müssen mindestens breite Desktop-, schmale Desktop-/Tablet- und Mobilbreite mit dem tatsächlich gerenderten HTML simuliert werden. Dabei sind Bildbreite, horizontaler Overflow, Innenabstand, Claim, H1 und Hero-Kurztext explizit zu prüfen. Der Hero-Kurztext darf nicht implizit aus dem Langtext abgeleitet werden, wenn ein eigener freigegebener Kurztext existiert.

## AF-045 – 1.50.675 ZIP ohne bestehenden Plugin-Wurzelordner gepackt

FEHLER:
Die erste 1.50.675-ZIP enthielt die Plugin-Dateien direkt an der ZIP-Wurzel statt unter `affiliate-portal-template-kit/`.

FOLGE:
WordPress konnte den Upload nicht als dieselbe vorhandene Plugin-Installation erkennen und bot daher keine normale Überinstallation des bestehenden Template-Kits an.

URSACHE:
Beim Packen wurde der **Inhalt** des Pluginordners gezippt statt der Pluginordner selbst.

KORREKTUR:
Keine Codeänderung. Die exakt gleichen 1041 Dateien wurden neu unter `affiliate-portal-template-kit/` gepackt. Innendateien 1041/1041 byte-identisch.

VERMEIDUNGSREGEL – HART:
Vor jedem WordPress-Plugin-Release zusätzlich zum Code-/ZIP-Test den Installer-Pfad gegen die letzte real installierbare Version prüfen:
1. identischer Top-Level-Pluginordner;
2. identische Main-Datei relativ zu diesem Ordner;
3. Plugin-Header vorhanden;
4. simulierter Overlay-Pfad entspricht exakt `wp-content/plugins/<bestehender-pluginordner>/...`.
Ein ZIP-Test allein reicht nicht.

## AF-046 – Claim als Flex-Kind gestreckt, dadurch Pinselunterstrich viel zu lang

FEHLER:
Im 1.50.675-Fullbleed-Hero war der Claim ein Flex-Kind ohne eigenes align-self/width. Dadurch streckte ihn der Flex-Container quer über die Copy-Fläche. Der Pinselunterstrich mit prozentualer Breite wurde deshalb viel länger als der sichtbare Claimtext.

FOLGE:
Unterstrich optisch stark überzogen; Claim/H1-Abstand wirkte gedrängt.

KORREKTUR:
1.50.676 setzt für den Fullbleed-Claim `align-self:flex-start` und `width:max-content`. Der Unterstrich wird zusätzlich auf 74 % der echten Claimbreite begrenzt. Claim wird etwas nach oben gesetzt und der Abstand zur H1 vergrößert.

VERMEIDUNGSREGEL:
Pseudo-Elemente mit prozentualer Breite dürfen in Flex-Spalten nicht auf einem gestreckten Inline-Element basieren. Vor Freigabe muss die reale Elementbreite des Claim-Wrappers explizit gebunden sein.

## AF-047 – starres 3/4-Bildziel drängte in den Textbereich; H1 konnte live umbrechen

FEHLER:
Der 1.50.677-Pilot reduzierte den geschützten Text-/Beigebereich zu stark zugunsten eines ungefähr 3/4 breiten Bildanteils. Im echten Frontend konnte dadurch die H1 `Audio & HiFi` umbrechen; gleichzeitig war die Bildfläche im Verhältnis zur Textlesbarkeit zu aggressiv.

FOLGE:
Die zentrale Gestaltungsregel `H1 auf Desktop einzeilig` war nicht zuverlässig erfüllt. Ein starres Verhältnis ist für unterschiedlich lange Kategorienamen ungeeignet.

KORREKTUR:
1.50.678 ersetzt das starre Verhältnis durch einen zentralen dynamischen Textschutzbereich ohne JavaScript:
- Breite folgt dem realen Schriftblock;
- Desktop begrenzt auf ca. 35–48 %;
- 901–1180 px begrenzt auf ca. 42–58 %;
- H1, Claim und Kurzzeile nowrap;
- kompletter Schriftblock etwas höher;
- <=900 px gestapelte Variante.

VERMEIDUNGSREGEL – HART:
Bei Hub2-Heroes kein starres Bild/Text-Verhältnis als Portalregel verwenden, wenn unterschiedlich lange H1 vorkommen. Der Textschutzbereich muss zentral begrenzt dynamisch sein; H1 und Hero-Kurztext müssen vor Release bei kurzen und langen Titeln gegen Umbruch geprüft werden. Kein JavaScript-/DOM-Messweg dafür einführen, solange CSS genügt.

## AF-048 – 1.50.678 als Local-Hard-PASS geführt, obwohl Visual-Harness den realen Hero nicht vollständig prüfte

FEHLER:
Der 1.50.678-Stand wurde zunächst als LOCAL HARD PASS dokumentiert. Bei der Abschluss-Nachprüfung zeigte der vorhandene lokale Screenshot jedoch zwei nicht erfüllte Abnahmebedingungen:
- Claim oben sichtbar angeschnitten;
- das eigentliche Hero-Bild wurde im Harness nicht geladen/gerendert.

Damit war der reale Bild/Text-Übergang nicht sichtbar geprüft. Zusätzlich fehlt eine dokumentierte lokale Positiv- UND Negativ-E2E-Simulation des real relevanten Renderpfads.

FOLGE:
Der Hard-PASS war nicht belastbar und hätte nicht als Upload-/Deploymentfreigabe verwendet werden dürfen.

KORREKTUR:
- Hard-PASS zurückgezogen;
- 1.50.678 bleibt nur gebauter technischer Stand;
- Current, Plugin-Current und Manifest auf VISUELLE E2E-PRÜFUNG OFFEN korrigiert;
- CURRENT.zip bleibt unverändert;
- vor Live-Installation muss der tatsächliche Plugin-Renderweg mit geladenem Hero-Bild positiv und negativ geprüft werden.

VERMEIDUNGSREGEL – HART:
Ein Screenshot-/Browser-Harness zählt nur als Visual-PASS, wenn alle für die Änderung maßgeblichen echten Assets tatsächlich geladen sind und der komplette Zielbereich sichtbar ist. Abgeschnittene Elemente oder nicht geladene Hero-Bilder sind automatisch FAIL. Zusätzlich bleibt die projektweite Pflicht zu positiver UND negativer lokaler Simulation bestehen.



## AF-049 – 1.50.679 wiederholt bereits bekannten Versionsketten-Fatal

FEHLER:
1.50.679 wurde freigegeben, obwohl die aktive Profilklasse V150679 in `route_template()` weiterhin die V150678-Templates zurückgab. Diese Templates riefen wiederum `Hobby_Depot_Profile_V150678` auf.

FOLGE:
Nach Installation zeigte WordPress auf Hobby-Depot-Seiten den kritischen Fehler.

WARUM DIE VORHERIGE PRÜFUNG FALSCH WAR:
Der behauptete `Release-Kette PASS` prüfte nicht den tatsächlich von `route_template()` gelieferten Front- und Content-Pfad. Damit wurde genau die bereits aus AF-043/AF-026 bekannte Fehlerklasse erneut durchgelassen.

KORREKTUR:
1.50.680 repariert ausschließlich die aktive Versionskette:
- Main V150680;
- Profilklasse V150680;
- Fronttemplate V150680;
- Contenttemplate V150680;
- Templates rufen V150680 auf.

NACHWEIS:
- reale Front-Route → V150680 PASS;
- reale Content-Route → V150680 PASS;
- beide Templates mit ausschließlich V150680 ausgeführt PASS;
- Negativtest mit ausschließlich V150679 scheitert erwartungsgemäß;
- 901/901 Bilder unverändert;
- Delta zu 1.50.679 nur 1 geänderte + 3 neue Dateien.

VERMEIDUNGSREGEL – BEREITS VORHANDEN, NICHT NEU:
Die bestehende AF-043/AF-026-Regel war ausreichend. Der Fehler entstand, weil sie nicht tatsächlich ausgeführt wurde. Kein neuer Regelaufbau. Künftig gilt weiterhin: der echte `route_template()`-Rückgabepfad und beide zurückgegebenen Templates müssen mit der tatsächlich geladenen Profilklasse positiv und mit der vorherigen Klasse negativ ausgeführt werden.


## AF-050 – Masterbild korrekt, aber Übergang verdeckte die Szene und erzeugte erneut Zoom-Eindruck

FEHLER:
1.50.684 verwendete bei Keramik & Glas zwar den korrekten hochauflösenden Szenenmaster und schnitt rechnerisch nur oben/unten. Trotzdem verdeckte der linke Textbereich mit einem sehr breiten Verlauf einen großen Teil der Bildszene.

FOLGE:
Im echten WordPress-Readback war nur ein enger Rest der Szene klar sichtbar. Das Ergebnis wirkte damit erneut wie ein hineingezoomter Ausschnitt, obwohl die Datei selbst horizontal nicht gecroppt war.

URSACHE:
Die lokale Prüfung bewertete nur Bildgeometrie und Seitencrop. Sie prüfte nicht ausreichend, wie viel der horizontalen Szene **nach Text-/Verlaufsüberlagerung tatsächlich sichtbar** bleibt.

KORREKTUR:
1.50.685 lässt die Masterdateien unverändert, verbreitert das Bildfeld leicht und verkürzt den Übergang stark. Keramik & Glas ist verpflichtender Sichtfall.

VERMEIDUNGSREGEL:
Bei Hero-Abnahme reicht `0 seitlicher Crop` technisch nicht. Zusätzlich muss die **sichtbare** Szene nach Text-/Fade-Overlay geprüft werden. Ein formal vorhandener Bildbereich, der vom Overlay verdeckt wird, zählt nicht als erhaltene Szenerie.


## AF-051 – Textregeln formal vorhanden, aber bei Massenproduktion nicht wirksam durchgesetzt

FEHLER:
Die Detail-Hobbytexte wurden wegen unterschiedlicher Volltexte und korrekter Wortzahlen zu positiv bewertet, obwohl wiederkehrende Generator-Satzanfänge, ähnliche Absatzgerüste und kalte Kachelfloskeln sichtbar blieben.

WARUM DAS FALSCH WAR:
Duplikatfreiheit und Wortzahl wurden wie redaktionelle Qualität behandelt. Die verbindlichen Regeln `natürliches Deutsch`, `keine Generator-/Padding-Sprache` und `keine generische Schlussformel` wurden dadurch nicht tatsächlich geprüft.

KORREKTUR:
Nicht einzelne Wörter austauschen. Der Textaufbau wird redaktionell neu gebunden:
- zuerst für Anfänger erklären, worum es beim Hobby geht, was man macht und was typisch ist;
- danach fachlich zusammenhängend vertiefen;
- keine Kacheln im Fließtext nacherzählen;
- Kacheluntertitel nur sachlich konkret;
- Zwischenüberschrift führt in die Tiefe statt `Themen im Überblick`.

VERMEIDUNGSREGEL:
Ein Textbestand darf nicht mehr allein wegen Wortzahl, Einzigartigkeit oder fehlender exakter Dubletten als Text-PASS gelten. Wiederkehrende Satzanfänge, Absatzmuster, Schlussformeln und austauschbare Handlungsfloskeln sind vor Freigabe explizit negativ zu prüfen.
