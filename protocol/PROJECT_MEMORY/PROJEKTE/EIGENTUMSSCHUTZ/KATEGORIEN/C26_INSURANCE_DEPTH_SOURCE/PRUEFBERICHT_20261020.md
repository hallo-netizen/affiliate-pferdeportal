# C2.6 – fehlende Versicherungs-Beitragskategorien einzeln ergänzt (2026-10-20)

**Aktueller technischer Kandidat, nicht live importiert:** Vollständiges Update des einzigen bisherigen Kategorie-Plugins **1.14.8.37**, Dateiname `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.37_VERSICHERUNGEN_VERTIEFT.zip` (368911 Bytes, SHA256 `f2f66abfd34956ce8d28d6cf4ced56879045ec20eed38dd5e5076a991d4c805a`). Lokal im aktuellen Chat erstellt, vollständiges ZIP 49 Dateien (36 PHP), ZIP-CRC PASS, alle PHP-Lint PASS.

## Fachliche Arbeit – 46/46 tatsächlich einzeln
- Basis ist **exakt** das WordPress-Kategorieplugin 1.14.8.36 mit 1 R1/5 R2/**46 konkreten Versicherungs-Keyword-R3** und **138 bereits bestehenden** WP-`category`-Endkategorien (Häufige Fragen, Beratung und je eine Fachfacette).
- Der zusätzliche Umfang wurde **für jeden der 46 Owner einzeln** in `profiles/hab-und-bewahr-insurance-c26-end-categories.json` konkret benannt und begründet (je 3 grobe Unterscheidungsrichtungen, **keine einzelnen Artikel/Überschriften**).
- **185 zusätzliche eigenständige Endkategorien**, individuell 3–6 Ergänzungen je Thema, danach **323 flache WP-Beitragskategorien** unter weiterhin genau **46 konkreten R3-Seiten**, also zwischen 6–9 Endkategorien pro Versicherungsart. **0 neue Seiten und 0 neue Hierarchieebenen.** Keine bestehenden Kategorien umbenannt oder verschoben; kein zwanghaftes 3er-Facetten-Schema.
- Beispiele: `Hausratversicherung → Versicherungssumme & Unterversicherung / Beiträge & Selbstbeteiligung / Leistungsumfang & Ausschlüsse / Schadensmeldung & Erstattung / Hausratversicherung vergleichen`; `Berufsunfähigkeitsversicherung → Gesundheitsprüfung & Antrag / BU-Rente & Leistungsdauer / Beiträge & Berufsgruppen / Berufsunfähigkeitsversicherung vergleichen / BU für Schüler & Selbstständige`; `Betriebsunterbrechungsversicherung → Ertragsausfall & Fixkosten / Haftzeit & Versicherungssumme / Betriebsunterbrechungsversicherung vergleichen`.
- Die 105 Versicherungsarten bleiben dem fachlichen 1.14.8.36-SEO-Profil zugeordnet. **45/46 R3-Versicherungsbegriffe** wurden zuvor exakt in zwei echten DataForSEO-Keyword-Overview-Exports gefunden; eine Abfrage ohne Provider-Zeile nicht automatisch streichen. **Subkategorie-Kombinationen selbst wurden NICHT durch zusätzliche DataForSEO-Abfragen gemessen.** Sie sind suchabsichts- und fachlich plausible Kategorien, keine behaupteten gemessenen Suchvolumen, keine zusätzlichen Providerkosten.

## Technische ADD-only-Implementierung in originalem Plugin
- **45 der 46 bisherigen Archivdateien sind byteidentisch** zur lokalen Version 1.14.8.36; nur Bootstrap-Versionsnummer und Einbindung geändert, dazu eine kleine neue PHP-Workerklasse, das JSON-Profil und eine Release-Info (kein neues Plugin).
- Quelle: `includes/class-apkw-insurance-c26-depth.php`; Original `APKW_TargetWriter` unverändert. Der bereits importierte C2.5-SEO-Baum **muss COMPLETE** sein und 46 Original-R3 sowie 138 ursprüngliche Endkategorien im aktiven Snapshot belegen.
- Eigenes Adminmenü: **Portal-Kategorien → Versicherungen vertiefen**. Dort schreibfreie Vorschau mit eindeutiger Zustimmung, danach 15 Endkategorien je Batch, gesicherte ID vor Metaschreiben, Original-WP-Metabindung, physischer Readback, Stage/Live-Readback und kontrollierter Rückbau **nur der jetzt neu angelegten, unbenutzten Kategorie-Terms**.
- Nie die sechs bestehenden Hauptwelten, ihre WP-Seiten, die 46 Versicherungsthemenseiten, 138 Altterm-IDs oder bestehende Artikel umbenennen, neu importieren oder löschen. Bei geänderter Originalrevision, fremdem Term, falschem Owner oder C2.5≠COMPLETE: FAIL-CLOSED.

## Reproduzierbare lokale Originalwriter-Tests
Test `tests/test_c26_with_original_writer.php` bindet **originale unmodifizierte** `includes/class-apkw-target-writer.php` aus der 1.14.8.36-Basis ein und simuliert die tatsächlichen 46 R3 + 138 Terme. PASS:
1. Nullschreib-Preflight: 185 zusätzliche Terms, 0 Seiten.
2. Vollständige 185/185-Neuanlage, 323 Gesamtbegriffe, 46 R3-Seiten unverändert, originaler 138er Bestand und alle sechs Hauptwelten identisch.
3. Readback-Stage/aktiv im kontrollierten Mock und Cache-Invalidierung.
4. Erzwungener Fehler beim 37. Term und erzwungene Stage-Readback-Verweigerung → Rückbau aller nur neu erstellten Terms; 138er Basis und Snapshot identisch erhalten.
5. Negativfälle C2.5 unvollständig, fehlende echte R3-WP-ID-Bindung, fremder Terms-Slug, fremde Revisions-ID, erneuter Importstart → jeweils BLOCKIERT.

**Grenze:** Der simulierte Frontend-Readback ist ein Mock; der echte `APKW_FinalTargetAdmin::frontend_readback` und realer WP-Core-/DB-/Frontend-Test stehen weiterhin aus. Also nicht behaupten, Live-Import oder echte DataForSEO-Prüfung der 185 Subkategorien sei bestanden.

**EINE NEXT ACTION:** Das komplette vorhandene Kategorieplugin auf 1.14.8.37 aktualisieren, **Portal-Kategorien → Versicherungen vertiefen** öffnen und dessen schreibfreien Preflight ablesen. Erst bei PASS getrennte ausdrückliche Freigabe zum ADD-only-Import. Separates Designplugin-Menüproblem (7. Welt umgebrochen) bleibt unberührt.
