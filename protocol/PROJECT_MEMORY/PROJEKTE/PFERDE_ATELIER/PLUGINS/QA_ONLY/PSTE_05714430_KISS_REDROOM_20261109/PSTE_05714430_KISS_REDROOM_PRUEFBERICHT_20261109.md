# Pferdeatelier – PSTE 0.57.144.30 – gezielter KISS-Fix Redaktionsbüro

Stand: 09.11.2026. **Nur TEST-WordPress. Keine produktive Freigabe.**

## Nachgewiesene Ursache aus echter TEST-Datei .29

Der originale Bericht `pste-stapelbericht-2026-11-09(2).json` enthält 61 ursprüngliche Themen, davon 52 `CATEGORY_ROOM_TOPIC_POOL` mit `STRUCTURE_GAP`, 7 normale PASS-Fälle, 1 normaler Discovery-Halt und 1 manuelle Sperre. Diese 52 haben gleichzeitig `automatic_pool_status=DISCOVERY_ONLY`; die bisherige PHP-Ampel beurteilt `DISCOVERY_ONLY` als GREEN. **Bisheriges `class-pste-admin.php::renderReview()` blendete die vorhandene Fach-/Magazin-/Redaktionsbüro-Entscheidung bei GREEN durch „Keine Aktion nötig“ aus.** Zudem zeigte der Standardfilter „Rot und Gelb“ die grünen Bürothemen nicht. Ein Bearbeitungsweg war gespeichert, aber nicht bedienbar. Das ist der konkret bewiesene Defekt.

## Enger Fix, keine neuen fachlichen Entscheider

Nur zwei bestehende PHP-Klassen und der Versionskopf geändert:

- `class-pste-admin.php`: sichtbarer Filter „Redaktionsbüro: Kategorie offen“ in der **bestehenden** Themenprüfung; sichtbare Kategorieaktion auch bei GREEN, aber ausschließlich wenn der **vorhandene** `normal_metadata_path` den Status `STRUCTURE_GAP + category_backlog_required + CATEGORY_ROOM_TOPIC_POOL` trägt. Im Büro nur die drei vorhandenen Aktionen `ROUTE_FACH`, `ROUTE_MAGAZIN`, `ROUTE_REVIEW`; keine zweite Freigabe, keine neue Titel-/Artikeltypentscheidung. Kategorien werden nicht aus Kurzkeywords geraten oder automatisch neu angelegt.
- `class-pste-repository.php`: ein optionaler, **rein lesender** Filter des bestehenden paginierten Themenlesers, mit von WordPress korrekt maskierter Suche nach dem gespeicherten `CATEGORY_ROOM_TOPIC_POOL`. Nach dem SQL-Vorfilter prüft der vorhandene PHP-Speicherstatus die Fachautorität nochmals **nur zur Anzeige**. Keine neue Fachklassifizierung und keine neue Produktionskontrolle. Im Normalmodus keinerlei zusätzliche Abfrage.
- `portal-seo-topic-engine.php`: WordPress-Plugin-Version `0.57.144.30` statt `.29`.

Die vorhandene manuelle Zuordnung kontrolliert weiterhin die echte WordPress-Term-ID, den Fach-/Magazinbereich und blockiert die K0-Übergabe ohne konkrete Kategorie. MINI, PSERC, PPM und K0 unverändert.

## Harte lokale Prüfung

- Vorhandene Regressionen gegen Originalexport, MINI-Reentry, 4-Worker-Weg und PSERC-/PPM-Grenzen: **2.564/2.564**.
- Direkt ausgeführte tatsächliche PHP-Funktion `PSTE_Admin::reviewReadPage()` und `categoryRoomPending()` mit **61 echten v29-Fällen**, 52 Bürothemen, Gegenfälle für falsche Verträge, gefälschte Raumangaben, fehlende Backlogfreigabe, Paging und Fremdeinträge: **338/338**.
- Tatsächliche PHP-Funktion `PSTE_Repository::adminTopicPoolPage()` mit nachgebauten WP-Tabellenzeilen und SQL-Leser: **116/116**, Büro 52 Treffer plus ein bewusstes Text-Scheinmatch als Negativfall, normaler Leser unverändert, keine Schreibabfrage.
- `PSTE_Admin::renderReview()` tatsächlich zu HTML ausgeführt, Kategorieformular und beschränkte drei Bürooptionen überprüft: **15/15**.
- Zusammen **3.033/3.033** lokale Positiv-/Negativchecks. **83/83 PHP-Syntaxchecks**.
- Installations-ZIP hat dieselben **121 Dateipfade** wie v29. Gegen v29 genau 3 Dateien geändert, ZIP-CRC und 121 SHA256-Dateiprüfungen nach frischem Entpacken bestanden, alle vier Testprogramme aus frischem Paket erneut ausgeführt: PASS.
- Installationspaket: `PSTE-0.57.144.30-KISS-REDAKTIONSBUERO-NUR-TEST.zip`, 643832 Bytes, SHA256 `3f32f511c39d77bd9a26d15222a46511ce81ef8180052caacbd3ca4405067d68`.

**Grenze:** Diese Version macht die 52 korrekt gespeicherten Redaktionsbüro-Fälle **bearbeitbar, nicht automatisch fachlich zugeordnet**. Sie legt keine WordPress-Kategorien neu an und übergibt keine offenen Fälle an K0. Eine sichere automatische Auswahl für die einzelnen 52 kann aus dem bisherigen Kurzbericht allein nicht belegt werden; wir raten keine Kategorien. Der Sonderfall „Regendecken Sale“ wird nicht blind entblockt. **FULL_WORKFLOW_PASSED=false**: realer WordPress/MySQL→PSERC→PPM→K0-Gesamtlauf nicht bewiesen.

## Konkreter Praxistest

Auf **WordPress-Testseite** die `.30`-ZIP als Update installieren. Unter **SEO Themenengine → Themenprüfung** den neuen Button **„Redaktionsbüro: offene Kategorien bearbeiten“** öffnen. Prüfen, dass die 52 offenen Fälle sichtbar sind, mit den Optionen Fachbereich, Magazin oder offen. **Nicht** „alte Planbindung erneuern“; der .29-Report zeigte 0 alte Plan-Driftfälle. Als nächster Praxistest eine existierende, eindeutig richtige Kategorie bei **einem** unkritischen Bürothema prüfen, speichern und den aktuellen Folge-Status beobachten. **Keine K0-/Produktionsübergabe ohne positive Endprüfung.**

GitHub: nur QA-Draft-Branch `fix/pste-kisten-einmalige-pruefung-20261107`, PR #682 unverändert DRAFT. Kein Merge, keine K0-/LIVE-Änderung.