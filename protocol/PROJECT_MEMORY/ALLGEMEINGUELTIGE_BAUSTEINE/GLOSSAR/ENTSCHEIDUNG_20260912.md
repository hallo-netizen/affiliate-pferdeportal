# MOD-008 – WAS / WARUM

STAND: 2026-09-13
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

## VERSIONIERUNGS- UND UPDATE-REGEL AB 2026-09-13

WAS:
Materiell verschiedene Pluginpakete dürfen niemals wieder unter derselben Versionsnummer ausgegeben oder als gleichwertig behandelt werden.

WARUM:
Bei 0.2.5 existierten im Entwicklungsverlauf unterschiedliche Paketinhalte unter derselben Versionsnummer. Dadurch war aus der Versionsnummer allein nicht mehr ableitbar, welcher Code tatsächlich installiert war. Das erschwerte insbesondere die Diagnose von Rewrite-/Routingproblemen.

REGEL:
- Jede materielle Paketänderung erhält eine neue Pluginversion.
- Rewrite-relevante Änderungen erhalten zusätzlich eine neue `REWRITE_SCHEMA_VERSION`.
- Ein Release-/Testkandidat wird an exakten ZIP-SHA-256 gebunden.
- Ein Updatekandidat muss vor Ausgabe sowohl Fresh-Install als auch echten WordPress-In-place-Updateweg positiv und negativ bestehen.
- Reines HTTP 200 genügt für Einzelbegriffe nicht; echter Glossar-Artikelmarkup/Inhalt muss nachgewiesen werden.
- Der Paketjob darf erst nach den gebundenen Fresh-/Upgrade-Hardtests laufen.

BELEG:
`TESTPROTOKOLL_0.2.6_20260913.md`
Run `34748541630`.

## PARALLELENTWICKLUNG

Aktuell nicht erforderlich.

Erst wenn ein echtes zweites WordPress-Portal eine nicht konfigurierbare Projektspezifik beweist, ist ein kleiner Adapter zulässig. Kein vollständiger Plugin-Fork.

## PRÜFSTATUS

Technischer Kandidat 0.2.6:
- deterministischer Bau aus dem getesteten 0.2.5-Kandidaten;
- erlaubtes Delta exakt zwei Dateien: Hauptplugin-Version + Core-Rewrite-Schema;
- Fresh-Install WordPress/MySQL/Astra positiv/negativ PASS;
- echter WordPress-In-place-Updateweg 0.2.5 → 0.2.6 positiv/negativ PASS;
- gezielt defekte Einzelbegriff-Rewrite-Regel unter 0.2.5 reproduziert und durch Schema 4 → 5 nach echtem WordPress-Update wiederhergestellt;
- komplette Frontend-/Regression-/Acceptance-Matrix nach Upgrade erneut PASS;
- exaktes Actions-Artefakt zusätzlich lokal positiv/negativ geprüft;
- innerer Plugin-ZIP SHA-256: `e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`.

Kein Pferde-Atelier-LIVE-PASS behauptet.

Autoritative aktuelle Standquelle:
`CURRENT_STATE.md`

Aktuelle Arbeit:
`HOBBYRAUM.md`
