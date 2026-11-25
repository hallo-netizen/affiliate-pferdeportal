# 19.11.2026 – Nachprüfung KLICKWEG „Recherche-Einrichtung abschließen“ (Hobbydepot 0.4.24.3)

**Kein Neubau, KEINE weitere ZIP.** Grundlage ist die tatsächlich gespeicherte aktuelle `Texterstellung_Hobbydepot_0.4.24.3_RECHERCHE_EINRICHTUNG.zip`, SHA256 `e5674fb897cc9ca4d4594d7c8ca2a1621d92535a8651815535040005fecb78d4`.

## Anlass
Bei Hab & Bewahr war im Nachbarchat ein Syntaxfehler im **tatsächlich ausgegebenen** JavaScript eines gleichnamigen Buttons nachgewiesen; Klick erreichte WordPress nicht. Hobbydepot daher exakt an diesem kritischen Punkt unabhängig geprüft.

## Lokale Evidenz (Originalcode, keine Behauptung eines Live-Tests)
1. Original-PHP-Methode `TXE_Workshop::migrationUi()` in WordPress-Mocks **wirklich gerendert**. Danach den aus diesem HTML entnommenen JavaScript-Block mit Node `--check` validiert: PASS.
2. Echten gerenderten Button-Listener per Node-VM ausgelöst; AJAX-POST an `admin-ajax.php` mit `action=txe_safe_migration`, passender Nonce und `mode=start` abgesetzt: PASS.
3. Folgerequests mit `mode=step`, dem vom Server gelieferten `job_uuid`, Fortschrittsanzeige und Abschluss-Reload: PASS.
4. HTTP-409-Kategoriefehler und Netzwerkfehler sichtbar angezeigt, kein stilles Hängen: PASS.
5. Original-Servermethode `TXE_Workshop::ajaxSafeMigration()` mit WordPress-/PSTE-Testzuständen geprüft: bestehende Baseline-Migration, Fortsetzung, vorhandener Kontextjob und abschließendes `feature_enabled`-Flag korrekt: PASS.
6. Wrong job ID → `SAFE_MIGRATION_JOB_CHANGED` (409). Unzulässige Kategoriebasis → `PSTE_PORTAL_TAXONOMY_V3_INCOMPLETE` (409) **vor Migrationsstart**: PASS.
7. **Kopplungstest:** gerendertes Browser-JavaScript ruft die echte PHP-Servermethode sequenziell auf: 3 Requests bis `COMPLETE` (mit simulierten PSTE-Originaldiensten), negativer Kategoriefall direkt sichtbar: PASS.
8. WordPress-Hook `wp_ajax_txe_safe_migration` vorhanden, `check_ajax_referer` + Admin-/Bestätigungsgate im echten Code. ZIP 87 Einträge, korrekter WP-Ordner, SHA stimmt.

## Urteil
**Der konkret aus Hab bekannte Fehler ist in der vorhandenen Hobbydepot-ZIP 0.4.24.3 lokal nicht reproduzierbar.** Im Unterschied zu der zuvor ungenügenden Syntaxprüfung der *Vorlage* wurde nun der tatsächlich gerenderte PHP-HTML-JS-Ausgabepfad mitsamt Klick und echtem PHP-AJAX-Controller getestet. Für das Nachstellen der WordPress-Datenbank wurden lokale Mocks verwendet; daher ist ein Live-End-to-End-PASS ausdrücklich **nicht** bewiesen. Portal-/Kategorienvalidierung kann auf der echten WordPress-Site weiterhin korrekt stoppen.

**Installierbarer Stand bleibt 0.4.24.3 ohne weitere Änderung.** Bereits im zentralen Büro gespeichert und kontrolliert. Schriftlicher Nachweis: `/Hobby Depot/Plugin-Büro/Texterstellung_0.4.24.3_KLICKWEG_PRUEFBERICHT_20261119.md` und Fachbüro `PRUEFBERICHTE/HOBBYDEPOT_04243_KLICKWEG_BROWSERSIMULATION_20261119.md`.

## Bedienhinweis
Wenn 0.4.24.3 installiert ist, `Texterstellung → Recherche → Recherche-Einrichtung abschließen` einmal anklicken. Direkt darunter muss `Einrichtung gestartet …` erscheinen und danach Fortschritt oder eine **konkrete Fehlermeldung**. Bei tatsächlichem Nonresponse auf LIVE keine weiteren Klicks, kein blindes neues Plugin: vorhandene echte Browserkonsole/AJAX-Antwort prüfen. Keine kostenpflichtige Recherche und keine K0-Produktion starten.
