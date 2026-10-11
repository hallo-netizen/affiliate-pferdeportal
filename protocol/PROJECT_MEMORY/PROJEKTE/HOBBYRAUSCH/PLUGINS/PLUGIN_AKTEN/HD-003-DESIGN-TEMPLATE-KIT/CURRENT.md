# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11  
STATUS: **1.50.610 LOCAL HARD PASS / LIVE-PASS OFFEN / CAMPUS-CURRENT.ZIP-SYNC BLOCKED**

## Plugin

ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Name:
`Affiliate Portal Template Kit – Hobby Depot Profil`

Art:
Eigenentwicklung / Projektprofil innerhalb des Template-Kit.

Fachbüro:
`DESIGN`

Theme-Basis:
`ListingHive`

## Aktuelle technische Wahrheit

Version:
**1.50.610**

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.610_HOBBY_DEPOT_HOMEPAGE_FINAL_LOCALPASS.zip`

SHA-256:
`c26ff929fa02a451dd4b7e7b9e6b2aa4dd42c2752bd261f13c134401389512a3`

Isolierte Ausgabekopie im Campus:
**PENDING / NICHT ERFUNDEN.**

Sollpfad:
`../../ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip`

Der verfügbare GitHub-Connector kann Textdateien schreiben, aber den Binärstand nicht belastbar aus dem lokalen Container als Repository-Datei übertragen. Deshalb wurde **kein falsches CURRENT.zip** erzeugt.

Manifest:
`../../ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/MANIFEST.md`

Der geprüfte ZIP-Kandidat liegt im Projekt-/Chat-Artefaktbestand und in der Hobbyrausch-Library.

## Scope 1.50.610

- ListingHive als WordPress-/HivePress-Grundtheme;
- Hobby-Depot eigener Header/Footer/Fronttemplate;
- Logo unverändert aus freigegebenem v150600-Asset;
- Topbar-Inhalt unverändert, mittig;
- weißer Body + warm-off-white Header;
- keine Anzeige im Header;
- 8 reale CORE-Welten in Navigation;
- Mega-Menü pro Welt;
- Hero mit erhaltenem Bildschriftzug + Desktop/Mobile-Safe-Crops;
- vollständige Startseitenstruktur;
- 8 neue native Weltmotive je 1400×620, hero-ready;
- Affiliate-Produkte/Banner: öffentlich leer unsichtbar, eingeloggt leer sichtbar;
- genau ein direkt verkaufbarer Werbeplatz pro Seite/Kategorie/Beitrag, öffentlich auch unverkauft sichtbar;
- breite Bannerfläche im Content;
- reale Magazin-Seiten statt TEST-Fallback;
- KISS-Meta-Titel/Description-Schicht mit Override.

## Lokale Abnahme

Fresh-ZIP:
- SHA-256 verifiziert;
- ZIP-Integrität PASS;
- PHP-Lint 9/9 PASS.

Positiv:
- 8/8 reale Welten;
- 8/8 neue Weltbilder 1400×620;
- 8/8 Weltbild-Hashes unterschiedlich;
- 3/3 Editorial-Karten;
- 5/5 reale Magazin-Themenseiten;
- belegte Affiliate-Produkte/Banner sichtbar;
- eingeloggt 3 leere Produktplätze + 1 leerer Bannerplatz sichtbar;
- unverkaufter direkt verkaufbarer Werbeplatz sichtbar;
- gebuchter Werbeplatz ersetzt Verfügbarkeitsplatz;
- Hero-Schriftzug erhalten;
- Topbar-Inhalt unverändert und mittig;
- Logo unverändert;
- Body/Header klar getrennt;
- keine Anzeige im Header;
- Reihenfolge Banner → Magazin/Themen → Produkte;
- ListingHive-Shell-Unterdrückung.

Negativ:
- öffentlich unbelegte Affiliate-Produkte vollständig abwesend;
- öffentlich unbelegter Affiliate-Banner vollständig abwesend;
- direkt verkaufbarer Werbeplatz nicht doppelt;
- kein TEST-Fallback;
- kein Shop-/Community-/Newsletter-Noise;
- kein zweiter ListingHive-Header/Footer;
- keine vertikale Mega-Menü-Hover-Lücke.

## Offene Live-Abnahme

Kein Live-PASS behauptet.

Besonders zu prüfen:
- Logo lädt real;
- Hero-Bildschriftzug Desktop/Tablet/Mobile vollständig;
- reale Bildschärfe aller 8 neuen Motive;
- Header/Body-Absetzung;
- Admin-/Public-Affiliatesicht;
- breite Bannerfläche;
- direkt verkaufbarer Werbeplatz;
- Untermenü-Lesbarkeit;
- vollständige Startseite Desktop/Tablet/Mobile.

## Rollback

Falls 1.50.610 live fehlschlägt:
- kein Blindfix;
- Livefehler reproduzieren/diagnostisch eingrenzen;
- nur belegtes Delta reparieren;
- nötigenfalls auf den zuletzt installierten funktionierenden Hobby-Depot-Template-Kit-Stand zurückgehen.

## EXAKT EINE NEXT ACTION

**1.50.610 in Hobby Depot installieren und die vollständige Startseite Desktop/Tablet/Mobile live prüfen.**

Erst nach Live-PASS wird Hub Ebene 1 begonnen.
