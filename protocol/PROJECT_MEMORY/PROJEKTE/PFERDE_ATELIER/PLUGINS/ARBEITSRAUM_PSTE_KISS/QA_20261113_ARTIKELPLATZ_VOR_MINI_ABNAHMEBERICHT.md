# Pferdeatelier – KISS: Einzelentscheidung → echter Planplatz → MINI nur Titel

**Stand 13.11.2026. Es ist ein geprüfter QA-Arbeitsstand, noch keine WordPress-Liveabnahme und kein Installationspaket.**

## Zielvertrag / festgelegte Fehlerliste

1. Zentrale PSTE-Recherche entscheidet über eine belegbar eigenständige Leserabsicht **einmalig und abschließend**, noch ohne einen fertigen Titel.
2. Im **gleichen vorhandenen WordPress-Datensatz** wird aus dem **vorhandenen PSERC-Produktionsplan** vor MINI eine feste kanonische Artikelplatz-ID samt Planplatz-Signatur ausgewählt und gespeichert. Bei keiner passenden freien Position **keine** Freigabe an MINI.
3. MINI formuliert zu dieser vorgegebenen Suchabsicht **exakt einen Titel**. JA/NEIN/VIELLEICHT, neue Kategorie/Artikelart oder neue Suchabsicht sind dort verboten.
4. PSERC übernimmt den bereits gebuchten **identischen** Platz, vergibt ihn nicht ein zweites Mal. Andere Kandidaten sehen ihn als belegt. Der schon zuvor beseitigte zweite SEO-Entscheid bleibt entfernt; die technisch notwendigen Kategorie-/Beitragsart-/Platz-/Titelgrenzen bleiben.
5. K0 erhält weiter die **fünf** festgelegten Angaben (`title`, `target_keyword`, `category`, `article_type`, `plan_slot`), schreibt Text. WordPress-Import bleibt unverändert.

## Ursprungsfehler und tatsächliche Originalcode-Korrekturen

| Ursprungsfehler | Bestehende Stelle, tatsächliche Änderung | KISS-Notwendigkeit |
|---|---|---|
| SEO-FREI verlangte MINI-Titel und MINI-Worker wollte JA/NEIN/VIELLEICHT entscheiden | `PSTE_Mini_Workflow` in `class-pste-mini-workflow.php`: vorgezogene Fremd-SEO-Einmalentscheidung, gefrorene Leserabsicht, genau EIN Titelworker. | Ohne Freigabe vor Titel ist der Zielvertrag unmöglich. Keine neue Workerfunktion. |
| Reserviert war nur die Leserabsicht, noch **kein Artikelplatz** | Gleiche bestehende `PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions`: verwendet vorhandenen `PSERC_Production_Reader` und `PSERC_Slot_Allocator::allocate` noch vor MINI; bucht `canonical_article_id` und `plan_slot` im **alten** WordPress-Optionsdatensatz `pste_mini_keyword_roundtrip_v1`, zusammen mit FREI-Bescheid; dessen vorhandener atomarer Speicherweg wird verwendet. | Der Artikelplatz muss vor Titel verbindlich feststehen; kein neues DB-Schema, keine neue Optionsbezeichnung. |
| PSERC könnte später versehentlich einen anderen Platz vergeben oder einen vorgebuchten Platz an ein anderes Thema vergeben | `class-pserc-slot-allocator.php`: bestehender Belegungsleser berücksichtigt die bereits gespeicherten PSTE-FREI-Plätze. Der eigentliche Eigentümer darf seine genau belegte kanonische Position wiederverwenden, wenn aktueller Produktionsplan, Kategorie, Beitragsart und echte PPM-/WP-Belegung passen; sonst gesperrt. | Der Platz muss unverändert durch alle Stationen gehen und darf nicht doppelt vergeben werden. |
| Die endgültige Vorbuchung kam nicht beim normalen PSERC-Eingang an | `class-pserc-seo-reader.php`: übermittelt die beiden festen Platzwerte aus **derselben** gültigen bisherigen Fremd-SEO-Freigabe; abweichender Titel, Kategorie, Beitragsart = STOP, nicht neue Freigabe. | Der Redaktionsplan darf nicht neu entscheiden oder neu zuteilen. |
| Fortgesetzter Planlauf konnte einen bereits im laufenden Auftrag reservierten Platz nochmals einsetzen | `class-pserc-plan-compile-job.php`: nutzt die bereits vorhandenen `reserved_ids` zur eindeutigen Belegung pro vorhandenem Lauf. | Sicherheit bei Fortsetzung ohne zweite Reservierungsliste. |
| Selbstprüfende Paketliste muss die geänderten Originaldateien erkennen | Das **vorhandene** `contracts/compiler-package-binding-v1.json` wird auf die neuen Dateiprüfsummen aktualisiert; `PSERC_Package_Integrity::validate()` unverändert. | Notwendig, damit der bestehende Sicherheitscheck das aktualisierte Plugin nicht fälschlich sperrt. |

