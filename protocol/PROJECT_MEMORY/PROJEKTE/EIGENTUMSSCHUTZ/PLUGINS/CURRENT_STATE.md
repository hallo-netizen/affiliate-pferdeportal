## 06.11.2026 – HAB-004-AFFILIATE – neues viertes vollständiges Eigenplugin
<!-- HAB004_20261106_RELEASENOTE -->
Im **bestehenden** Hab-&-Bewahr-Pluginbüro ist die ganze installierbare `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` (0.1.0-rc2, 603.323 Bytes, 27 Dateien, SHA-256 `014e42b9657eed74b4d2e1f29ea51c6c6bf5c276ec30402011289b3821cbe153`, Git-Blob `077a35ccb3d2f9fc75c646629f183a28acbf342c`) hinzugekommen. Nachweis: GitHub-Run 42246580133 einschließlich vollem unabhängigen GitHub-Wiederabruf, CRC, PHP/JS-Syntax, 26 originalen Source-Files, unveränderten ursprünglichen Funktionen, fünf zuvor fehlenden Modul-Starts sowie Positiv/Negativprüfungen der Hab-Kategoriebindung. Installationskandidat, **WordPress-Liveprüfung und Prüfung gegen das vollständige Pferdeatelier 6.72.306 Archiv sind NICHT abgeschlossen**. Automatik bleibt in Standardeinstellungen AUS. Nur die eigene Projekt-Binärdatei; kein fremdes Portal, keine Provider-Zugänge importiert.

**Neuer Bestand: 4/4 echte vollständige Eigenplugin-ZIPs**. Die vorhandenen Design 0.1.189, Kategorie-Workflow 1.14.8.37 und Bildzentrale 1.0.0 wurden nicht geändert. Dies ist die einzige aktuelle Pluginbüro-Statusautorität, technische Einzelheiten in `PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md`. **NEXT ACTION:** Kandidat in einer gesicherten Hab-&-Bewahr-WordPress-Installation aktivieren und zunächst ohne Provideraktivierung die Adminseiten, den aktiven zentralen Katalog, die Hub-/Artikel-/Glossar-/HivePress-Brücken, die Performance und die unveränderte Ausgangslage der bestehenden Plugins prüfen.

---

# HAB & BEWAHR – PLUGINS / AKTUELLER CAMPUS-RELEASE-STAND
<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->
## Stand 06.11.2026 – DIE DREI EIGENPLUGINS / VERSION 0.1.189

**Versionsautorität:** die drei bestehenden `PLUGIN_AKTEN/<ID>/CURRENT.md`. Physische echte Voll-ZIPs in `ISOLIERTE_PLUGINS/<ID>/CURRENT.zip`; keine zweite Autorität und keine Bibliothek.

