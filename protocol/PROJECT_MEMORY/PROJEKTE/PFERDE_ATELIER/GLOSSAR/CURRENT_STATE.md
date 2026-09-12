# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-12
STATUS: BÜRO EINGERICHTET / MOD-008 FRONTENDKONZEPT KORRIGIERT / WORDPRESS-REALTEST OFFEN

## Belastbarer aktueller Stand

- Eigenes Büro `GLOSSAR` ist die Projekt-Steuerstelle für das öffentliche Pferde-Atelier-Glossar.
- Fachliche Glossar-Datenbank bleibt autoritativ in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Keine zweite Fachbegriffs-Datenbank im Büro GLOSSAR.
- Vom Nutzer im WordPress-Live-Backend bestätigt: Seite `Glossar` ist angelegt und verlinkt.
- Keine normalen Beiträge oder WordPress-Seiten pro Glossarbegriff.
- Technischer Kern ist `MOD-008 – Universal Glossar Engine` unter `../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`.
- Der bisherige Frontend-Prototyp `eine Hauptseite + HTML-Anker + alle Begriffe auf einmal` ist fachlich verworfen und darf nicht real getestet oder released werden.
- Verbindliche neue Frontend-Richtung steht in `SEITENKONZEPT_V1.md`.
- Glossar-Startseite bleibt ein begrenzter Einstieg mit passendem Hero-/Foto-Bereich und wechselnden Glossarbegriffen.
- Glossar-Kategorien werden als echte eigene Seiten/URLs dargestellt und über eine waagerechte Navigation auf jeder Glossarseite erreicht.
- Kategorien werden auf der Startseite nicht noch einmal vollständig wiederholt.
- Jede Begriffsseite besitzt weiter eine eigene Zieladresse und eigene SEO-Metadaten.
- Kein Beitragsbild pro Begriff erforderlich.
- Design muss sich am tatsächlichen Pferde-Atelier-Designplugin orientieren, nicht nur an übernommenen Farben/Radiuswerten.
- Autoritativer aktueller Designstand laut DESIGN/CURRENT_STATE: `Pferde Atelier Design 1.50.472 / Contract V104 + DESIGN-ORDER-SWAP-002`.
- Eigene SEO-Titel-/Meta-Description-Werte je Begriff; keine direkten Yoast-Datenbankwrites; Core soll ohne Yoast funktionsfähig bleiben.

## Pferde-spezifische Konfiguration

Bleibt außerhalb des neutralen Fachkerns bzw. wird nur konfiguriert:
- bereits vorhandene Glossar-Hauptseite;
- Glossar-Kategorien und deren echte URLs;
- gemeinsame waagerechte Glossar-Navigation;
- URL-Basis;
- Pferde-SEO-Schemata;
- Text-/Pflichtfeldregeln;
- Designprofil;
- Hero-/Bildanbindung nach bestehender Pferde-Designlogik;
- Importquelle Wissensdatenbank.

## Noch NICHT bewiesen

- korrigierter Frontend-Code für echte Kategorieseiten;
- echter WordPress-Install-/Upgrade-Test;
- reale Permalink-Auflösung neben der vorhandenen Seite `/glossar/`;
- echte Kategorieseiten mit Pagination;
- echter Yoast-Test im Zielsystem;
- echte Astra/Pferde-Frontenddarstellung inkl. Hero/Foto und waagerechter Navigation;
- realer Import aus der Campus-Wissensdatenbank;
- Performance mit größerem echten Begriffsbestand;
- zweites echtes WordPress-Portal.

Daher aktuell kein Release-/LIVE-PASS.

## Nächster belastbarer Schritt

Frontend-Prototyp zuerst auf das korrigierte Seitenmodell umbauen und dabei die reale Pferde-Atelier-Designlogik als Vorlage verwenden. Erst danach neuer Positiv-/Negativtest und WordPress-Smoke-Test. Aktuelle Arbeitsbindung ausschließlich in `HOBBYRAUM.md`.