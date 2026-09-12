# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-12
STATUS: BÜRO EINGERICHTET / MOD-008 V1-PROTOTYP LOKAL PASS / WORDPRESS-REALTEST OFFEN

## Belastbarer aktueller Stand

- Eigenes Büro `GLOSSAR` ist die Projekt-Steuerstelle für das öffentliche Pferde-Atelier-Glossar.
- Fachliche Glossar-Datenbank bleibt autoritativ in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Keine zweite Fachbegriffs-Datenbank im Büro GLOSSAR.
- Vom Nutzer im WordPress-Live-Backend bestätigt: Seite `Glossar` ist angelegt und verlinkt.
- Keine weiteren WordPress-Seiten und keine normalen Beiträge pro Glossarbegriff anlegen.
- Das bestehende Pferde-Designplugin bleibt unangetastet.
- Technischer Kern ist `MOD-008 – Universal Glossar Engine` unter `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`.
- V1-Prototyp 0.1.0 ist isoliert gebaut und lokal positiv/negativ geprüft.
- PHP-Lint 8/8 PASS; statische Prüfmatrix 15/15 PASS; Runtime-Stub PASS.
- Fachfremde Zweitkonfiguration `Lexikon` funktioniert im lokalen Vertrags-/Stubtest ohne Coreänderung.
- JSON-Import/Export vorhanden; Import nur als Entwurf, kein Auto-Publish.
- Feldschema, Oberbereiche, URL-Basis, SEO-Schemata und Designwerte sind erweiterbar/änderbar.
- Pferde-Designprofil orientiert sich an den tatsächlichen Designplugin-Werten: Grün `#27a653`, Blau `#37abf2`, Text `#172018`, Sekundärtext `#5e665f`, Linie `#e7ebe7`, 22px Rundung, 16px/1.55.
- Frontend-Prototyp: vorhandene Glossar-Seite → Suche → A–Z → Oberbereiche → Aufklapper → eigene Begriffszieladresse.
- Eigene SEO-Titel-/Meta-Description-Werte je Begriff; keine direkten Yoast-Datenbankwrites; Core funktioniert ohne Yoast.
- Aktueller lokaler Kandidaten-Hash: `c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`.

## Pferde-spezifische Konfiguration

Bleibt außerhalb des neutralen Fachkerns bzw. wird nur konfiguriert:
- bereits vorhandene Glossar-Hauptseite;
- URL-Basis;
- Pferde-Oberbereiche;
- Pferde-SEO-Schemata;
- Text-/Pflichtfeldregeln;
- Designprofil;
- Importquelle Wissensdatenbank.

## Noch NICHT bewiesen

- echter WordPress-Install-/Upgrade-Test;
- reale Permalink-Auflösung neben der vorhandenen Seite `/glossar/`;
- echter Yoast-Test im Zielsystem;
- echte Astra/Pferde-Frontenddarstellung;
- realer Import aus der Campus-Wissensdatenbank;
- Performance mit größerem echten Begriffsbestand;
- zweites echtes WordPress-Portal.

Daher aktuell kein Release-/LIVE-PASS.

## Nächster belastbarer Schritt

Exakt den lokal grünen 0.1.0-Prototyp in einem echten isolierten WordPress-System testen. Aktuelle Arbeitsbindung ausschließlich in `HOBBYRAUM.md`.
