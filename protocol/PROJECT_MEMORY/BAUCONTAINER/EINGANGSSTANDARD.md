# CAMPUS – EINGANGSSTANDARD

STAND: 2026-09-05
REGEL: **Ein Klick = alles klar.**

Jeder Campus-, Gebäude-, Büro- und besondere Arbeitseingang beginnt mit einer kurzen `1-KLICK-ÜBERSICHT`.

Sie muss sofort beantworten:

1. **WAS IST DAS?**
2. **HIER BIST DU RICHTIG, WENN …**
3. **DU DARFST …**
4. **DU DARFST NICHT …**
5. **ALS NÄCHSTES …**

Danach dürfen erst Details, Quellen und Sonderregeln folgen.

## Ebenenspezifisch

### Campus-Eingang
Erklärt:
- Zweck des Campus;
- Pförtnerrolle;
- Routing;
- globale Sperren.

### Gebäude-Eingang
Erklärt:
- Zweck des Projekts/Gebäudes;
- vorhandene Büros;
- wie man das richtige Büro findet;
- was auf Gebäudeebene erlaubt/verboten ist.

### Büro-Eingang
Erklärt:
- Fachzuständigkeit;
- Schreibgrenze;
- wichtigste Originalquellen;
- `CURRENT_STATE` und `HOBBYRAUM` als nächste Schritte.

### Paul-Eingang
Erklärt:
- **WORKER_ONLY – nur bei ausdrücklichem Paul-Auftrag**;
- vollständiges Leserecht;
- `protocol/PROJECT_MEMORY/**` und Büroakten = READ ONLY;
- technischer Schreibbereich muss ausdrücklich gebunden sein;
- eigener `paul/*`-Branch;
- keine Integration / kein Merge durch Paul;
- Rückübernahme nur durch zuständigen Arbeitschat/Fachbüro;
- kein paralleles Schreiben am selben technischen Bereich.

## KISS

Kein langer Einführungstext vor der 1-KLICK-ÜBERSICHT.

Ein neuer Chat soll nach dem ersten Bildschirm wissen:
**Wo bin ich, wozu ist das da, was darf ich, was darf ich nicht und wo geht es weiter?**


## Dauerhafte Adressen

Bestehende Campus-/Gebäude-/Büro-/Paul-Eingangsadressen werden nicht still umbenannt oder verschoben.

Wenn später eine neue Struktur nötig wird:
- alte Adresse bleibt als eindeutiger Weiterweiser erhalten;
- keine tote Eingangstür;
- bereits verteilte Paul-/Chat-Einstiege bleiben funktionsfähig.

## Büro-Pflichtweg

Jeder Projektbüro-Eingang muss im sichtbaren nächsten Schritt enthalten:
`CURRENT_STATE.md` → `HOBBYRAUM.md`.

Weitere Inventare/Quellen dürfen danach folgen.

## Paul-Pfade

Pflichtlektüre für Paul verwendet vollständige echte Pfade.

Keine Abkürzungen wie:
`.../datei.md`

## Dauertexte statt Chattexte

Dauerhafte Eingänge und Hobbyräume dürfen keine Berechtigung an Formulierungen wie
„dieser Chat“, „Sortierchat“ oder einen längst vergangenen Parallelchat knüpfen.

Temporäre Belegung gehört in den Hobbyraumstatus; dauerhafte Rechte kommen aus Rolle, Zielvertrag und Arbeitsweg.


## Direkter Büro-/Hobbyraum-Einstieg

Ein direkter Link in ein Büro darf Hauptpförtnerwissen nicht voraussetzen.

Projektbüros führen bei echter Arbeit zusätzlich sichtbar zu:
- Handlungsverzeichnis;
- Fehlerregister;
- Änderungsregister;
- Zielvertragsregister.

Ein direkter Hobbyraum-Einstieg erfüllt ebenfalls die 1-Klick-Übersicht.


## Flächendeckende Eingangstafel

Jedes echte Verzeichnis unter `protocol/PROJECT_MEMORY/` besitzt eine `START_HERE.md`.

Auch Lesesammlungen, Flure und Bestandsräume sind damit bei Direktlink selbsterklärend.

Neue Verzeichnisse ohne `START_HERE.md` sind ein Architekturfehler.


## Rollen der Informationsquellen

Für Projektbüros gilt:
- START_HERE = Orientierung
- CURRENT_STATE = aktuelle Büro-Zusammenfassung
- HOBBYRAUM = aktuelle Arbeitsbindung
- FEHLERREGISTER = Index zur Fehlerquelle
- ZIELVERTRAEGE/REGISTER = Index zur Zielquelle
- AENDERUNGSREGISTER = Begründungen
- ARCHIV/REGISTER = Historie

