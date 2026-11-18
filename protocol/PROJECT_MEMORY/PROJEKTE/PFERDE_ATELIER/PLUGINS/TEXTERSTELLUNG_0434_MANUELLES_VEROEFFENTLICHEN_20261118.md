# Pferdeatelier – Texterstellung 0.4.34: Manuelles Veröffentlichen wieder möglich

**Datum:** 18.11.2026. **Version:** 0.4.33 → 0.4.34.
**Plugin-Büro (gespeicherte installierbare ZIP):** `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.34-MANUELLES-VEROEFFENTLICHEN.zip`.
**SHA-256:** `14a3976702fa782e110184c3abc8eba82a0225f28384b4d540488c96f65dfb6b`.

## Belegter Fehler
Die WordPress-Diagnose vom 18.11.2026, 16:35:46 UTC zeigt, dass die importierten Artikel **974725** (Lebermoos), **974726** (Pfriemenschwanz) und **974735** (Weidehaltung) erfolgreich als Entwürfe gespeichert wurden: `WP_INSERT_RETURNED_ID`, `held=0`. Eine Sperre in der installierten Texterstellung 0.4.33 (`TXE_Workshop::preventPilotPublish` plus eine `wp_insert_post_data`-Closure) verhinderte auch die bewusste manuelle Veröffentlichung. **Es lag kein Schreib-/Importfehler vor.**

## KISS-Fix in 0.4.34
- K0- und MINI-Rückimporte bleiben **draft-only**; keine automatische Veröffentlichung.
- Ein bereits gespeicherter Entwurf darf **nur auf ausdrücklichen, berechtigten WordPress-Editor-Publish-/Schedule-Wunsch** veröffentlicht werden.
- Bereits veröffentlichte Beiträge dürfen beim Bearbeiten nicht wieder in Entwürfe umgewandelt werden.
- Kein K0-/MINI-/SEO-Workflow- oder Architekturumbau, keine neue Prüfstation, kein Neuimport nötig.

## Archiv- und Testnachweis
- Exaktes ZIP im oben genannten **Pferdeatelier-Büro** abgelegt (Library-Upload bestätigt).
- ZIP selbst geöffnet und fehlerfrei geprüft: **89 Einträge**, WordPress-Header `Version: 0.4.34`.
- Verglichen mit der archivierten Version 0.4.33: **87/89 Dateien byteidentisch**, nur `texterstellung/texterstellung.php` und `texterstellung/README-TESTINSTALLATION.txt` verändert.
- Vorheriger Releasebericht: **79 PHP-Syntaxprüfungen, 12 Funktionstests erfolgreich**; diese Tests wurden bei dieser Protokollierung nicht erneut ausgeführt.
- Nutzer meldete nach Bereitstellung **„pass“**. Ein unabhängiger Live-Nachweis des Poststatus nach dem manuellen Veröffentlichen liegt nicht vor; daher **kein erfundener Live-PASS**.

**Folgeaktion:** Keine weitere Datei/Plugin-Version nötig. Bereits vorhandene K0-Artikel in WordPress manuell unter **Beiträge → Entwürfe** veröffentlichen; nicht erneut importieren. Dieses ZIP mit Hash als archivierten Versionsstand verwenden.
