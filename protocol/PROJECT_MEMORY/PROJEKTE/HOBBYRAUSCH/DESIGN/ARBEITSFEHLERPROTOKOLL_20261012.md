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

