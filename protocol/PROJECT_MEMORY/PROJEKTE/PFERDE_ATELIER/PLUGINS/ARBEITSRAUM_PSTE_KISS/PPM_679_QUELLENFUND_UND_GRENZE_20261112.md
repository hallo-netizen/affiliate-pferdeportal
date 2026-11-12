> **KORREKTUR ZUR ORIGINALQUELLEN-VERFUEGBARKEIT:** **Die verbindlich festgelegten Original-Plugins PSTE 0.57.144.45 und PSERC 0.28.69 sind im Pferdeatelier-Pluginbüro des Campus vollständig vorhanden und wurden tatsächlich geöffnet und SHA-geprüft.** Die nachfolgenden Angaben über schwer auslesbare **PPM-6.7.9-Binärdateien** dürfen **nicht** auf diese vorhandenen Original-Plugins übertragen werden. [Prüfnachweis und Pfad](CAMPUS_AUSGANGSPLUGINS_TATSAECHLICH_GELESEN_20261112.md).

# PPM 6.7.9 – historisches Originalpaket gefunden; Vor-MINI-Reservierung noch nicht beweisbar

Stand 12.11.2026; **keine Pluginänderung, keine neue KISTE, kein neuer Worker, keine neuen Schreibwege.**

## Reale Quellen
- Einziger aktueller PSTE/PSERC-Arbeitsstand im Projekt: `AKTUELLER_ARBEITSSTAND_TESTIDENTISCH_NICHT_INSTALLIEREN.zip`, **1.831.122 Bytes**, lokale SHA-256-Nachrechnung **8fc55bca1fc7e4fe019203b2c56d169a734f0c3c941b08606fa9bed6b9183e33**. Unverändert.
- Auf dem bereits bestehenden GitHub-Zweig **`temp/dev-export-existing-ppm679-20260926`** liegt das historische PPM-Originalpaket unter `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`; GitHub-Dateimetadaten belegen Git-Blob `151e9d6f908453dfc5b4acb497c4927a3f03c940`. **Der Inhalt wird über den gegenwärtigen GitHub-Dateizugriff leer geliefert; ein Versuch über die Blob-Schnittstelle brach mit UTF-8-Dekodierfehler ab. Keine Bytes und keine verifizierte Prüfsumme des aktuellen Pakets erhältlich.**
- Das auf derselben GitHub-Branch ausgelesene **echte Textskript** `control/startmaster0107/fachworkflow_proof_handoff.py` nennt die historische Paketdatei, `PPM679_VERSION = "6.7.9"`, und historische erwartete Paket-SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`. **Diese ist aus dem Skript zitiert, nicht unabhängig an den ZIP-Bytes nachgerechnet.**
- Gleiches Skript benutzt `PPM679_Editorial_Plan_Registry::plan()`, die originale PPM-Planverwaltung. Das heutige PSERC-Modul liest auch `ppm679_editorial_plan_runtime_state_v1` und importiert nach WordPress via `PPM679_Editorial_Plan_Runtime_Gate::record_readback`.
- Die GitHub-PRs #122 und #124 wurden auf ihre geänderten Dateilisten geprüft. Darin liegt **kein PPM-Quellcode**, nur die Anbindung. Die zugehörigen historischen GitHub-Workflow-Läufe (33859560025, 33868392108) haben aktuell **keine abrufbaren Artefakte**. Die beiden vorhandenen PSTE-/PSERC-Original-ZIPs enthalten **keine Definition** der PPM-Runtime-Gate-Klasse.

## Verbindlicher Soll-/Ist-Beschluss
Der Benutzer verlangt **einmalige** endgültige Themenentscheidung → **sofortige und dauerhafte Reservierung vor MINI** → MINI nur Titel → PSERC ohne Zweitprüfung → K0 → WordPress-Import und Planaktualisierung. Das ist unverändert der Zielvertrag.

**Technische Konsequenz:** Vor einer echten Änderung, die Reservierungen direkt im bestehenden PPM-Laufzeitbesitzer verbucht, muss deren tatsächlicher aktueller Programmcode/Schreibvertrag bekannt sein. Ein zweiter Speicher oder ungeprüftes `update_option` auf PPM-Daten wäre ein riskanter Zusatzweg und widerspräche KISS. Die echte PPM-Version in der heutigen WordPress-Installation ist aus diesem historischen Repo-Fund **nicht nachgewiesen**.

**Fortschritt:** Historische Paketquelle samt Prüfsumme und früheren Abläufen exakt lokalisiert. **Blockade:** lesbarer aktueller PPM-Originalquellcode und echte WP-Testumgebung weiterhin nicht vorhanden. Kein neuer Installer, kein Umbau auf Verdacht, keine erdachte E2E-Abnahme. Für die restliche PSTE-/PSERC-Vereinfachung gilt das vorhandene vollständige Soll-/Istprotokoll; keine zusätzliche Prüfung beim nachfolgenden Worker.