1. `HAB-001-DESIGN` **0.1.189**: 84.349.647 Bytes, 430 ZIP-Einträge, SHA-256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`, Git-Blob `504fccb82f4e9a3b10bb6405b468e1dbd03c62e1`. Voll-ZIP im bestehenden Pfad. GitHub-Run **42223947280**: neuer unabhängiger Abruf direkt vom GitHub-Releasezweig `hbd-design-0189-release-20261106`, ZIP vollständig neu geöffnet, CRC/Hash/Version PASS. Das ist ein GitHub-Artefakt-/Quelltest, **keine WP-Live-Freigabe**. Vorherige 0.1.184 als Rollback unverändert in Git-Historie, PR #625.
2. `HAB-002-KATEGORIE-WORKFLOW` **1.14.8.37**: 368.530 Bytes, SHA-256 `ec39080e5350b9f7b3924239376e11580ce7de195a60bb89feafae6152533f98`, Blob `35651f44ac70ed51e663d5dfaf45094bc9f1e3b2`, bestehende Voll-ZIP unverändert.
3. `HAB-003-BILDZENTRALE` **1.0.0**: 70.397 Bytes, SHA-256 `58af0d394752e767b5f0c7d6d9901eeaec921331ab6245144859e3e6626e4559`, Blob `8b8b3b84b494eb2784181d5bfd6acfb2efceafde`, bestehende Voll-ZIP unverändert.

**Status für die drei echten Projekt-Plugins:** ZIP-Archiv/Paket lokal geprüft; separate WordPress-Liveinstallation unbestätigt. **NEXT ACTION:** Design-0.1.189 im bestehenden WordPress-Plugin installieren und je einen normalen Beitrag mobil/desktop und eine Schutzbereichsseite auf tatsächliche Darstellung prüfen. Niemals ein neues Plugin hinzufügen oder K0/andere Portale anfassen.

**Wichtig vor Merge:** Dieser Nachtrag ist auf dem geprüften Releasezweig vorbereitet; er wird erst nach erfolgreicher geschützter Übernahme in den Campus-Hauptzweig zur offiziellen Current-Wahrheit. Kein PR ersetzt den Merge.

---

## Verbindlicher Ablageablauf für jedes künftige Plugin-Update (06.11.2026)

**Dieser vorhandene Weg hat mit PR #634 tatsächlich funktioniert; kein neues Plugin, kein zusätzliches Büro und keine Bibliothek.**

1. **Nur das betroffene Plugin aktualisieren:** von seiner originalen `CURRENT.zip` ausgehen; identischen Pluginordner behalten; ganze neue ZIP auf ZIP-CRC, PHP/JS-Syntax, Version, Hash, Dateibestand und unveränderte Fremddateien prüfen.
2. **Voll-ZIP am vorhandenen Ort aktualisieren:** in einem regulären Freigabezweig vom offiziellen Campus genau `ISOLIERTE_PLUGINS/<ID>/CURRENT.zip` als echte Binärdatei ablegen, technische `PLUGIN_AKTEN/<ID>/CURRENT.md` und Manifest mit Nachweisen aktualisieren. Die anderen zwei Original-ZIPs nicht anfassen.
3. **Normalen GitHub-PR statt Sonderwege:** `single-current-lock` bestehen lassen, geschützten PR in den offiziellen Campus mergen. Nicht auf reine Chat-Datei, kurzlebiges Actions-Artefakt oder offene PR als Ablageersatz ausweichen.
4. **Frischer unabhängiger Wiederabruf:** nach dem Merge alle drei aktuellen `CURRENT.zip` aus dem offiziellen Campus separat abrufen und Größe, SHA-256, ZIP-CRC, Pluginversion prüfen; `PLUGINS/CURRENT_STATE.md` als einzige aktuelle Büro-Autorität pflegen. Ohne Readback kein PASS.
5. **Rollback:** Vorgänger-ZIP bleibt über den vorherigen freigegebenen Git-Commit/PR zugänglich; ein Live-PASS wird nie aus lokalen Tests abgeleitet.

**Nachgewiesene Referenz:** PR #634 enthält echte vollständige Design-ZIP 0.1.189 im bestehenden Büro; GitHub-Actions-Run **42224724306**: unabhängiger frischer Download **aus dem offiziellen Campus** und dreimal `OFFICIAL_CAMPUS_ZIP_READBACK_PASS`:
Design 0.1.189 (84.349.647 B/430 Einträge), Kategorie-Workflow 1.14.8.37 (368.530 B/49), Bildzentrale 1.0.0 (70.397 B/3). Alle drei SHA-256 und CRC stimmen mit ihren technischen Akten überein.

**Verbleibender fachlicher Schritt:** Der neue Plugin-Code ist noch nicht unabhängig auf der tatsächlichen WordPress-Webseite live geprüft; das ist keine Ablagesperre, sondern gesonderte Abnahme.

---

## Historische Ablageakte vom 03.11.2026 (durch obere Fassung für Designversion abgelöst)


## Stand 03.11.2026 – ABLAGE ABGESCHLOSSEN: 3/3 ORIGINAL-ZIPS IM OFFIZIELLEN PLUGINBÜRO

**Geltungsbereich:** ausschließlich die drei belegten eigenen Hab-&-Bewahr-WordPress-Plugins. Keine Fremdplugins und keine Dateien anderer Portale.

**Offizieller Campus-Branch:** `hobbyroom/project-memory-campus-v1-20260905`.
**Speicherort:** `protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/<ID>/CURRENT.zip`.

- **HAB-001-DESIGN:** Version **0.1.184**. Originale vollständige `CURRENT.zip`, **84.339.643 Bytes**, Git-Blob `e153339c967cabcc4953ed6fb0882d9792b622fe`, SHA-256 `76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3`. 426 ZIP-Einträge und CRC PASS. GitHub-Actions-Run **41687120534** erfolgreich; **PR #625** am 03.11.2026 gemergt. Das offizielle GitHub-Verzeichnis bestätigt Größe und Blob-SHA.
- **HAB-002-KATEGORIE-WORKFLOW:** Version **1.14.8.37**. Originale vollständige `CURRENT.zip`, **368.530 Bytes**, Git-Blob `35651f44ac70ed51e663d5dfaf45094bc9f1e3b2`, SHA-256 `ec39080e5350b9f7b3924239376e11580ce7de195a60bb89feafae6152533f98`. 49 ZIP-Einträge und CRC PASS; **PR #622** gemergt. GitHub-Größe und Blob-SHA bestätigt.
- **HAB-003-BILDZENTRALE:** Version **1.0.0**. Originale vollständige `CURRENT.zip`, **70.397 Bytes**, Git-Blob `8b8b3b84b494eb2784181d5bfd6acfb2efceafde`, SHA-256 `58af0d394752e767b5f0c7d6d9901eeaec921331ab6245144859e3e6626e4559`. 3 ZIP-Einträge und CRC PASS; **PR #622** gemergt. GitHub-Größe und Blob-SHA bestätigt.

**Belege:** https://github.com/hallo-netizen/affiliate-pferdeportal/pull/622 · https://github.com/hallo-netizen/affiliate-pferdeportal/pull/625 · https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/41687120534

**Versionsautorität:** `PLUGIN_AKTEN/<ID>/CURRENT.md` für jedes Plugin. Vollständiges Original unter `ISOLIERTE_PLUGINS/<ID>/CURRENT.zip`. Manifestdateien sind nur Prüfnachweise. Die 71 Design-Übertragungsteile gehören zum separaten Staging, nicht zum offiziellen Pluginbüro; die vollständige Original-ZIP wurde inzwischen erfolgreich übernommen. Deshalb **keine weiteren Design-Teile zur Vervollständigung nötig**.

**Status: PLUGINABLAGE ABGESCHLOSSEN (3/3).** Die WordPress-Liveinstallation ist dadurch **nicht** geprüft oder freigegeben. Keine Änderungen an WordPress, K0 oder anderen Portalen.

**NEXT ACTION:** Keine weiteren Archivübertragungen erforderlich. Eine spätere WordPress-Liveprüfung ist ein gesonderter Auftrag.
