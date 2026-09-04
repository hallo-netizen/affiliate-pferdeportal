# HOBBYRAUM UNIVERSAL V1

Zweck: Ein einzelner, isolierter Arbeitsraum für klar begrenzte Aufgaben.

## Was technisch erzwungen wird
- Der Container sieht nur die Dateien, die im Task unter `inputs` ausdrücklich freigegeben wurden.
- Netzwerk ist zur Laufzeit vollständig deaktiviert: `--network none`.
- Der Container bekommt keine Host-Secrets und keinen Repository-Mount.
- Das Root-Dateisystem des Containers ist read-only.
- Änderungen außerhalb der unter `writable` erlaubten Pfade führen zu BLOCKED.
- Das Originalprojekt wird nie direkt verändert. Gearbeitet wird ausschließlich auf einer Kopie.
- Ergebnis ist ein Patch plus die erlaubten geänderten Dateien.
- Fehlschlägt Aufgabe oder Test, lautet das Ergebnis BLOCKED.

## Verwendung in jedem Projekt / jedem Chat
1. Benötigte Dateien gezielt in einen lokalen Aufgabenordner legen oder als genaue `inputs` referenzieren.
2. `TASK.example.json` kopieren und Ziel, Inputs, Schreibziele, Befehl und Tests eintragen.
3. Ausführen:
   `python3 HOBBYRAUM/hobbyraum.py TASK.json`
4. Nur `.runs/<task_id>/PATCH.diff` bzw. `.runs/<task_id>/out/` zurück ins eigentliche Projekt übernehmen.

## Wichtig
Der verwendete Docker-/Podman-Image muss bereits lokal vorhanden sein, weil der Lauf absichtlich keinen Netzwerkzugriff hat.
Das Image wird mit `--pull=never` gestartet.

Der Hobbyraum ist projektunabhängig. Der Task bestimmt, welche Dateien hineindürfen.
