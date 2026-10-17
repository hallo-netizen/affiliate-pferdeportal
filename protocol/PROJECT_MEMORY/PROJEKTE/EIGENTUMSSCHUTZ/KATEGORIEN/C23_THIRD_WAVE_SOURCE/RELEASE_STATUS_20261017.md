# Hab & Bewahr – vorhandenes Kategorieplugin 1.14.8.32 – getestetes Release
**17.10.2026 · STATUS: ZIP FERTIG, LOKAL GEPRÜFT, NICHT LIVE INSTALLIERT**

## Identischer Quellstand
Ausgangspunkt war das vollständige vorhandene, bereits live für 743+472 erfolgreich eingesetzte Kategorieplugin **1.14.8.31**. Erweiterung als dritter, ausschließlich ADD-only-Wave im **selben Plugin**. Keine neue Pluginarchitektur und keine Änderung bestehender Kategorie-/Seiten-IDs, Slugs, URLs oder Post-Term-Bindungen.

Das verbindliche C2.3-Fachdelta ist `../C23_471_ADDONLY_TECHNISCHES_MANIFEST_NUR_GITHUB_20261017.json` (nicht der überholte 475/490-Vorentwurf). Die **471 Quellzeilen** (Owner/Typ/Name) wurden byteidentisch gegen das GitHub-Original abgeglichen:
SHA256 `eab5be9258c80cb31336cee5741cc4f14f932e6d99a30a42671490e24a2e760f`. Nach fachlicher Prüfung aller 265 Themen:
- **93 FAQ** unter alten R3-Themenseiten.
- **220 Beratungen**, davon 93 ältere und 127 neue Themen; vorhandene Beratung bleibt erhalten.
- **91 Vergleiche** bei alten Themen; 2 rein organisatorische Themen vergleichen innerhalb der Beratung.
- **67 zusätzliche individuell tragfähige Aspekte**. Keine pauschalen Wartungs-/Kosten-Schablonen.
- **340 neue flache Artikelkategorien an 93 historischen echten WP-Seite3-IDs**, **131 an bestehenden neuen C2.2-Topic-IDs**. Alle bisher vorhandenen 1323 Artikelkategorien geschützt.

## Release-Artefakte dieses GitHub-Büros
- `includes/class-apkw-c23-471-add-only.php` – echte zusätzliche PHP-Importlogik mit administrativer Freigabe, eigenem Backup/Lock, Batches zu je 20, Revisionssicherung, Stage-/Physical-Readback, vorsichtigem Rollback und Wiederholungsblockade.
- `profiles/hab-und-bewahr-c23-471-add-only.json` – **exakt dieselben 360949 Bytes** wie die lokal getestete Manifestdatei; Git-Blob-SHA1 `0c2d750abb0d3dc6558105ead6aca6dd7d370316`.
- `tests/test_471_real_original.php` – echter, lokal ausgeführter Integrationscheck mit originalem C2.2-743-PHP-Auditor, originalem 472-PHP-Auditor, neuer C2.3-Komponente und echtem APKW-Frontendrenderer in einer WordPress-Mockumgebung.
- `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.32.zip.b64` – vollständig installierbares Originalplugin als nachvollziehbar gespeichertes Base64-Archiv, Git-Blob-SHA1 `8b61591566b5e862af34cae5fad9f2dbf5b90747`. `decode_release.py` stellt das ZIP mit harter SHA256-Prüfung wieder her.
- **Fertiges ZIP:** 308081 Bytes, **40 Original-/Erweiterungsdateien, 33 PHP-Dateien**, ZIP-CRC PASS; SHA256 `e72e30aa6f9394e62d64cfcc29fca7848399dbd9787b619da7d4fd80f170b79e`.

Diff gegenüber 1.14.8.31: Nur vier vorhandene Dateien geändert – Bootstrap, README, vorhandener C2.2-Admin-/Fachprüfer, vorheriger 472-Abschlussprüfer (zur Anerkennung der neuen Revision). **Zwei Dateien ergänzt** – neue PHP-Klasse und 471er-Profil. Die bestehenden Module des 743-Imports und dessen Profildatei blieben unverändert; keine alten Jobs erneut ausführen.

## Tatsächlich lokal ausgeführt
1. **33/33 PHP-Lints bestanden**; ZIP-CRC und Dateidifferenz 40/40 PASS.
2. Manifest: **471/471** global eindeutige neue Term-Namen, keine Normalisierungs-/Slug-Überschneidung gegen die 285 alten, 566 C2.2 und 472 aus zweiter Welle. 220 betroffene physische/technische Themen-Owner eindeutig.
3. Positive Importprobe: **471/471 WordPress-Term-Anlagen über die vorhandene TargetWriter-Schnittstelle**, 340 bei alten, 131 bei neuen Themen. Alte 1323 Terms und sämtliche ursprünglichen Snapshot-Knoten/Zuordnungen unverändert.
4. **Die drei Original-/Zusatz-Completion-Audits gleichzeitig PASS**: alte 743, zweite 472, dritte 471.
5. **Echter PHP-Frontendrenderer:** 471/471 neue Kategorielinks auf 220 korrekten alten/neuen Thema-Owners, keine zusätzliche Seitenebene.
6. Negativ: Fehler nach 30 neuen Writes → 30/30 eigene Terms gelöscht, 0 Altobjekte angefasst.
7. Negativ: fehlende alte physische WordPress-Elternseite → 0 Writes, gesperrt.
8. Negativ: fehlende alte geschützte Term-ID im Snapshot → 0 Writes, gesperrt.
9. Negativ: Ausfall der Endprüfung **nach Schreiben des neuen SNAP, vor kompletter Freigabe** → sichere Rückkehr zur Originalrevision, 471 neue Terms gelöscht, 1323 geschützte erhalten.
10. Negativ: bereits mit Inhalt belegter neuer Term → Rückbau ausdrücklich **gesperrt**, Term erhalten, Fehlstatus statt gefährlicher Löschung.

**Grenze:** Die WordPress-Funktionen waren bei der lokalen Ausführung gemockt; dies ist kein echter 1:1-Live-Test und **noch keine Liveinstallation**. Aussagen zur Live-Navigation nach Update oder Erfolg in echtem WordPress bleiben bis nach der Installation offen.

## Genau eine NEXT ACTION
**Das vorhandene Kategorieplugin als normales Update auf 1.14.8.32 installieren** (keinen 743er- oder 472er-Import erneut starten). In **WordPress → Portal-Kategorien → C2.2 Kategorien** wird der neue Abschnitt „C2.3 – 471 fehlende vertiefende Artikelkategorien“ sichtbar. Dort muss die eigene **Vorschau ohne Schreibzugriff: 471 neue Kategorien** erfolgreich sein. **Erst mit der gesonderten ausdrücklichen Freigabe-Checkbox** den 471er-ADD-only-Lauf starten, danach grüne Endmeldung „471 Ergänzungen abgeschlossen und geprüft.“ prüfen. Kein Nutzerexport, kein Bibliotheksworkflow, keine Einzelartikelprüfung. Sichtbare alte H1/Kacheltitel bleiben im Designplugin ein separater bereits dokumentierter Darstellungsauftrag und werden durch dieses Kategorieplugin bewusst nicht stillschweigend umbenannt.
