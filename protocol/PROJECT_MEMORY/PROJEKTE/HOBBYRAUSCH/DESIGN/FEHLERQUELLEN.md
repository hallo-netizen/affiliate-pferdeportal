# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Autoritative Fehlerhistorie dieses Design-Scopes.  
Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 – Startseite im WordPress-Blogloop
STATUS: CLOSED

## HRD-002 – Startseite wich vom freigegebenen Entwurf ab
STATUS: CLOSED FÜR CODEPFAD / LIVE-REGRESSIONSSCHUTZ AKTIV

## HRD-003 – Hero-CTAs/Bildschriftzug bei Zwischenbreiten abgeschnitten
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

## HRD-004 – Mega-Menü verschwindet beim Mausweg
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

## HRD-005 – Weltbilder unscharf / fachlich unpassend
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

## HRD-006 – Startseite unvollständig / TEST-Fallback
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

## HRD-007 – Affiliate-Leerzustand / Direktwerbung
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

## HRD-008 – Header/Body zu einheitlich / Logo-Readback
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

## HRD-009 – 1.50.611 sichtbar wirkungslos
STATUS: CLOSED DURCH 1.50.612 / LIVE REGRESSIONSSCHUTZ

## HRD-010 – Navigation weiterhin zu hoch
STATUS: LOCAL CLOSED IN 1.50.614 / LIVE OFFEN

Korrektur:
Desktopnavigation gegenüber 1.50.613 nochmals abgesenkt; Mobile unverändert.

## HRD-011 – Hobbyfinder-Karte anderer Schatten/Farbton
STATUS: LOCAL CLOSED IN 1.50.613 / LIVE REGRESSIONSSCHUTZ

## HRD-012 – Verkaufbarer Werbeplatz nicht attraktiv/zu tief
STATUS: LOCAL CLOSED IN 1.50.614 / LIVE OFFEN

Befund:
Ein technisch wirkender bzw. tief platzierter Werbeplatz verkauft sich schlecht.

Korrektur:
- direkt nach der nächsten Kategorieebene;
- prominentes, aber natives Vermarktungsmodul;
- Bildcollage;
- Headline `Hier könnte Ihre Werbung stehen.`;
- CTA `Werbemöglichkeiten & Preise`;
- weiterhin maximal einmal.

## HRD-013 – Hub-/Breadcrumb-Darstellung
STATUS: LOCAL CLOSED IN 1.50.613 / LIVE REGRESSIONSSCHUTZ

## HRD-014 – Hubtext zu kurz / kein Pferdeatelier-Aufklappprinzip
STATUS: LOCAL CLOSED IN 1.50.614 / LIVE OFFEN

Korrektur:
Pferdeatelier-Regel übernommen:
- manuelle Texte geschützt;
- automatische Ableitung aus Titel/Ebene/realen Kindern;
- lange Texte Lead + `Mehr erfahren` + `Was du hier findest`;
- Text vollständig im initialen HTML;
- Gestalten als konkreter Referenztext.

## HRD-015 – Ungerade Unterkategorieanzahl erzeugt Leerfläche
STATUS: LOCAL CLOSED IN 1.50.614 / LIVE OFFEN

Korrektur:
6-Spalten-Desktopgrid:
- regulär 3 Karten;
- Rest 2 = 50/50;
- Rest 1 = volle letzte Reihe;
- Tablet 2 / Mobile 1.

## HRD-016 – Affiliateflächen wirken wie technische Fremdkörper
STATUS: LOCAL CLOSED IN 1.50.614 / LIVE OFFEN

Korrektur:
- Banner ohne große technische Zwischenüberschrift;
- kleine Kennzeichnung `Anzeige · Partner`;
- Produktmodule als native Contentkarten;
- weiterhin klare Werbekennzeichnung;
- Leerregeln unverändert.

## HRD-017 – Topbar optisch nicht abgesetzt
STATUS: LOCAL CLOSED IN 1.50.614 / LIVE OFFEN

Korrektur:
Topbar dunkel im Footer-Farbton; Inhalt unverändert.

## Aktuell erster Fehler-/Abnahmeblocker

**Live-Abnahme 1.50.615 auf Startseite + Gestalten bei mittleren Breiten.**


## HRD-018 – Hauptnavigation bei mittlerer Breite rechts abgeschnitten

STATUS: LOCAL CLOSED IN 1.50.615 / LIVE OFFEN

Befund:
Bei einem mittleren Browserfenster blieb die komplette 8-Welten-Desktopzeile zu lange aktiv. Rechts wurde mindestens `Sammeln` sichtbar angeschnitten.

Korrektur:
- Vollnavigation nur oberhalb 1320 px;
- 761–1320 px Hamburger-/Dropdownmodus;
- Dropdown 4 Spalten, unter 980 px 2 Spalten;
- Mobilepfad bleibt separat;
- kein horizontaler Text-Cutoff im Tabletmodus.

## HRD-019 – Obere Hub-Unterkategorien noch zu textlastig

STATUS: LOCAL CLOSED IN 1.50.615 / LIVE OFFEN

Befund:
Hobby Depot darf auf den inspirativen oberen Hubebenen visueller sein als Pferdeatelier, ohne die tieferen Ebenen erneut zu überladen.

Korrektur:
- Hub1/Hub2-Karten mit kompakter Fotokante;
- echtes Child-Featured-Image hat Priorität;
- sonst kontrollierter Crop des Weltmotivs;
- tiefe Category-/Leafkarten bleiben ohne Bildzwang;
- kein neuer Struktur- oder Medienworkflow.

