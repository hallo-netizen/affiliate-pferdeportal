# Pferdeatelier / MINI – kompletter Ablauf und einzige Verantwortung, Stand 07.11.2026

## Verifiziert
- ORIGINAL-TESTARCHIV `PSTE-0.57.144.22-NUR-TEST.zip` unverändert; semantisch **NICHT zur Installation freigegeben**.
- Rückfallbranch `backup/pste-mini-v22-before-kisten-20261107`, isolierter Arbeitsbranch `fix/pste-kisten-einmalige-pruefung-20261107`, Draft-PR #682.
- Aus tatsächlichem PHP: `PSTE_Mini_Workflow::createBatch` exportiert Quellsuchfragen und fordert JA/NEIN/VIELLEICHT/Titel; **keine** beweisbar vollständige SEO-/Artikelbelegung. `validateResult` importiert nur Entscheidungen und Titel. `forwardToPlan` ruft `saveManualTitleOverride`, `scheduleTitleDeskReentry`, `reanalyzeRetainedBacklogBatch`. Dort wird der bestehende `PSTE_Planning_Readiness_Gate` erneut ausgeführt. Seine `evaluate()` kombiniert `preTitleDuplicate` und `PSTE_Cannibalization::decide` (noch falsche PASS für 2er/zwei und 0g/ungefüttert).
- `PSTE_Normal_Metadata_Path::applyToPayload()` bewertet Relevanz, Kategorie, Beitragsart und Titel-Pipeline beim Wiederanlauf; `PSTE_Repository::prepareEditorialPayload()` nutzt die bereits gespeicherte MINI-JA-Relevanz, verarbeitet aber die normal- und planungsseitige Ableitung neu. Fach-/Magazin-Zuordnung ist **nicht** derselbe Auftrag wie Belegtheit einer Suchintention, darf aber keinen bereits autoritativen SEO-Stellplatzentscheid überschreiben.
- `PSTE_Snapshot::inventory()` derzeit nur WP post publish/draft, `editorialPlan()` ggf. NOT_AVAILABLE. `manualArticleBrief()` bei 1.200 Artikeln/1.200 PSTE-Plänen gedeckelt. PSERC-eigene aktive Pläne nicht nachgewiesen. Ohne eine neue, **vollständige** reale Gesamtquelle keine produktive "FREI"-Freigabe.
- Der ältere v19-WordPress-Report zeigt, dass **einzelne Kategoriefehler** die 87er-Reanalyse nicht zwingend stoppen. Das gilt NICHT für alle MINI-Importfehler. Das ist bei der bestehenden Eingangs-Implementierung gesondert nachgewiesen.

## KISS: eine Aufgabe / ein vorhandener Besitzer
| Abschnitt | Einzige Aufgabe | Nicht erlaubt |
|---|---|---|
| WP / Data4SEO | Suchbegriffe und Messdaten unverändert bereitstellen | Suchintention oder Artikel-Dublette abschließend freigeben |
| WP-Bestand / vorhandene Pläne | **Vollständigen** aktuellen Parkhausplan liefern (WP aller relevanten Status, Seiten/Glossar, PSTE, PSERC, Reservierungen) | SEO-Urteil, Titel erzeugen |
| vorhandener externer Relevanzworker | JA / NEIN / VIELLEICHT für Portalbezug | "Stellplatz frei" behaupten |
| **bestehender zentraler Planungs-/SEO-Entscheid, nach außen verlagert statt kopiert** | **einmalig**: Suchintent und Belegtheit am kompletten Plan, inklusive Themen desselben Stapels; mit Trefferbelegen | zweite SEO-Prüfung in WordPress, Freigabe nur nach gleicher Titelwortfolge |
| vorhandene Titel-/Sprachwerkstatt | Einen natürlichen Titel zur *festgelegten* Suchintention formulieren und sprachlich prüfen | Intent, Kategorie oder Parkplatz neu entscheiden |
| WP Rückweg | Technische Quellen-/Versionsbindung, unveränderten Entscheid speichern, einmalige **atomare** Slotbelegung; echte Änderungen -> selben Entscheider neu aufrufen | Text, Intent oder semantische Dubletten ein zweites Mal bewerten |
| bestehende Fach-/Magazin-/Kategorienzuordnung | Artikel in passende vorhandene Kategorie oder das vorhandene Redaktionsbüro führen | Intent-/Stellplatzurteil überschreiben; neue Kategorie ausdenken |
| bestehender PSERC → K0/Produktion | Nur fachlich und technisch fertige Artikelaufträge übernehmen; K0 erstellt Text wie bisher | K0 verändern, andere Archivsysteme als Fallback aktivieren |
| WordPress Artikelimport | Fertige Artikel unter dem reservierten Suchintent übernehmen | zweiten SEO-Gate erfinden |

