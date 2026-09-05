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
NACHHER: neuer organisatorischer Wegweiser unter `PROJECT_MEMORY/`.
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

## TECH-KEYFLOW-001 – Schlüsselübergabe

Bereich: TEXT / Maschinenraum
WAS: historisch wurde die Schlüssel-/Signer-Übergabe verändert.
WARUM: UNGEKLÄRT – vor technischem Rückbau anhand Commit/PR/Protokoll belegen.
ENTFERNBAR: NEIN, BIS WARUM GEKLÄRT.
