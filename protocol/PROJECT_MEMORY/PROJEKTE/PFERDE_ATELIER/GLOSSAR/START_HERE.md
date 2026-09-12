# BÜRO GLOSSAR – PFERDE-ATELIER

STAND: 2026-09-12
STATUS: EINGANG AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das Steuerungsbüro für das öffentliche Pferde-Atelier-Glossar: Struktur, kurze Glossartexte, SEO-Felder, WordPress-Konzept, Navigation und Übergaben an Design/Technik.

**HIER BIST DU RICHTIG, WENN …**  
du das öffentliche Glossar planst, einen recherchierten Begriff für die Veröffentlichung aufbereitest, Oberbegriffe/Navigation festlegst oder die WordPress-/Design-Anbindung prüfst.

**DU DARFST …**  
quellengebundene Glossarfakten aus der Wissensdatenbank lesen, daraus kurze Veröffentlichungsfassungen ableiten, SEO-/Strukturbedarf definieren und im gebundenen Hobbyraum technische Kandidaten prüfen.

**DU DARFST NICHT …**  
eine zweite Glossar-Faktendatenbank aufbauen, ungeprüfte Fachfakten erfinden, normale Beiträge/Seiten pro Begriff erzwingen, die große Textmaschine ohne belegten Bedarf anbinden oder DESIGN/TEXT/WISSENSDATENBANK ungefragt überschreiben.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → benötigtes Nachbarbüro.

---

## EINE WAHRHEIT – HARTE TRENNUNG

### Fachliche Begriffe, Definitionen und Quellen
Autoritativ ausschließlich:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`

Dort bleiben:
- Begriff;
- Definition/Fakten;
- Quellen;
- Synonyme;
- fachliche Einordnung;
- verwandte Begriffe.

**Keine Kopie dieser Fachwahrheit im Büro GLOSSAR.**

### Öffentliche Glossarlogik
Dieses Büro ist zuständig für:
- Oberbegriffe und Navigationskonzept;
- Veröffentlichungsfassung eines Begriffs;
- benötigte Felder für SEO und Frontend;
- WordPress-Backend-Konzept;
- Regeln für Aufklapper/A-Z/Verlinkung;
- Übergabe an DESIGN bzw. TEXT/SEO;
- Abnahme der Glossar-spezifischen Funktion.

### WordPress
Zielrichtung: Glossarbegriffe sollen **nicht wie normale Beiträge** erscheinen und **keinen Bildzwang** haben. Jeder veröffentlichte Begriff soll technisch eigene SEO-Angaben erhalten können. Die exakte Speicherung/URL-Logik wird erst nach Prüfung des bestehenden Designplugins verbindlich festgelegt.

**Kein zweites CMS im Plugin bauen.**

### Textproduktion
Aktuell **keine eigene große Textmaschine** und keine automatische Anbindung an die bestehende Artikel-Textmaschine.

Für Glossartexte gilt KISS:
Fachfakten lesen → kurze standardisierte Veröffentlichungsfassung → SEO-/Qualitätsprüfung → WordPress.

Der spätere Kurztextstandard darf sich an den bewährten strengen Regeln der Kategorietexte orientieren, ohne deren Technik blind zu kopieren.

---

## BENÖTIGTE NACHBARBÜROS

### 1. WISSENSDATENBANK – PFLICHTQUELLE FÜR FACHINHALT
`../WISSENSDATENBANK/START_HERE.md`

Glossar-Aktenschrank:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`

**Aufgabe:** recherchierte Fachwahrheit und Quellen.  
**Nicht Aufgabe:** öffentliche WordPress-/SEO-/Designentscheidung.

### 2. DESIGN – PFLICHT BEI DARSTELLUNG/PLUGIN
`../DESIGN/START_HERE.md`

**Aufgabe:** Pferde-Atelier-Design, vorhandenes Designplugin, Kategorietext-Mechanik, Frontend-Darstellung.  
Das Büro GLOSSAR definiert den Bedarf; DESIGN liefert/prüft die technische Darstellung im gebundenen Arbeitsweg.

### 3. TEXT/SEO – BEI SEO-/SUCHINTENT-/KANNIBALISIERUNGSFRAGEN
`../TEXT/START_HERE.md`

**Aufgabe:** bestehender SEO-/Textbestand, Keyword-/Kannibalisierungsprüfung, globale Text-/SEO-Regeln.  
Glossarbegriffe werden nicht automatisch Teil der normalen Artikelproduktion.

### 4. CAMPUS-WORDPRESS-REGISTER – WERKZEUGBESTAND PRÜFEN
`../../../WORDPRESS_REGISTER.md`

Vor neuer WordPress-Technik prüfen, ob vorhandene Komponenten wiederverwendet werden können.

---

## ARBEITSREGELN

1. **KISS:** kleinste tragfähige Erweiterung; keine Plugin-Orgie.
2. **Backend und Frontend getrennt denken.** Backend = Speichern/Pflegen/SEO-Felder. Frontend = Navigation/Oberbegriffe/Aufklapper/Einzel-URL falls nötig.
3. **Kein Grafikzwang.** Glossarbegriffe benötigen standardmäßig kein Beitragsbild.
4. **Keine normalen Beitragskarten.** Glossarbegriffe dürfen nicht ungefragt in normalen Kategorie-/Beitragslisten auftauchen.
5. **SEO pro Begriff nur mit technischer Zieladresse.** Eigene Meta-Angaben sind nur sinnvoll, wenn der veröffentlichte Begriff eine indexierbare eigene Zieladresse besitzt.
6. **Fachwahrheit bleibt in WISSENSDATENBANK.** Öffentliche Fassung ist ein Veröffentlichungsartefakt, keine zweite Rechercheakte.
7. **Keine technische Umsetzung aus Erinnerung.** Vor Änderung aktuellen DESIGN-/WordPress-Bestand frisch prüfen.
8. **Vor Plugin-Ausgabe positiv und negativ testen.** Kein PASS nur aus Codeansicht.
9. **`main` nicht für Experimente verändern.** Technische Kandidaten ausschließlich im gebundenen Hobbyraum/Branch.
10. **Keine automatische Veröffentlichung.** WordPress-Ausgabe/Import erst nach ausdrücklicher Freigabe und bestandenem Test.

---

## SCHNELLWEGWEISER – EINE WAHRHEIT

- **Aktueller Glossar-Bürostand:** `CURRENT_STATE.md`
- **Aktuelle Arbeit / NEXT ACTION:** `HOBBYRAUM.md`
- **Fachliche Glossar-Datenbank:** `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- **Design:** `../DESIGN/START_HERE.md`
- **TEXT/SEO:** `../TEXT/START_HERE.md`
- **WordPress-Werkzeugbestand:** `../../../WORDPRESS_REGISTER.md`
- **Handlungsverzeichnis:** `protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md`
- **Fehler:** `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle
- **Warum geändert:** `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- **Ziel:** `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- **Historie:** `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

## HARTE FEHLERABGLEICH-SPERRE

Vor jeder technischen Aktion:
1. `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` lesen;
2. relevante autoritative Fehlerquelle prüfen;
3. bekannten Fehler/verbotenen Weg nicht erneut ausprobieren;
4. erst bei belegtem KEIN-TREFFER technische Arbeit fortsetzen.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
