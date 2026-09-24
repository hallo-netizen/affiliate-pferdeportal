# Pferde Atelier Performance Optimierung – Zielvertrag 2026-09-24

Rolle: autoritative Zielquelle fuer den neu geoeffneten Performance-Auftrag nach abgeschlossenem Kategorie-/Strukturscope.

## Oberziel

Pferde Atelier schrittweise bis zum praktisch sinnvollen Performance-Optimum optimieren, soweit Ursache und Aenderung in eigener Hand liegen.

Harte Grenzen:
- keine Inhalts-, Design-, Qualitaets-, Ranking-, Provider-, Slot-, Veto-, Publish- oder Kategorienregel veraendern;
- keine Architektur-Neuerfindung;
- keine Funktion entfernen, nur um Messwerte zu verbessern;
- keine Verdachtsfixes ohne Messbezug;
- mehrere zusammengehoerige Aenderungen pro Block buendeln und danach genau eine Gesamt-/Zwischenpruefung;
- Kategorie-/Strukturscope bleibt FINAL_FROZEN.

## Messbasis

Aktuelle Nutzerdiagnose:
`performance-diagnose-safe-20260924-121142.json`

Belegte Hauptbefunde:
1. Affiliate-Zentrale: sehr hohe request-lokale CPU-Wiederholungen bei Normalisierung/Routing.
2. Template Kit / Menue: hohe Meta-/Term-/Menuearbeit; der vorhandene Design-Performance-Helper 2.0.0 arbeitet bereits und bleibt in Block A unveraendert.
3. Kein persistenter Object Cache in der Diagnose erkannt.
4. HivePress, Kubio und Astra sind spaetere pruefbare Performance-Scope-Bestandteile, aber nicht Teil von Block A.
5. Browser-/Assetwerte stammen aus eingeloggtem Admin-Kontext und duerfen fuer Besucher-Frontend nicht blind ueberinterpretiert werden.

## Block A – jetzt

Nur Affiliate-Zentrale, nur gemessene Wiederholungsarbeit:
- bereits in `campaign_from_post()` normalisierte Kampagnenwerte request-lokal wiederverwenden statt sie pro Rankingdurchlauf erneut zu sanitizen;
- bereits normalisierte Placements nicht erneut sanitizen;
- `campaign_is_complete()` soll vorhandene normalisierte Assignment-Werte wiederverwenden;
- identische Runtime-Slotregel innerhalb desselben oeffentlichen Frontend-Requests einmal berechnen und wiederverwenden;
- fuer Admin, Cron, REST, WP-CLI und AJAX bleibt die bisherige nicht-gecachte Semantik erhalten.

Nicht Teil von Block A:
- Template-Kit-Hauptdatei veraendern;
- Kubio/Astra/HivePress veraendern;
- Object Cache/LiteSpeed/WP-Optimize veraendern;
- Frontend-Asset-Tuning.

## Abnahme Block A

Ein gebuendelter Hardtest muss gleichzeitig beweisen:
- PHP-Syntax PASS;
- alter und neuer fachlicher Output der betroffenen Kampagnen-/Slotpruefungen identisch;
- Normalisierungsarbeit messbar reduziert;
- Runtime-Slotregelcache liefert identische Werte und greift nur im erlaubten oeffentlichen Frontend-Kontext;
- bestehende Affiliate-/Bannerregressionen bleiben PASS;
- keine Kategorie-/Strukturdatei wird veraendert.

Danach genau eine reale Server-Zwischenmessung mit demselben Performance-Pruefplugin und denselben Testseiten.

## Weitere Reihenfolge

Nach Server-Zwischenmessung:
- Block B: Object Cache / LiteSpeed / WP-Optimize / Cache-Doppelarbeit;
- Block C: HivePress + Kubio + Astra seitenabhaengige Last;
- Block D: Frontend CSS/JS/Fonts/Assets;
- Abschluss: Browser-/Lighthouse-/Besuchermessung und nur noch messbar lohnende Restpunkte.
