# BÜRO GLOSSAR – PFERDE-ATELIER

STAND: 2026-09-13
STATUS: EINGANG AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das Steuerungsbüro für das öffentliche Pferde-Atelier-Glossar: Struktur, kurze Glossartexte, SEO-Felder, WordPress-Konfiguration, Navigation und Abnahme.

**HIER BIST DU RICHTIG, WENN …**  
du das öffentliche Glossar planst, einen recherchierten Begriff für die Veröffentlichung aufbereitest, Oberbegriffe/Navigation festlegst oder die Pferde-Anwendung des allgemeinen Glossarmoduls prüfst.

**DU DARFST …**  
quellengebundene Glossarfakten aus der Wissensdatenbank lesen, daraus kurze Veröffentlichungsfassungen ableiten, Pferde-Konfiguration/SEO-/Strukturbedarf definieren und im gebundenen Hobbyraum technische Kandidaten prüfen.

**DU DARFST NICHT …**  
eine zweite Glossar-Faktendatenbank aufbauen, ungeprüfte Fachfakten erfinden, normale Beiträge/Seiten pro Begriff erzwingen, Pferde-Fachlogik unkontrolliert in den Universal-Core schreiben, die große Textmaschine ohne belegten Bedarf anbinden oder DESIGN/TEXT/WISSENSDATENBANK ungefragt überschreiben.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → `PRODUKTIONSREGELN.md` → benötigtes Nachbarbüro.

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
- Regeln für A–Z/Verlinkung/Clusterproduktion;
- Übergabe an DESIGN bzw. TEXT/SEO nur bei echtem Fachbedarf.

### Allgemeiner technischer Kern
Autoritativ:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`

Modul:
`MOD-008 – Universal Glossar Engine`.

Der allgemeine Core verwaltet:
- eigenen Glossar-Inhaltstyp;
- eigene hierarchische Oberbereiche;
- auswählbare vorhandene Hauptseite;
- eigene Begriffszieladressen;
- erweiterbares Feldschema;
- Suche / A–Z;
- providerneutrale SEO-Felder;
- strukturierten JSON-Import/Export.

Pferde-spezifische Inhalte und Gestaltung bleiben Projektanwendung; allgemeine Kernlogik und projektspezifische Inhaltsproduktion dürfen nicht als zweite Fachwahrheit vermischt werden.

### WordPress
Vom Nutzer bestätigt: Die WordPress-Seite `Glossar` ist bereits angelegt und verlinkt.

Für einzelne Glossarbegriffe gilt:
- nicht als normale Beiträge ausgeben;
- nicht als normale Seiten pro Begriff manuell pflegen;
- kein Bildzwang;
- keine normalen Beitragskarten im Portal;
- eigene SEO-Angaben je veröffentlichtem Begriff.

**Importregel:** Ein generischer Datenimport veröffentlicht nicht ungeprüft automatisch.

**Clusterregel:** Für ausdrücklich gebundene maschinelle Pferde-Glossar-Produktionspakete gilt `PRODUKTIONSREGELN.md`: alle Cluster-Mitglieder zuerst als Entwurf anlegen, vollständig verbinden und prüfen; erst wenn der gesamte Cluster geschlossen ist, darf die gebundene Produktionsstrecke die vollständigen Cluster-Mitglieder gemeinsam veröffentlichen. Kein halber Cluster darf öffentlich werden.

Der Nutzer muss dafür keine normalen WordPress-Seiten/Kategorien/Beiträge pro Begriff anlegen.

### SEO-Meta
Gebundener KISS-Weg:
- SEO-Titel und Meta-Description je Begriff nach konfigurierbarem Schema;
- individuelle Überschreibung je Begriff möglich;
- keine manuelle Yoast-Pflege nötig;
- keine direkten Writes in interne Yoast-Datenbankfelder;
- Core funktioniert ohne Yoast;
- bei Yoast Nutzung nur über dessen Schnittstellen.

### Textproduktion
Aktuell keine eigene große Textmaschine und keine automatische Anbindung an die bestehende Artikel-Textmaschine.

Verbindlicher Pferde-Arbeitsweg für neue kurze Glossarbeiträge:
Fachfakten aus autoritativer Wissensquelle lesen → kurzen geschlossenen Themencluster bilden → alle Mitglieder als Entwurf anlegen → Inhalte/Meta/Kategorie/Beziehungen setzen → Links und Negativregeln prüfen → gesamten Cluster gemeinsam freigeben/veröffentlichen.

Details ausschließlich in `PRODUKTIONSREGELN.md`; Produktionsstatus ausschließlich in `BEGRIFFSREGISTER.md`.

Pferde-/Ponyrassen sind dort ausdrücklich ausgeschlossen und gehören in das separate Pferderassen-System.

## BENÖTIGTE NACHBARBÜROS

### WISSENSDATENBANK – Pflichtquelle Fachinhalt
`../WISSENSDATENBANK/START_HERE.md`
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`

