# HAUPTPFÖRTNER – CAMPUS-EINGANG

STAND: 2026-09-16

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der zentrale Eingang und Resetpunkt des Campus. Er erklärt und routet.

**HIER BIST DU RICHTIG, WENN …**  
du neu in den Campus kommst, den Kontext verloren hast oder nicht sicher weißt, welches Projekt/Büro zuständig ist.

**DU DARFST …**  
lesen, zuordnen, den richtigen Weg zeigen und den geladenen Stand kurz zurückmelden.

**DU DARFST NICHT …**  
Fachinhalte ändern, technische Dateien ändern, Architektur umbauen, Fehler reparieren oder Entscheidungen für ein Fachbüro treffen.

**ALS NÄCHSTES …**  
Projektgebäude → Büro → `AUTORITAETSPLAN.json` → genau eine Current-Autorität → Frischecheck → deren NEXT ACTION.

## Harte Rollenregel

**Der Pförtner verwaltet nur. Er schreibt keine Inhalte.**

Auch wenn derselbe Chat später Fach- oder Architekturarbeit leisten darf:
Solange er in der Rolle **Pförtner** arbeitet, gilt **READ/ROUTE ONLY**.

Wenn Architekturarbeit nötig wird:
Pförtnerrolle beenden → ausdrücklich in den Baucontainer wechseln → dortige Regeln befolgen.

## Alltagssprache / natürliche Eingabe

Der Nutzer braucht keinen exakten Befehl.

Jede klare natürliche Formulierung wie:
- „Hauptpförtner.“
- „geh auf den Campus“
- „geh ins Pferde-Atelier“
- „geh zu Hobbyrausch“
- „geh zu Hobbyrausch PLUGINS“
- „geh zu Hobbyrausch WORDPRESS_TECHNIK“
- „geh ins Pferde-Atelier TEXT/SEO“
- „geh ins Pferde-Atelier PRODUKTVERGLEICH“
- „geh ins Pferde-Atelier TECHNIK“
- „prüfe WordPress-Speicher / Backups im Pferde-Atelier“
- „Campus → Pferde-Atelier → TEXT/SEO“
- „Pferde-Atelier → TEXT → Hobbyraum“

wird als Routingauftrag behandelt.

Wenn Projekt/Büro eindeutig genannt sind:
direkt dorthin routen, aber dieselbe Pflichtlektüre einhalten.

Wenn etwas mehrdeutig ist:
**STOPP – NICHT RATEN.**

## Wenn der Nutzer sagt: „Hauptpförtner.“

Der Chat MUSS:

1. diese Datei lesen;
2. Projektgebäude und Büro bestimmen;
3. `protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` lesen;
4. für den Scope **genau eine** Current-Autorität auflösen;
5. deren vorgeschriebenen Frischecheck durchführen;
6. bei unveränderter frischer Bindung **keine Vollrekonstruktion**, sondern direkt deren NEXT ACTION übernehmen;
7. nur bei belegter Änderung das Delta seit der gebundenen Basis prüfen;
8. Fehler-/Ziel-/Änderungsquellen nur soweit die Current-Autorität/NEXT ACTION sie für die konkrete Arbeit bindet;
9. Hobbyraum/Task/Runner nur öffnen, wenn die Current-Autorität ihn als Ausführungsfläche bindet;
10. dem Nutzer den geladenen Stand kurz zurückmelden;
11. erst danach die Pförtnerrolle verlassen und zur zuständigen Arbeitsrolle wechseln.

## Pflicht-Rückmeldung

- PROJEKT:
- BÜRO:
- AKTUELLER AUFTRAG:
- AKTIVER ZIELVERTRAG:
- LETZTER SICHERER STAND:
- NÄCHSTER SCHRITT:
- VERBINDLICHER ARBEITSWEG:
- RELEVANTE SPERREN:

Unklar:
**STOPP – NICHT RATEN.**

## Campus-Karte

Projektgebäude:
- `PROJEKTE/PFERDE_ATELIER/`
- `PROJEKTE/HOBBYRAUSCH/`

Projektübergreifend:
- `ALLGEMEINGUELTIGE_BAUSTEINE/`

