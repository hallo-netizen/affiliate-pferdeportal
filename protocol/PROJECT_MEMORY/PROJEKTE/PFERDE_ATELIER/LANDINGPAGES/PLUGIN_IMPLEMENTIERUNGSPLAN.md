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
- Template Kit 1.50.575 ist der real gemessene Live-Basisstand.
- Template Kit 1.50.576 ist der neuere Performance-Kandidat mit HARD LOCAL PASS; realer Server-Readback ist noch offen.
- Candidate ZIP SHA256: edea3d49585012b0c99f6263d5772654c3c61c463be106466cf54a4fecec16de.
- Die Performance-Arbeit wird nicht durch Landingpage-/Providercode zurückgedreht.
- Jede spätere Landingpage-Kacheländerung muss auf dem nach Real-Readback bestätigten aktuellen Template-Kit-Stand aufsetzen; kein Reapply auf 1.50.575.

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
