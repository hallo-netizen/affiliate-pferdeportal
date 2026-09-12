# GLOSSAR – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / MOD-008 V1-PROTOTYP LOKAL PASS

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
die Pferde-Atelier-Anwendung des allgemeinen Glossar-Cores vorbereitet oder geprüft wird.

**DU DARFST …**  
die Pferde-Konfiguration definieren, Fachquellen aus der Wissensdatenbank binden und den allgemeinen Glossar-Core isoliert gegen das Pferde-Atelier testen.

**DU DARFST NICHT …**  
`main` verändern, eine zweite Glossar-Faktendatenbank bauen, normale Beiträge/Seiten pro Begriff erzwingen, Pferde-Fachlogik in den allgemeinen Core schreiben, das bestehende Designplugin zur Glossar-Engine umbauen oder vor echtem WordPress-PASS ein Release behaupten.

**ALS NÄCHSTES …**  
den lokal grünen 0.1.0-Kandidaten in einem echten isolierten WordPress-System testen.

## AKTUELLER AUFTRAG

Pferde Atelier als erste reale Anwendung von `MOD-008 – Universal Glossar Engine` bis zum WordPress-Smoke-Test bringen.

Bestätigter Live-Ausgangspunkt:
- Seite `Glossar` ist angelegt;
- Seite ist verlinkt;
- Nutzer muss aktuell nichts Weiteres manuell anlegen.

## ARBEITSORT

Campus-Basis:
`hobbyroom/project-memory-campus-v1-20260905`

Isolierter Glossar-Hobbyraum-Branch:
`hobbyroom/glossar-office-20260912-v2`

`main` bleibt unangetastet.

## ALLGEMEINER CORE

Autorität:
`../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
→ `CURRENT_STATE.md`
→ `HOBBYRAUM.md`

Quellstand:
`../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/prototype/0.1.0/universal-glossary-engine/`

QA:
`../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/PROTOTYPE_QA_0.1.0.md`

Kandidaten-Hash:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

## PFERDE-KONFIGURATION

- vorhandene Seite `Glossar` als Hauptseite;
- URL-Basis zunächst `glossar`, Realtest muss Kollision ausschließen;
- Oberbereiche nicht im Core fest verdrahten;
- SEO-Schema konfigurierbar, je Begriff überschreibbar;
- Designprofil übernimmt nur tatsächliche Pferde-Designwerte;
- Fachimport später aus `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`;
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

## LOKALER PRÜFSTAND

- PHP-Lint 8/8 PASS;
- Positiv/Negativ 15/15 PASS;
- Runtime-Stub PASS;
- Pferde-Profil PASS;
- fachfremdes Zweitprofil PASS ohne Coreänderung;
- Import/Export sicherheitsgebunden;
- Import niemals Auto-Publish;
- ZIP-Struktur PASS.

## NEXT ACTION – ECHTER WORDPRESS-REALTEST

1. exakt hashgebundenen 0.1.0-Kandidaten installieren;
2. vorhandene Seite `Glossar` als Hauptseite auswählen;
3. zwei Test-Oberbereiche + drei Testbegriffe anlegen;
4. prüfen: Begriffe nur im Glossarbereich, nicht normale Beiträge/Seiten;
5. Hauptseite: Suche, A–Z, Oberbereiche, Aufklapper;
6. Einzelbegriff: eigene URL, vollständiger Text;
7. SEO-Titel + Meta-Description mit Yoast aktiv/inaktiv;
8. keine doppelten Meta-/Canonical-/Robots-Ausgaben;
9. JSON-Export → Reimport ausschließlich als Entwurf;
10. normale Beiträge, normale Seiten und bestehendes Designplugin negativ unverändert prüfen;
11. erst bei Gesamt-PASS einen installierbaren Kandidaten freigeben.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

Nur bei echtem unkonfigurierbarem Zweitportalproblem:
Core + kleiner Adapter. Kein zweiter Plugin-Fork.

## HARTE REGEL

**Noch kein Plugin an WordPress ausgeben, solange der echte WordPress-Smoke-Test fehlt.**

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Bürotür: `START_HERE.md`
- Seitenkonzept: `SEITENKONZEPT_V1.md`
- Allgemeiner Core: `../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Ziel: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
