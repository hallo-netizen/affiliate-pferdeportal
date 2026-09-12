# MOD-008 – BAUPROTOKOLL 2026-09-12

STATUS: PROTOTYP ISOLIERT / LOKAL PASS / WORDPRESS-REALTEST OFFEN

## AUSGANGSLAGE

- Nutzer hat im Pferde-Atelier bereits die WordPress-Seite `Glossar` angelegt und verlinkt.
- Kein normaler Beitrag/keine Seite pro Glossarbegriff gewünscht.
- Eigene Meta-Titel/Meta-Description je Begriff gewünscht.
- Lösung muss flexibel, erweiterbar, veränderbar und portalübergreifend nutzbar sein.
- Bestehendes Pferde-Designplugin darf nicht unnötig gefährdet werden.

## AUSGEFÜHRT

1. neues Büro `PFERDE_ATELIER/GLOSSAR/` eingerichtet;
2. fachliche Datenbank bewusst in `WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/` belassen;
3. allgemeinen Baustein `MOD-008 – Universal Glossar Engine` angelegt;
4. Datenvertrag V1 definiert;
5. 0.1.0-Prototyp gebaut;
6. Pferde-Designprofil aus bestehendem Designstand abgeleitet, ohne Designplugin zu ändern;
7. eigener Glossar-Inhaltstyp + eigene hierarchische Oberbereiche implementiert;
8. konfigurierbare Hauptseite, URL-Basis, SEO-Schemata und Feldschema implementiert;
9. Suche, A–Z, Oberbereiche, Aufklapper und Einzelbegriff-Template implementiert;
10. providerneutrale SEO-Ausgabe + optionale Yoast-Brücke implementiert;
11. JSON-Import/Export ergänzt; Import immer Entwurf, Feld-Allowlist;
12. lokale Positiv-/Negativtests und Runtime-Stub ausgeführt;
13. fachfremde Zweitkonfiguration ohne Coreänderung geprüft;
14. Source-Hashmanifest und Prototyp-ZIP-Hash gebunden;
15. stale Arbeitsbranch verworfen und geprüfte Glossarbäume auf frischen offiziellen Campus-Stand `99b0468d8c1823a75b8c9c957621bf3b11fa4514` übertragen;
16. MOD-008 und WP-009 als Prototyp registriert.

## PRÜFUNGEN

- PHP-Lint: 8/8 PASS;
- statisch Positiv/Negativ: 15/15 PASS;
- Runtime-Stub: PASS;
- Pferde-Profil: PASS;
- fachfremdes `Lexikon`-Profil: PASS ohne Coreänderung;
- ZIP Single-Root/Struktur: PASS;
- Designplugin geändert: NEGATIV / nein;
- TEXT/AFFILIATE geändert: NEGATIV / nein;
- `main` geändert: NEGATIV / nein.

Prototyp-ZIP SHA-256:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

## NICHT AUSGEFÜHRT / NICHT BEHAUPTEN

- kein echter WordPress-Install-/Upgrade-Test;
- kein echter Permalink-Kollisionstest mit `/glossar/`;
- kein echter Yoast-/Astra-Test im Zielsystem;
- kein echter Wissensdatenbankimport;
- kein großer Performance-Test;
- kein zweites echtes WordPress-Portal;
- kein Live-/Release-PASS;
- kein Merge in `main`.

## NEXT ACTION

Exakt den hashgebundenen 0.1.0-Kandidaten in einem isolierten echten WordPress-System gegen die in `HOBBYRAUM.md` gebundene Realtest-Matrix prüfen.

Bei erstem echten Fehler: STOP, Fehler binden, kein Plugin-Serienbau.
