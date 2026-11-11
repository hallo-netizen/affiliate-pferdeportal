# Pferdeatelier KISS – Checkpoint B / Stand 11.11.2026

**Nur Teststand; keine Freigabe für Live-WordPress.** Ersetzt nicht den Zielvertrag, verändert weder die Fachregeln noch K0/PSERC.

## Ausgangspunkt / nachgewiesener Fehler
- Vorherige, tatsächlich installierte PSTE 0.57.144.40 / PSERC 0.28.67.
- `PSTE_Admin::productionAutoStepAjax`: Start verlangt einen historischen, vollständigen Bestand-Audit. Obwohl PSERC `PSERC_Plan_Compile_Job::start/advance` bereits die aktuellen Plan- und Quellenprüfungen besitzt, wird ein neuer freigegebener Einzelauftrag bei fehlendem Alt-Audit blockiert.
- `PSTE_Admin::productionAutoState`: dieselbe Alt-Audit-Sperre vor READY-Anzeige.
- **Zusätzlich im Quellenabgleich aufgedeckt:** `PSTE_Admin::exportPlanningTopics` hatte dieselbe Alt-Audit-Sperre unmittelbar vor dem echten Metadatenexport. Nur Start und Anzeige zu korrigieren hätte den Download weiterhin blockiert.
- `PSTE_Research_Driver::executeOneStep/maybeKickExisting` stoppt wegen **jeder** gespeicherten `existing_only`-Queue, selbst wenn sie `COMPLETE` oder `CANCELLED` ist; dadurch können gültige neue Einzeljobs nicht laufen und nach Serverunterbrechungen nicht wieder anlaufen.
- Die ursprüngliche negative .37-Falschvalidierung (4 vs. 5 Intent-Felder) ist bereits in PSTE .40 nicht mehr vorhanden. Keine neue semantische Regelkorrektur.

## Umgesetzte minimale Korrektur (lokale Quelle, **nicht** auf WP installiert)
- Testversion **PSTE 0.57.144.41**, direkt auf dem installierten .40-Code aufbauend; **nur drei Dateien** geändert: `includes/class-pste-admin.php`, `includes/class-pste-research-driver.php`, `portal-seo-topic-engine.php` (Versionsnummer).
- Keine neue Klasse, Tabelle, Option, Arbeitsstrecke, Artikelregel oder Doppelentscheidung. **PSERC 0.28.67 und K0 vollständig unverändert**.
- Entfernt **nur** die historische Komplett-Audit-Voraussetzung am Automatikstart, in der READY-Anzeige und beim Export. Stattdessen verbleiben die vorhandenen **PSERC-Freigabe-, aktuellen Quellen- und 5-Felder-Export-Prüfungen**.
- Der alte `existing_only`-Job wird **nie automatisch wieder aufgenommen**. Bei `RUNNING/PAUSED_ERROR/OUTCOME_UNKNOWN` weiterhin gesperrt; `COMPLETE/CANCELLED` gilt dagegen als historischer Datensatz und blockiert keine neuen Einzeljobs/keinen neuen Compiler.
- Preflight bekommt bei alten `existing_only`-Queues ausdrücklich `null`, um die frühere Rebind-/Kick-Stelle nicht unbeabsichtigt erneut anzusteuern.
- Ein aktiver 0-READY-Plan wird nicht als READY übergeben. PSERC .67 blockiert bereits 0 Quellen und 0 READY vor Aktivierung. Ein unverändert signierter Plan wird nur übernommen, wenn PSERC ihn als **aktuell** und mit >0 Positionen ausweist.

## Durchgeführte Simulation / tatsächlich ausgeführter Code
- **20/20 lokale PHP-Funktionstests PASS**: 10 Admin-Szenarien, 4 Worker-Steps, 4 Worker-Neustarts, 2 Exporte.
- Originaler `PSTE_Admin`-Start/Status/Export und originaler `PSTE_Research_Driver` wurden geladen. WordPress- und Provider-Funktionen wurden nur **in-memory nachgebildet**. Bei den Compiler-Start-/Advance-Aufrufen wurde die externe PSERC-Jobfunktion im Test simuliert, nicht ein ganzer echter Compilerlauf.
- Reale, unveränderte **PSERC-Metadata-Boundary** prüft die signierte originale Drei-Artikel-Datei. READY-Anzeige **3/3** und PDF? **Nein, JSON-Export** liefert dieselben Daten wie die ursprüngliche JSON-Datei; bei absichtlich veralteter Quellenbindung gibt es **keine Exportdatei**.
- RUNNING alter Audit: **nicht** erneut gestartet, kein neuer Einzelworker. COMPLETE/CANCELLED alter Audit: **einzelner Worker** kann weiterlaufen und serverseitig wieder anlaufen.
- **126 PHP-Syntaxprüfungen PASS**, **PSERC-Paketintegrität 61 Dateien PASS**, vollständige Byteprüfung des gepackten PSTE-ZIPs (121 Dateien) PASS.
- **0 echte WordPress-/DB-Aktionen, 0 reale Provideraufrufe, 0 Artikelproduktion, 0 K0-Start.**

## Ablage / Nachweise
Persistente Library `/pferdeatelier/PLUGINS/QA/`:
- `PSTE-0.57.144.41-KISS-AUTOMATIK-NUR-WP-TEST.zip` – SHA256 `1d0b755f6bff12231c9e8eaeb7d1432859a6763632c06b0e2b03b704dd9ea178`, **648312 Bytes**, 121 Dateien.
- `PSTE_40_ZU_41_KISS_ONLY.patch` – 3-Dateien-Diff gegen .40; SHA256 `33a7aaa5753e4faab79e54d0a7f40c4f9f1012583fd2436bc5a590b7dbd65128`.
- `PRUEFBERICHT_FINAL.json` und `KISS-41-NACHWEISE-UND-SIMULATIONEN-20261111.zip` (Tests, Diff, Bericht).

## Offen – nicht übertreiben
**Nicht** belegt: echter WordPress-Ende-zu-Ende-Lauf mit neuer Keyword-Recherche und DataForSEO, reale Neubewertung/Neufreigabe im bereits beschädigten WP-Themenpool, frisch erzeugter PSERC-Plan mit 1+ READY oder erfolgreicher K0-Auftrag.

**Spezifische Grenze der alten PSERC-Frischebindung:** `PSERC_Plan_Dependency_Fingerprint::current` benutzt unter anderem maximale IDs (Wasserzeichen) und Kontextgeneration, **keine Voll-Hash-Prüfung aller vorhandenen Themenzeilen**. Bei in-place-Änderung alter Zeilen darf deshalb nicht allein aus der Mock-Simulation behauptet werden, ein historischer READY-Plan sei in der aktuellen realen WordPress-Tabelle gültig. Nur der tatsächliche WP-Endtest kann die Freigabe abschließen. Keine DB-Restauration und kein 5k-Audit empfohlen.

**Nächste Aktion:** Die neue .41 nur isoliert in der vorhandenen getrennten WordPress-Testinstallation verifizieren: ein neuer Einzel-Keywordauftrag, Abschluss/planbares Thema, Automatik-Planer, echter JSON-Export; 5.013er-Audit darf nicht starten. Nur bei echtem PASS freigeben. Keine anderen Plugins austauschen oder Änderungen an Live-Webseite.

Status: `LOCAL_20_OF_20_PASS; PHP_LINT_126_PASS; PSERC_UNCHANGED; QA_ARCHIVED; WP_REALRUN_PENDING; NO_DB_DIRECT_WRITE`.
