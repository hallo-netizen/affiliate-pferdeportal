# AKTENSCHRANK GLOSSAR

STAND: 2026-09-15
STATUS: AKTIV / MASSENAUFBAU-VERTRAG

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Die zentrale quellengebundene Fachbegriffs-Datenbasis des Pferde-Ateliers.

**UMFANG**  
Aufgenommen wird grundsätzlich jeder sinnvoll erklärbare Begriff, der im weitesten fachlichen Sinn mit Pferden, Pferdehaltung, Reiten, Pferdesport, Medizin, Zucht, Ausrüstung, Geschichte, Kultur, Recht, Wirtschaft oder dem Leben mit Pferden zusammenhängt.

**EINZIGER FACHLICHER AUSSCHLUSS**  
Ein neuer Glossarbegriff wird nicht angelegt, wenn sein technisch normalisierter sichtbarer Begriff **identisch mit einem vorhandenen WordPress-Kategorienamen** ist. Keine Singular/Plural-Gleichsetzung, keine Portal-Seiten-Sperre, keine Artikel-/Kannibalisierungssperre, keine Keyword- oder Suchvolumen-Sperre.

Bestehende Glossarbegriffe und Synonyme werden weiterhin dedupliziert: Ein Begriff = ein Datensatz; Synonyme sind Aliase und keine neuen Datensätze.

## RECHERCHE UND TEXT

Ein dedizierter **Glossar-Worker** übernimmt pro Begriff Recherche **und** Kurztext in demselben Arbeitsschritt. Es gibt keine separate Übergabe Recherche → Texter.

Recherche folgt verbindlich `../../RECHERCHE_STANDARD.md`:
- bevorzugt eine autoritative Primärquelle;
- wenn keine geeignete Primärquelle existiert, zwei voneinander unabhängige hochwertige Quellen;
- Medizin, Recht, aktuelle Regeln und andere Hochrisikothemen nur nach den dort strengeren Fachregeln;
- unzureichend belegte Begriffe bleiben `NACHRECHERCHE` und werden nicht erfunden.

Die Maschine besitzt Workflow und Schutzregeln. Der Worker recherchiert und formuliert, darf aber Kandidatenidentität, Kategorien-Ausschluss, Validierung, WordPress-Write oder Readback nicht umgehen.

## MASSENWEG

`Begriffspool → exakter Kategorienamen-Check → Glossar-Worker (Recherche + Text) → Validator → uge-json-v1/Research-Paket → WordPress → Readback`

Der Pool darf in großen Batches wachsen. Dubletten- und Kategorienamenprüfung müssen mengenfähig über Schlüssel/Indizes erfolgen; keine paarweisen Vollvergleiche des gesamten Bestands.

## TEXTVERTRAG – KURZ

- 150–200 Wörter;
- individueller Einstieg je Begriff;
- fachlich erklären und sauber abgrenzen;
- Hauptbegriff und Pferdekontext natürlich verwenden;
- keine Generator-/Schablonenphrasen;
- kein Keyword-Stuffing;
- 0 Bodylinks;
- individuelle SEO-Titel und Meta-Description;
- Quellen bleiben am Datensatz/Research-Paket gebunden.

## STRUKTUR

Ein Begriff = ein Datensatz. Verbindliche Felder und Oberbereiche stehen in `GLOSSAR_STRUKTUR.md`.

**ALS NÄCHSTES**  
`GLOSSAR_STRUKTUR.md` → `GLOSSAR_REGISTER.md` → `DATEN/START_HERE.md`.
