# HAB & BEWAHR – GLOSSAR MANAGER TECHNIK / QUELLVERTRAG
**Fachquelle für Architektur:** Pferde-Atelier `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/TECHNIK_GLOSSAR_MANAGER_CURRENT.md`, getesteter Core 1.4.0/Design 1.50.528 (dort lokal PASS, dort WP-LIVE noch offen). Keines der Pferde-Plugins blind installieren; gemeinsame Engine ggf. durch Codeaudit adaptieren.

**Vorgabe:** wie PA ein bewusst manueller sicherer Import. max 25 per `HB_GLOSSARY_BATCH_V1`, stabile IDs, genau eine Welt, Related, Quelle, 150–200 Wörter, individuelles SEO, Aktualisierungsintervall 6/12/24. Zuerst Stage/Validator/Hash, WP `draft`, vollständiger Readback, sonst Rollback. Kein Auto-Publish, keine autonome Suche/Cron/Loopbacks.

**WordPress-Ziel:** bekannte `editorial:glossar`-Page ID 184 nur als historischer R3-Readback – bei Live-Änderung ID frisch auflösen. 0.1.7-Design-Route `/glossar/` ist kollisionsanfällig und nach Nutzerbefund leer. Künftiger Code muss einen Owner für öffentliche URLs herstellen, die bestehende Seite integrieren und `template_include`-Konflikte testen. Bis zum LIVE-Befund kein als installiert geltendes Plugin behaupten.

**Inhaltliche Grenzen:** keine Änderung am Kategoriebaum, keine Demo-/Vorproduktions-Inhalte indexieren, kein automatisches Verlinken jedes Begriffvorkommens, keine Fremdartikel anfassen. Assets nur auf Glossaransicht, keine REST-API, kein Frontend-Staging-Write.

**Implementierungsnachweis:** echte WordPress-DB-Simulation mit bestehender Page, Positiv-, Negativ- und Rollbacktest; Snapshot/Kanonische-URL-Test; nur bei PASSED neues Paket, noch kein LIVE-PASS ohne realen WordPress-Readback.
