# Robotik – Pluginbüro / Kategorie-Workflow

## 0.4.5 / V58 – gezielte Wiederaufnahme des beim Anbieter bestätigten 50000-Abbruchs (TEST)
- **Kein kompletter Neustart, kein neues Plugin.** Der tatsächlich in WordPress `BLOCKED_UNCERTAIN 0/38` gestoppte 0.4.4-Durchlauf kann mit derselben Identität auf 0.4.5 aktualisiert werden. Nur bei gespeichertem ersten HTTP-500-Fehler bietet das Backend **einmalig manuelle Wiederaufnahme** mit erneuter ausdrücklicher Kostenbestätigung.
- Bestehende 38er-Auftragsliste, Run-ID, Kostenrahmen und V52-Fachmaster bleiben erhalten. Nach weiteren Fehlern wird kein zweites Mal automatisch oder manuell wiederholt. Original-Import-/Veröffentlichungsdateien byte-identisch.
- Quellprüfungen und lokale WP-Simulation bestanden; **noch kein echter Live-Lauf**. `PLUGIN/CURRENT.zip` = `PLUGIN/VERSIONEN/0.4.5.zip` (TEST). Bericht `PLUGIN/SEO_V58_RELEASEPRUEFUNG_20261114.md`.


## NEUESTE GEBÜNDELTE TESTVERSION 14.11.2026 – 0.4.4 / V57
- **Einziges vorhandenes Kategorie-Plugin**. Geschütztes 0.4.3-Update, V52-Fachbestand weiterhin nur SEO, alter Erstimport 104/89 **bytegleich**, vorhandene WordPress-Inhalte unangetastet.
- Ein kostenbegrenzter SEO-Gesamtlauf: **437 Overview-Keywords**, **8 Keyword-Ideas-Aufträge** für alle 141 Typseiten über acht Hauptwelten, **29 Google-Top10-Suchen** als **16** URL-Konfliktvergleiche. 38 interne Aufträge, **ein Nutzer-Kostenstart**, ein Ergebnis-JSON. 300 Ideen je Welt sind Begrenzung, keine garantiert vollständige Forschung.
- PHP/ZIP und 38 Mock-Aufträge bestanden, **noch nicht** echtes WordPress oder bezahlte API. Nutzer darf den neuen Test-Installer nur selbst installieren, Kosten nur selbst ausdrücklich freigeben. Alte Einzelabfragen vorhanden, aber eingeklappt.
- **GitHub `PLUGIN/CURRENT.zip` und `PLUGIN/VERSIONEN/0.4.4.zip` = identische aktuelle Test-ZIP 0.4.4.** Library-Backup und Quellen im V57-Protokoll. Nicht mit früheren 0.3.0-/0.4.3-Hinweisen verwechseln.


## NEUESTE VORBEREITETE TESTVERSION 14.11.2026 – 0.4.3, NOCH NICHT LIVE
- **Gleiche Pluginidentität**, quellgeprüft aus Original **0.4.2**. Fertiges Test-ZIP liegt in der Library **`/robotik/Konzeptbüro/ROBOTIK_KATEGORIE_WORKFLOW_0.4.3_SEO_V52_NUR_TEST.zip`** (SHA256 `c06fb36d5e1e1d2d5955de6f9f90daeb28f35db9b23bf09d4269dfc212c52382`). Das GitHub-`CURRENT.zip` **ist weiterhin die historische 0.3.0** und wird **nicht fälschlich als 0.4.3 bezeichnet**; für V53 **keine ZIP-Datei in GitHub synchronisiert**, aber die drei geänderten/zusätzlichen Quellkomponenten vollständig im `V53_SOURCE/` und Tests in `SEO_V53_RELEASE_PRUEFUNG_20261114.md`.
- Nur **WordPress → Robotik Kategorie → DataForSEO** nutzt jetzt **141 Typseiten-/296 Rubrik-Suchbegriffe** aus dem V52-Fachentwurf; 16 alte HOLDs werden mitgeführt. 437 eindeutige Suchbegriffe, 0 verworfen, kostenloser JSON-Export ergänzt. **Kostenpflichtige Abfrage unverändert nur mit Nutzerbestätigung.**
- **Vier alte Dateien bytegleich**: Inventur, Erstimport, Sammelveröffentlichung und altes Erstimportprofil. **Daher weiterhin keine Möglichkeit, mit dem historischen Erstimport alle 141 V52-Typen zu übernehmen.** Nicht den alten Erstimport starten, um V52 umzusetzen.
- **Tests lokal:** 5 PHP-Dateien syntaxgeprüft, ZIP CRC okay, PHP-Preflight 437/437 und 16/16 HOLD, Backend-UI-Simulation bestanden; **keine echte WordPress-Installation oder bezahlte API geprüft**. Noch keine Freigabe für WordPress-/URL-/SEO-Änderungen.
- **Unmittelbarer Nutzerweg nach Installation der Testversion:** `Robotik Kategorie → DataForSEO → Gesamte Keywordliste prüfen (kostenlos) → SEO-Keywordliste als JSON herunterladen`. Datei zurück in den Chat, damit der tatsächliche WordPress-Readback mit V52 übereinstimmt. Kein Paid-Start.


