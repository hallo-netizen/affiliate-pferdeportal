# Echte WordPress-Test-Ausgabedatei → K0: Metadaten-Handoff PASS (10.11.2026)

## Quellen und Schutz
Vom Betreiber **direkt aus der tatsächlichen WordPress-Testseite** hochgeladene Datei `seo-redaktionsplan-produktionshandoff-42619ca7b6e36a625e0c8ae4e562534a9ff1b115ac7772f598435a064d06f546.json`, **1.393 Bytes**, Dateibyte-SHA256 `d943ebe3ab65ca53de04b54aca02321c1b2052b3e30e40ab6ff4d5a4cc9b22c9`. Die konkrete personenbezogene/redaktionelle Quelldatei **nicht** auf GitHub hochgeladen. Lokal als Original unverändert gelesen, nicht bearbeitet, keine Artikelproduktion angestoßen.

## Gegen den tatsächlichen Originalcode geprüft
- Original-PHP aus **PSERC 0.28.60**, unveränderte `PSERC_Metadata_Boundary::validateBatch` und `requireReadyBatchForExport`, gemeinsam mit Original-`PSERC_Stable_Json` direkt lokal unter PHP 8.4 ausgeführt: **`PSERC_METADATA_BOUNDARY_PASS`**; der Download ist wirklich exportfähig.
- **3 Positionen**; `contract=PSERC_TEXTMACHINE_METADATA_BATCH_V2`; `status=READY_FOR_TEXTMACHINE_METADATA_INTAKE`; `publish_allowed=false`; `content_or_format_payload_present=false`.
- Je Thema **genau fünf** nichtleere Textfelder `article_type, category, plan_slot, target_keyword, title`; keine zusätzlichen Inhalts- oder Formatfelder; **3 verschiedene** gebundene 64-stellige Plan-Slots; keine doppelten Titel.
- Im originalen **aktiven K0-Branch** `konzept0-portal-neutral-20261002` unter `engine/k0_portal_resolver.py::validate_intake` sind exakt dieselben fünf Felder und der stabile Hash-Eingangsvertrag vorgesehen; die **unveränderte K0-Quellformel** `sha256(json.dumps(core,ensure_ascii=False,sort_keys=True,separators=(',',':')))` wurde anhand der Originaldatei berechnet und ergab exakt `42619ca7b6e36a625e0c8ae4e562534a9ff1b115ac7772f598435a064d06f546`, **identisch** mit `batch_sha256`.
- Die gewählte Zielkategorie `pferdedecken-regendecken-beratung` ist im **von K0 referenzierten** `affiliate-release-current:CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv` wirklich vorhanden, **term_id=10**. Kein bloß erratener Slug.
- Direkte **Negativprobe mit Original-PHP**: nach Titelmanipulation `PSERC_METADATA_BATCH_HASH_MISMATCH`; bei doppeltem Artikelplatz `PSERC_DUPLICATE_PLAN_SLOT`.

## Abnahmeentscheidung
**PASS für die echte bestehende Dateiübergabe `WordPress-TEST → PSERC → K0-METADATEN-EINGANG`.** Die letzte zuvor fehlende echte Exportdatei ist eingetroffen und hat die Originalquelle-/Form-/Hash-/Kategorieregister-Prüfung bestanden. **Kein neuer Dateiexporter erforderlich.**

**NICHT behaupten:** K0 hat damit bereits drei Artikel recherchiert/geschrieben, eine WordPress-Artikeldatei erzeugt oder die komplette K0-Produktionskette erfolgreich durchlaufen. Das war ausdrücklich zurückgestellt. Die nachgelagerten K0-Regeln zu Artikel-ID, Recherchen, Writer, LanguageTool und finaler WordPress-Ausgabe wurden hier **nicht ausgeführt**.

## KISS-Nächster Schritt
- Bestehende K0-Metadatenausgabe als stabilen Normalweg beibehalten.
- Backend-Technik **auf isolierter Kopie** verschlanken; zuerst nur doppelte UI-/Workflow-Auslöser, verwaiste Funktionen und widersprüchliche Gate-Altwege nach Referenzbeweis. Alle gespeicherten WP-Daten, Recherchen, bestehenden Legacy-Funktionen, K0 und Schutzprüfungen erhalten.
- Nach jedem verlustfreien Abbau denselben Original-Dokumententest und ein kontrolliertes Test-WP-Readback verwenden. Keine neuen Datenbanken/Worker/Architektur.
