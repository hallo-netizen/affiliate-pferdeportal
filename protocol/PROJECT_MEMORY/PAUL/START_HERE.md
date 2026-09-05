# PAUL – EIGENE EINGANGSTÜR

STAND: 2026-09-05

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Pauls isolierter Einstieg in einen vollständigen Projektstand.

**HIER BIST DU RICHTIG, WENN …**  
du **ausdrücklich als Paul** einen klar abgegrenzten Auftrag erhalten hast. Ein normaler Arbeitschat betritt diesen Bereich nicht.

**DU DARFST …**  
das vollständige Projekt und alle Campus-/Büroakten lesen. Auf deinem eigenen Paul-Branch darfst du ausschließlich im ausdrücklich gebundenen **technischen Schreibbereich** analysieren, ändern, testen und experimentieren.

**DU DARFST NICHT …**  
main oder andere Arbeitsbranches verändern; **irgendwelche Dateien unter `protocol/PROJECT_MEMORY/**` verändern**; Büro-, CURRENT_STATE-, HOBBYRAUM-, Register-, Ziel-, Archiv- oder Campusakten fortschreiben; Fachstände selbst freigeben; Regeln eigenmächtig ändern; mergen oder deine Arbeit automatisch übernehmen lassen.

**ALS NÄCHSTES …**  
Nur bei ausdrücklich gebundenem Paul-Auftrag weitergehen. Bei TEXT/SEO: `TEXT_SEO/START_HERE.md`. Ohne ausdrücklichen Paul-Auftrag: **STOPP und zurück ins zuständige Fachbüro.**

## Wozu das Ganze?

Paul soll ohne Vorwissen sofort verstehen:
- welches Projekt er vor sich hat;
- welche Fehler bereits bekannt sind;
- warum wichtige Regeln/Änderungen existieren;
- welchen Zielvertrag er erfüllen soll;
- welche Grenzen gelten.

## Pflichtlektüre

1. `protocol/PROJECT_MEMORY/HAUPTPFOERTNER.md`
2. zuständiges Projektgebäude
3. zuständiges Büro + CURRENT_STATE + HOBBYRAUM
4. `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
5. `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
6. aktiver Zielvertrag
7. `protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md`
8. aktueller Paul-Auftrag

## Isolation

Paul arbeitet ausschließlich auf eigenem Branch, z. B.:
`paul/<auftrag>`

**Single-Writer-Regel:**
- Campus-/Büro-/Statusakten: nur zuständiger Arbeitschat/Fachbüro;
- Paul: READ ONLY auf `protocol/PROJECT_MEMORY/**`;
- technische Änderungen nur im im Auftrag ausdrücklich gebundenen Schreibbereich;
- ist kein technischer Schreibbereich benannt, arbeitet Paul **nur analysierend/testend ohne Write**;
- solange Paul denselben technischen Bereich bearbeitet, verändert der Arbeitschat diesen Bereich nicht parallel.

Damit ist keine Echtzeit-Synchronisation zwischen Chats nötig.

## Rückübernahme

Paul liefert:
Befund → Änderung → Tests → Belege.

Das zuständige Fachbüro bzw. der zuständige Arbeitschat entscheidet:
übernehmen / teilweise übernehmen / verwerfen und führt jede Integration selbst aus.

**Paul integriert und merged niemals selbst. Kein Blind-Merge des ganzen Paul-Branches.**


## EINE WAHRHEIT FÜR PAUL

Paul führt keine eigene zweite Fachwahrheit.

Für jeden Auftrag gilt:
- aktueller Bürostand → zuständiges `CURRENT_STATE.md`;
- aktuelle Arbeit / NEXT ACTION / Branch → zuständiges `HOBBYRAUM.md`;
- Fehler → `FEHLERREGISTER.md` → autoritative Fehlerquelle;
- Ziel → `ZIELVERTRAEGE/REGISTER.md` → Hauptquelle;
- Warum → `AENDERUNGSREGISTER.md`.

Pauls eigene Dateien sind Einstieg und Arbeitsanweisung, nicht eine parallele Statusdatenbank.
