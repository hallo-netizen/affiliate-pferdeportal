# PSTE – VORHANDENES POTENZIAL / AUTOMATISCHE EDITORIALISIERUNG – BEFUND 2026-10-01

ROLLE: Fehler-/Arbeitsprotokoll und Nachweis. **Keine CURRENT-Autorität.**
Aktueller Status/NEXT ACTION ausschließlich:
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md`.

## Frisch geprüfter Kernbefund

Die automatische Umwandlung vorhandener Suchbegriffe/Themen in redaktionell nutzbare Metadaten ist **nicht neu zu bauen**. Sie existiert bereits im PSTE-Bestand.

Der bestehende Normalweg `PSTE_Normal_Metadata_Path` ist ausdrücklich für:
- normale Recherche;
- gespeicherte Themen-Rebuilds;
- Sandbox-Normal-Reentry.

Er führt – fail-closed – durch:
1. Portalrelevanz;
2. Familien-/Gruppenzuordnung;
3. Themen-Normalisierung;
4. Intentanalyse;
5. Artikeltyp-Auflösung;
6. Titelpipeline;
7. Zielkeyword;
8. Zielkategorie;
9. nachgelagerte Planning-Readiness / Dubletten-/Kannibalisierungsprüfung.

Bei PASS werden u. a. `editorial_title` / `production_title`, `target_keyword`,
`suggested_article_type` / `proposed_article_type` sowie Ziel-/Vorschlagskategorie gebunden.
Der PASS-Grund enthält `ARTICLE_TYPE_AUTOMATICALLY_RESOLVED`.

## Historischer Beleg – gute Titel waren bereits implementiert

Spätestens PSTE 0.56.25 besaß den expliziten Rootfix für natürliche, grammatisch bessere Titel.
Dabei blieb das exakte Zielkeyword die SEO-Autorität; reine Präsentationswörter durften nur die Lesbarkeit verbessern.
Der gleiche Stand band Retained/Current Backlog vor Provider-Aufrufen an dieselbe Planning-Readiness.

Quelle:
`protocol/STARTMASTER0100_ATTRIBUTE_RICH_COMPILER_READY_BREADTH_ROOTFIX_20260828.md`.

## Frisch geprüfter Retained-Backlog-Weg

`PSTE_Repository::reanalyzeRetainedBacklogBatch()` liest gespeicherte `topic_pool`-Zeilen
(`manual_status=''`) und führt sie erneut durch den bestehenden Normal-Metadata-Pfad.

Dabei gilt bereits:
- kein Provider-Aufruf;
- Rohbegriff bleibt unverändert;
- Normal-Metadata-Pfad darf Familie, Artikeltyp, Titel, Zielkeyword und Kategorie neu auflösen;
- danach Planning-Readiness;
- nur `AUTO_RESOLVED` + gültige Planung darf weiterkommen;
- bestehende Dubletten/Abdeckung werden weiterhin fail-closed demotiert.

## Aktuelles Verwertungsproblem

Das aktuelle Problem ist daher **nicht**:
„Es gibt keinen automatischen Übersetzer von Keywords/Gruppen zu guten Titeln und Kategorien.“

Das aktuelle Problem ist:
**Von dem großen gespeicherten Bestand schaffen es zu wenige Kandidaten durch den bereits vorhandenen automatischen Aufbereitungsweg bis zur realen Planung/READY-Stufe.**

Der letzte reale Ablauf nach abgeschlossenem Portalabgleich zeigte:
- 23 geeignete/geprüfte Themen im PSERC-Lauf;
- davon nur 2 READY;
- diese 2 wurden anschließend vollständig über K9 produziert.

Der Nutzer meldet am 01.10.2026 zusätzlich, dass die aktuell laufende neue Recherchewelle nur geringe Ausbeute liefert.

Ohne terminalen Readback dieser laufenden Welle ist **noch nicht belegt**, an welcher vorhandenen Stufe das meiste Potenzial verloren geht.
Nicht raten.

Zu unterscheiden sind mindestens:
- Rohbegriff/Quelle vorhanden, aber Portalrelevanz nicht bewiesen;
- Familien-/Gruppenzuordnung nicht eindeutig;
- Intent/Artikeltyp nicht eindeutig;
- Titelpipeline nicht PASS;
- Zielkategorie fehlt / STRUCTURE_GAP;
- Planning-Readiness scheitert an Dublette/Kannibalisierung/Abdeckung;
- Kontext nicht CURRENT;
- Sandbox-Fall benötigt Normal-Reentry;
- echte nicht-redaktionelle/alte/irrelevante Begriffe.

## 0.57.18-Kandidat – nur Teilfix, nicht Gesamtlösung

Lokal wurde aus dem geprüften 0.57.17-Paket der Kandidat
`PSTE 0.57.18 – EXISTING POTENTIAL FIRST`
gebaut.

Sein einzig relevanter fachlicher Zusatz:
**bereits sichere `AUTO_REENTRY_ELIGIBLE`-Sandbox-Kandidaten werden vor Retained-Backlog und vor Provider-Recherche über den bestehenden Normal-Reentry geleert.**

Dieser Kandidat ändert **nicht** Titelcomposer, Familienauflösung, Artikeltyp-Auflösung,
Normal-Metadata-Pfad, Dubletten-/Kannibalisierungsregeln oder Qualitätsgates.

Lokale Evidence:
- PHP-Lint 79/79 PASS;
- sicherer Sandbox-Reentry ohne Provider PASS;
- gemischter Positiv-/Negativ-Reentry PASS;
- Provider-Aufruf in Reuse-Phase wird BLOCK;
- keine eligible Sandbox erfindet keinen Kandidaten;
- Fresh-Unpack Wiederholung PASS.

**Wichtig:** 0.57.18 ist ein Teilfix für die Reihenfolge der Verwertung. Er beweist noch nicht,
warum der große gespeicherte Topic-Pool aktuell nur geringe READY-Ausbeute liefert.

## Exakte nächste Diagnose – KISS

Nach Ende der bereits laufenden Recherchewelle:
**keine weitere Provider-Recherche starten.**

Stattdessen den vorhandenen Bestand read-only als Verwertungs-Funnel auswerten:

`GESPEICHERT`
→ `SOURCE QUERY VERWERTBAR`
→ `PORTALRELEVANZ PASS`
→ `FAMILIE/GRUPPE PASS`
→ `ARTIKELTYP PASS`
→ `TITEL + ZIELKEYWORD PASS`
→ `KATEGORIE PASS`
→ `PLANNING-READINESS PASS`
→ `KONTEXT CURRENT`
→ `READY`.

Für jede Verluststufe:
- Anzahl;
- führende Reason-Codes;
- Anteil A / B / C / D gemäß `ZV-PSTE-THEMENVERWERTUNG-001`.

Ziel ist besonders **Lane B**:
vorhandene Evidenz reicht, und nur bestehende automatische Zuordnung/Titel/Reentry muss erneut sauber greifen.

Keine neue Architektur, kein neues Themenlager, kein pauschales Freigeben.