Aktuelle Versions-, Fehler- oder Zielangaben werden nicht parallel in mehreren Wegweisern gepflegt.


## Spezialworker-Regel – Single Writer, Multi Reader

Spezialworker wie Paul sind **nicht Teil der normalen Campus-Navigationskette**.

Sie werden ausschließlich durch ausdrücklichen Auftrag aktiviert.

Grundregel:
- mehrere Chats dürfen dieselben Quellen lesen;
- offizielle Büro-/Campuswahrheit hat genau einen Schreiber;
- Spezialworker verändern keine Büro-/Campusakten;
- technische Parallelbranches sind nur für klar abgegrenzte Schreibbereiche zulässig;
- derselbe technische Schreibbereich hat gleichzeitig genau einen aktiven Schreiber;
- Spezialworker liefern Lösungspakete zurück; der zuständige Arbeitschat entscheidet und integriert.

Damit verlangt der Campus **keine Echtzeit-Synchronisation zwischen Chats**.


## Universelle Protokollpflicht vor Abschluss

Diese Regel gilt für **jede Ebene und jeden Raum** unter PROJECT_MEMORY, einschließlich Campus, Projektgebäude, Büros, Hobbyräume, Paul, Register, Archiv, Tresor und Baucontainer.

Vor `fertig`, `PASS` oder Übergabe:
1. aktuellen autoritativen Stand frisch lesen;
2. prüfen, ob Fehlerquelle betroffen ist;
3. tatsächliche Arbeit protokollieren;
4. dauerhaftes WAS/WARUM im Änderungs-/Erklärungsregister nachziehen;
5. CURRENT_STATE nur bei geändertem belastbarem Stand;
6. HOBBYRAUM/NEXT ACTION nur bei geändertem Auftrag/Arbeitsstand;
7. Zielvertrag nur bei echter Zieländerung;
8. negativ prüfen, dass keine zweite Wahrheit oder Historie als CURRENT entstanden ist.

Wenn ein Punkt nicht betroffen ist: **nicht künstlich ändern**.

Ein Abschluss ohne diese Prüfung ist kein belastbarer Campus-PASS.


## Maschinenlesbarer PROTOKOLLCHECK – technische Abschlussbremse

Für jeden PR, der irgendeinen Pfad unter `protocol/PROJECT_MEMORY/**` verändert, muss der PR-Text künftig genau einen maschinenlesbaren Abschlussblock enthalten:

```
PROTOKOLLCHECK
FEHLER: PASS|NACHGEHOLT|NICHT_BETROFFEN
PROTOKOLL: PASS|NACHGEHOLT|NICHT_BETROFFEN
WARUM: PASS|NACHGEHOLT|NICHT_BETROFFEN
CURRENT_STATE: PASS|NACHGEHOLT|NICHT_BETROFFEN
HOBBYRAUM_NEXT_ACTION: PASS|NACHGEHOLT|NICHT_BETROFFEN
ZIELVERTRAG: PASS|NACHGEHOLT|NICHT_BETROFFEN
ARCHIV: PASS|NACHGEHOLT|NICHT_BETROFFEN
EINE_WAHRHEIT: PASS
TESTS: PASS
TECHNISCHE_CHECKS: PASS|NICHT_BETROFFEN
```

Technische Regel nach Aktivierung des Security-Hardlocks:
- fehlt der Block → FAIL;
- fehlt ein Feld → FAIL;
- `EINE_WAHRHEIT != PASS` → FAIL;
- `TESTS != PASS` → FAIL;
- ein tatsächlich geänderter CURRENT_STATE/HOBBYRAUM/Ziel-/Archiv-/Fehler-/Protokoll-/WARUM-Pfad darf nicht als `NICHT_BETROFFEN` deklariert werden;
- Architekturdateien wie START_HERE, Hauptpförtner, Handlungsverzeichnis oder Baucontainer-Standards erzwingen zusätzlich eine Änderung von `AENDERUNGSREGISTER.md` und `BAUCONTAINER/BAUPROTOKOLL.md`.

**Geltungsbereich:** der gesamte Baum `protocol/PROJECT_MEMORY/**`. Damit gilt die Abschlussbremse auch für den Baucontainer selbst, Paul-Akten, Archive, Tresor, Register, Gebäude, Büros und Hobbyräume.

Die Prüfung ersetzt nicht die fachliche Wahrheit. Sie zwingt nur dazu, die Abschlussentscheidung sichtbar und widerspruchsfrei zu treffen.

AKTIVIERUNGSSTATUS:
Vorbereitet im Security-PR #137; noch nicht auf `main` aktiv, solange der immutable Base-Hardlock die eigene Security-Wartung blockiert.
