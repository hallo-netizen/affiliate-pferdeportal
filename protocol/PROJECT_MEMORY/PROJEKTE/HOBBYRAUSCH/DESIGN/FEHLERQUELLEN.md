# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-056
Historie bleibt bestehen.

## HRD-057 – Navigation 1.50.627 gleichmäßig, aber insgesamt zu tief
STATUS: **LIVE CLOSED**
Navigation wurde danach korrigiert und vom Nutzer live als PASS bestätigt. Ab jetzt eingefroren.

## HRD-058 – Hub-Kartenbilder zu klein
STATUS: **LAYOUT LIVE CLOSED 1.50.628**
Die sichtbare Bildfläche bleibt Desktop 200×107, Tablet 165×88, Mobile 145×78.

## HRD-059 – Zu viele interne Links in Seitenendtexten
STATUS: **LIVE CLOSED 1.50.628**

## HRD-060 – Kategorie-/Link-Bilder zu eng / Lupeneindruck
STATUS: **VORERST AKZEPTIERT 1.50.634 / KEINE WEITERE BILDRUNDE JETZT**

Anforderung:
- Szene weiter gefasst;
- klares Hauptmotiv;
- wenig konkurrierendes Drumherum;
- Thema sofort erkennbar;
- keine Hero-Änderung.

Fix 1.50.634:
- 65 aktive Kategorie-Vorschaubilder visuell geprüft;
- 48× v150629, 11× gezielt ausgewählte weitere v150623-Szenen, 6× v150616;
- keine globale Reaktivierung des alten v150623-Satzes;
- Hub1 bleibt designkontrolliert und fällt nicht auf alte Featured Images zurück.

## HRD-061 – 1.50.630 brachte Doppelbilder zurück
STATUS: **CLOSED / 1.50.630 VERWORFEN**

Root Cause:
- alter v150623-Satz wurde pauschal bevorzugt;
- dadurch wiederholten sich ganze Szenenfamilien.

Fix:
- keine pauschale alte Bildserie mehr;
- nur einzeln visuell geprüfte weitere Szenen werden verwendet.

## HRD-062 – Claim/Logo/Navigationslinie
STATUS: **LIVE CLOSED / EINGEFROREN**

Der Nutzer hat den aktuellen Navigations-/Headerstand live als PASS bestätigt.
Keine weitere Header-/Navigationsänderung in 1.50.634.

## HRD-063 – Kategorie-Vorschaubilder mit sichtbarem Rahmen/Passepartout
STATUS: **VORERST AKZEPTIERT 1.50.634 / KEINE WEITERE BILDRUNDE JETZT**

Root Cause:
Die aktive Karten-CSS enthielt weiterhin eine eingerückte Bildbox, u. a. mit Margin, Hintergrund und Radius. Deshalb blieb trotz Bildwechsel ein sichtbarer Rahmen/Passepartout-Effekt.

Fehler 1.50.632:
Der Build wurde ausgegeben, ohne die endgültige berechnete Karten-CSS im gerenderten Zustand zu simulieren. Die Aussage "Rahmen weg" war damit unbelegt und falsch.

Fix 1.50.634:
- Kategorie-Vorschau füllt ihren Slot vollständig;
- Margin 0;
- Padding 0;
- Border 0;
- Border-Radius 0;
- transparenter Slot-Hintergrund;
- Bildgröße exakt gleich Slotgröße.

Simulation mit echten Assets:
- 1440 px: 200×107, Rahmengeometrie 0;
- 930 px: 165×88, Rahmengeometrie 0;
- 760 px: 145×78, Rahmengeometrie 0.


**Live-Abnahme 1.50.635 auf einer realen Kategorieebene-2-/Hub2-Seite.**

