# LANDINGPAGES – PLUGIN-IMPLEMENTIERUNGSPLAN

STATUS: VORBEREITET / SOURCE-WRITE DURCH AFFILIATE-PERFORMANCE-LOCK GESPERRT

## Aktuelle Performance-Bindung

Die Affiliate-Zentrale darf aktuell nur den gebundenen Performance-Schritt 6.72.166 abschließen.

Aktueller kanonischer Affiliate-Stand:
- Kandidat: 6.72.166
- Release: noch nicht freigegeben
- Current NEXT ACTION: RUN_BOUND_RELEASE_GATES
- Performance-Scope: keine Provider-, Slot-, Design-, Ranking-, Content- oder Kategorienänderung bis Abschluss des Gates.

Parallel bestätigter Design-/Template-Performance-Stand:
- Template Kit 1.50.575 war die vorherige real gemessene Live-Basis.
- Template Kit 1.50.576 ist inzwischen real auf dem Portal aktiv belegt: die Diagnose vom 2026-09-28 10:07–10:09 UTC liefert Frontend-Assets mit `?ver=1.50.576`.
- HARD LOCAL für 1.50.576: 35/35 PASS; Candidate ZIP SHA256 `edea3d49585012b0c99f6263d5772654c3c61c463be106466cf54a4fecec16de`.
- Der erwartete Warm-Request-Gewinn der sieben Menüabfragen ist im aktuellen Real-Server-Lauf **noch nicht belegt**: auf mehreren normalen Seiten bleibt die betreffende Template-Kit-Queryfamilie sichtbar. Deshalb kein PERFORMANCE_PASS behaupten.
- Die Performance-Arbeit wird nicht durch Landingpage-/Providercode zurückgedreht.
- Solange der Nachbar-Performance-Strang diesen 1.50.576-Realbefund nicht geschlossen hat, wird **kein Template-Kit-Source-Write** für die Landingpage-Kachel ausgeführt.
- Jede spätere Landingpage-Kacheländerung setzt ausschließlich auf dem dann frisch bestätigten aktuellen Template-Kit-Stand auf; kein Reapply auf 1.50.575 oder einen älteren Stand.

## Nach Freigabe – kleinster Affiliate-Delta

Nur die bestehende Affiliate-Zentrale erweitern. Kein neues Plugin.

### Provider

1. Tarifcheck als eigener Provider registrieren.
2. CHECK24 als eigener Provider vorbereitet registrieren.
3. Beide zunächst ohne erfundene API-/Feed-/Creative-Quelle.
4. Tarifcheck darf im Pferdehaftpflicht-Pilot aktiv verwendet werden, sobald der echte Tarifrechner-Code gebunden ist.
5. CHECK24 bleibt vorbereitet, bis eine reale passende Werbemittel-/Datenquelle belegt ist.

### Performance-Hardrules

- vorhandenen request-lokalen Provider-Registry-Cache nicht umgehen;
- keine Provider-Registry pro Slot oder pro Kachel neu aufbauen;
- keine neue globale the_content/pre_get_posts/taxonomy/menu-Abfrage für Rechner;
- keine externe Providerabfrage auf normalen Frontendseiten;
- keine neue Datenbankabfrage auf Seiten ohne Landingpage-/Providerbedarf;
- Admin-/Sync-Arbeit nur im Admin-/Worker-Kontext;
- Rechner nur durch expliziten Landingpage-Aufruf/Shortcode laden;
- Banner ausschließlich über bestehende Creative-Library/Relevanz-/Veto-/Verteilungslogik;
- keine zweite Bannerverteilung;
- keine neue Architektur;
- Änderungen als ein zusammengehöriger Block, danach ein Positiv-/Negativ-/Regressionslauf;
- exakter Fallback auf den vorherigen kanonischen Affiliate-Stand.

## Pilot Pferdehaftpflicht vergleichen

Nur:
- eine eigenständige WordPress-Seite;
- Tarifcheck Tierhalter/Pferdehaftpflicht Tarifrechner;
- keine zweite Versicherungs-Ausgabe von CHECK24;
- keine Änderung auf anderen Seiten;
- kein globales Laden des Rechners.