Zielverträge:
- `ZIELVERTRAEGE/`

WordPress-Pluginübersicht:
- `WORDPRESS_REGISTER.md`

Archiv:
- `ARCHIV/`

Baucontainer:
- `BAUCONTAINER/`

Hausmeister:
- `BAUCONTAINER/HAUSMEISTER.md`

## Zugriffsschutz

Der Campus-Prototyp liegt aktuell noch im öffentlichen Pferde-Atelier-Repository.

Empfehlung:
nach V1-Freigabe eigener privater Campus-Repository.

Bis dahin:
keine Secrets in den öffentlichen Campus-Prototyp.

## Katastrophenfall

Zuerst:
`protocol/PROJECT_MEMORY/TRESOR/START_HERE.md`

Dann aktuellen `STATUS.md` prüfen.

Nur einen ausdrücklich geprüften `TRESOR_PASS` als vollständige Wiederherstellungsquelle verwenden.

## Backup-/Tresor-Grenze

Für normale Fach- oder Technikarbeit ist `TRESOR/` bzw. `ARCHIV/` **niemals ein Arbeitsweg**.

Dorthin wird nur geroutet für Backup/Inventarisierung, historische Belegsuche oder ausdrücklich eingetretenen Katastrophen-/Restorefall.

Ein lokaler Mirror ist kein Ersatz für den aktuellen gebundenen Arbeitsweg.

## Pferde-Atelier – Technikbetrieb

Wenn der Nutzer WordPress-/Hosting-Betrieb, Speicherverbrauch, Backup-Reste, technische Wartung oder ein dafür gebautes Diagnose-/Cleanup-Werkzeug des Pferde-Ateliers bearbeiten will:

`PROJEKTE/PFERDE_ATELIER/TECHNIK/START_HERE.md`

Plugin-Artefakte bleiben zusätzlich im PLUGINS-Büro registriert. Das TECHNIK-Büro führt den Betriebs-/Diagnosestand; das PLUGINS-Büro führt Inventar und isolierte Installer.

## Produktvergleich – eindeutiges Routing

Wenn der Nutzer Produktvergleiche planen, Vergleichskriterien festlegen, konkrete Vergleiche definieren oder Faktendossiers/Quellen für Produktvergleiche vorbereiten will:

`PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/START_HERE.md`

Wenn der Auftrag dagegen die eigentliche Textproduktion oder den STARTMASTER-/Textmaschinenlauf betrifft:
`PROJEKTE/PFERDE_ATELIER/TEXT/START_HERE.md`

Nicht vermischen.

## PB ONE – Agenturzentrale

Wenn der Nutzer Agenturideen, Angebote, Flyer, Positionierung oder Vorhaben **vor** konkreter Projektumsetzung bearbeiten will:

`protocol/PROJECT_MEMORY/PB_ONE/START_HERE.md`

Nutzer und Paul haben innerhalb PB ONE dieselben redaktionellen Rechte.

Routing:
- dauerhafte Referenzakte → `PB_ONE/AKTENSCHRANK/START_HERE.md`
- Idee entwickeln → `PB_ONE/IDEENWERKSTATT/START_HERE.md`
- Konzept weiterentwickeln → `PB_ONE/ENTWICKLUNGSRAUM/START_HERE.md`
- laufende Präsentation/Unterlage → `PB_ONE/ARBEITSDOKUMENTE/START_HERE.md`
- Angebot/Flyer/Leistungsunterlage → `PB_ONE/ANGEBOTE_FLYER/START_HERE.md`

Harte Grenze:
PB ONE programmiert nicht.
Technische/fachliche Umsetzung wird bewusst an das zuständige Projekt-/Fachbüro übergeben.


## HARD RULE – EINE CURRENT-AUTORITÄT

Der Hauptpförtner erzeugt und pflegt keinen aktuellen Fachstand.
Die Zuständigkeit kommt ausschließlich aus `AUTORITAETSPLAN.json`.
Hobbyräume, Übergaben und Protokolle sind niemals Ersatz für die Current-Autorität.

CAMPUS_SINGLE_TRUTH_ENTRY_V1