## Arbeitsfehlerprotokoll
Dauerhafte interne Fehler-/Lernakte:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/ARBEITSFEHLERPROTOKOLL_20261012.md`

## HRD-064 – Testbeiträge in 1.50.636 angelegt, aber auf Hub2 nicht sichtbar
STATUS: **LOCAL CLOSED 1.50.637 / LIVE OFFEN**

LIVE-BEFUND:
Auf `Druck & Fotografie` blieb die Beitragsvorschau leer und zeigte den Hinweis, dass keine gleichnamige Beitragskategorie gebunden sei.

ROOT CAUSE:
`render_post_previews()` brach bei Seiten ohne gleichnamige WordPress-Beitragskategorie ab, bevor die vier Testbeiträge überhaupt abgefragt wurden. Die Zuordnung der Testbeiträge zu allen vorhandenen Beitragskategorien konnte dieses Gate daher nicht überwinden.

FIX 1.50.637:
- Testposts werden robust bei erstem eingeloggten Admin-/Frontend-Aufruf angelegt bzw. wiederverwendet;
- sie sind privat, klar mit `[TEST]` markiert und besitzen Beitragsbilder;
- für eingeloggte Hub2-Designprüfung existiert ein gezielter Demo-Fallback über Meta `_hd_demo_post_v150637=1`;
- reale öffentliche Beitragslogik bleibt unverändert.

TEST:
PHP-Harness ohne gleichnamige Beitragskategorie → 4 Demo-Karten PASS.

## HRD-065 – Hub2-Bildkarten 1.50.641–1.50.643 nicht 1:1 aus Ebene 1 übernommen
STATUS: **LOCAL CLOSED 1.50.644 / LIVE OFFEN**

LIVE-BEFUND:
Trotz mehrfacher Teilfixes blieben Buch-&-Papier-Karten optisch falsch; 1.50.643 änderte zusätzlich die gewünschte 3er-Struktur in der realen Ansicht.

ROOT CAUSE:
Es wurde weiter ein eigener `hd-bp-card`-/`hd-bp-photo`-Sonderweg gepflegt, obwohl die bereits korrekte Ebene-1-Lösung vollständig vorhanden war. Dadurch kollidierten Pilotregeln mit der bestehenden Kartenkaskade.

FIX 1.50.644:
Der Pilot-Sonderweg für Karten/Bilder ist im aktiven Markup entfernt. Buch & Papier nutzt jetzt exakt `hd-next-grid`, `hd-next-card has-photo`, `hd-next-photo`, `hd-next-card-body`, `hd-next-copy` und `hd-row-size-*` wie Ebene 1.

BEWEIS:
Browser-Simulation mit echter CSS-Kaskade und echten Bildern:
- 1440: 3+2;
- 900: 2+2+1;
- 760: 1-spaltig;
- Bildslot/Card-Border-Geometrie flush 0;
- Bild/Slot Δ 0;
- kein Overflow.








## HRD-066 – Hub2-Hero bei Tabletbreiten gequetscht / Hero-Bildwirkung nicht stabil
STATUS: **LOCAL CLOSED 1.50.651 / LIVE OFFEN**

LIVE-BEFUND 1.50.650:
- Desktop-Grundaufteilung grundsätzlich brauchbar;
- bei mittleren Breiten standen längerer Text und Hero weiter nebeneinander und wirkten gequetscht;
- Hero-Motive waren teilweise weiterhin zu detailnah.

FIX 1.50.651:
- langer regelkonformer Text aus dem Split-Hero herausgezogen und unter den Hero gesetzt;
- im Hero verbleiben Claim + H1 + kurzer individueller direkter Einsteigertext;
- >1100 px: 38/62 Split;
- <=1100 px: Hero vollständig gestapelt;
- 65 Hero-Motive erneut auf vorhandene weiter gefasste Varianten gebunden;
- 65 verschiedene Hero-Dateien, keine v150631-Vignetten.

TEST:
Browser-CSS-Render 1440/1200/1100/1024/900/760/600; überall Overflow 0; Stack-Grenze und Text-Reihenfolge geometrisch geprüft.



## HRD-067 – 1.50.651 live verworfen: Hero und Bildmapping weiterhin fehlerhaft
STATUS: **CONTAINED / DURCH 30ER-NEUBILDSTAND + HRD-SCOPE13 REPARATUR LOKAL ÜBERHOLT / LIVE-RESTPRÜFUNG OFFEN**

LIVE-BEFUND:
- Hero zu hoch;
- Hero-Motive teils Detail-Crops statt klarer, weiter gefasster Szene;
- teils unscharf / hochskaliert;
- Claim-Unterstrich verrutscht und zu lang;
- Unterkategoriebilder semantisch falsch und teils doppelt/ähnlich.

Konkrete Live-Beispiele:
- Genuss → Kakteen;
- Essbare Pflanzen → Kakteen, teils identisches Motiv;
- Ameisen & Insekten → Blumen;
- Papier & Dokumente / Postkarten-Kontext → unpassende Münzen-/Globusmotive.

ROOT CAUSE:
Bisherige automatische/heuristische Bildzuordnung ist für die inhaltliche Genauigkeit nicht zuverlässig genug. URL-Eindeutigkeit und technische Existenz ersetzen keine echte semantische Motivprüfung.

REGEL:
Kein neues Bildrelease ohne manuelle semantische Zuordnung aller sichtbaren Hero-/Kindmotive und lokale visuelle Simulation der realen Ausschnitte.


## Aktuell erster Blocker
**Kein lokaler Bild-/Mapping-Blocker mehr. Offen ist ausschließlich der Live-Readback des HRD-SCOPE13-Kandidaten für die 13 erlaubten Kategorien. Alle anderen Kategorien sind gesperrt.**



## HRD-068 – Reparatur-/Recovery-Serie 1.50.653–1.50.663
STATUS: **CONTAINED / KORRIGIERT**

Belastbarer Endstand:
- Template Kit **1.50.650** bleibt Grundstand;
- der bereits fertiggestellte reine Hero-Bildersatz **1.50.660** wurde wiederhergestellt und lokal technisch vollständig validiert;
- **1.50.661–1.50.663 nicht verwenden**;
- 1.50.660 ändert ausschließlich 65 gemappte Hero-Bilddateien und weder Mapping noch PHP/CSS/Templates/Routing/Karten/Architektur.

Nachweis:
`HERO_1.50.660_RECOVERY_VALIDATION_20261015.md`.

## HRD-069 – Falscher Rückfall auf 7/30-Rekonstruktion trotz bereits fertigem 65er-Bildsatz
STATUS: **CLOSED / REGRESSION VERWORFEN**

FEHLER:
Nach dem bereits fertiggestellten 1.50.660-Hero-Paket wurde fälschlich eine neue Rekonstruktionsschiene mit 7/30 Einzelquellen, 13 Referenzrichtungen und weiteren BLOCKED-Kategorien aufgebaut.

URSACHE:
Der vorhandene vollständige 1.50.660-Bildstand wurde nicht zuerst als Artefakt wiederhergestellt und geprüft.

KORREKTUR:
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.660.zip` wurde wiedergefunden und gegen die echte 1.50.650-Basis validiert:
- 65/65 Payload-Heroes;
- 65/65 Map-Slugs identisch;
- 65/65 Zielpfade vorhanden;
- alle Bilder 600×220;
- keine exakten Payload-Dubletten;
- exakt 65 Bilddateien geändert;
- 0 sonstige Änderungen;
- Mapping byte-identisch.

