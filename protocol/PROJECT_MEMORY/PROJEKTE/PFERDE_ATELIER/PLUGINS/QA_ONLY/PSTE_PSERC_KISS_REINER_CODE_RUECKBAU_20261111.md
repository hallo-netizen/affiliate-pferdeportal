# Pferdeatelier: reiner Rückbau statt weiterer Einzel-Fixes – 11.11.2026

**Stand:** Die Codeänderungen nach dem historischen Drei-Artikel-Export wurden als getrennte ZIPs auf frühere Quellstände zurückgesetzt; **keine neue Funktionalität eingebaut**. Original-K0-Zweig unverändert.

## Warum dieser Rückbau und keine weitere Automatik-Korrektur?
Original-Export vom 10.11.2026 wurde mit PSTE **0.57.144.32** und PSERC **0.28.61** erstellt; dort waren 3 READY und ein original signierter Fünf-Felder-Handoff mit den drei Regendecken-Artikeln. Nach späteren PSTE-.37-Änderungen startete tatsächlich ein kompletter 5.013er Neu-Prüflauf und schrieb viele gespeicherte Themenbewertungen um; anschließend aktivierte PSERC 0 READY. Das ist durch die originalen Flugschreiber vom 11.11. belegt. Eine erneute volle Quellenprüfung oder weitere neue Einzel-Sonderwege sind ausdrücklich nicht zulässig.

## Rückbaupaket – exakte Herkunft / keine erfundene Originalversion
1. **PSTE 0.57.144.32** aus dem physisch vorhandenen .33 ZIP **durch Rückanwendung des archivierten, bereits dokumentierten echten `.32→.33`-Quellpatches** rekonstruierte Plugin-Dateien. Alle 121 Dateien der rekonstruierten .32 wurden anschließend mittels Vorwärts-Wiederanwendung des Patches zu einer **byteidentischen** .33 geprüft. Das ist starker Quellbeleg, ersetzt aber nicht den nicht vorliegenden Original-ZIP-Hash von .32. Neues ZIP `PSTE-0.57.144.32-ORIGINALCODE-RUECKBAU-TEST.zip` SHA256 `0dddb890ac1cd7a24a996b843965521b9a65196cbe7013f3f2dc179d280eabe4`, 648988 Bytes.
2. **PSERC 0.28.60**, das **unveränderte physisch vorhandene Original-ZIP** als unmittelbarer Vorgänger der zur historischen Datei passenden **0.28.61**-Version. Das exakte 0.28.61 Plugin-ZIP ist **hier nicht vorhanden und wurde nicht erfunden**. Die fachliche Plan-Compiler-Datei ist zwischen .60 und .62 byteidentisch; da die Dokumentation .61→.62 keine Compileränderung nennt, ist dies der unveränderte alte Berechnungsweg, nicht die identische alte Admin-Export-UI. `PSERC-0.28.60-ORIGINALCODE-RUECKBAU-TEST.zip` SHA256 `c9c7e90b265e650739d2568a7cb807238db7f081ddcf7d8698fe64961b84f22a`, 268511 Bytes.
3. Originaler signierter Drei-Artikel-Metadatenexport unverändert mitgesichert, ausdrücklich **keine WordPress-Importdatei**.
4. Gemeinsames ARCHIV `PFERDEATELIER-KISS-CODE-RUECKBAU-TESTPAKET-20261111.zip` SHA256 `d42473ddd24c42a8b1c8fb7634a5e7521d52e8ae199a32bd19bb68f6cfa11c37`. **Gesamtarchiv selbst ist KEIN WordPress-Plugin**; nur einzelne Originalstand-Plugin-ZIPs wären installierbar.

## Tatsächliche lokale Prüfungen
- 121 + 63 Plugin-Dateien korrekt in je unverändertem WordPress-Plugin-Verzeichnis; ZIP-CRC, Quell-Dateien bytes-equal nach Entpacken, **126/126 PHP-Dateien lint PASS**.
- Originale PSERC .60 `PSERC_Package_Integrity::validate` **61/61 PASS**.
- Ursprünglicher Drei-Artikel-V2-Metadatenblock durch Original `PSERC_Metadata_Boundary::validateBatch` **PASS**; manipulierte/unsignierte Varianten BLOCKED.
- Drei originale signierte PSTE-.32 `PRE_TYPE`-Profile via Original-Hash-Funktion des originalen `PSTE_Intent_Profile` bestätigt, original drei READY und jeweilige fünf Metadata-Felder stimmen. **Kein vorliegender BOUND_TYPE-K0-Owner-Handoff**.
- **Keine echte WordPress/MySQL-Ausführung, kein DataForSEO, kein K0-Lauf. Kein neuer QA-Fixcode.**

## ZWINGEND – Code-Rückbau ist nicht Datenbank-Rückbau
Ein älteres Plugin kann **nicht** die durch den .37-Lauf überschriebenen 5013 WordPress-Datenbank-Bewertungen zurückzaubern. Der aktuelle WP-TEST-Stand laut echten Flugschreibern ist `planning_ready=0`. Eine Rückkehr zu 3 READY erfordert **eine tatsächlich verfügbare, passende WordPress-Datenbanksicherung von vor dem schadhaften 11.11.-Lauf** (z. B. eine zuvor angelegte WPvivid-Sicherung auf der isolierten Testseite). Die aus dem 10.11. gesicherte PSERC JSON enthält nur Metadaten für 3 Artikel, **keinen WP-Datenbankabzug der 5013 Themen**. Keine Aussage, dass eine passende Sicherung vorliegt; keine Wiederherstellung oder Installation durchgeführt.

**Freigabegrenze:** `SOURCE_ROLLBACK_PACKAGE_LOCAL_PASS`, `LIVE_DATA_NOT_RESTORED`, `WP_TEST_NOT_RUN`, `NO_K0_GO`, `NO_AUTOMATION_RESTART`, `NO_NEW_PLUGIN_LOGIC`. **Nicht blind beide ZIPs installieren und Automatik drücken – das behebt keinen beschädigten Datenbankstand.**

Permanente Pluginbüro-Library: `/pferdeatelier/PLUGINS/QA/PFERDEATELIER-KISS-CODE-RUECKBAU-TESTPAKET-20261111.zip`, einzelne PSTE .32 / PSERC .60 und maschinenlesbares Prüfprotokoll.
