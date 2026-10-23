# HD-003 – EVIDENCE 1.50.720

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / NICHT LIVE ABGENOMMEN

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.720_UPDATE_MAGAZIN_HUB_UND_ZIELSEITEN_HARDPASS.zip`

SHA-256:
`4d0dc99d9abf056517ee845a0fda3f2260e39a740ef55427fc3d6951bcb8ee90`

Größe:
584,713 Bytes.

## Paket

UPDATE, kein FULL-Paket.

Exakt zwei Dateien unter dem festen Hauptordner `affiliate-portal-template-kit/`:
- `pferde-template-kit.php`
- `includes/class-hobby-depot-profile-v150709.php`

## Autoritative Magazinstruktur geprüft

Die 12 Magazin-Oberziele sind laut aktuellem Zielbaum echte `page`-Objekte unter `editorial:hub`, keine zweite Kategorie-Taxonomie:

- hobbyfinder
- alter-lebensphasen
- geschichte-herkunft
- hobby-portraets
- hobby-ideen-inspiration
- menschen-geschichten
- neue-hobbys-trends
- saison-drinnen-draussen
- ungewoehnliche-skurrile-hobbys
- vergleiche-alternativen
- wissen-glossar
- zeit-budget-platz

Die Designruntime liest die vorhandenen Editorial-Seiten und deren echte `journal_cat`-Kinder bevorzugt read-only aus der zentralen Registry. Nur ohne Registry greift ein exakter Slug-Fallback für Standalone/Preview. Keine zweite Struktur wird angelegt.

## Magazin-Startseite

- gleicher Seitenbreiten-/Body-Vertrag wie die bestehenden Hobby-Depot-Hubs;
- Hero verwendet den bestehenden akzeptierten Hub2-Hero-Vertrag:
  - grüne Schreibschrift;
  - bestehender gezeichneter Brush/Bogen;
  - warmer Hintergrund;
  - weicher Bildübergang;
  - natürliche Bildmaße über `--hd-scene-w`, `--hd-scene-h`, `--hd-scene-ratio`;
- 12 Bildkacheln;
- jede Kachel nutzt dieselbe Bilddefinition wie ihre Zielseite;
- aktuelle Magazinbeiträge in 2 Reihen;
- `journal_banner` wird zwischen die beiden Beitragsreihen gemischt;
- `journal_product_1–3`;
- eigener Bereich Kaufberatung/Affiliate-Artikel;
- bestehende Rental-Werbefläche `journal`.

## Magazin-Zielseiten

Alle 12 vorhandenen Seiten sind gebunden.

Standard:
- Breadcrumb;
- identischer Hero-Vertrag wie bestehende Kategorie-/Hubseiten;
- Hero-Bild = Kachelbild;
- grüne Schreibschrift + Brush/Bogen;
- kurzer Hero-Einstieg;
- darunter sichtbarer grün hinterlegter Lead;
- weiterer Text nativ aufklappbar;
- Textvertrag pro Seite: 150–200 Wörter, natürliche direkte Sprache, keine Fülltexte;
- vorhandene echte `journal_cat`-Unteransichten werden aus der Registry angezeigt;
- Beiträge / Banner / Produkte / Affiliate-Artikel / Rental im Magazinvertrag.

Hobbyfinder ist funktionale Sonderseite:
- bekommt denselben Magazin-Hero + denselben erklärenden Lead/Aufklapper;
- der bestehende 8-Schritte-Funnel bleibt darunter unverändert funktionsfähig;
- sein bisher eigener doppelter Hero wird im eingebetteten Modus unterdrückt.

## Bildzuordnung

- Hobbyfinder → suchen-finden
- Alter & Lebensphasen → alltagsobjekte
- Geschichte & Herkunft → papier-dokumente
- Hobby-Porträts → citizen-science
- Hobby-Ideen & Inspiration → werbung-design
- Menschen & Geschichten → naturbeobachtung
- Neue Hobbys & Trends → digitale-fertigung
- Saison, drinnen & draußen → outdoor
- Ungewöhnliche & skurrile Hobbys → ameisen-insekten
- Vergleiche & Alternativen → spielzeug-spiele
- Wissen & Glossar → buch-papier
- Zeit, Budget & Platz → mechanik-uhren

## QA

- PHP-Lint beide Dateien: PASS
- ZIP exakt 2 Dateien: PASS
- Fresh-Unpack + PHP-Lint: PASS
- 12/12 vorhandene Editorial-Seiten-Slugs gebunden: PASS
- 12/12 Bildassets physisch vorhanden: PASS
- 12/12 Kategorietexte 150–200 Wörter: PASS
- Kachelbild und Zielseiten-Hero stammen aus derselben Definition: PASS
- Hub2-Hero-Klassen + natürliche Bildmaße: PASS
- grün hinterlegter Lead + nativer Aufklapper: PASS
- Banner zwischen Beitragsreihen: PASS
- 3 bestehende Produkt-Slots: PASS
- Affiliate-Artikel-Bereich: PASS
- zentrale Editorial-Registry read-only bevorzugt: PASS
- FAQ 1.50.715 erhalten: PASS
- PB-one neues Fenster erhalten: PASS

1.50.718 wurde nach Nutzerkritik ausdrücklich verworfen und ist kein Kandidat.

Kein Live-PASS für 1.50.720 behaupten.
