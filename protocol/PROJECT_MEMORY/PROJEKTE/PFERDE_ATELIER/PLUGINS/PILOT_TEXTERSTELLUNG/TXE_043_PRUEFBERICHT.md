# Texterstellung 0.4.3: Kategorie-Worker – geprüfter KISS-Abgleich (14.11.2026)

**Ausgang:** Echte Diagnose 0.4.2: 61/61 `METADATEN_OFFEN`; `ORIGINAL_EDITORIAL_METADATA_NOT_FINAL:61` bei WordPress-Nutzerlauf. Historischer ORIGINAL-Stapelbericht 09.11.2026 (PSTE 0.57.144.29) zeigt **8 NORMAL_PASS**, davon 7 Titelweitergaben `PASS`, **52 CATEGORY_ROOM_TOPIC_POOL**, 1 andere Sperre. Das ist ein historischer Zustand, kein Nachweis der aktuellen 61 vollständigen Datensätze.

## Belegte Ursache – warum 61 FREI?
Die ursprüngliche externe SEO-Freigabedatei entschied `FREI`, Titel und Intent, aber enthielt bei allen 61 **keine** `category_slug`, `article_type`, `canonical_article_id`, `plan_slot`. `FREI` war damals keine vollständige K0-Produktionsfreigabe. Der vorhandene Kategorie-Worker hatte 8 konkrete Normalwege, 52 offene Büro-Fälle und einen weiteren Sperrfall. Die Import-Bridge 0.4.2 las fälschlich nur `manual_status=APPROVED`, während der Original-Worker abgeschlossene Kategorie-Entscheidungen als `manual_status=REASSIGNED` und `manual_category_id` + `manual_article_type` speichert.

## Präzise Regeln aus bestehenden Originalen
1. Einmalige SEO-Freigabe bleibt bei Original-PSTE. Fach/Magazin-Bereich und Artikelart nach originalem `PSTE_Normal_Metadata_Path`, `PSTE_Article_Type_Intent_Ontology` und `PSTE_Article_Type_Registry`. **Keine neue Entscheidung durch Export/K0/Import.**
2. Kategorie nur mit **existierendem echtem WordPress-Term** und vollständigem Fach- oder Magazinpfad. Die Artikelart ist in der Fachkategorie gespeichert; Magazin benötigt die explizite Journal-Route. Bei nicht belegbarer Eindeutigkeit bleibt der Vorgang **im bestehenden Redaktionsbüro** – keine künstliche Zwischen-Tabelle.
3. Der neue technische Reader erkennt ursprüngliches `REASSIGNED` mit echtem gespeicherten Prüfer, identischer Kategorie-ID und Artikelart, oder den gültigen originalen `NORMAL_PASS` mit unverändertem Quell-/Strukturbezug. **Keine zweite Kategorieprüfung**, sondern unveränderte Originalevidenz. Frühere PPM-`planning_suitability` ist kein Veto gegen vorhandene Kategorieentscheidung.
4. Ein täglich geplanter WordPress-Cron-Aufruf ruft **denselben Alt-FREI-Abgleich** auf, statt zusätzliche Fachentscheidungen zu erzeugen; bei neuer Original-Quellenzuordnung aktualisiert er vorhandene offene TXE-Aufträge. Kein neuer Worker, kein zweites Kategoriensystem, keine zusätzliche Tabelle. **Wichtig:** Das Cron-Lesen erstellt keine fehlende Kategorie und trifft keine ungelöste Erstentscheidung.

## Durchgeführte Simulation / Ergebnis
- **61 echte Aufträge unverändert**, gegen 100 Original-MINI-Antworten, Original-0.4.3-PHP geladen: 17/17 erwartete Kontrollaussagen bestanden. **0 K0, 0 Entwürfe in der Offline-Simulation.** Kein Original-Kategorie-/Artikelartwert erfunden. Der aktuelle WordPress-Pool ist offline nicht zugänglich.
- 12/12 isolierte Regressionen zum tatsächlichen Quell-Code für REASSIGNED/NORMAL_PASS sowie Gegenfälle (stale Struktur, ungültiger Reviewer, anderes Keyword, Kategorie- oder Typkonflikt). **Testterm-Daten sind nur Regressionstests**, nie in die 61 übernommen.
- 27/27 alte 20er-Ablaufregressionen durch Original-SEO-/Titel-/K0-/WordPress-Importquellen mit WordPress-Mocks bestanden. **Die 20 hier sind künstliche Regressionsthemen, keine echten 61.**
- 5/5 Cron-/Testumgebung-/Deaktivierungsprüfungen bestanden; 117/117 PHP-Lint; ZIP-Integrität okay, 164/164 PSTE-/PSERC-Originaldateien unverändert; nur zwei Programmdateien und README geändert.

**Zielvertragstatus: NOCH NICHT VOLL BESTANDEN.** Fehlende Kategorien bei 52 historischen Bürofällen kann kein technischer Leseadapter selbst fachlich zuweisen. Original-Worker und Portal-Standort werden nicht aus einem Titel geraten. Auf WordPress-Testinstallation mit 0.4.3 erneut `Bestehende FREI-Freigaben übernehmen` und Diagnose erstellen; dort wird sichtbar, ob die früheren acht Normalwege und der bestätigte Kolik-Fall nachweislich vorhandene Originalbindungen besitzen.

**Weder echte K0-81-Regel-Texterstellung noch echter WordPress-Server-Entwurfsimport wurden offline durchgeführt. Keine Livefreigabe.**
