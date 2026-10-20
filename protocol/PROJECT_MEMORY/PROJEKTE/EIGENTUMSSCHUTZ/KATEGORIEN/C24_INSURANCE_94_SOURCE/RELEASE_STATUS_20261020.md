# Hab & Bewahr – Versicherungs-Erweiterung C2.4 im BESTEHENDEN Kategorieplugin
Stand 2026-10-20. **Fertiges binaeres Kandidaten-ZIP 1.14.8.33 im GitHub; nicht live installiert, kein WordPress-Freigabevermerk.**

## Ziel und Umfang
Ergaenzende siebte Hauptwelt Versicherungen, keine neue Portalarchitektur.
**1 R1 + 5 R2 + 20 R3 = 26 WordPress-Seiten, 68 flache Kategorie-Terms, 94 neue Objekte.**
Alle **105 zuvor beschlossenen Versicherungsarten** exakt einmal einem der 20 R3-Hubs zugeordnet. Darunter auch gesetzliche/private Krankenversicherung, Rente, Kapital- und Lebensversicherung. 28 schmale Policen koennen spaeter durch Einzelbeitraege abgedeckt werden. **Keine Artikel, Artikelideen oder Titel** hier erzeugt.

Fachliche Quellautoritaet: `../KONZEPT/VERSICHERUNGEN_KOMPAKT_26_SEITEN_68_KATEGORIEN_105_THEMEN_20261020.json`
Verbindliches gebundenes PHP-Profil: `profiles/hab-und-bewahr-insurance-94.json`, `source_blob_sha=a74e6b3c62a49115bc58bc4fb233ca882dd87306`.

## Original und neu gebautes Plugin
Original `1.14.8.32`: GitHub C23-Archiv, 308081 Bytes, 40 Dateien, 33 PHP-Dateien; laut seinem archivierten lokalen Release SHA256 `e72e30aa6f9394e62d64cfcc29fca7848399dbd9787b619da7d4fd80f170b79e`.
Neues BINÄRES Originalplugin `1.14.8.33`: **394395 Bytes, 43 Dateien, 34 PHP-Dateien**, Git-Blob-SHA1 **`c81533d58029dcddde4d88108909d7f31d6f1e67`**.
Datei: `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.33.zip` – **wirkliche ZIP-Datei**, kein separater Plugin-Neubau. Zusätzlich als `.zip.b64` quellengetreu im selben Büro gesichert.

**Exakte Änderung zum gesicherten 1.14.8.32:**
- 39 von 40 Altdateien inklusive sämtlicher vorhandener Fachklassen, C2.2-/C2.3-Module, Tests, Profile, IDs vollständig unverändert auf ZIP-Ebene (komprimierte Daten byteidentisch).
- In einziger bisheriger Bootstrap-PHP Version `1.14.8.32→1.14.8.33` und `require_once/includes/class-apkw-insurance-94-add-only.php`; einmaliges `APKW_Insurance_94_AddOnly::init()` hinzugefügt.
- 3 neue Dateien: `includes/class-apkw-insurance-94-add-only.php`, `profiles/hab-und-bewahr-insurance-94.json`, `INSURANCE_C24_RELEASE_INFO.txt`.

## Testnachweise – ehrlich abgegrenzt
PASS: 94er-Datenstruktur und 105/105 Policen im GitHub-Konzept, 10/10 absichtliche Datenfehler blockiert.
PASS: Import-PHP mit PHP 8.4 lokaler Syntaxcheck.
PASS: WordPress-Mock-Simulation 94 Jobs (26 Seiten/68 Kategorien); schreibfreie Vorschau, Duplikat-Slug/Term-Slug/Term-Name, fehlender 471er-C2.3-Abschluss und fehlerhafter 471er-Audit, Doppelstart, Batch 94/94, Rückbau bei erzwungenem Schreibfehler, alte Revision bleibt unverändert.
PASS: Dieselben Fälle mit **echtem, byteidentisch aus Original-1.14.8.32 entnommenem APKW_TargetWriter** (WordPress-Funktionen im Mock simuliert).
PASS: ZIP-Struktur 43/43, alle 39 übertragenen Original-Kompressionsblöcke byteidentisch; 4 neu STORED-Einträge CRC-PASS; reales PHP und fachliches JSON byteidentisch zu den separaten GitHub-Quellen; manipulierter CRC-Fall blockiert.
**NICHT als PASS behauptet:** kompletter Originalplugin-End-to-End-Test mit echtem `APKW_FinalTargetAdmin::frontend_readback()` und `APKW_FrontendStructure`; Original-WordPress-Core/Live-Datenbank-Test, reale 6-Welten-Navigation, WP-Backend-Version, Designplugin-Megamenü. Keine produktive Veröffentlichung.

## Harte Ablauf- und Bestandsschutzregeln
1. Keine automatische Schreibaktion durch ZIP-Update. Versicherungslauf nur im bisherigen WordPress-Kategorie-Plugin über eigenes Untermenü mit Nullschreib-Preflight und gesondertem Freigabe-Häkchen.
2. **C2.3-Nachholimport 471 MUSS vorher COMPLETE und dessen Original-Completion-Audit PASS sein**; sonst blockiert Versicherungs-Preflight. 743 und 472 bleiben unangetastet. Bei Live-C2.3-Status keine Annahmen.
3. Vor Import read-only Bestands-Revision, Anzahl aktiver Welten=6, Slug-/Term-Kollisionen und alte Snapshot-Konsistenz prüfen; kein Löschen/Umbenennen existierender Seiten, Kategorien oder Beiträge.
4. 15 neue Objekte je Batch, physische IDs sofort journalisieren, Stage-Readback und Live-Readback, vorsichtiger Rückbau; fremd belegte Terms/Seiten dürfen nicht gelöscht werden.
5. Das **Megamenü** wird über das bestehende Designplugin dargestellt und ist **getrennt** zu prüfen: fünf Bereiche optisch passend verteilen, keine künstlichen Inhalte.

**AKTUELLE NÄCHSTE HANDLUNG:** Auf dem vorhandenen WordPress erst Status des 471er-C2.3-Laufs prüfen bzw. separat abschließen; danach Pluginkandidaten aktualisieren und im selben Plugin **nur die nicht schreibende Versicherungs-Vorschau** ansehen. Erst nach externer Freigabe den Import. Der Stand ist NUR lokaler/GitHub-Releasekandidat, bis Live-Preflight und Originalfrontend-Prüfung nachgeholt sind.
