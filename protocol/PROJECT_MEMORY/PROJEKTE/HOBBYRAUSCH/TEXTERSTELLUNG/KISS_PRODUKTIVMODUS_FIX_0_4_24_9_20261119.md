# 19.11.2026 – Hobbydepot Texterstellung KISS: DataForSEO immer Production, kein Modus-Wahlkasten (0.4.24.9)

**Nutzerentscheidung:** Immer Produktivmodus für neue Hobbydepot-Recherchen. Keine Moduswahl, kein zusätzlicher Bestätigungsschritt, keine Architekturänderung. Vorhandener Kostenhaken **beim bezahlten Recherchestart** unverändert.

## Vergleich mit Pferdeatelier und Ursache
- Das Pferdeatelier-Original (verifizierte Blanko-Kopie 0.4.31.1) enthielt ebenso wie Hobbydepot 0.4.24.8 die **alte Default-Einstellung `environment=sandbox`** in `PSTE_Plugin::defaults()`. Welchen Wert das Pferdeatelier live gespeichert hat, ist ohne dessen Diagnose nicht bewiesen. Es ist falsch, aus der bloßen Existenz von Originalcode zu behaupten, andere Portale würden immer production verwenden.
- Die Übernahme der Original-Sandbox-Voreinstellung und später die unnötig hinzugefügte Sandbox/Production-Auswahl waren nicht im Sinne des KISS-Zielvertrags. Für Hobbydepot wird der Modus künftig nicht mehr vom Betreiber entschieden.
- Der Nutzer hat die DataForSEO-Zugangsdaten schon gespeichert; nicht erneut erfragen.

## Minimalfix – ein Owner, zwei bereits vorhandene Dateien
**Aktuelle einzige installierbare ZIP** `Texterstellung_Hobbydepot_0.4.24.9_FEST_PRODUKTIVMODUS.zip`, SHA256 `b5894c2f2942a117a6c53a2452922a508cb24f44b38f210a39c5583d761bf500`, 507896 Bytes, root `texterstellung-hobbydepot/`, WordPress-Plugin-Header `0.4.24.9`.
1. `original/pste/includes/class-pste-plugin.php`: **die ursprüngliche zentrale PSTE-Settings-Funktion** `defaults` setzt production; `migrateSettings` erzwingt denselben Wert für **jede neue Recherche**, auch wenn bisher ein alter Sandbox-Wert in `pste_settings_v1` steht. Andere Einstellungen incl. bestehender DataForSEO-Kosten- und Budgetgrenzen bleiben erhalten. Der getroffene Wert wird nicht ein zweites Mal im Workshop entschieden.
2. `texterstellung.php`: nur neue Version, störende UI-Modusauswahl/Bestätigungs-POST entfernt, stattdessen reiner Hinweis `Echtdaten (Production) – api.dataforseo.com`. Die vorhandene kostenpflichtige Recherchestart-Bestätigung `cost_ack` bleibt. Zuvor hinzugefügter Modus-POST-/Handlerpfad entfernt.
**85/87 Datei-Inhalte byteidentisch, keine neuen Dateien/Plugins/Module**. Keine K0-/K-Multi-/PSERC-/MINI-/Kategorie-/Artikel-Funktion verändert. Alter 3D-Bogenschießen-Job bleibt mit ursprünglicher im Archiv gespeicherter Sandbox-Quelle unverändert; nicht automatisch nochmals recherchieren.
**Technischer Unterschied:** Beim lesenden Aufruf wird der bestehende gespeicherte Sandbox-Wert nicht umgeschrieben; der zentrale Original-Leser liefert für alle **neuen** Aufträge dennoch fest production. Erst eine künftig vorhandene Settings-Migrationsphase persistiert den Wert. So entstehen keine Datenbankwrites beim Backendaufruf.

## Echte lokale Testnachweise (keine Live-Behauptung)
- **20/20 Original-PHP-WordPress-Stubchecks**: Default, alter Sandbox-Wert, gespeicherter Production-Wert, ungültiger Wert, leerer Wert → stets Production; übrige Einstellungen unverändert; UI wirklich gerendert ohne Moduswahl; keine GET-Speicherwrites; Kostenbestätigung vorhanden; alter Job unverändert; kein alter Modus-Handler.
- **38/38 Original-PAA-ID-/Provider-Status-Tests** und **31/31 Original-Archiv-/Fortsetzungs-Tests** aus 0.4.24.8 tatsächlich erneut gegen die aktuelle Quellstruktur ausgeführt. **Insgesamt 89/89** gezielte PASS.
- **78/78 PHP-Syntax**, **8/8 JSON gültig**, **87/87 ZIP-CRC**. Keine echten WordPress-/DataForSEO-Live-Anfragen ausgeführt, keine Kosten erzeugt. Echte Produktion erst nach Installation und ausdrücklich bestätigtem Test-Recherchestart (nicht automatisch).
- Der historische Jobabschluss mit neun ungeeigneten Pizza-/Phone-/SEO-Begriffen ist keine fachlich gültige Recherche; keine stillschweigende Neubewertung.

## Ablage und Nutzerweg
- In echtem zentralem Büro `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.9_FEST_PRODUKTIVMODUS.zip` und Fachbüro `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/` gespeichert; `Texterstellung-CURRENT.md` in beiden Büros aktualisiert. Prüfbericht in beiden Büros. Vorgänger 0.4.24.8 bleibt archiviert.
- **Jetzt:** WPvivid-Backup → ZIP 0.4.24.9 in WordPress per **Ersetzen** hochladen → `Texterstellung → Recherche`, dort sofort `Echtdaten (Production)` ohne Auswahl. Noch keine neue große Kategorienrecherche; vor Kosten darf Nutzer einmalig einen neuen Pilotauftrag starten und bestehenden Kostenhaken bestätigen.
