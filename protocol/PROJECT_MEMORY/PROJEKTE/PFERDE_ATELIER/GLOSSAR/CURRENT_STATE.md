# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-12
STATUS: KONZEPT GEBUNDEN / UNIVERSALER CORE FESTGELEGT / TECHNISCHE UMSETZUNG OFFEN

## Belastbarer aktueller Stand

- Eigenes Büro `GLOSSAR` ist die Projekt-Steuerstelle für das öffentliche Pferde-Atelier-Glossar.
- Die fachliche Glossar-Datenbank bleibt autoritativ in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Keine zweite Fachbegriffs-Datenbank im Büro GLOSSAR.
- Vom Nutzer im WordPress-Live-Backend bestätigt: Seite `Glossar` ist angelegt und verlinkt.
- Keine WordPress-Seite pro Glossarbegriff vorgesehen.
- Das bestehende Pferde-Designplugin wird **nicht** zur Glossar-Engine erweitert.
- Der Glossar-Kern wird separat und von Anfang an projektunabhängig als `MOD-008 – Universal Glossar Engine` konzipiert.
- Allgemeiner Hauptort: `../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`.
- Pferde Atelier ist die erste Projektanwendung und liefert nur Projektkonfiguration/Fachdaten.
- Ziel im Frontend: Glossar-Startseite mit Navigation zu Oberbegriffen und A–Z; darunter mehrere Glossarbegriffe ohne Grafikzwang, bevorzugt kompakt/aufklappbar.
- Glossarbegriffe sollen nicht wie normale Beiträge/Karten in bestehenden Pferde-Atelier-Kategorien erscheinen.
- Jeder veröffentlichte Glossarbegriff soll eine eigene technisch auflösbare Zieladresse und eigene SEO-Angaben erhalten können.
- SEO-Titel und Meta-Description sollen nach festem Pferde-Glossar-Schema erzeugt werden können; keine manuelle Yoast-Pflege je Begriff.
- Der universale Core darf nicht von Yoast abhängig sein; bei vorhandenem Yoast wird nur dessen offizielle Filter-/Metadatenschnittstelle genutzt.
- Aktuell ist keine neue große Glossar-Textmaschine vorgesehen. Für kurze Glossartexte reicht ein kleiner standardisierter Schreib-/Prüfweg.

## Projektkonfiguration Pferde Atelier

Muss außerhalb des universalen Core liegen:
- Glossar-Hauptseite / Seiten-ID;
- URL-Basis;
- Pferde-Oberbegriffe;
- Pferde-SEO-Titel-Schema;
- Pferde-Meta-Description-Schema;
- Text-/Pflichtfeldregeln;
- Designklassen;
- Importquelle aus der Wissensdatenbank.

## Noch offen – nicht als beschlossen behandeln

- exakte V1-Feldnamen im WordPress-Backend;
- endgültige URL-Struktur je Begriff;
- ob Oberbegriffe zusätzlich eigene öffentliche Zieladressen bekommen;
- konkrete Import-/Synchronisationsautomatik zwischen Campus-Wissensbasis und WordPress;
- Pluginname/Version des ersten technischen Kandidaten;
- endgültige allgemeingültige Modulfreigabe: erst nach Zweitportaltest.

## Allgemeingültigkeitsregel

Ein Core, zwei Konfigurationen:
1. Pferde Atelier real;
2. fachlich neutrale Testkonfiguration.

Nur wenn beide ohne Core-Codeänderung funktionieren, darf MOD-008 als technisch ALLGEMEINGÜLTIG gelten.

Aktuelle Arbeitsbindung steht ausschließlich in `HOBBYRAUM.md`.