Negativbeweis:
- normale Kategorie-/Journal-/Startseiten erzeugen weder Rechneroutput noch zusätzliche Provider-/DB-/Taxonomiearbeit;
- bestehende Banner-, Ranking-, Veto- und Kategorieausgabe bleibt identisch.

## Banner-Import

Tarifcheck/CHECK24-Banner werden nur automatisiert angebunden, wenn eine echte dokumentierte oder im Partnerbereich eindeutig bereitgestellte Quelle gebunden ist.

Zielweg:
Provideradapter -> bestehende Creative-Library -> bestehende Relevanz-/Verteilung -> bestehende Veto-/Outputlogik.

Kein:
- manuelles Dauer-Einzelkopieren;
- geratenes API;
- Scraping einer privaten Oberfläche;
- separater Banner-Router.

## Technische Dateigrenze

Vor Source-Write erneut Current-Autorität lesen.

Voraussichtlich kleinster Affiliate-Korridor:
- bestehende Provider-Registry für Providerdefinitionen;
- vorhandener Adapter-/Sync-Hook nur falls echte Quelle belegt;
- vorhandene Output-/Shortcode-Schicht für den expliziten Rechneraufruf.

Keine Änderung an eBay-/Ranking-/Kategorie-/Performancecode, sofern der echte Implementierungsbedarf das nicht zwingend beweist.


## Exakter vorbereiteter Code-Korridor

Noch **kein Source-Write**, solange die Affiliate-Current-Autorität den Performance-Scope exklusiv bindet.

Nach Freigabe ist der kleinste vorgesehene Korridor:

### 1. Provider-Registry

Bestehende Funktion:
`PPAR_Provider_Registry_Trait::provider_registry_defaults()`

Nur zwei neue Providerdefinitionen ergänzen:
- `tarifcheck`
- `check24`

Beide zunächst:
- `state=prepared`
- `access_owner=adapter`
- kein Specialist-Menü
- nur tatsächlich belegte Capabilities.

Wichtig:
Der vorhandene request-lokale Registry-Cache aus 6.72.148 bleibt unverändert. Keine neue Registry-Abfrage pro Slot/Kachel.

### 2. Rechner-Ausgabe

Der vorhandene normale Affiliate-Slot ist für Banner/Produkte optimiert. Der große Tarifrechner wird deshalb **nicht** in die globale Slot-Automatik eingeschleust.

KISS:
- genau ein expliziter, providerneutraler Rechner-Shortcode;
- dieser läuft nur dort, wo er tatsächlich im Seiteninhalt steht;
- ohne Shortcode: null Rechnerarbeit;
- ohne freigegebenen Provideradapter: leere Ausgabe/fail closed;
- keine externe Anfrage beim bloßen Registrieren des Providers;
- keine `the_content`-, `pre_get_posts`-, Menü-, Kategorie- oder Taxonomie-Suche zum Finden der Landingpage.

Der Adapter liefert ausschließlich den real gebundenen Tarifrechner-Embed.

### 3. Pilot-Hardlock

Für den ersten Realtest akzeptiert der Rechner nur:
- Provider `tarifcheck`;
- Produkt `tierhalter/pferdehaftpflicht`;
- die explizit gebundene WordPress-Seite `Pferdehaftpflicht vergleichen`.

CHECK24 wird nur registriert/vorbereitet und erzeugt im Pilot keinerlei Frontendoutput.

### 4. Banner

Banner von Tarifcheck/CHECK24 bleiben im bestehenden Weg:
Provider/Import -> Creative-Library -> Relevanz -> Verteilung -> Veto -> Output.

Der Rechner-Shortcode erzeugt **keinen zweiten Bannerweg**.

### 5. Performance-Testpflicht

Vor Freigabe:
- normale Startseite: 0 Rechneraufrufe;
- normale Kategorie: 0 Rechneraufrufe;
- Journalartikel: 0 Rechneraufrufe, sofern kein expliziter Shortcode gesetzt ist;
- Pilot-Landingpage: genau 1 Rechnerausgabe;
- unbekannter Provider: leer/fail closed;
- falsche Seite: leer/fail closed;
- Provider pausiert/veto: leer/fail closed;
- keine zusätzlichen DB-/Taxonomie-/Menüabfragen auf Negativseiten;
- bestehende Banner-/Ranking-/Veto-Regression PASS.