REGEL:
Vor jeder Bild-Neugenerierung zuerst den letzten bereits fertigen Bildartefaktstand wiederherstellen und prüfen. Keine Rekonstruktion eines Bildsatzes, wenn ein vollständiges, technisch validierbares Artefakt bereits existiert.

---


## HRD-070 – HRD-SCOPE13 gezielte Bildreparatur nach Nutzerbefund
STATUS: **LOCAL CLOSED / LIVE READBACK OFFEN**

HARTE SPERRE:
Nur diese 13 Kategorien durften verändert werden:
Druck & Fotografie; Oberfläche & Dekoration; Genuss; Metall; Schmuck; Funk; Smart Home; Zucht & Futtertiere; Gehegegestaltung; Geschick & Tricks; Team & Wettkampf; Rollen & Balance; Wurf & Ziel.

KORREKTUR:
- vor Neugenerierung alte Bildstände geprüft;
- keine neue Bildgeneration erforderlich;
- 7 frühere gute Vollquellen wiederverwendet;
- 2 Kategorien gezielt auf bessere 1.50.625-Bilder zurückgesetzt;
- 4 Kategorien gezielt auf bessere WIP-1.50.653-Bilder zurückgesetzt;
- keine Collage als Releasequelle;
- alle anderen Kategorien unverändert.

KANDIDAT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HRD_SCOPE13_REPAIR_LOCALPASS.zip`
SHA-256:
`d32805e2747f9df25e722efc7242f4df820bd273f19db2e2b8b97e5b249e1bf4`

LOCAL QA:
- exakt 26 Bilddateien geändert = 13 Heroes + 13 Previews;
- 0 Dateien hinzugefügt;
- 0 Dateien entfernt;
- Mapping byte-identisch;
- 55/55 PHP byte-identisch;
- 55/55 PHP-Syntax PASS;
- ZIP-Roundtrip PASS.

NACHWEIS:
`HRD_SCOPE13_IMAGE_REPAIR_20261016.md`

OFFEN:
Live-Readback ausschließlich der 13 Kategorien. Kein allgemeiner Bildumbau.
