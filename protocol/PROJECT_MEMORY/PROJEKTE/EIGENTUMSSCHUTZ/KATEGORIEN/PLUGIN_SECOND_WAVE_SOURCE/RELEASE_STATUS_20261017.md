# Hab & Bewahr – C2.2 zweite Kategorie-Ergänzungswelle – Plugin 1.14.8.31

**Stand 17.10.2026: DER CODE IST ERSTELLT, LOKAL GETESTET UND IN GITHUB GESICHERT; NICHT LIVE INSTALLIERT.**

## Exakt nachgewiesene Basis
- Original `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.30_NACHGEPRUEFT.zip`, unverändertes bestehendes Kategorieplugin; ursprünglicher C2.2-Import laut bestätigtem Status schon abgeschlossen: 5 neue Bereiche, 172 Themenseiten, 566 flache Artikelkategorien = 743 Objekte.
- 172 Themen- und 566 Kategoriennamen/Owner-Pfade im GitHub-Fachstand exakt gleich wie in `profiles/hab-und-bewahr-c22-plan.json` des Originalplugins.
- Nach ausdrücklicher Nutzerbestätigung **keine Benutzeränderung in WordPress** seit Import. Es ist **kein erneuter WordPress-Export** erforderlich.
- 93 alte Themenseiten, 285 historische Kategorie-Terms und vier bekannte alte Artikel-/Kategoriebindungen bleiben geschützt. Keine Beiträge werden produziert oder geprüft.

## Tatsächlich implementierte Plugin-Arbeit
- Update **derselben Plugin-Architektur**, Versionswechsel 1.14.8.30 → **1.14.8.31**.
- Getrennter `APKW_C22_472_AddOnly`-Durchlauf mit 472 neuen WordPress-`category`-Terms unter den bestehenden 172 C2.2-Seite3-Eltern, darunter 172 FAQ, 172 Vergleich, 102 optionale Vertiefungen und 26 weitere Bereiche mit fachlichem Mehrwert.
- Identitäts- und Elternkennungen exakt nach dem bisherigen PHP SHA-256-Verfahren, flache WP-Kategorien (`parent=0`), keine neue Page-Ebene. Die ursprünglichen 743 Jobs werden **nicht** neu ausgeführt oder mutiert.
- Echte Kategorieanlage durch bereits vorhandenen `APKW_TargetWriter`, gespeicherter Basissnapshot, eigene Optionen/Status, 20 Kategorieanlagen je Durchlauf, physische Metadaten/URL-/Owner-Readback-Kontrolle, bei Fehlern nur die eigenen ungenutzten neuen Terms rückrollen; Unterbrechung zwischen Snapshot- und Revisionsoption wird erkannt.
- Adminfläche im vorhandenen Menü `Portal-Kategorien → C2.2 Kategorien`, mit vorheriger additiver Vorprüfung und **separater, ausdrücklicher Checkbox-Freigabe**. Kein Plugin-Zweitwriter.

## GitHub-Artefakte
- Getesteter neuer Modulcode: `includes/class-apkw-c22-472-add-only.php`.
- Laufzeit-Manifest: `profiles/hab-und-bewahr-c22-472-add-only.json`.
- Exakte Änderungen am vollständigen Original-1.14.8.30-Plugin: `apply_to_original_1_14_8_30.py`.
- Echte Tests mit WordPress-Mocks: `tests/test_472_mocks.php`.
- Exaktes vollständig installierbares ZIP **als Base64-Text**: `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.31.zip.b64`.
- Dessen geprüfte Wiederherstellung: `decode_release.py`. Ein normales ZIP entsteht mittels `python3 decode_release.py`, geprüft auf originale SHA-256.

**ZIP:** 265.246 Bytes, 38 Dateien, CRC gültig. SHA-256 `6cd47955df14a65d681c7508e1674be94e98cad4dd68df5a6605ce8ef534d933`.

**Modul-PHP:** 22.434 Bytes, SHA-256 `d29f130a6e2015de90dd5b204d414c1780413eb007d8b46c0a29417d2d5a7654`.

## Reale lokale Positiv- und Negativprüfung
- PHP-Syntax: **alle 32 PHP-Dateien** fehlerfrei.
- Struktur: 472 eindeutige Kategorie-IDs, 172 vorhandene Themen-Parent-IDs, keine Kollisionen der 738 ursprünglichen C2.2-Themen-/Kategorie-IDs.
- **Positiv:** 472/472 mit Original-`TargetWriter`-Aufruflogik in WordPress-Mocks erstellt, termbezogene Metadaten und Snapshot um 472 ergänzt, die vorherigen 738 C2.2-Themen-/Kategorienknoten und 285 historische Begriffe unverändert.
- **Negativ:** bewusst erzwungener Schreibfehler nach 30 neuen Kategorien → alle 30 neu angelegten Terms sicher gelöscht, ursprünglicher Snapshot unverändert, keine Altterm-Löschung.
- **Negativ:** fehlende physische Elternbindung blockiert vor der ersten Schreiboperation.
- Vorherige Fach-/Struktursimulation: 12/12 absichtlich beschädigte Bestands-/Deltafälle korrekt abgewiesen.

**Einschränkung:** Lokale PHP-/WordPress-Mocktests sind **kein echter Live-WordPress-Funktionstest**, und das Update wurde noch **nicht installiert**.

## GENAU EINE NEXT ACTION
Den bereits lokal geprüften **vollständigen Plugin-Build 1.14.8.31** mit dem vorhandenen normalen WordPress-Plugin-Updateweg installieren (kein erneuter C2.2-Import), dort das eingebaute 472er-Preflight prüfen und die zweite Schreibwelle **nur nach separater Freigabe** auslösen. Danach die eingebaute positive/negative WordPress-Verifikation kontrollieren. Keine Bibliothek, keine Artikelgenerierung, kein neuer Benutzerexport.