### DESIGN – Referenz/Integration
`../DESIGN/START_HERE.md`

### TEXT/SEO – bei Suchintention/Kannibalisierung/SEO-Regeln
`../TEXT/START_HERE.md`

### PLUGINS – Inventar/Update/isolierte Ausgabekopie nach echter Pluginänderung
`../PLUGINS/START_HERE.md`

### WordPress-Werkzeugbestand
`../../../WORDPRESS_REGISTER.md`

## ARBEITSREGELN

1. KISS: kleinste tragfähige Erweiterung; keine Plugin-Orgie.
2. Backend und Frontend getrennt denken.
3. Flexibel/erweiterbar: allgemeine Kernfelder/-routen nicht unnötig projektspezifisch verdrahten.
4. Kein Grafikzwang.
5. Keine normalen Beitragskarten für Glossarbegriffe.
6. Eigene Meta-Angaben je Begriff brauchen eine technisch auflösbare eigene Zieladresse.
7. Fachwahrheit bleibt in WISSENSDATENBANK.
8. Bestehendes Designplugin bleibt unverändert; Integration wird gegen realen Designcode geprüft.
9. Vor Plugin-Ausgabe positiv und negativ testen.
10. `main` nicht für Experimente verändern.
11. Kein ungeprüftes automatisches Publizieren; gebundene Clusterpublikation nur nach vollständiger Closure gemäß `PRODUKTIONSREGELN.md`.
12. Kein Release-/LIVE-PASS aus lokalen Stubtests ableiten.
13. Unterschiedliche Paketbytes = unterschiedliche Pluginversion.
14. Bei echter Pluginentwicklung/-aktualisierung `../PLUGINS/` nach Abschlussregel synchronisieren; `CURRENT.zip` ist nur abgeleitete hashgebundene Kopie.

## SCHNELLWEGWEISER

- **Aktueller Bürostand:** `CURRENT_STATE.md`
- **Aktuelle Arbeit / NEXT ACTION:** `HOBBYRAUM.md`
- **Fehler:** `FEHLERQUELLEN.md`
- **Produktionsregeln:** `PRODUKTIONSREGELN.md`
- **Produktionsstatus Begriffe:** `BEGRIFFSREGISTER.md`
- **Zielvertrag:** `ZIELVERTRAG_GLOSSAR_ABDECKUNG_V1.md`
- **Seitenkonzept:** `SEITENKONZEPT_V1.md`
- **Allgemeiner Glossar-Core:** `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- **Fachdatenbank:** `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- **Design:** `../DESIGN/START_HERE.md`
- **TEXT/SEO:** `../TEXT/START_HERE.md`
- **Plugins:** `../PLUGINS/START_HERE.md`
- **WordPress-Werkzeugbestand:** `../../../WORDPRESS_REGISTER.md`
- **Handlungsverzeichnis:** `protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md`
- **Zentrales Fehler-Wegweiserregister:** `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- **Zentrales Warum-Register:** `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- **Zielregister:** `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`

## HARTE FEHLERABGLEICH-SPERRE
Vor jeder technischen Aktion zuerst `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` und die relevante Originalquelle prüfen. Bekannten Fehlerweg nicht erneut ausprobieren.

## Globale Arbeitsort-Sperre
Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
