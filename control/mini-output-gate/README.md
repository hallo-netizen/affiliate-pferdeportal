# MINI – genau eine Ausgabesperre mit Reparaturschleife

## Ziel

Kein verfrüht ausgegebener Einzel-Checkpoint. **Ein Original-MINI-Export → sämtliche fehlenden Entscheidungen einmalig bearbeiten → eine einzige technische Abschlussprüfung → alle erforderlichen WordPress-Importdateien freigeben.**

Bei Fehlern bleibt der Originalauftrag erhalten; der Gate-Status wird **REPARATUR**. Der Gate-Ausgang `REPARATUR.json` benennt die betroffene Stufe und das konkrete Thema. **Nur diese Felder werden durch den jeweiligen bereits zuständigen Worker repariert**, dann läuft **derselbe** `mini_release_gate.py` erneut. Kein Reset, keine Neurecherche, keine doppelte Entscheidung, keine zweite Fachprüfung.

## Anwendung für den MINI-Chat

1. `python mini_release_gate.py --original /pfad/texterstellung-mini-gesamtauftrag.json --workspace /pfad/mini-arbeitsraum` (kopiert und bindet das Original unveränderlich; zunächst Reparaturstatus, weil Ergebnisse fehlen).
2. Bestehende MINI-Worker erzeugen **nur die für diesen Auftrag offenen** Stufendateien `CATEGORY.json`, `EDITORIAL.json`, `TITLE.json` im Arbeitsraum – anhand derselben Originaldatei und der jeweiligen Worker-Vorlage. Abgeschlossene Entscheidungen bleiben unangetastet.
3. `python mini_release_gate.py --workspace /pfad/mini-arbeitsraum`.
4. Falls **REPARATUR**: `REPARATUR.json` lesen, nur den dort genannten vorhandenen Worker mit der Korrektur der genannten Themen beauftragen und **Schritt 3 erneut ausführen**. Keine Dateien an den Nutzer ausgeben, solange `FREIGABE/NACHWEIS.json` fehlt.
5. Erst bei **FREIGEGEBEN_FUER_WP_IMPORTE** ausschließlich die nummerierten Dateien aus `FREIGABE/` in einem Chat weitergeben. WordPress importiert sie anschließend **in der vom Plugin unverändert vorgegebenen Reihenfolge**.

## Kein Architekturumbau und keine Doppelprüfung

- `mini_release_gate.py` entscheidet nicht, ob Keyword, Kategorie oder Titel fachlich richtig sind. Das bleibt allein bei den vorhandenen Workern beziehungsweise WordPress. Das Gate prüft **einmal an der Ausgabestelle** nur die Vollständigkeit, Hashbindung, Ursprungsdaten-Unverändertheit und die nötigen Entscheidungen.
- Keine neue WordPress-Plugin-Version, kein K0-Umbau, keine zusätzliche WordPress-Prüfstufe, keine geänderten MINI-Entscheidungen.
- Beim Prüffehler wird die alte Freigabe entfernt, die Arbeitsdateien und der genaue Korrekturauftrag bleiben bestehen.
- **Grenze:** Diese Sperre ist technisch wirksam, wenn MINI-Dateien ausschließlich über den Gate-Freigabeordner verteilt werden. Sie ist keine systemweite Sperre für beliebige, manuell verlinkte Dateien in ChatGPT. Eine solche plattformweite Verhinderung kann ein Repository-Skript allein nicht erzwingen.
- WordPress-Import wurde nicht auf der Live-Website ausgeführt; die Freigabe bestätigt ausschließlich die vorab lokal getestete technische Lieferfähigkeit.

## Test

`python -m unittest -v test_mini_gate.py`

Die Tests laufen mit einer auf die erforderlichen Felder gekürzten 10-Themen-Testkopie und einer aus der echten Kategorie-Rückgabedatei abgeleiteten Testdatei. Wahlweise können die beiden vollständigen echten Dateien per `MINI_TEST_ORIGINAL` und `MINI_TEST_CATEGORY` angegeben werden. Die zur Prüfung künstlich erzeugten Redaktions- und Titelentscheidungen sind **reine Testdaten** und werden niemals als produktive MINI-Rückgaben freigegeben.