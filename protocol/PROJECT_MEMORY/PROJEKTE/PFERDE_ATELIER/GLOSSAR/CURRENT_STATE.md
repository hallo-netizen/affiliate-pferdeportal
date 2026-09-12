# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-12
STATUS: BÜRO EINGERICHTET / MOD-008 ECHTER WORDPRESS+MYSQL-SMOKE-TEST PASS / PFERDE-LIVE OFFEN

## Belastbarer aktueller Stand

- Eigenes Büro `GLOSSAR` ist die Projekt-Steuerstelle für das öffentliche Pferde-Atelier-Glossar.
- Fachliche Glossar-Datenbank bleibt autoritativ in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Keine zweite Fachbegriffs-Datenbank im Büro GLOSSAR.
- Vom Nutzer im WordPress-Live-Backend bestätigt: Seite `Glossar` ist angelegt und verlinkt.
- Keine weiteren WordPress-Seiten und keine normalen Beiträge pro Glossarbegriff anlegen.
- Das bestehende Pferde-Designplugin bleibt unangetastet.
- Technischer Kern ist `MOD-008 – Universal Glossar Engine` unter `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`.
- V1-Prototyp 0.1.0 ist isoliert gebaut, lokal positiv/negativ geprüft und in echtem WordPress/MySQL getestet.
- PHP-Lint 8/8 PASS; statische Prüfmatrix 15/15 PASS; Runtime-Stub PASS.
- GitHub Actions Run `34699122729` → echter WordPress/MySQL-Gesamt-PASS.
- WordPress 6.9 / PHP 8.1.34 / MySQL 8.0 → PASS.
- WordPress 7.1 / PHP 8.3.33 / MySQL 8.0 → PASS.
- `/glossar/` und `/glossar/kolik/` funktionieren im Realtest gleichzeitig.
- Fachfremde reale Zweitkonfiguration `Lexikon` funktioniert ohne Coreänderung.
- JSON-Import/Export funktioniert; Import nur als Entwurf, kein Auto-Publish.
- Unbekannte Importfelder werden verworfen.
- Feldschema, Oberbereiche, URL-Basis, SEO-Schemata und Designwerte sind erweiterbar/änderbar.
- Pferde-Designprofil orientiert sich an den tatsächlichen Designplugin-Werten: Grün `#27a653`, Blau `#37abf2`, Text `#172018`, Sekundärtext `#5e665f`, Linie `#e7ebe7`, 22px Rundung, 16px/1.55.
- Frontend: vorhandene Glossar-Seite → Suche → A–Z → Oberbereiche → Aufklapper → eigene Begriffszieladresse.
- Eigene SEO-Titel-/Meta-Description-Werte je Begriff; keine direkten Yoast-Datenbankwrites; Core funktioniert ohne Yoast.
- Deaktivieren/Reaktivieren erhält Daten und Konfiguration.
- Glossarbegriffe erzeugen keine normalen WordPress-Seiten.

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

- Astra + Yoast gemeinsam im isolierten Realtest;
- realer Import der vorhandenen Campus-Glossardatensätze;
- Performance mit größerem echten Begriffsbestand;
- finaler Installer-/Update-/Reinstall-Test;
- Pferde-Atelier-LIVE-Installation.

Daher aktuell kein Pferde-LIVE-/Release-PASS.

## Nächster belastbarer Schritt

Unveränderten 0.1.0-Core mit Astra + Yoast im isolierten echten WordPress-System positiv und negativ prüfen. Aktuelle Arbeitsbindung ausschließlich in `HOBBYRAUM.md`.
