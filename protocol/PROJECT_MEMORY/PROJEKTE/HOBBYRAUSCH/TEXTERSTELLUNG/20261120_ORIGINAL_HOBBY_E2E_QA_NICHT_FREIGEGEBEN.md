# Hobbydepot Texterstellung – Originalworkflow-Prüfstand 20.11.2026
**Status: keine Produktivfreigabe, keine neue Plugin-ZIP.** Nutzer verlangt Beweis gegen Pferdeatelier, kein Neubau.

## Quellen und Livebefund
- Nutzer-Diagnose vom 20.11.2026, 08:21:11 UTC: Version 0.4.24.13, Originalrecherche RUNNING, Texterstellung 0 Aufträge, 0 K0-Ausgaben. DataForSEO production; Diagnose enthält keine 223 Originalkeyword-Zeilen. Alte Keywords nicht als gelöscht bezeichnen.
- Lokale Originalpakete: Hobbydepot-Texterstellung 0.4.24.13, Pferdeatelier-Texterstellung 0.4.34, vollständiger Pferdeatelier-PSTE 0.57.144.25. Alle ZIP-Integritätsprüfungen PASS.

## Harte Ursache und Reproduktion
- Original-Methode PSTE_Breadth_Research_Queue::backlogAuditLogicHash prüft 14 Originaldateien. In Hobbydepot UND eingebettetem Pferdeatelier fehlen `class-pste-family-structure-router.php` und `class-pste-product-choice-classifier.php`. Im separaten vollständigen Pferdeatelier-PSTE liegen beide vor.
- Original-PHP reproduziert exakt `PSTE_RETAINED_BACKLOG_AUDIT_LOGIC_FILE_MISSING:includes/class-pste-family-structure-router.php`. Nach nur einer Originaldatei meldet er die zweite. Mit beiden unveränderten Originaldateien in isolierter Kopie geht der echte Prüfschritt durch. Original-Plugin unverändert, keine Live-Daten verändert.
- 302/302 bestehende 0.4.24.13-Testprüfungen wirklich erneut ausgeführt und PASS; diese Suite enthält den fehlenden Original-Audit-Aufruf NICHT. Zusätzlich 63/63 gezielte Test-/Beweisgruppen PASS (exakte Reproduktion, Einzeldatei-Negativtest, Audit-Fingerprint-Drift, Original-PHP MINI→K0→WP-Mock, UI/Queue/Ajax, Syntax, Paketvergleich).
- Technische K0-Übergabe: originale Hobby-PHP-Methoden erzeugen `WP_K0_UPLOAD_PACKAGE_V1` für Beispiel `3D-Bogenschießen Regeln`; mit simuliertem Writer-Text ergibt Originalimport 1 WordPress-Testentwurf, gefälschte Kennungen werden blockiert. Das ist KEINE echte Hobby-K0-Autor-/LanguageTool-Abnahme.
- Original-Pferdeatelier: 2 vorhandene verifizierte K0-Artikel in lokalem Original-Importer als 2 Entwürfe, Wiederimport ohne Dubletten.
- Original GitHub Hobby-Discgolf-Akzeptanzlauf 44545937080 SUCCESS inklusive PPM 104/104 und LanguageTool 6.8; Original-Selbsttest 44545937102 SUCCESS. Fixture-Test, kein neuer Hobby-Writer-Lauf.
- **Weitere echte K0-Grenze:** `.github/workflows/k0-writer-accept.yml` im Branch `konzept0-portal-neutral-20261002` fragt Kategorie hart gegen `https://pferde-atelier.de/wp-json/wp/v2/categories?slug=...` ab, auch wenn WordPress-Herkunftsbeleg den Hobby-Host bereits eindeutig zuordnet. Vollständiger Hobby-Live-K0-Writersiegelsatz NICHT nachgewiesen.

## Verbindlich nächster Schritt
1. Die zwei Original-Quelldateien versionsgenau und kompatibel im vorhandenen Pluginpfad sicherstellen; vorrangig Originalaudit für echten gespeicherten Backlog abnehmen, keine neue kostenpflichtige Recherche.
2. Echte vorhandene 223 Stichwörter bis zum MINI-Abschluss kostenfrei nachprüfen und Originalquittung belegen.
3. Im Original-K0-Workflow die Portal-Kategorieabfrage anhand des bereits signierten Hostbelegs abnehmen, ohne zweite Entscheidung; echten Hobby-K0-Writer/81 Regeln/PPM/LanguageTool/WordPress-Output prüfen.
4. Erst danach eine gebündelte Installations-ZIP freigeben. Keine alten Tests als K0-Gesamtnachweis ausgeben.

Der detaillierte maschinenlesbare Prüfbericht und die K0-Techniksimulation wurden als Chat-Dateien ausgegeben: `hobbydepot_workflow_pruefbeweis_20261120.json`, `hobbydepot_k0_lokalsimulation_20261120.json`, plus das lokale Quellen-/Test-Belegpaket.
