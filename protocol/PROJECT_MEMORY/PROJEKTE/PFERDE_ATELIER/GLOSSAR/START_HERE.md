# BÜRO GLOSSAR – PFERDE-ATELIER

STAND: 2026-09-14
STATUS: EINGANG AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das Steuerungsbüro für das öffentliche Pferde-Atelier-Glossar: Struktur, kurze Glossartexte, SEO-Felder, WordPress-Konfiguration, Navigation, Einzelansicht und Abnahme.

**HIER BIST DU RICHTIG, WENN …**  
du das öffentliche Glossar planst, einen recherchierten Begriff für die Veröffentlichung aufbereitest, Oberbegriffe/Navigation festlegst, die Einzelansicht gestaltest oder die Pferde-Anwendung des Glossarmoduls prüfst.

**DU DARFST …**  
quellengebundene Glossarfakten aus der Wissensdatenbank lesen, daraus kurze Veröffentlichungsfassungen ableiten, Pferde-Konfiguration/SEO-/Struktur-/Designbedarf definieren und im gebundenen Hobbyraum technische Kandidaten prüfen.

**DU DARFST NICHT …**  
eine zweite Glossar-Faktendatenbank aufbauen, ungeprüfte Fachfakten erfinden, normale Beiträge/Seiten pro Begriff erzwingen, bestätigte funktionierende Routingwege ohne Fehlerbeleg umbauen, normale WordPress-Artikel durch Glossar-Design verändern oder ungeprüft Pluginstände als LIVE/CURRENT behaupten.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → `FEHLERQUELLEN.md` → `TEXT_UND_LINKREGELN.md` → `PRODUKTIONSREGELN.md`.

## EINE WAHRHEIT – HARTE TRENNUNG

### Fachliche Begriffe, Definitionen und Quellen
Autoritativ ausschließlich:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`

Dort bleiben Begriff, Definition/Fakten, Quellen, Synonyme, fachliche Einordnung und verwandte Begriffe.

**Keine Kopie dieser Fachwahrheit im Büro GLOSSAR.**

### Öffentliche Glossarlogik
Dieses Büro ist zuständig für:
- Pferde-Oberbegriffe und Navigationskonzept;
- Veröffentlichungsfassung eines Begriffs;
- Pferde-spezifische SEO-/Feld-/Designkonfiguration;
- Abnahme der WordPress-Ausgabe;
- Regeln für A–Z, Verlinkung und Clusterproduktion;
- Gestaltung der Glossar-Einzelansicht;
- Übergabe an DESIGN bzw. TEXT/SEO nur bei echtem Fachbedarf.

### Allgemeiner technischer Kern
Autoritativ:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`

Modul:
`MOD-008 – Universal Glossar Engine`.

Pferde-spezifische Inhalte und Gestaltung bleiben Projektanwendung; allgemeine Kernlogik und projektspezifische Inhaltsproduktion dürfen nicht als zweite Fachwahrheit vermischt werden.

### WordPress
Für einzelne Glossarbegriffe gilt:
- eigener Inhaltstyp `uge_term`;
- nicht als normale Beiträge ausgeben;
- nicht als normale Seiten pro Begriff manuell pflegen;
- kein Bildzwang;
- eigene SEO-Angaben je Begriff;
- Glossar-Einzelansicht darf normale Posts/Seiten technisch und optisch nicht beeinflussen.

## VERBINDLICHE TEXTPRODUKTION

Pflichtquelle:
`TEXT_UND_LINKREGELN.md`

Kernregeln:
- ca. 150–200 Wörter;
- keine Zwischenüberschriften im Begriffstext;
- keine wiederkehrenden Floskeln/Schablonen;
- nur `GEPRUEFT`-WDB-Fakten;
- Kurzdefinition/Zusammenfassung Pflicht;
- dasselbe Linkziel nie zweimal;
- Fließtext bevorzugt passende übergeordnete Portal-Kategorie;
- Journal nur ersatzweise;
- verwandte Glossarbegriffe als Links ausschließlich im Block `Verwandte Begriffe`, nicht zusätzlich im Fließtext.

Produktionsstatus ausschließlich in `BEGRIFFSREGISTER.md`.

Pferde-/Ponyrassen sind ausdrücklich ausgeschlossen und gehören in das separate Pferderassen-System.

## BENÖTIGTE NACHBARBÜROS

- WISSENSDATENBANK: `../WISSENSDATENBANK/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- PLUGINS: `../PLUGINS/START_HERE.md`
- WordPress-Werkzeugbestand: `../../../WORDPRESS_REGISTER.md`

## ARBEITSREGELN

1. KISS: kleinste tragfähige Erweiterung; keine Plugin-Orgie.
2. Backend und Frontend getrennt denken.
3. Kein Grafikzwang.
4. Fachwahrheit bleibt in WISSENSDATENBANK.
5. Vor jeder Plugin-Ausgabe positiv und negativ testen.
6. `main` nicht als Experimentierfläche verwenden.
7. Kein Release-/LIVE-PASS aus lokalen Stub-/Browser-/Codeprüfungen ableiten.
8. Unterschiedliche Paketbytes = unterschiedliche Pluginversion bzw. eindeutig gebundener Buildstand.
9. Bei echter Pluginentwicklung/-aktualisierung `../PLUGINS/` nach Abschlussregel synchronisieren; `CURRENT.zip` ist nur abgeleitete hashgebundene Kopie.
10. Designänderungen an Glossar-Einzelansichten müssen hart auf `uge_term` begrenzt und gegen normale Posts negativ geprüft werden.
11. Bekannten funktionierenden Routingweg nicht ohne neuen Fehlerbeleg umbauen.
12. Neue Begriffe erst nach frisch belegtem `GEPRUEFT`-Status der WDB-Quelle.

## SCHNELLWEGWEISER

- Aktueller Bürostand: `CURRENT_STATE.md`
- Aktuelle Arbeit / NEXT ACTION: `HOBBYRAUM.md`
- Fehler: `FEHLERQUELLEN.md`
- Text-/Linkregeln: `TEXT_UND_LINKREGELN.md`
- Produktionsregeln: `PRODUKTIONSREGELN.md`
- Produktionsstatus Begriffe: `BEGRIFFSREGISTER.md`
- Zielvertrag: `ZIELVERTRAG_GLOSSAR_ABDECKUNG_V1.md`
- Seitenkonzept: `SEITENKONZEPT_V1.md`
- Allgemeiner Glossar-Core: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- Plugins: `../PLUGINS/START_HERE.md`

## HARTE FEHLERABGLEICH-SPERRE
Vor jeder technischen Aktion zuerst die relevante Original-Fehlerquelle und `CURRENT_STATE.md` prüfen. Bekannten Fehlerweg nicht erneut ausprobieren.

## Globale Arbeitsort-Sperre
Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
