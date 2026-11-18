# Hobbydepot – Texterstellung: vollständiges Kopie- und Fehlerprotokoll

**Erstellt:** 18.11.2026  (nachträgliche Bestandsaufnahme und Dokumentation)
**Status:** REINE ARBEITSKOPIE – NICHT INSTALLIEREN.
**Quellversion:** Pferdeatelier Texterstellung 0.4.23 (Testversion, 88 Dateien).
**Quelle SHA-256:** `c2b5b8f8921cf783da87a28f525ec81b99888277fbe9929a0f8ffccdd659a3ab`.
**Vorherige Kopie SHA-256:** `03ffe443d6879ca4170cc8660aceb8b567cbc7a85d8673e9b00bea90971420dc`.

## 1. Chronologie und Bestandsdaten

| Schritt | Aktion / Beobachtung | Status |
|---|---|---|
| 01 | Quell-ZIP 0.4.23 aus der Pferdeatelier-Dateiablage gelesen. | Belegt |
| 02 | Isolierte Arbeitskopie für **Hobbydepot** erzeugt. Original unverändert. | Belegt |
| 03 | Sieben Dateien im Kopie-Quellbestand verändert. Einzelheiten unten. | Belegt |
| 04 | Eine alte Signaturdatei für geänderte Portalregeln aus der Kopie entfernt, statt eine falsche Signatur weiterzuverwenden. | Belegt |
| 05 | 78 PHP-Dateien unverändert bewahrt; keine K0- oder Live-Seitenänderung. | Belegt am ZIP-Vergleich; Live-Installation nicht geprüft |
| 06 | Drei Handreichungs-Dateien (`START_HIER.md`, `PORTAL_ARBEITSSTAND.json`, `OFFENE_PORTAL_ANPASSUNGEN.md`) dem Arbeitskopie-Ordner beigelegt. | Belegt |
| 07 | Die ZIP in separater persönlicher Dateiablage `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/` gespeichert. | Erfolgreich |
| 08 | Direkter GitHub-Schreibversuch in `hobbyroom/project-memory-campus-v1-20260905` wurde durch vorhandene Regel `single-current-lock` abgewiesen. **Kein** Umgehen/Abschalten der Sperre. | Fehler 409 protokolliert |
| 09 | Eigenen Arbeitszweig `work/texterstellung-hobby-hab-arbeitskopien-20261116` erstellt. | Erfolgreich |
| 10 | Neues Büro mit `START_HERE.md` und `CURRENT_STATE.md` erstellt. | Im Arbeitszweig erfolgreich |
| 11 | Entwurfs-Änderungsantrag [#819](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/819) gestellt. **Nicht** als übernommen oder freigegeben zählen. | Offen |
| 12 | Am 18.11. Verzeichnis und Originaldateien erneut verglichen. Mehr Pferde-Namensbezüge als zuvor pauschal angegeben, siehe Fehler F02. | Nachgewiesen |
| 13 | Am 18.11. existieren gesonderte Portalversionen mit der Kennung 0.4.24 in der Dateienablage. Deren Unterschiede und Freigaben sind **nicht** Bestandteil dieser 0.4.23-Arbeitskopie und nicht durch sie geprüft. | Versionsabgrenzung |
| 14 | Dieses genaue Protokoll wird sowohl der Arbeitskopie als auch dem GitHub-Büro beigefügt. | Dokumentation |

## 2. Originaldateien: tatsächlicher Vergleich

**Sieben veränderte Quelldateien:**
- `texterstellung/README-TESTINSTALLATION.txt`
- `texterstellung/contracts/k0-article-type-capabilities-v1.json`
- `texterstellung/original/pste/contracts/article-type-extension-manifest-v1.json`
- `texterstellung/original/pste/contracts/family-identity-v2.json`
- `texterstellung/original/pste/contracts/journal-article-type-v1.json`
- `texterstellung/original/pste/contracts/portal-domain-seeds-v1.json`
- `texterstellung/original/pste/fixtures/portal-category-map-v1.json`

**Eine entfernte Datei:**
- `texterstellung/original/pste/contracts/article-type-extension-manifest-v1.sig`
- Keine zusätzlichen Quelldateien.

**Technische Bestandswerte:** 87 Quellcodedateien aus dem ursprünglichen Paket erhalten, davon 78 PHP. 0 Excel-XLS/XLSX-Dateien im Paket. 74 PHP-Dateien enthalten mindestens einen Suchbegriff aus `pferd`, `pferdeatelier`, `pferde-atelier`, `pste_`; darunter sind auch interne Bezeichner. Ein bloßer Treffer beweist nicht, dass der Code eine Pferderegel erzwingt. Die programmatische Umstellung auf Hobbydepot ist ausdrücklich **noch nicht abgeschlossen**.

## 3. Fehler, fehlende Nachweise und Aufträge

- **F01 – GitHub 409:** Direkte Ablage in den geschützten Campus-Zweig nicht erlaubt. Maßnahme: separater Arbeitszweig und offener PR #819. Hauptzweig unverändert.
- **F02 – Vorherige zu niedrige Bezugszahl:** Eine frühere Notiz nannte nur „15 PHP-Dateien mit Restbezügen“. Der vollständige Suchabgleich ergibt **74 von 78** mit Pferde-/PSTE-Begriffen. Dies ist eine rohe Trefferzahl, keine geprüfte Anzahl fachlicher Blockaden. Maßnahme: Zahl korrigieren; keine pauschale Wortersetzung.
- **F03 – Keine Freigabe:** Kopie ist kein installierbares WordPress-Plugin, sondern ein Arbeitsordner. Ein realer Portaltest ist nicht durchgeführt. Maßnahme: kein Installationsangebot; zuständiger Chat führt Portalanpassung und Funktionsabnahme durch.
- **F04 – Signaturkonflikt:** Nach Ändern der Portalregeln passt die frühere Signatur nicht mehr. Die alte Datei wurde aus der Arbeitskopie entfernt. Maßnahme: vor einer Installationsfreigabe neue passende Signatur/Regelbindung prüfen; nicht blind ersetzen.
- **F05 – Portaldaten fehlen bewusst:** Echte Hobbydepot-Kategorien, Themen- und Regelzuordnungen wurden nicht erfunden. Maßnahme: anhand des entsprechenden Portals bereitstellen und verbinden.
- **F06 – Fremde Folgeversion:** Separate 0.4.24-Pakete existieren; dieses Büro darf seine 0.4.23-Kopie nicht als aktuelle 0.4.24-Version ausgeben. Maßnahme: Versionsvergleich mit dem jeweiligen Folgechat.
- **F07 – Rückimportdiagnose Pferdeatelier:** Diagnose von oliver-beil.de am 18.11. zeigt `ORIGINAL_PSERC_IMPORT_BLOCKED` bei zwei Artikeln ohne sichtbaren Untergrund. Dieser Fehler betrifft die Pferdeatelier-Vorlage und wird **nicht** in den Portal-Arbeitskopien still geändert. Maßnahme: zentrale Fehlerweitergabe beim Originalimporter sauber protokollieren und danach kontrolliert übertragen.

## 4. Verbindliche Weiterarbeit

Jede spätere Änderung im zuständigen Portalchat erhält **eine neue Zeile** mit Datum, Ausgangsdatei/Version, geänderten Dateien, Ursache, konkreter Änderung, Prüfbeleg, Ergebnis, offenen Punkten und Freigabestatus. Kein weiterer Fortschritt ist damit bereits behauptet.

**Nicht verändert:** K0, WordPress-Live-Inhalte, veröffentlichte Beiträge, Redaktionsplan, Original-Plugin-Datei 0.4.23. Das Zurücksetzen des Redaktionsplans erfolgt gesondert anhand des aktuellen Exports.