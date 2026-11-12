# Pferdeatelier – KISS-Kategorieübergabe: geprüfte QA-Umsetzung

**Stand:** 09.11.2026. **Ausschließlich isolierte Testkopie. Nicht als Plugin installieren; K0, PSERC, PPM und WordPress unangetastet.**

## 1. Verbindliches Konzept – vor dem Ändern abgeglichen

Quelle: Vier-Worker-Vertrag vom 17.10.2026 (GitHub-Datei `PSTE_FOUR_WORKERS_UNIFIED_EXISTING_PLUGIN_20261017.patch`) und Fach-/Magazin-/Redaktionsbüro-Zuordnung vom 19.10.2026 (`PSTE_KISS_CENTRAL_CATEGORY_ROUTING_20261019.patch`) sowie WordPress-TEST-Bericht `pste-stapelbericht-2026-11-09(1).json`.

- Externe MINI-Worker 1 und 2: **Suchintention** und **genehmigter Titel** – jeweils ein Eigentümer. Keine neue Prüfung in WordPress.
- Bestehender Kategorie-Worker: eindeutige **Fachkategorie** oder **Magazinkategorie**, sonst **Redaktionsbüro als Arbeitsweg**. Offene Kategorie ist keine SEO-/Titelablehnung.
- Übergabe an PSERC/K0 **nur mit konkreter Kategorie und fünf vollständigen Angaben** (Artikeltyp, Kategorie, Planplatz, Keyword, Titel). Sonst bleibt der Vorgang ein geschützter Arbeitsauftrag. Keine K0-Vertragsänderung.
- Tatsächlich vorhandene WordPress-Artikel, gültige manuelle Sperren und eine eindeutig abgedeckte Suchintention bleiben Schutzfälle. Ein neuer Titel ersetzt keine andere Suchintention.

## 2. Echte, zuvor sinnwidrige Doppelprüfung nachgewiesen

Im bestehenden `PSTE_Planning_Readiness_Gate::apply()` wurde bei signiertem MINI `FREI` allein `production_title` mit `approved_title` verglichen. Bei noch offener Kategorie ist `production_title` **absichtlich leer**, der bereits genehmigte `editorial_title` aber vorhanden. **Daher hat WordPress die fachliche FREI-Entscheidung allein wegen eines fehlenden Kategorienamens wieder zur KLÄRUNG herabgestuft.**

**Exakte KISS-Korrektur:** Nur wenn der *vorhandene* vierstufige Pfad einen gültigen `CATEGORY_ROOM_TOPIC_POOL` ohne Kategorie-ID/Slug und ohne Produktionstitel meldet, wird das bereits gespeicherte `editorial_title` gegen den **unveränderten externen genehmigten Titel** abgeglichen. In allen anderen Zuständen gilt weiterhin der strenge Produktionstitel-Abgleich. Abweichende/geänderte Titel oder gefälschte Kategorie-/Büroangaben bleiben gesperrt. **Keine SEO-Neubewertung, keine neue Textfreigabe, keine Datenbanktabelle, kein neuer Worker.**

**Vorher-Nachher-Beweis am tatsächlichen PHP:** Vorher `192/304` erwartete Prüfungen bestanden (112 erwartete Negativfälle belegen den Fehler); nach enger Korrektur `408/408`, einschließlich 104 zusätzlicher Gegenfälle gegen gefälschte Kategorie- und Büroangaben.

## 3. Vollständiger lokaler Rücktest

| Durchgeführter Test | Ergebnis |
|---|---:|
| Reale WordPress-Exportstruktur und Plan-Ableitung | 51/51 |
| Echte PSTE-Reentry-/Queue-Methoden mit nachgebildeten WP-Optionsdaten | 12/12 |
| Tatsächliche eindeutige Kategorieidentitäten (45 gleiche Namen) | 1.304/1.304 |
| Einzige persistente Warteschlange / technische Gegenfälle | 22/22 |
| Lesender Kontextindex verändert keine Daten | 9/9 |
| Einmalige externe SEO-Entscheidung beim Versionswechsel | 188/188 |
| Tatsächlicher MINI-Quittungsleser über alle 61 Themen | 246/246 |
| Bestehender Produktionsvorprüfer und Fehlerfälle | 16/16 |
| Original-PSERC-Grenzen, mit künstlichen PPM-Belegen | 13/13 |
| Originale vier Worker: 52 Fach-/Magazin-/Redaktionsbüro-Routen, 8 Normalwege, manuelle Sperre | 295/295 |
| Externer SEO-Owner/Original-PHP: Kategorie offen, Kategorie da, veränderte Titel, gefälschte Ziel-ID und falscher Produktionsstatus | 408/408 |
| **Alle lokal ausgeführten Prüfungen** | **2.564/2.564** |
| PHP-Syntax in der isolierten Plugin-Testquelle | **83/83** |

Das reale WordPress-Testprotokoll enthält 61 Themen: **52 bereits dem Redaktionsbüro als Arbeitsweg zugeordnet**, 8 im Fach-Normalweg, 1 manuell gesperrt. Der technische Stapel führt weiterhin **61 zurückgestellte** Einträge, darunter **60 wegen alter Planprüfsummen**. Diese isolierte Korrektur schreibt diese historischen Berichte nicht um und beweist keine neue WordPress-Weitergabe.

## 4. Kritisch nicht verändert

- Kein Eingriff in die ersten zwei MINI-Worker, den externen Titelimport oder den SEO-Owner.
- Kein Eingriff in PSERC, PPM, aktives K0, WordPress-Beiträge und WordPress-Kategorien.
- Alte Planprüfsummen nicht blind entfernen: Die gezielte .28-Rebind-Aktion ist im letzten WordPress-Export **nicht** als ausgeführt/nicht ausgeführt identifizierbar.
- Keine generelle Aufhebung von Dubletten-, Signatur- oder Berechtigungsprüfungen.
- **Exakt sechs schon bestehende PSTE-PHP-Dateien** unterscheiden sich vom Original .28, fünf aus der vorangegangenen geprüften Zentralisierung und die eine jetzt korrigierte Planungsprüfer-Datei. Alle 121 Originaldateipfade unverändert.

## 5. Prüfgrenze, nächster echter Schritt

`FULL_WORKFLOW_PASSED = false`. Die WP-Option für den 61er-MINI-Quittungsleser ist aus dem tatsächlich exportierten MINI-Bericht **rekonstruiert**, nicht die direkte Original-WP-Option. Die WordPress-Datenbank, aktive PPM-Reservierung und tatsächliche K0-Texterstellung konnten **nicht in einer echten WordPress/MySQL-Testinstallation gemeinsam ausgeführt** werden. Ein `PASS` der lokalen Tests ist deshalb **keine Produktionsfreigabe**.

Zur endgültigen Freigabe gehört ausschließlich der noch fehlende isolierte WordPress/PSERC/PPM/K0-Gesamtdurchlauf (positiv: gültige Fach- und Magazinkategorie; negativ: offene Kategorie, doppelte Suchintention, manuelle Sperre, veraltete Planbindung und manipulierter Titel), unter Beibehaltung aller bisherigen Schutzregeln.

Das QA-Paket liefert den **einen** geänderten Owner-Abgleich, den vollständigen sechs-Datei-Vergleich gegenüber `.28`, den echten 61er-Ausgangsbericht, die WordPress-Exportdaten, sämtliche lokalen Tests, Prüfsummen und den Wiederholungslauf `bash run_kiss_category_qa.sh`.