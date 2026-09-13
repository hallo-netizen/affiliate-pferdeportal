# ALLGEMEINGÜLTIGER BAUSTEIN – UNIVERSAL GLOSSAR ENGINE

STAND: 2026-09-13
STATUS: 0.2.6 TECHNISCHER KANDIDAT HARDTEST PASS / MODULKLASSE WEITER UNGEKLÄRT

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der projektunabhängige WordPress-Kern für Glossare in mehreren Portalen.

**HIER BIST DU RICHTIG, WENN …**  
ein Portal ein eigenes Glossar mit getrenntem Backend, Oberbegriffen, kurzen Begriffstexten, eigenen Zieladressen und eigenen SEO-Metadaten benötigt, ohne normale Beiträge oder Bildpflicht.

**DU DARFST …**  
den neutralen Glossar-Kern, Datenvertrag, Backend-/Frontend-Vertrag und harte Tests projektübergreifend entwickeln.

**DU DARFST NICHT …**  
Pferde-Begriffe, Pferde-Oberbereiche, Pferde-Texte, Pferde-URLs oder Pferde-SEO-Schemata in den Kern hart einbauen, unterschiedliche Pakete unter derselben Version ausgeben oder Allgemeingültigkeit ohne zweites echtes Portal behaupten.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → erste Projektanwendung Pferde Atelier.

## MOD-ID

MOD-008

## LEITPRINZIP

**Ein neutraler Core. Projektspezifische Konfiguration außerhalb des Core.**

Pferde Atelier ist die erste Anwendung, aber keine Kernwahrheit.

## AKTUELLER TECHNISCHER NACHWEIS

Technischer Kandidat:
`Universal Glossary Engine 0.2.6`

Autoritativer Run:
`34748541630`

Bewiesen:
- Fresh-Install WordPress + MySQL + Astra positiv/negativ PASS;
- echter WordPress-In-place-Updateweg 0.2.5 → 0.2.6 positiv/negativ PASS;
- gezielt defekte Einzelbegriff-Rewrite-Regel erzeugt 404 und wird durch Schema-Migration 4 → 5 über den echten Updateweg repariert;
- komplette Frontend-/Regression-/Acceptance-Matrix nach Upgrade erneut PASS;
- gated Package erst nach beiden Hardtests;
- exaktes Actions-Artefakt zusätzlich lokal positiv und negativ geprüft.

Innerer Plugin-ZIP SHA-256:
`e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`

Details:
`TESTPROTOKOLL_0.2.6_20260913.md`

Dauerhafte Versions-/Update-Regel:
`ENTSCHEIDUNG_20260912.md`

## KERNFUNKTIONEN – PROJEKTUNABHÄNGIG

1. eigener WordPress-Backendbereich `Glossar`;
2. Glossarbegriffe als eigener Inhaltstyp – nicht im normalen Beitragsbereich;
3. eigene hierarchische Glossar-Gruppen;
4. erweiterbare Felder für Begriff, Kurzdefinition, Erklärung, Synonyme und verwandte Begriffe;
5. eigene SEO-Felder je Begriff;
6. eigene technisch auflösbare Zieladresse je veröffentlichtem Begriff;
7. auswählbare vorhandene Glossar-Hauptseite;
8. Frontend-Navigation nach Oberbegriffen und A–Z;
9. kompakte Glossar-Ausgabe ohne Bildpflicht;
10. keine automatische Veröffentlichung;
11. Import-/Export-Schnittstelle für strukturierte Datensätze;
12. Theme-/Portal-Anpassung über Konfiguration/CSS-Klassen und gebundene Schnittstellen, nicht über Fachcode.

## NICHT KERN

- Fachrecherche;
- Fachwahrheit;
- Textmaschine;
- Keywordrecherche;
- Affiliate;
- Bildsystem;
- projektspezifische Oberbegriffe;
- projektspezifische SEO-Formulierungen;
- projektspezifische Farben/Designwerte.

## TECHNISCHE KISS-ARCHITEKTUR

### Backend
WordPress erhält einen eigenen Menübereich `Glossar`.

Ein Glossarbegriff wird intern als eigener WordPress-Inhalt gespeichert, erscheint aber nicht unter normalen Beiträgen oder Seiten. Der Core steuert eigene Felder und eigene Ausgabe.

Oberbegriffe werden als eigene Glossar-Gruppen gespeichert, getrennt von normalen WordPress-Kategorien.

### Frontend
Ein Projekt wählt eine bereits vorhandene WordPress-Seite als `Glossar-Hauptseite`.

Der Core rendert dort automatisch Navigation, A–Z, Glossarbegriffsausgabe und Links auf die eigenen Begriffszieladressen.

### SEO
Jeder veröffentlichte Begriff besitzt eigene SEO-Felder, u. a. Titel und Meta-Description; Canonical/Index-Status sind konfigurierbar.

Keine Pflicht zur manuellen Yoast-Pflege und keine direkten Writes in interne Yoast-Datenbankfelder.

## PROJEKTKONFIGURATION

Jedes Portal liefert nur Konfiguration, z. B.:
- Hauptseiten-ID/Slug;
- öffentliche Bezeichnung `Glossar` oder andere Portalbezeichnung;
- URL-Basis;
- Oberbegriffe;
- SEO-Titel-Schema;
- Meta-Description-Schema;
- Textlängen-/Pflichtfelder;
- optionale Designwerte/-klassen;
- Importquelle.

## ALLGEMEINGÜLTIGKEITSREGEL

Trotz technischem 0.2.6-PASS bleibt MOD-008 formal:
`MODULKLASSE: UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Grund:
Ein neutrales Zweitprofil ist getestet, aber ein separates zweites echtes Portal als unabhängiger Realbeleg fehlt noch.

Erst dieser Beleg darf die formale Hochstufung auslösen.

## ERSTE PROJEKTANWENDUNG

PFERDE_ATELIER:
`../../PROJEKTE/PFERDE_ATELIER/GLOSSAR/START_HERE.md`

Fachliche Datenquelle dort:
`../../PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`

## GLOBALE ARBEITSORT-SPERRE

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
