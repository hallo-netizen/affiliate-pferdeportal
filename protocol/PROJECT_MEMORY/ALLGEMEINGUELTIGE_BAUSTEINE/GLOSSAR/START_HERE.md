# ALLGEMEINGÜLTIGER BAUSTEIN – UNIVERSAL GLOSSAR ENGINE

STAND: 2026-09-12
STATUS: KONZEPT / ALLGEMEINGÜLTIGKEIT ZIEL, NOCH NICHT TECHNISCH BEWIESEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der projektunabhängig geplante WordPress-Kern für Glossare in mehreren Portalen.

**HIER BIST DU RICHTIG, WENN …**  
ein Portal ein eigenes Glossar mit getrenntem Backend, Oberbegriffen, kurzen Begriffstexten, eigenen Zieladressen und eigenen SEO-Metadaten benötigt, ohne normale Beiträge oder Bildpflicht.

**DU DARFST …**  
den neutralen Glossar-Kern, Datenvertrag, Backend-/Frontend-Vertrag und Tests projektübergreifend entwickeln.

**DU DARFST NICHT …**  
Pferde-Begriffe, Pferde-Oberbereiche, Pferde-Texte, Pferde-URLs oder Pferde-SEO-Schemata in den Kern hart einbauen oder Allgemeingültigkeit ohne zweiten Projektbeleg behaupten.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → erste Projektanwendung Pferde-Atelier.

## MOD-ID

MOD-008

## LEITPRINZIP

**Ein neutraler Core. Projektspezifische Konfiguration außerhalb des Core.**

Pferde-Atelier ist die erste Anwendung, aber keine Kernwahrheit.

## KERNFUNKTIONEN – PROJEKTUNABHÄNGIG

1. eigener WordPress-Backendbereich `Glossar`;
2. Glossarbegriffe als eigene kleine Datensätze – nicht im normalen Beitragsbereich;
3. Oberbegriffe/Gruppen zur Ordnung und Navigation;
4. Felder für Begriff, Kurzdefinition, Erklärung, Synonyme, verwandte Begriffe;
5. eigene SEO-Felder je Begriff;
6. eigene technisch auflösbare Zieladresse je veröffentlichtem Begriff;
7. zentrale Glossar-Hauptseite als Ausgabepunkt;
8. Frontend-Navigation nach Oberbegriffen und A–Z;
9. kompakte Aufklappdarstellung ohne Bildpflicht;
10. keine automatische Veröffentlichung;
11. Import-/Export-Schnittstelle für strukturierte Datensätze;
12. Theme-/Portal-Anpassung ausschließlich über Konfiguration/CSS-Klassen, nicht über Fachcode.

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

Der Core rendert dort automatisch:
- Oberbegriff-Navigation;
- A–Z;
- Begriffsliste/Aufklapper;
- Links auf die eigenen Begriffszieladressen.

### SEO
Jeder veröffentlichte Begriff besitzt eigene Felder:
- SEO-Titel;
- Meta-Description;
- optional Canonical/Index-Status.

Der Core darf diese Werte selbst an WordPress/SEO-Ausgabe übergeben. Keine Pflicht zur manuellen Yoast-Pflege und keine harte Bindung an Yoast.

## PROJEKTKONFIGURATION

Jedes Portal liefert nur Konfiguration, z. B.:
- Hauptseiten-ID/Slug;
- öffentliche Bezeichnung `Glossar` oder andere Portalbezeichnung;
- URL-Basis;
- Oberbegriffe;
- SEO-Titel-Schema;
- Meta-Description-Schema;
- Textlängen-/Pflichtfelder;
- optionale Designklassen;
- Importquelle.

## ALLGEMEINGÜLTIGKEITSREGEL

Bis zum echten Test mit einer zweiten, fachlich anderen Portal-Konfiguration bleibt MOD-008 formal:
`MODULKLASSE: UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Erst wenn derselbe Core ohne Codeänderung mit mindestens zwei Projektkonfigurationen funktioniert, darf auf `ALLGEMEINGÜLTIG` hochgestuft werden.

## ERSTE PROJEKTANWENDUNG

PFERDE_ATELIER:
`../../../PROJEKTE/PFERDE_ATELIER/GLOSSAR/START_HERE.md`

Fachliche Datenquelle dort:
`../../../PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`

## GLOBALE ARBEITSORT-SPERRE

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
