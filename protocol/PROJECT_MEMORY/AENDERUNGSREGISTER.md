# ÄNDERUNGS- UND ERKLÄRUNGSREGISTER

STAND: 2026-09-05

Zweck: dauerhaft beantworten können:
**Was wurde geändert – und warum?**

Jeder relevante Eintrag enthält:
- WAS
- VORHER
- NACHHER
- WARUM
- BELEG
- ENTFERNBAR?

Wenn WARUM nicht belastbar geklärt ist:
`WARUM: UNGEKLÄRT`
`ENTFERNBAR: NEIN, BIS GEKLÄRT`

## ARCH-001 – Campus/Bürogebäude-Modell

WAS: Zentrales Projektgedächtnis als Campus → Projektgebäude → Büro → Hobbyraum.
VORHER: Wissen lag verteilt in Chatverläufen, Protokollen, technischen States und Dateien.
NACHHER: organisatorischer Wegweiser unter `protocol/PROJECT_MEMORY/`.
WARUM: neue/wechselnde Chats sollen ohne Vorwissen zuverlässig aktuellen Stand, Regeln, Fehler und vorhandene Arbeitswege finden.
BELEG: Architekturentscheidung 2026-09-05.
ENTFERNBAR: nur durch dokumentierte Nachfolgearchitektur.

## ARCH-002 – Hauptpförtner als Resetpunkt

WAS: ein universeller Befehl „Hauptpförtner.“
WARUM: Chat soll bei Kontextverlust nicht raten, sondern verbindliche Projektinformationen neu laden.
NACHWEISREGEL: Chat muss Projekt/Büro/Stand/Nächster Schritt/Arbeitsweg zurückmelden.
ENTFERNBAR: nur wenn gleichwertiger oder besserer Resetmechanismus existiert.

## ARCH-003 – Ein Hobbyraum pro Büro

WARUM: Seitensprünge, Parallelreparaturen und Nebenarchitektur verhindern.
REGEL: Nebenfund dokumentieren, nicht spontan reparieren.

## ARCH-004 – Paul isoliert über eigenen Branch

WARUM: Paul soll vollständiges Projektwissen lesen und frei testen können, ohne offizielle Arbeitsstände zu verändern.
REGEL: Kein Blind-Merge seines ganzen Branches. Zuständiges Fachbüro prüft und übernimmt gezielt.

## ARCH-005 – Modulares Gebäude

WARUM: neue Räume, Büros, Abteilungen und vollständige Projekte müssen ohne Umbau bestehender Bereiche ergänzt werden können.
REGEL:
- neues Thema → vorhandenes Büro;
- neue dauerhafte Funktion → neues Büro;
- größerer Teilbereich → neue Abteilung;
- eigenständiges Projekt → neues Projektgebäude.

## ARCH-006 – Technischer Standort unter protocol/

WAS: PROJECT_MEMORY liegt technisch unter `protocol/PROJECT_MEMORY/`.
VORHER: erster Entwurf lag direkt unter `PROJECT_MEMORY/`.
NACHHER: unverändertes Campusmodell, aber technischer Ablageort unter bereits bestehender `protocol/**`-CI-Abdeckung.
WARUM: der vorhandene Required Check `hardlock` wird bei Pull Requests für `protocol/**` bereits automatisch ausgelöst. So braucht die neue Gebäudeordnung keine Änderung an geschützten Workflows/Gates und keinen künstlichen Parallelmechanismus.
BELEG: Draft-PR #134.
ENTFERNBAR: nur wenn ein anderer bestehender, gleichwertig geschützter Speicherort beide Required Checks ohne Maschinenraum-Umbau auslöst.

## ARCH-007 – Externer Notfall-Tresor

WAS: versionierte vollständige Wiederherstellungskapsel des gesamten Campus.
VORHER: normales Repository/Git-Historie ohne einen einzigen geprüften Gesamt-Wiederaufbaupunkt.
NACHHER: jeder künftige lokale Backup-Lauf soll zuerst einen frischen Tresorstand erzeugen und vollständig prüfen.
WARUM: bei Feuer, Fehlumbau, verlorener Struktur oder Totalausfall soll das gesamte Projekt ohne Vorwissen aus einem einzigen gesicherten Stand wiederhergestellt werden können.
REGEL: kein Überschreiben alter PASS-Stände; keine stillen Lücken; UNGEKLÄRT blockiert TRESOR_PASS.
BELEG: `protocol/PROJECT_MEMORY/TRESOR/`
ENTFERNBAR: nur durch nachweislich gleichwertiges oder besseres Disaster-Recovery-System.

## TECH-KEYFLOW-001 – Schlüsselübergabe

Bereich: TEXT / Maschinenraum
WAS: historisch wurde die Schlüssel-/Signer-Übergabe verändert.
WARUM: UNGEKLÄRT – vor technischem Rückbau anhand Commit/PR/Protokoll belegen.
ENTFERNBAR: NEIN, BIS WARUM GEKLÄRT.
