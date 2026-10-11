# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Autoritative Fehlerhistorie dieses Design-Scopes.  
Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 – Startseite im WordPress-Blogloop

STATUS: CLOSED

Befund:
1.50.593/1.50.594 wurden innerhalb des WordPress-Blog-/Contentloops gerendert; sichtbar waren u. a. `Blog`, `TEST` und Theme-Footer.

Ursache:
Startseite wurde über den bestehenden Contentpfad eingeschoben statt den Root-/Frontpage-Rahmen vollständig zu übernehmen.

Korrektur:
ab 1.50.595 eigenes Fronttemplate.

## HRD-002 – Startseite wich vom freigegebenen Entwurf ab

STATUS: CLOSED FÜR CODEPFAD / LIVE-REGRESSIONSSCHUTZ AKTIV

Befund:
zu schmale/zu kleine Weltkarten, fehlende Mittelbereiche, falsche Portalnavigation, falsche dekorative Elemente.

Korrektur:
1.50.596–1.50.610 schrittweise auf freigegebenen Aufbau zurückgeführt; keine Community-/Shop-Navigation; 8 reale Welten; vollständiger Mittel-/Magazin-/Monetarisierungsbereich.

## HRD-003 – Hero-CTAs bzw. Bildschriftzug bei Zwischenbreiten abgeschnitten

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
starre Hero-Geometrie konnte CTAs bzw. den im Bild enthaltenen Schriftzug bei bestimmten Breiten abschneiden.

Korrektur 1.50.610:
- flexibler Hero;
- unter 1100 px gestapelte Darstellung;
- separater Desktop-Safe-Crop 1370×620;
- separater Tablet/Mobile-Safe-Crop 1240×620;
- Bildschriftzug „Mehr Zeit für das, was dich begeistert.“ bleibt erhalten;
- CTAs bleiben normale responsive HTML-Elemente.

## HRD-004 – Mega-Menü verschwindet beim Mausweg

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
vertikale Hover-Lücke zwischen Trigger und Dropdown.

Korrektur:
Dropdown direkt an Navigation + Hover-Brücke; 0-px-Gap lokal gemessen.

## HRD-005 – Weltbilder sichtbar unscharf / unpassende Motive

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
frühere Weltbilder waren teilweise hochskalierte Mockup-Ausschnitte. Rein höhere Dateiabmessungen erzeugten keine echten Bilddetails. Zusätzlich waren Motive zu eng/generisch; das alte `Tiere`-Motiv hatte einen dekorativen Rahmen und trug die reale Tierwelt fachlich nicht ausreichend.

Korrektur 1.50.610:
- alle 8 alten Weltmotive ersetzt;
- 8 neue native Ausgangsbilder;
- 8/8 Ausgaben exakt 1400×620;
- 8 unterschiedliche Hashes;
- Motive gegen die tatsächlichen Weltinhalte abgeglichen;
- gleiche Quelle als Startseitenkarte und späterer Welt-/Kategorie-Hero vorgesehen;
- `Tiere`: Aquaristik + Terraristik + Insekten/Futtertiere + Imkerei/Bestäuber; kein dekorativer Rahmen, kein Hund/Haustier.

Live-Schärfe bleibt Teil der WordPress-Abnahme.

## HRD-006 – Startseite unvollständig / TEST-Fallback

STATUS: LOCAL CLOSED / LIVE OFFEN

Korrektur:
- 3/3 redaktionelle Mittelkarten;
- `Wissen & Glossar` real gebunden;
- 5 reale Magazin-Themenseiten;
- kein TEST-Post-Fallback;
- breiter Affiliate-Bannerplatz;
- drei Produktplätze;
- genau ein direkt verkaufbarer Werbeplatz.

## HRD-007 – Affiliateplätze für Admin unsichtbar / Werbeplatz-Verkaufslogik unklar

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
Die alte harte Leerregel versteckte auch im eingeloggten Arbeitszustand alle Affiliateplätze. Gleichzeitig muss ein noch unverkaufter direkt vermietbarer Werbeplatz öffentlich sichtbar sein, damit potenzielle Werbekunden ihn sehen.

Korrektur 1.50.610:
- Affiliate-Produkte/Banner öffentlich leer weiterhin unsichtbar;
- eingeloggt werden leere Affiliate-Arbeitsplätze klar gekennzeichnet angezeigt;
- direkt verkaufbarer Werbeplatz maximal einmal pro Seite/Kategorie/Beitrag;
- unverkauft öffentlich „Werbeplatz verfügbar / Hier werben“;
- verkauft als Anzeige/Werbung;
- keine Werbefläche im Header.

## HRD-008 – Header und Body optisch zu einheitlich / Logo live nicht sichtbar

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
Live-Readback 1.50.601 zeigte Header und Body zu ähnlich; das Logo erschien als Alt-Text statt als Grafik.

Korrektur 1.50.610:
- Body weiß;
- Header warm-off-white `#f5f1e9`;
- Logo verweist bewusst auf das unveränderte freigegebene `logo-variant3-v150600.png`;
- Topbar-Inhalt unverändert und mittig;
- keine Headeranzeige.

Logo-Dateiladung muss live verifiziert werden.

## Aktuell erster Fehler-/Abnahmeblocker

**Live-Abnahme 1.50.612.**

Prüffokus:
1. Logo real sichtbar;
2. Hero vollständig responsiv;
3. 8 neue Weltbilder real scharf;
4. Header/Body-Absetzung;
5. Affiliate Admin/Public;
6. direkt verkaufbarer Werbeplatz;
7. breite Bannerfläche;
8. vollständige Startseite Desktop/Tablet/Mobile;
9. Mega-Menü.


## HRD-009 – 1.50.611 scheinbar geändert, live aber alter Stand sichtbar

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
Nach Installation von 1.50.611 waren Headline, Heroabstand/-farbe, Navigation und Weltbilder live praktisch unverändert.

Bewiesene Ursachen:
1. der Release verwendete weiter die alte Renderklasse/-datei v150610;
2. Assetnamen/-pfade blieben für wesentliche Bilder wiederverwendet und waren cacheanfällig;
3. die Startseiten-Weltkarten bevorzugten bei ausreichend großen WordPress-Featured-Images diese alten Bilder vor den kontrollierten neuen Assets.

Korrektur 1.50.612:
- neue Renderklasse/-datei und neues Fronttemplate;
- neues Assetverzeichnis, neue Dateinamen, Versionsparameter;
- alter Hobby-Depot-Renderer und alter Assetordner aus Release entfernt;
- Weltkarten immer auf kontrollierte 1400×620-Assets gebunden;
- einmalige Cache-Purge beim erkannten Releasewechsel im Backend;
- HTML-Releasemarker für direkten Readback;
- neue Personenmischung Frau/Mann/Hände; kein Weltbild ohne mindestens Hände.

Lokale Fresh-ZIP-Prüfung:
PASS.
