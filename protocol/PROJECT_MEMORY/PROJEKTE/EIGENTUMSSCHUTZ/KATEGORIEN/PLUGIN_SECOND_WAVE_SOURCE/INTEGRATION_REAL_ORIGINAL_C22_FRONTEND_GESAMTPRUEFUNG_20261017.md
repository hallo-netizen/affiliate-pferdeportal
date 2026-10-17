# 1.14.8.31 – Zusatz-Integrationstests am Originalcode, 17.10.2026

**Prüfergebnis: lokal bestanden; keine Live-Installation und keine Änderung an WordPress.** Ausgangspunkt: identisches geprüftes vollständiges Plugin-ZIP 1.14.8.31, SHA-256 `6cd47955df14a65d681c7508e1674be94e98cad4dd68df5a6605ce8ef534d933`.

## Original-C2.2-Abschlussprüfung – Integration statt bloßem isoliertem Stub
Der echte PHP-Code der Klasse `APKW_C22_AddOnly` (inklusive unveränderter `jobs()`, `completion_audit()` und Originalprofil `profiles/hab-und-bewahr-c22-plan.json`) wurde mit dem neuen echten `APKW_C22_472_AddOnly` in einer gemeinsamen lokalen WordPress-Mock-Laufzeit ausgeführt. Die Baseline bildet explizit 93 alte Seite-3-Knoten, 285 alte Kategorien, alle 743 Originaljobs und die originalen Parent-/Term-IDs ab. Die alten WordPress-Objekte sind dabei unverändert geblieben.

- Vor der neuen Welle: tatsächliches `APKW_C22_AddOnly::completion_audit()` = **PASS**, 743/743.
- 472er-Welle: tatsächliches `APKW_C22_472_AddOnly::dry_run()` = **PASS**, genau 0 Writes.
- 472er vollständiger Lauf mit kontrollierter originaler `APKW_TargetWriter`-Schnittstelle: **472/472**, 172 Themen, 0 neue WordPress-Seiten.
- Abschluss: **Beide echten Completion-Audits gleichzeitig PASS**; alter 743er-Stand und 93+285 historische Datensätze bleiben sichtbar und geschützt.
- Crash zwischen `SNAP` und `REV`: Erneuter Rollback verarbeitet exakt die 472 vom neuen Durchlauf angelegten Terms und stellt den alten Snapshot vollständig wieder her. **PASS**.
- Test mit dem **echten Frontend-Renderer** `APKW_FrontendStructure::render_page_structure()`: Alle 172 konkreten Thema-Seiten durchlaufen; auf ihnen werden **472/472 neue Kategorien** als richtige Links dargestellt. Keine weitere Seite- oder Kategorieebene angelegt. **PASS**.

## WordPress-Termnamen – strenge globale Namenskollision
Anders als bei logisch getrennten Themen kann eine native, flache WordPress-`category`-Taxonomie für gleiche Namen unter `parent=0` einen harten Konflikt verursachen. Daher wurden die tatsächlichen Anzeigenamen unabhängig von den SHA-basierten Slugs abgeglichen:
- 472 neue Term-Namen: **472 global eindeutige Namen**, 0 Wiederholungen.
- Gegen die 566 ursprünglichen C2.2-Kategorien: **0 identische Namen**.
- Gegen die dokumentierten 285 geschützten Altkategorien: **0 identische Namen**.
- Daher **keine nachgewiesene globale Namenskollision in diesem geprüften Stand**. Slugs sind zusätzlich unterschiedlich und Parent ist immer 0.

## Sonstige produktionsnahe Prüfungen
- Vollständiges ZIP kann erfolgreich entpackt werden: **38 Dateien**, darunter **32 PHP-Dateien**, ZIP CRC **PASS**.
- `php -l` für **alle 32 PHP-Dateien**: **PASS**.
- Vorheriger Negativtest: absichtlicher Fehler nach 30 Anlagen → alle 30 eigenen Terms entfernt, alte Struktur unberührt.
- Eltern-WordPress-Zuordnung fehlt vor dem Start → **kein WordPress-Write**.
- Echtes WordPress auf Server **nicht** angesprochen. Auch PHP-Testfixtures sind kein Ersatz für einen echten WP-Live-Test.

## Auslieferung
Plugin **1.14.8.31** liegt in GitHub unter `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.31.zip.b64`, rekonstruiert mittels `decode_release.py` mit SHA-256-Prüfung. Quellcode, Manifest, Originalplugin-Patch und Tests sind ebenfalls in diesem Unterbüro gespeichert. Die bereits importierten **743** C2.2-Objekte dürfen **NICHT** neu importiert werden.

**Technische NEXT ACTION:** Das vollständige bestehende Plugin auf 1.14.8.31 aktualisieren; im bereits vorhandenen Adminmenü die eigene 472er-Trockenprüfung (0 Writes) durchführen und erst danach den separaten 472er-Import ausdrücklich freigeben. Kein neues Plugin, kein WordPress-Neuexport, keine Artikel.
