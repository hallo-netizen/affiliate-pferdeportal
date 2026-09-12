# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-12
STATUS: V1-PROTOTYP LOKAL PASS / WORDPRESS-REALTEST OFFEN

## Belastbarer Stand

- Modulname: `MOD-008 – Universal Glossar Engine`.
- Ziel: ein einziger projektunabhängiger WordPress-Core für mehrere Portale.
- Erste Projektanwendung: Pferde Atelier.
- Pferde-spezifische Begriffe, Oberbereiche, Texte, URL-Basis und SEO-Schemata sind nicht im Core hart verdrahtet.
- Projektkonfiguration liegt außerhalb des Fachkerns bzw. wird ausschließlich über Konfiguration/Filter gebunden.
- Eigener WordPress-Backendbereich `Glossar`.
- Glossarbegriffe als eigener Inhaltstyp, getrennt von normalen Beiträgen/Seiten.
- Oberbereiche getrennt von normalen WordPress-Kategorien und hierarchisch erweiterbar.
- Vorhandene WordPress-Seite als Glossar-Hauptseite auswählbar.
- Eigene Zieladresse je veröffentlichtem Begriff.
- Eigene SEO-Titel-/Meta-Description-Werte; providerneutraler Core mit optionaler Yoast-Brücke.
- Suchfeld, A–Z, Oberbereiche und Aufklapper im Frontend-Prototyp vorhanden.
- Kein Bildzwang.
- Kein Auto-Publish.
- JSON-Import/Export vorhanden; Import ausschließlich als Entwurf und nur für erlaubte Felder.
- Feldschema erweiterbar, ohne bestehende Begriffe umzuschreiben.

## Prüfstand

Autoritativ:
`PROTOTYPE_QA_0.1.0.md`

Aktuell belegt:
- PHP-Lint 8/8 PASS;
- statische Positiv-/Negativprüfung 15/15 PASS;
- Runtime-Stub-Vertragstest PASS;
- Pferde-Konfiguration PASS im lokalen Vertrags-/Stubtest;
- fachfremde Zweitkonfiguration `Lexikon` PASS ohne Coreänderung;
- ZIP-Struktur PASS.

Prototyp-ZIP SHA-256:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

## Modulklasse

Formal weiterhin:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Grund:
Der lokale Zweitkonfigurationsbeweis ist positiv, aber ein zweites echtes WordPress-Portal wurde noch nicht ausgeführt.

## Kritische Entscheidung

Keine parallele Pluginentwicklung.

`Core + Projektkonfiguration` ist aktuell technisch tragfähig. Falls ein echter Zweitportaltest später eine unkonfigurierbare Projektspezifik beweist, wird nur ein kleiner Adapter ergänzt; kein vollständiger Fork.

## Noch offen

- echter WordPress-Install-/Upgrade-Test;
- Permalink-Kollisionstest mit vorhandener `/glossar/`-Seite;
- echter Yoast-Test;
- echter Astra/Pferde-Frontendtest;
- realer Import aus der Wissensdatenbank;
- größerer Bestands-/Performance-Test;
- zweites echtes WordPress-Portal.

Keine Release-/LIVE-Freigabe vor diesen Prüfungen.
