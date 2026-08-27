# Verbindliches Protokoll – Codex-Handoff-Option

Stand: 27.08.2026

## Regel
Wenn ein technischer Fehler nach mehreren lokalen Versuchen nicht sauber gelöst ist oder sich durch weitere Iterationen verschlimmert, darf nicht einfach weiter mit neuen Plugin-Versionen geraten werden.

Stattdessen ist ausdrücklich die Codex-Handoff-Option zu nutzen:

1. Aktuellen relevanten Quellcode und die betroffenen Dateien vollständig zusammenstellen.
2. Eine präzise Codex-Aufgabe formulieren: konkrete Fehlerbeschreibung, gewünschtes Sollverhalten, unveränderliche Bereiche, Negativtest, Positivtest und erwartete Ausgabe.
3. Dem Nutzer Quellcode/ZIP plus fertigen Codex-Prompt geben, damit er Codex extern ausführen kann.
4. Codex-Ergebnis anschließend lokal gegen den vollständigen Workflow prüfen, bevor ein neuer Installer gebaut oder empfohlen wird.

## Verbindliche Ausgabe-Disziplin für Codex
Codex darf dem Nutzer nach Abschluss nicht einen ganzen Arbeitsbaum oder dutzende Einzeldateien als Download anbieten. Die vielen Prüf-, Diff- und Quelldateien dürfen intern erzeugt werden, gehören aber nicht in die primäre Übergabe.

Pflichtausgabe an den Nutzer:
- genau **eine installierbare Plugin-ZIP** als Hauptdownload,
- optional genau **eine kompakte Textdatei** mit Prüfergebnis/SHA-256, nur wenn sie für die Übergabe wirklich benötigt wird.

Nicht als Einzel-Downloads ausgeben: Quellbaum, unveränderte Plugin-Dateien, Testfixtures, JSON-Messdaten, Lint-Protokolle, Diffs, Screenshots, Evidence-Dateien oder sonstige interne Arbeitsartefakte. Falls diese aus Dokumentationsgründen benötigt werden, bleiben sie im Codex-Arbeitsbereich bzw. Git-Commit und werden nur auf ausdrückliche Anforderung separat bereitgestellt.

Der Abschluss muss den einzigen benötigten Installer eindeutig benennen, z. B. `affiliate-zentrale_vX.Y.Z_....zip`, und ausdrücklich sagen: **Nur diese ZIP herunterladen.**

## Wichtiger Hinweis
Die Codex-Handoff-Option gilt auch dann, wenn in diesem Chat kein direkt ausführbarer Codex-Agent verfügbar ist. In diesem Fall wird Codex über den Nutzer als externer Prüfer/Entwickler eingebunden.

## Eskalationsregel
Nach wiederholten Fehlversuchen soll diese Option frühzeitig angeboten bzw. genutzt werden, statt weitere unbewiesene Plugin-Versionen zu erzeugen.