**Kein neuer Worker, keine neue Tabelle, keine zusätzliche SEO-Prüfung, keine zweite fachliche Stelle, keine Änderung an K0 oder dem WordPress-Importer.** Ältere Original-PSTE und -PSERC-ZIPs bleiben byteidentisch.

## Gegenbeweise mit originalen PHP-Funktionen

- **30/30** PSTE-MINI-Gegenproben: Freigabe ohne Titel, Vorreservierung, Titel-only, gefrorene Absicht, keine Plätze → KLÄRUNG, Kategorie-/Typwechsel gesperrt.
- **11/11** bestehender PSERC-Platzverteiler: Eigentümer erhält genau seinen Platz, fremdes Thema bekommt nächsten, falsche Zuordnung, echte WP-/PPM-Belegung, Job-Doppelbuchung gesperrt.
- **32/32** tatsächlicher PSERC-Eingang: Quittung durchreichen, keine neue SEO-Entscheidung, verdrehte Kategorie/Art/Titel/Signatur gehalten.
- **159/159** historische echte 87 SEO-Entscheidungen gegen 1.179 alte Bestandszeilen; 61 FREI / 20 BELEGT / 6 KLÄRUNG unverändert.
- **27/27 + 15/15 + 11/11** alte Reader-, fortsetzbarer Job- und normale Compiler-Gegenproben.
- **18/18** vorhandene Offline-Gesamtsimulation bis zu zwei **nachgebildeten** WordPress-Entwürfen bestanden.
- **126/126** PHP-Dateien Syntax PASS; bestehendes `PSERC_Package_Integrity::validate` 61 Dateieinträge PASS; ZIP-CRC PASS; genau **vier bestehende PHP-Dateien plus bestehende Dateiliste** geändert.

**Summe der acht Offline-Testgruppen: 303/303 PASS.** Die Gesamtsimulation benutzt nachgebildetes WordPress/PPM/K0. Das sind keine 303 live erzeugten Artikel.

## Prüfbare Abstammung

- Vorheriger, bereits im Campus verifizierter QA-Arbeitsstand: `PFERDEATELIER_KISS_MINI_NUR_TITEL_VORAB_FREIGABE_QA_20261113.zip`, SHA256 `489ca173ea7be9e5c88cdbfc8ef9f8182575ad04a0c6e893aa754a5432111439`.
- **Neuer einziger aktueller QA-Stand:** `PFERDEATELIER_KISS_PLANPLATZ_VOR_MINI_NUR_QA_20261113.zip`, SHA256 `690543b7e9ecab60c2fcda6e0bee1f0c7db61320b2dd1b8a306cd5e5cdded8fd`, 1.870.184 Bytes und 216 ZIP-Einträge.
- Der exakte Textunterschied aller fünf geänderten Dateien steht in `QA_20261113_CANONICAL_VOR_MINI_KISS_PATCH.patch`, automatischer Hash-/ZIP- und Quellvergleich in `QA_20261113_CANONICAL_VOR_MINI_ABNAHME.json`.
- Zwei ursprüngliche Original-Plugin-ZIPs im Paket wurden **unverändert kopiert**.

## Ehrlich verbleibende Lücke

**Das ist bisher eine dauerhafte Vorreservierung im bereits bestehenden PSTE-Optionszustand, die PSERC versteht – noch keine getestete Schreibbuchung in der tatsächlichen PPM-WordPress-Plan-Datenbank.** Die verfügbare Offline-Gegenprobe arbeitet mit einem signierten, simulierten PPM-Plan. Ob ein dritter, direkter PPM-Schreiber diesen vorreservierten Platz ebenfalls meidet, wurde damit noch **nicht** bewiesen. Daher **keine Installation und keine Behauptung eines echten End-to-End-WordPress-/K0-Laufs.** Vor der Produktionsfreigabe muss auf der vorhandenen Test-WP-Installation mit realem PPM-Plan geprüft werden, dass auch parallele PPM-Schreiber den reservierten Slot respektieren. Dafür kein neues Reservierungssystem erfinden.