# HAB & BEWAHR – GLOSSAR MANAGER TECHNIK / QUELLVERTRAG
**Fachquelle für Architektur:** Pferde-Atelier `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/TECHNIK_GLOSSAR_MANAGER_CURRENT.md`, getesteter Core 1.4.0/Design 1.50.528 (dort lokal PASS, dort WP-LIVE noch offen). Keines der Pferde-Plugins blind installieren; gemeinsame Engine ggf. durch Codeaudit adaptieren.

**Vorgabe:** wie PA ein bewusst manueller sicherer Import. max 25 per `HB_GLOSSARY_BATCH_V1`, stabile IDs, genau eine Welt, Related, Quelle, 150–200 Wörter, individuelles SEO, Aktualisierungsintervall 6/12/24. Zuerst Stage/Validator/Hash, WP `draft`, vollständiger Readback, sonst Rollback. Kein Auto-Publish, keine autonome Suche/Cron/Loopbacks.

**WordPress-Ziel:** bekannte `editorial:glossar`-Page ID 184 nur als historischer R3-Readback – bei Live-Änderung ID frisch auflösen. 0.1.7-Design-Route `/glossar/` ist kollisionsanfällig und nach Nutzerbefund leer. Künftiger Code muss einen Owner für öffentliche URLs herstellen, die bestehende Seite integrieren und `template_include`-Konflikte testen. Bis zum LIVE-Befund kein als installiert geltendes Plugin behaupten.

**Inhaltliche Grenzen:** keine Änderung am Kategoriebaum, keine Demo-/Vorproduktions-Inhalte indexieren, kein automatisches Verlinken jedes Begriffvorkommens, keine Fremdartikel anfassen. Assets nur auf Glossaransicht, keine REST-API, kein Frontend-Staging-Write.

**Implementierungsnachweis:** echte WordPress-DB-Simulation mit bestehender Page, Positiv-, Negativ- und Rollbacktest; Snapshot/Kanonische-URL-Test; nur bei PASSED neues Paket, noch kein LIVE-PASS ohne realen WordPress-Readback.

## GEBAUTER KANDIDAT 0.1.8 (14.10.2026)
Nicht die Pferde-Engine blind übertragen. Stattdessen fachlich analoger sicherer Manager als `includes/glossary-manager.php` im bereits bestehenden Hab-&-Bewahr-Designplugin gebaut; WP-Inhaltsobjekte bleiben unabhängig vom Plugin-ZIP. Staging/Doppelklick/Readback/Rollback für `HB_GLOSSARY_BATCH_V1` und 25er-Grenze, manuelle Fachfreigabe vor Publish, read-only „Prüfbedarf“, A–Z-Seite + Terminologie-Detailseite nach PPA-Reihenfolge. Kein zusätzliches Designplugin, keine WDB-Content-Daten im öffentlichen Assets-Ordner.
- ZIP SHA256 `c4b3f89eb1e3bebecc1c7ac3f78510f6f3c37ddae41b6adc87ad17dbbd253769`, `HAB_UND_BEWAHR_DESIGN_0.1.8_GLOSSAR_MANAGER.zip`.
- PHP-Lint und ZIP PASS; 17 Validatorchecks; 4 Adminimportpfade inkl. zwei echter Mock-Rollbacks; 20 Browseransichten lokal PASS. **ECHTER WP-LIVE-READBACK OFFEN**, kein Releasefreigabe-Märchen.
- Gewollter Status: 0 published terms. Vor Freigabe ist die Übersicht serverseitig noindex, ihre späteren URLs entstehen erst durch manuelles Veröffentlichen geprüfter WP-Drafts.


## TECHNIKERGÄNZUNG 0.1.17 – GET-PAGINATION UND LESBARE GLOSSAR-KURZANSICHTEN (15.10.2026)
Aus der echten Pferde-Atelier-Architektur **nur Fachvertrag** übernommen; kein Übertragen der Pferde-Atelier-Design-Assets/Termtexte. Je Begriff `term-*`-WDB-Vertrag, Related, Quellen, Suchintent, optional starke Hauptseite. Bis Volltext-Readback: `/glossar/<slug>/` technische read-only Ansicht ohne CPT-Writes, always **noindex**, kein Fake-Publish; native veröffentlichte Validatortermseiten bleiben bevorzugt kanonisch. A–Z serverseitig auf 9 Karten paginiert mit kombiniertem GET-Filter/Suche/Letter; kein Frontend-Loopback, kein Cron, kein JSON-Upload aus Benutzerbrowser. Unveränderte Max25-Draft-Batchlogik. ZIP und Prüfungen in DESIGN/CURRENT_STATE.md. WordPress-Live-Gate OFFEN.
