# MINI – verbindliche Ausgabesperre vor dem Chat

## Vertrag (KISS, kein neues Plugin)

**Ein MINI-Gesamtexport → CATEGORY → EDITORIAL → TITLE → bestehende Abschlussprüfung → genau eine JSON-Datei für den Chat.**

Das WordPress-MINI-Importieren einer CATEGORY-Zwischendatei kann technisch erfolgreich sein; das bedeutet ausdrücklich **nicht**, dass der gesamte MINI-Auftrag abgeschlossen ist. Der Chat darf eine solche Datei nicht als Gesamtrückgabe ausgeben.

## Existierender Freigabeweg (unverändert)

- `mini_release_gate.py` kontrolliert die Vollständigkeit, Identität und gesperrte Entscheidungen. Fehler werden als `REPARATUR.json` an den betroffenen ursprünglichen Worker gegeben.
- `mini_single_release.py` erzeugt bei PASS das finale `FREIGABE/MINI_EINMAL_REIMPORT.json` mit gesondertem `NACHWEIS.json`.
- Die private GitHub-Aktion nutzt denselben Code, prüft ihn vor der Ausgabe und lädt **nur** die freigegebene Datei des aktuell bearbeiteten Batches hoch. Keine Änderungen an K0 oder am WordPress-Plugin.

## Zusätzliche Sperre genau am Ausgabepunkt

Statt eine selbst erzeugte CATEGORY-/EDITORIAL-/TITLE-JSON direkt in den Chat zu verlinken, muss zur Ausgabedatei der **bestehende** Freigabebefehl verwendet werden:

```bash
python mini_single_release.py --workspace /pfad/zum/mini-batch \
    --deliver /mnt/data/MINI_EINMAL_REIMPORT.json
```

Bei einer bereits vorhandenen Kandidatendatei zusätzlich:

```bash
python mini_single_release.py --workspace /pfad/zum/mini-batch \
    --candidate /pfad/zur/vorliegenden-datei.json \
    --deliver /mnt/data/MINI_EINMAL_REIMPORT.json
```

Die freizugebende Kandidatendatei muss **byteidentisch** zur vom Originalgate erzeugten Gesamtrückgabe sein. Eine CATEGORY-Zwischendatei wird selbst dann abgewiesen, wenn ihr WordPress-MINI-Import technisch erfolgreich war.

**Vollständiger Auftrag fehlt:** Status `GESPERRT`, Ausgabedatei wird nicht erstellt (eine frühere gleichnamige Ausgabedatei wird entfernt), `REPARATUR.json` enthält die noch offene Station. **Vollständiger Auftrag:** Status `FREIGEGEBEN` mit Dateipfad und Prüfsumme, genau eine Chatdatei.

Niemals vor dem PASS dieser Ausgabeprüfung eine MINI-JSON als fertigen Importlink anbieten; kein paralleler direkter Dateierzeugungsweg und keine Zwischenfreigabe.

## Tests / echter Fehlerfall

`python -m unittest -v test_mini_gate.py test_mini_single_release.py`

Negative Tests: nur Kategorie, Kategorie plus Redaktion ohne Titel, manipulierte Ausgangsdaten, vorgetäuschte Freigabe, abweichende Kandidatendatei und bereits vorhandene veraltete Ausgabedatei. Positive Tests: vollständiger Auftrag erzeugt genau eine Datei; Datei ist byteidentisch zur geprüften Freigabe.

Am 21.11.2026 wurde zusätzlich der **tatsächlich fehlgeschlagene 20-Themen-Vorgang** mit Original-MINI-Export und der im Chat ausgegebenen `MINI_KATEGORIE_RUECKGABE_2026-11-21.json` erneut durch den Ausgabebefehl geführt: Ergebnis `GESPERRT`, nächster Worker `EDITORIAL`, **keine Chatdatei erzeugt**.

## Grenze, die nicht als Garantie ausgegeben werden darf

Der Code sperrt die Ausgaben **über diesen verbindlichen Freigabeweg**. Ein Repository-Skript kann aber technisch weder ChatGPT selbst noch das manuelle Verlinken einer anderen Datei plattformweit unterbinden. Deshalb ist eine absolute Aussage wie „ChatGPT kann niemals eine falsche Datei verlinken“ **nicht nachgewiesen**. Als MINI-Enddatei gilt ausschließlich die nachweislich aus diesem Gate ausgegebene Datei.