**Kein neuer Dienst und kein neuer paralleler Gate:** Für den einen externen SEO-Entscheid muss die bestehende Planungsautorität tatsächlich verlegt und der WordPress-Zweitaufruf für bereits gültige externe Ergebnisse stillgelegt werden. Nicht einfach einen "KI-Gate" zusätzlich davor setzen.

## Vier Kisten – EINGANG, FREI, BELEGT, KLÄRUNG
- FREI nur mit gebundenem Suchintent, dokumentiertem vollständigem Parkhausplan, einer eindeutigen externen Entscheidung und erfolgreicher technischer Belegung.
- BELEGT nur mit konkreter Bestands-/Plan-Trefferreferenz; keinen Artikel neu erstellen.
- KLÄRUNG bei Mehrdeutigkeit, fehlender Kategorie, Einzelfehler, nicht eindeutig belegter freier Absicht, frischer Änderung, unvollständiger Entscheidbegründung; später **derselbe** externe SEO-Entscheid über eine tatsächlich andere Suchintention. Bloßes Umtiteln ergibt keinen freien Platz.
- Einzelne Fälle werden nicht global gestoppt. Nur Infrastrukturfehler oder fehlender Gesamtplan erlauben für den betreffenden Stapel keine neuen **FREI**-Freigaben. Ein sicherer "Klärung"-Export darf weiterlaufen.

## Was tatsächlich in Code geändert / getestet ist
- Unter `QA_ONLY/apply_existing_mini_kisten_import.py` wird **ausschließlich** die bestehende `class-pste-mini-workflow.php` in einer separaten TEST-ZIP umgestellt: fehlerhafte Einzelzeilen in `validateResult` landen als `clarification` im **bestehenden WP-Option-Speicher**, nicht als zusätzliche Tabelle oder Worker. Nur `completed` zählt als erledigt, Klärfälle bleiben erneut exportierbar; Import/Quellenprüfung bleibt technisch. Es gibt **keine zusätzliche inhaltliche Prüfung**.
- Echtes PHP-Lauftestskript `QA_ONLY/test_existing_mini_import.php`, isolierter GitHub-Lauf **42389959640: PASS**, 7 Fälle zu Einzelfehler/Wiederholung/Tampering/globalem Defekt. Separater bestehender rein technischer Kisten-QA-Lauf **42387802824: 9 PASS**. Gesamte ZIP: **83/83 PHP-Syntaxchecks PASS**.
- TEMPORÄRE QA-WORKFLOWDATEI nach Test wieder vom Arbeitsbranch entfernt. K0-, PSERC-, Live- und Original-Installerdateien **nicht geändert**.
- Das ist ein **getesteter Teilschritt**, **kein** End-to-End-Test und noch **keine** fertige installierbare Pluginlösung. Die Kisten-Logik ist im vorbereiteten Code noch nicht mit der vollständigen Portalquelle und dem externen Suchintententscheider verbunden.

## Verbindliche verbleibende Blocker (Ursachen, keine Symptom-Fixes)
1. Bestandsleser für alle WordPress-Inhalte, Status und tatsächlich aktive PSTE-/PSERC-Planquellen inkl. Reservierungen real vollständig nachweisen. Sonst keine FREI-Freigabe.
2. Die bestehende Planungs-/SEO-Entscheidung **genau einmal** extern ausführen und mit gebundenem Ergebnis/Quellenbelegen zurückliefern. Ein autonomer sprachlich urteilender KI-Lauf ohne nachgewiesenen KI-Dienst ist aktuell **nicht** bewiesen.
3. In der **bestehenden** WP-Rückgabestrecke rein technischen Empfang/Frische/Belegung durchsetzen; vorhandenen Zweit-SEO-Gate für extern geprüfte Fälle nicht nochmals ausführen, aber unveränderte Legacy-Pfade schützen. Kein zusätzlicher Gate.
4. Vollständige negativen und positiven **87 Originalfälle** über Quellen/Artikel/Pläne/WP-Testumgebung inkl. 2er, 0g, echter Horseware-Longtail, Kategoriefehler, fehlerhaften Einzelzeilen, geändertem Plan, wiederholtem Import, parallelem Slot nachweisen. Ohne WordPress-DB-Staging und tatsächlichen externen Entscheider **keine Release-Freigabe**.

## Veröffentlichungsregel
Die getestete EINZEL-Korrektur der MINI-Importfunktion bleibt zusammen mit dem Gesamtziel nur im **Draft/QA-Arbeitsbranch**. Keine Einzel-ZIP, keine Live-Installation und keine Behauptung, die Gesamtarchitektur sei schon fertig. Alle neuen Arbeiten nur innerhalb der vorhandenen Funktionen/Klassen und der einen Test-/Fallback-Trennung.
