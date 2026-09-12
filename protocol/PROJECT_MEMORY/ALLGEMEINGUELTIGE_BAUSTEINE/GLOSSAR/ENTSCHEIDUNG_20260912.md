# MOD-008 – WAS / WARUM

STAND: 2026-09-12
STATUS: DAUERHAFTE ENTSCHEIDUNG

## WAS

Das öffentliche Glossar wird als eigener WordPress-Funktionsbaustein entwickelt:
`MOD-008 – Universal Glossar Engine`.

Architektur:
- ein neutraler, wiederverwendbarer Core;
- Pferde Atelier nur als erste Projektkonfiguration;
- kein Umbau des bestehenden Designplugins zur Glossar-Engine;
- keine zweite Glossar-Faktendatenbank;
- Fachdaten bleiben in der Wissensdatenbank;
- WordPress speichert nur die Veröffentlichungsfassung;
- eigener Glossar-Inhaltstyp und eigene Oberbereiche;
- vorhandene WordPress-Seite `Glossar` bleibt Haupt-/Einstiegsseite;
- Einzelbegriffe werden nicht als normale Beiträge oder manuell angelegte Seiten gepflegt;
- Felder, Gruppen, URL-Basis, SEO-Schemata und Designwerte sind konfigurierbar/erweiterbar;
- Import/Export strukturiert; Import ausschließlich als Entwurf;
- keine automatische Veröffentlichung.

## WARUM

Das bestehende Designplugin besitzt einen stabilen, bestätigten Pferde-Live-Stand und soll nicht mit Datenhaltung, URL-/SEO-Logik und Glossar-Backend belastet werden.

Ein eigener neutraler Funktionskern trennt:
- Fachwissen;
- Veröffentlichungsdaten;
- Design;
- Portal-Konfiguration.

Damit kann derselbe Kern später in anderen Portalen verwendet werden, ohne Pferde-Begriffe, Farben, Oberbereiche oder SEO-Schemata im Code fest zu verdrahten.

## PARALLELENTWICKLUNG

Aktuell nicht erforderlich.

Erst wenn ein echtes zweites WordPress-Portal eine nicht konfigurierbare Projektspezifik beweist, ist ein kleiner Adapter zulässig. Kein vollständiger Plugin-Fork.

## PRÜFSTATUS

0.1.0-Prototyp lokal:
- PHP-Lint 8/8 PASS;
- Positiv/Negativ 15/15 PASS;
- Runtime-Stub PASS;
- fachfremde Zweitkonfiguration ohne Coreänderung PASS;
- ZIP-Struktur PASS.

Kein WordPress-Live-/Release-PASS behauptet.

Autoritative aktuelle Standquelle:
`CURRENT_STATE.md`

Aktuelle Arbeit:
`HOBBYRAUM.md`