## AKTUELLER ERGÄNZUNGSSTAND 11.11.2026 – 0.4.1 FERTIG, NOCH NICHT LIVE
- Das unterhalb dieser Ergänzung beschriebene GitHub-`CURRENT.zip` 0.3.0 ist **historischer GitHub-Bestand**; es ist nicht mit dem inzwischen bereitgestellten 0.4.0 zu verwechseln.
- Nutzer meldete den vorherigen 0.4.0-Schritt als erledigt. Echte 193/193-WordPress-Live-Prüfung wurde nicht erneut bereitgestellt.
- **0.4.1 Kategorie-Workflow** erweitert dieselbe Pluginidentität ausschließlich um sichere Sammelveröffentlichung bereits importierter 104 Robotik-Seiten. Lokal geprüft; Library-ZIP `/robotik/Konzeptbüro/ROBOTIK_KATEGORIE_WORKFLOW_0.4.1_PUBLIKATION_TEST.zip`; diese Datei wurde **noch nicht** als `PLUGIN/CURRENT.zip` in GitHub synchronisiert.
- **Getrenntes Designplugin**: `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.1.0_TEST.zip` für Mega-Menü und Footer, lokal geprüft, ohne WordPress-Schreibzugriff.
- **Details und Nachweise:** `PUBLIKATION_041_20261111.md`.


**Einziger aktiver Installer:** [CURRENT.zip](CURRENT.zip) – Version **0.3.0**.

**Versionsarchiv:** [VERSIONEN/0.1.0.zip](VERSIONEN/0.1.0.zip) · [VERSIONEN/0.2.0.zip](VERSIONEN/0.2.0.zip) · [VERSIONEN/0.3.0.zip](VERSIONEN/0.3.0.zip). Alte Versionen ausschließlich Archiv, nicht parallel installieren.

**Verbindliches Versions-/Prüfprotokoll:** [RELEASE_PROTOKOLL.md](RELEASE_PROTOKOLL.md).
**Einziger operativer Status für Übergaben:** [../CURRENT_STATE.md](../CURRENT_STATE.md).
**Allgemeine Plugin-Altlastenprüfung:** [ORIGINAL_AUDIT_20261109.md](ORIGINAL_AUDIT_20261109.md).

## Version 0.3.0 – tatsächliche Fähigkeiten
- WordPress-Adminmenü „Robotik Kategorie“.
- Bisherige Prüfung von JSON-Plänen und Speichern des eigenen Entwurfs.
- Manuell ausgelöste **nur lesende** WordPress-Bestandsaufnahme von Seiten, Beiträgen, WordPress-Kategorien und – sofern vorhanden – HivePress-Inseraten/-Kategorien.
- Ein zusammengefasster JSON-Bericht statt Einzeldateien.
- Keine Erstellung/Änderung/Löschung von WordPress-Seiten, WordPress-Kategorien oder Beiträgen; WordPress-Entwurfsoption kann gespeichert werden.

**Noch nicht enthalten:** vollwertige Keyword-Recherche/DataForSEO, GitHub-Master-Abgleich, fachlich vollständige Drei-Säulen-/Anzeigeprüfung, WordPress-Kategorie-/Seitenimport. Der Bericht ist Bestandsinventar, keine vollständige fachliche Abnahme.

**Dateiprüfung:** 7.926 Byte, SHA256 `3c31aaaf86379a054034a80c8aeb3eaebdf616baa953ac079793f6495f1ecd30`; ZIP-CRC und PHP-Lint PASS. 20 historische lokale Prüffälle sind im vorherigen Erstellungsstand dokumentiert, aber **ein WordPress-Live-Test ist NICHT durch den ZIP-Nachweis ersetzt**.

**Installation:** Nutzer meldet 0.3.0 am 09.11.2026 als installiert. Echte Backend-/Frontend-Abnahme noch offen.

## KISS-Regel für jede Folgeversion
1. ZIP in `VERSIONEN/<version>.zip` ablegen, erst nach Dateiintegrität/Version-/Pfadkontrolle.
2. `CURRENT.zip` auf denselben geprüften ZIP-Inhalt aktualisieren; nur ein aktiver Installer.
3. `RELEASE_PROTOKOLL.md` und `../CURRENT_STATE.md` im **selben Campus-Commit** aktualisieren.
4. In `ROBOTIK/PLUGINS` lediglich auf diesen echten Ablageort verweisen (nicht nochmal kopieren).
5. Lokale Prüfungen, Nutzer-Installationsmeldung und echten WordPress-Live-Test **getrennt** berichten. Neue Chats beginnen über `START_HERE.md` und `CURRENT_STATE.md`.
6. K0/Pferdeatelier, Hobbydepot und Hab & Bewahr strikt unangetastet lassen.

Die alte Datei `INSTALLATIONSKANDIDAT_0.2.0.zip` bleibt aus Gründen der Rückverfolgung erhalten, ist aber **historisch** und nicht der aktive Download.
