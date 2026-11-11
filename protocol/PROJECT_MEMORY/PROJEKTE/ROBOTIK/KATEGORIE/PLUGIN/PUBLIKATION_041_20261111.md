# Robotik – Mini-Testdesign und Sammelveröffentlichung (11.11.2026)

**Bisheriger Nutzerschritt:** Der Betreiber meldete die Arbeiten mit Kategorie-Workflow 0.4.0 am 11.11.2026 als „erledigt“. Dies ist eine Nutzer-Rückmeldung, **kein technisch ausgewerteter WordPress-Live-Readback**. Die Website ist laut Betreiber gesperrt und alle importierten Robotik-Seiten dürfen veröffentlicht werden.

## Vorgeprüfter Ansatz
- **Kategorie-Workflow 0.4.1:** derselbe Pluginordner `robotik-kategorie-workflow`, nur Sammelveröffentlichung ergänzt; Erstimport 0.4.0 unverändert.
- Publikationsfreigabe erst bei tatsächlichem Erstimportstatus `COMPLETE` und `verified=193`; alle 104 mit `_robotik_kategorie_node_id` verknüpften Seiten, Slug, Titel, Eltern und Rolle müssen unverändert sein.
- Bei ausdrücklicher Sammelfreigabe wird in 12er-Paketen publiziert; keine Fremdseiten/Kategorien/Beiträge; Abschluss-Readback 104/104 `publish`; Wiederholung ohne Duplikate.
- **Robotik Strukturdesign 0.1.0:** eigenständiges minimales Designplugin gemäß der vorhandenen Regel (Design und Kategorien getrennt), liest echte WordPress-Seiten und zeigt sieben Hauptbereiche im Mega-Menü und als Footer-Kategorieübersicht. `Gewerbe > Industrie` grau abgesetzt. Schwarz/Weiß/Grau, keine Bilder, keine neue DB-Struktur.
- **Zusatzbereiche:** Magazin, Glossar, Roboterfinder und Anzeigenmarkt erhalten erst dann anklickbare Links, wenn reale WP-Seiten dafür existieren, sonst nur Beschriftung.

## Lokale echte Tests
- Originales 0.4.0-ZIP geöffnet; PHP-Klasse und Kennungsfeld `_robotik_kategorie_node_id` analysiert.
- 0.4.1-PHP: vollständige Syntaxprüfung bestanden; ZIP-CRC bestanden; isolierte WordPress-Mockprobe: 104 Seiten geändert und zurückgelesen, 104 beim zweiten Lauf unverändert, Fremdseite unangetastet, negative Testfälle blockiert.
- Design-PHP/JS/ZIP: Syntax- und Archivprüfung bestanden; Rendering mit tatsächlichem 104-Seiten-Profil: 7 Hauptmenüs, Industrie unter Gewerbe, 7 Footerbereiche, echte Produktseitenverweise, keine Fantasielinks.
- **Noch nicht nachgewiesen:** Plugin-Installation 0.4.1 auf WordPress, tatsächlicher Live-Publishstatus, Frontend-/Mobilansicht im echten Theme.

## Fertige Installationsdateien (Library)
- `/robotik/Konzeptbüro/ROBOTIK_KATEGORIE_WORKFLOW_0.4.1_PUBLIKATION_TEST.zip` – SHA256 `92cb4d5af534f1c7a981ea3ee23564b5f79ee3840c212ce4ccf946c2a71e35b1`
- `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.1.0_TEST.zip` – SHA256 `e6b2e864bd469a081ac2c5b6cc7b147458232fe5e3dfc5bfd88a3db4ed6b5112`
- `/robotik/Designbüro/ROBOTIK_TESTDESIGN_UND_PUBLIKATION_STAND_2026-11-11.md` – ausführliches Protokoll.

**Wichtig:** Die neuen ZIP-Bytes sind in der Library abgelegt; die historische GitHub-Datei `KATEGORIE/PLUGIN/CURRENT.zip` wurde **nicht** still überschrieben. GitHub-Releasedateien und echte WordPress-Installationsstände bleiben getrennt.

## Nächste zusammengefasste WordPress-Handlung
1. Bestehendes Robotik Kategorie-Workflow-Plugin auf 0.4.1 aktualisieren; unter **Robotik Kategorie → Veröffentlichung** prüfen und nur bei PASS gesammelt veröffentlichen.
2. Robotik Strukturdesign 0.1.0 installieren/aktivieren; Mega-Menü und Footer im Frontend prüfen.
3. Bei sichtbarer Abweichung nur ein Screenshot/Fehlerbild, keine langen manuellen Einzelschritte.
