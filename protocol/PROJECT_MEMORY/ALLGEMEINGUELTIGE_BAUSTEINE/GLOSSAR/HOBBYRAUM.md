# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / V1-KONZEPT

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**HIER BIST DU RICHTIG, WENN …**  
der projektunabhängige WordPress-Kern des Glossars entworfen, gebaut oder getestet wird.

**DU DARFST …**  
den neutralen Core, Datenvertrag, Projektkonfiguration und Positiv-/Negativtests entwickeln.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den Core schreiben, `main` verändern, das bestehende Designplugin als Glossar-Engine umbauen oder vor Test-PASS einen Release behaupten.

**ALS NÄCHSTES …**  
V1-Vertrag festlegen → Core-Prototyp bauen → Pferde-Konfiguration + neutrale Zweitkonfiguration testen.

## AKTUELLER AUFTRAG

Ein allgemeingültig geplantes Glossarplugin konzipieren, dessen erste reale Anwendung das Pferde Atelier ist.

## V1-KERNVERTRAG

Pflicht:
- eigener Backend-Menübereich;
- eigener Glossarbegriff-Datensatz;
- eigene Glossar-Oberbegriffe;
- eigene Zieladresse je veröffentlichtem Begriff;
- eigene SEO-Titel-/Meta-Description-Felder;
- zentrale Hauptseite als auswählbarer Ausgabepunkt;
- A–Z + Oberbegriffe + Aufklapper;
- kein Bildzwang;
- kein normales Beitragsarchiv;
- kein Auto-Publish;
- Import/Export strukturierter Datensätze;
- keine Yoast-Pflichtabhängigkeit;
- keine Fachbegriffe im Core.

## PROJEKTKONFIGURATION – MUSS AUSSERHALB DES CORE BLEIBEN

- Portalname;
- Glossarbezeichnung;
- Hauptseiten-ID/Slug;
- URL-Basis;
- Oberbegriffe;
- SEO-Schema;
- Text-/Pflichtfeldregeln;
- Designklassen;
- Importquelle.

## TESTVERTRAG

POSITIV:
1. Pferde-Konfiguration funktioniert ohne Core-Codeänderung.
2. fachlich neutrale Zweitkonfiguration funktioniert ohne Core-Codeänderung.
3. Begriff erscheint nur im Glossarbereich, nicht unter normalen Beiträgen.
4. eigene URL, SEO-Titel und Meta-Description werden korrekt ausgegeben.
5. Hauptseite zeigt Oberbegriffe/A–Z/Begriffe.

NEGATIV:
1. fehlende Hauptseite → fail-closed, keine fremde Seite überschreiben;
2. fehlender SEO-Wert → definierter Fallback, kein doppelter Meta-Tag;
3. deaktiviertes Yoast → Core bleibt funktionsfähig;
4. aktiviertes Yoast → keine doppelten Titel/Descriptions;
5. normaler Beitrag → vom Glossar-Renderer unberührt;
6. normales Designplugin → unverändert.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

Nur wenn der Zweitportaltest beweist, dass eine Projektspezifik nicht sauber konfigurierbar ist:
Core beibehalten + kleiner Adapter. Kein zweiter vollständiger Fork.

## RÜCKGABEWEG

Projektanwendung Pferde Atelier:
`../../../PROJEKTE/PFERDE_ATELIER/GLOSSAR/`

Fachquelle Pferdebegriffe:
`../../../PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
