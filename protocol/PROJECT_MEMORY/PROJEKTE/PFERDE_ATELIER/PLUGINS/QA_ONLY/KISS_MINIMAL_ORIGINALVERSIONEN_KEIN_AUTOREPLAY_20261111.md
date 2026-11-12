# Pferdeatelier – minimaler, nicht freigegebener WordPress-Teststand 11.11.2026

## Ziel und Grenzen
KISS-Zielvertrag unverändert: SEO→Redaktionsplan→Export→K0, kein neuer 5.000er-Durchlauf, kein direktes Anfassen oder Restore der Datenbank, K0 und Artikeltexte unangetastet, keine neuen Klassen, Tabellen, Worker oder zweiten Prüfschleifen.

## Tatsächlich gebaut – Originalquellen statt Patchstapel
- Basis **tatsächlich archiviertes** `PSTE-0.57.144.32-KISS-REDAKTIONSBUERO-AUTOMATIK-TITEL-NUR-TEST.zip`; neue Version **PSTE 0.57.144.40**, Quelländerungen nur in `includes/class-pste-admin.php` und `includes/class-pste-research-driver.php`, plus Version. Automatik ruft `startExistingOnly` weder beim normalen Auto-Klick noch nach abgebrochenem Audit auf; gespeicherte bestehende Full-Audit-Warteschlange wird bei init und Treiberschritt nicht selbst weitergetrieben. Sie meldet stattdessen einen klaren Stop mit Hinweis auf **bereits vorhandenen Kurzen Dienstweg**, der nur explizit ausgewählte Themen lokal verarbeitet.
- Basis **tatsächlich archiviertes** `PSERC-0.28.61-K0-SEO-HERKUNFT-NUR-WORDPRESS-TEST.zip`; neue Version **PSERC 0.28.67**, nur vorhandener `class-pserc-plan-compile-job.php`, Version und bestehendes signiertes Paketmanifest verändert. Null planbare Zeilen vor aufwendigem Neubau bzw. Null READY vor `activate` blockiert; aktiver leerer Plan wird nicht als READY-Plan akzeptiert.
- **Keine andere Funktion, kein neuer Datenweg**. Originale 14 PSTE SEO-Entscheidungsdateien unverändert. Keine neue SQL-Migration.

## Verifizierte Tests – realistische Grenze
- 126 PHP-Dateien Syntax PASS; PSERC 61/61-Paketsignaturen PASS; CRC und Byteidentität der zwei tatsächlich gepackten WP-Plugin-ZIPs PASS.
- Mit den **drei originalen Regendecken-Artikeln vom 10.11.2026**: alte PSERC-Metadaten-Fünffelder-Batch-Integrität PASS, drei alte signierte PRE_TYPE-Profile PASS, 3/3 READY-Identitäten PASS, Manipulation BLOCKED.
- Aus den **tatsächlichen neuen Klassendateien** ausgeführt: vorhandene RUNNING-existing-only-Queue wird von `maybeKickExisting` nicht geweckt und von `executeOneStep` nicht verarbeitet; 0-READY-Plan ruft `activate` nicht auf. Beide Tests PASS.
- **Nicht getestet:** echte WordPress-Installation, mit 0 planbaren Artikeln wieder 3 READY erzeugen, echter K0-BOUND_TYPE-Start, produktive Migration/Upgrades. Diese Prüfungen dürfen **nicht** als erledigt gelten.
- **Kein** aktiver Eingriff in echte WordPress-DB; kein Plugin live installiert, kein K0-Lauf, keine neue DataForSEO-Recherche.

## Paket und Pfad
Gesamtarchiv `PFERDEATELIER-KISS-MINIMAL-ZWEI-PLUGINS-NUR-TEST-20261111.zip` SHA256 `d12c4e44dd7d54342753e2866c21f6c578a4339d85f07de14d3c762d696a0842`, mit **zwei getrennten** WordPress-Plugin-ZIPs, Prüfbericht und genau zwei Originaldifferenzen. Dauerhaft unter `/pferdeatelier/PLUGINS/QA/` abgelegt.
- PSTE 0.57.144.40 SHA256 `31716238747a93819dc169fbfa37ba5e8c02f3ef832d37af9e2ad5d9a6c31af6`
- PSERC 0.28.67 SHA256 `435ef69b0046d5e574be6cde56c6643aa2cd80a97943323a22c1b7ebc5fbb3fd`

## Was tatsächlich noch fehlt
Die verlorene **WordPress READY=3-Freigabe** kann nicht durch Quellcode-Rückbau hergestellt werden. Die originale Drei-Artikel-Übergabe ist separat erhalten und direkt für die vorhandene K0-Fünffelder-Eingangsvalidierung geeignet; K0-Schreibkontext/BOUND_TYPE und echter WordPress-Ablauf sind noch nicht belegt. Der alte Code ermöglicht weiterhin den expliziten **Kurzen Dienstweg** für genau drei ausgewählte Themen, ohne einen 5.000er-Rechercheauftrag. **Ob diese konkreten drei im inzwischen beschädigten WordPress-Bestand READY werden, muss an der separaten Testinstallation gemessen werden**, nicht behauptet.

**Status:** `ORIGINAL_BASE_SAFE_AUTO_REPLAY_REMOVED_LOCAL_QA_PASS`; `WP_END_TO_END_UNVERIFIED`; `READY_3_NOT_RESTORED`; `NOT_LIVE_APPROVED`.
