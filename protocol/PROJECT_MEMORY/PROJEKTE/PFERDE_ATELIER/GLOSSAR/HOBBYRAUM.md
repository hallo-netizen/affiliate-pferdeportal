# GLOSSAR – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / MOD-008 ECHTER WORDPRESS+MYSQL-SMOKE-TEST PASS

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
die Pferde-Atelier-Anwendung des allgemeinen Glossar-Cores vorbereitet oder geprüft wird.

**DU DARFST …**  
die Pferde-Konfiguration definieren, Fachquellen aus der Wissensdatenbank binden und den allgemeinen Glossar-Core isoliert gegen das Pferde-Atelier testen.

**DU DARFST NICHT …**  
`main` verändern, eine zweite Glossar-Faktendatenbank bauen, normale Beiträge/Seiten pro Begriff erzwingen, Pferde-Fachlogik in den allgemeinen Core schreiben, das bestehende Designplugin zur Glossar-Engine umbauen oder vor Release-/LIVE-Nachweis einen Release behaupten.

**ALS NÄCHSTES …**  
den unveränderten 0.1.0-Core mit Astra + Yoast im echten isolierten WordPress-System prüfen.

## AKTUELLER AUFTRAG

Pferde Atelier als erste reale Anwendung von `MOD-008 – Universal Glossar Engine` nach bestandenem WordPress/MySQL-Smoke-Test bis zum Astra+Yoast-PASS und anschließend zum realen Wissensdatenbankimport bringen.

Bestätigter Live-Ausgangspunkt:
- Seite `Glossar` ist angelegt;
- Seite ist verlinkt;
- Nutzer muss aktuell nichts Weiteres manuell anlegen.

## ARBEITSORT

Campus-Basis:
`hobbyroom/project-memory-campus-v1-20260905`

Isolierter Glossar-Hobbyraum-Branch:
`hobbyroom/glossar-v1-current-20260912`

`main` bleibt unangetastet.

## ALLGEMEINER CORE

Autorität:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
→ `CURRENT_STATE.md`
→ `HOBBYRAUM.md`

Quellstand:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/prototype/0.1.0/universal-glossary-engine/`

QA:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/PROTOTYPE_QA_0.1.0.md`

Früher lokal gebauter Prototyp-ZIP-Hash:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

Dieser Hash ist kein finaler Installer.

## PFERDE-KONFIGURATION

- vorhandene Seite `Glossar` als Hauptseite;
- URL-Basis `glossar` im echten WordPress-Test kollisionsfrei bestätigt;
- Oberbereiche nicht im Core fest verdrahten;
- SEO-Schema konfigurierbar, je Begriff überschreibbar;
- Designprofil übernimmt nur tatsächliche Pferde-Designwerte;
- Fachimport aus `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`;
- Import immer als Entwurf, Veröffentlichung manuell.

## DESIGNBINDUNG

Bestehendes Designplugin wird nicht geändert.

Pferde-Profil im Glossar-Prototyp orientiert sich an:
- Grün `#27a653`;
- Blau `#37abf2`;
- Text `#172018`;
- Sekundärtext `#5e665f`;
- Linie `#e7ebe7`;
- Weiß;
- 22px Rundung;
- 16px Grundschrift / 1.55 Zeilenhöhe;
- kompakte Karten-/Akzentlogik.

## PRÜFSTAND

Lokal:
- PHP-Lint 8/8 PASS;
- Positiv/Negativ 15/15 PASS;
- Runtime-Stub PASS;
- Pferde-Profil PASS;
- fachfremdes Zweitprofil PASS ohne Coreänderung;
- ZIP-Struktur PASS.

Echter WordPress/MySQL-Realtest:
- Run `34699122729` → GESAMT PASS;
- WordPress 6.9 / PHP 8.1.34 / MySQL 8.0 → PASS;
- WordPress 7.1 / PHP 8.3.33 / MySQL 8.0 → PASS;
- `/glossar/` + `/glossar/kolik/` → PASS;
- Entwurfssperre → PASS;
- SEO ohne Yoast → PASS;
- JSON Import/Export → PASS;
- Zusatzfeld ohne Coreänderung → PASS;
- reale `Lexikon`-Zweitkonfiguration → PASS;
- Persistenz nach Deaktivieren/Reaktivieren → PASS;
- keine normalen WordPress-Seiten pro Begriff → PASS.

## NEXT ACTION – ASTRA + YOAST

1. Astra aus offiziellem WordPress-Verzeichnis installieren/aktivieren;
2. Yoast SEO aus offiziellem WordPress-Verzeichnis installieren/aktivieren;
3. vorhandene Glossar-Seite + Begriffszieladresse real laden;
4. SEO-Titel + Meta-Description + Canonical + Robots prüfen;
5. negativ: keine doppelten Description-/Canonical-/Robots-Ausgaben;
6. Astra darf Glossarindex und Einzelansicht nicht zerstören;
7. normale WordPress-Seite/Beitrag negativ unverändert;
8. danach realen Campus-Glossarimport prüfen.

## DANACH OFFEN

- realer Campus-Wissensdatenbankimport;
- größerer Bestand/Performance;
- finaler ZIP Install-/Update-/Reinstall-Test;
- Pferde-Atelier-LIVE-Installation.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

Nur bei echtem unkonfigurierbarem Zweitportalproblem:
Core + kleiner Adapter. Kein zweiter Plugin-Fork.

## HARTE REGEL

**WordPress-Smoke-PASS ist noch kein Pferde-Atelier-LIVE-PASS.**

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Bürotür: `START_HERE.md`
- Seitenkonzept: `SEITENKONZEPT_V1.md`
- Allgemeiner Core: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Ziel: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
