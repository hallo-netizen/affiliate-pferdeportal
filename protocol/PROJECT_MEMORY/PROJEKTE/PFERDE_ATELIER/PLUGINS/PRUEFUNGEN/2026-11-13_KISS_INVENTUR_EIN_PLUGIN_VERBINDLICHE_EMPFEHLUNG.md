# Pferde Atelier – verbindliche KISS-Empfehlung nach Quellinventur
**Stand:** 13.11.2026. **Status:** Beschlussvorschlag für isolierten Test, keine Live-/Installerfreigabe, kein Ersatz einer Current-Autorität.

## Prüfbasis – Dateien tatsächlich ausgewertet
- PSTE **0.57.144.50 QA**, vollständiges ZIP (83 PHP-Dateien), aktueller lokaler **nicht installierter** Arbeitsstand.
- PSERC **0.28.71 QA**, vollständiges ZIP (42 PHP-Dateien), aktueller lokaler **nicht installierter** Arbeitsstand.
- Tatsächlicher WordPress-Lesediagnose-Export `pste-gesamtdiagnose-2026-11-13.json` (13:51 UTC; read-only); originale SEO-Einmalentscheidung vom 09.11.2026 (87 Zeilen).
- Bericht `ARBEITSBERICHT_C_VERTRAG_20261113.md` und echte PHP-Funktionsprüfungen aus dem laufenden QA-Arbeitsraum; deren PPM-/K0-Komponenten sind **Mocks**, keine Live-Ende-zu-Ende-Beweise.
- GitHub: Campus-Pluginbüro, `PFERDE_ATELIER/PLUGINS/START_HERE.md` und verbindliche Current-Einschränkungen sowie laufendes Prüf-PR #768.
- Inventur direkt mit 12 Quelltext-Verankerungen und zwei Original-ZIPs: 12/12 Funktionen/Aufrufstellen tatsächlich vorhanden. Keine Aussage, 12/12 live funktionierten. Beleg lokal `source_inventory_verified_20261113.json`.

## Tatsächlich vorhandene Bausteine
| Fachaufgabe | Originalquellfunktion | Befund |
|---|---|---|
| SEO-Keyword-Recherche | PSTE: `PSTE_DataForSEO_Client`, `PSTE_Breadth_Research_Queue` | Code vorhanden; kompletter Live-Erfolg aus diesen Dateien nicht nachgewiesen |
| Einzige redaktionelle SEO-Entscheidung | PSTE: `PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions`, Editorial Gates | Code vorhanden; alter Freigabebestand unvollständig gebunden |
| Lücken im Kategoriebaum / Bedarfsgewichtung | PSTE: `PSTE_Analytics::coverageWithArticleCounts` und `priorities` | Code **bereits vorhanden**; kein neuer Planer nötig; misst Bestand und geplante Themen pro Themenfamilie |
| Externes Titelbüro | PSTE: `exportKeywords`, `importTitleCorrections` | Code vorhanden; feste Titelweitergabe abhängig von Freigabe-/Statusdaten |
| Übergabe an K0 | PSERC: `PSERC_Admin::exportK0Manifest`, `PSERC_Metadata_Boundary` | Fünf-Felder-Dateiformat vorhanden: `title,target_keyword,category,article_type,plan_slot` |
| WordPress-Entwurfimport | PSERC: `PSERC_System4_Import::importPayload` | Code vorhanden; **ruft zwingend** `PPM679_Editorial_Plan_Runtime_Gate::record_readback` auf, kann daher nicht ohne PPM unverändert betrieben werden |
| Einmalige Auftragsentnahme und Rückgabe OHNE Produktionsplan | Als vollständiger, echter, parallelsicherer Weg nicht nachgewiesen | **Fehlt als fertig belegter End-to-End-Weg**; mögliches kleines KISS-Modul statt eigenständigen PPM-Planers |
| K0 Textqualität / 81 Regeln | Separate unveränderte K0-Fabrik | Nicht in neues Plugin kopieren und nicht doppelt in WordPress prüfen |

## Fehlerhistorie und harte Tatsachen
- 87 Originalentscheidungen: **61 FREI / 20 BELEGT / 6 KLÄRUNG**.
- Bei diesen **61 FREI** fehlen im Freigabeexport die Felder Kategorie-Slug, Artikelart, kanonische Artikel-ID, Artikelplatz. Dies beweist nicht, dass alle Werte auch im vollständigen WordPress-Datensatz fehlen.
- **61/61** alte Titel-Fälle haben im WordPress-Diagnose-Export `planning_gate_status=NOT_STORED`.
- **PSERC 0 READY**: `planning_topic_count_expected=0`, `PSERC_PLAN_NO_SOURCE_TOPICS_PRESERVE_PRIOR_SNAPSHOT`. Diese Blockade beginnt mit nicht bereitgestellten PSTE-Daten; bloßes Zusammenkopieren von PSTE/PSERC heilt sie nicht.
- 5.020 gespeicherte PSTE-Poolzeilen sind **keine 5.020 genehmigten Artikel**. Rollen: 4.818 `RESEARCH_KEYWORD`, 196 `RESEARCH_CLUSTER`, 1 `ARTICLE_TOPIC`, weitere Nebenrollen. 0 Produktionsbereite. Bereits genehmigte 61 liegen in der gesonderten historischen Freigabe.
- Ein nachweisbarer Altfehler: bereits vorhandener Titel verhinderte in PSTE .47 die Zuteilung (originaler Funktionsaufruf 61 Fälle -> 0 Allokatoraufrufe); .50 QA hat hierfür Korrekturen, aber ist **kein Livebeweis**.
- PSTE/.50 und PSERC/.71 sind **eng gekoppelt**, keine vollständig unabhängigen Bausteine: statische Quellreferenzen PSTE->PSERC **94**, PSERC->PSTE **133**, PSERC->PPM679 **59**. Referenzzählung = keine Anzahl aktiver fachlicher Doppelentscheidungen, belegt aber Kopplung.
- PSERC hält Plankompilierung und PPM-Slot-Allocator sowie WordPress-Importer. PSTE hält eine **eigene** atomar geschriebene Freigabeoption. PPM verlangt einen eigenen Runtime-Plan. Das erklärt das Risiko verteilter Statuswerte. Die vollständige native PPM-6.7.9-Implementierung ist hier weiterhin nicht lesbar; nicht behaupten, dass alle PPM-Funktionen überflüssig seien.
- Es existieren verschiedene QA-Versionen, aber die Liveversion darf nicht aus ZIP-Dateinamen erschlossen werden. Frühere WordPress-Leistungsanalyse vom 12.11.2026 listete PSTE .0.57.120, PSERC .0.28.43, PPM 6.7.9; spätere Testinstallation wurde separat bearbeitet.

## Verbindliche technische Empfehlung – kleinster sichere Weg
**JA: Ein schlankes gemeinsames WordPress-Plugin als isoliertes Pilotprojekt auf der geklonten Testumgebung entwickeln. NEIN: weder bestehende funktionierende Programme blind zusammenkopieren noch sofort PSTE, PSERC oder PPM aus Live entfernen.**

Die neue Plugin-Grenze ersetzt nicht die inhaltliche Aufgabenteilung. Sie hält nur die technisch notwendigen Zustände in **einem** WordPress-Auftrag pro freigegebenem Thema.

**Minimaler interner Worker-Ablauf:**
1. `RECHERCHE+EINMALIGE_REDAKTIONSENTSCHEIDUNG` (bestehendes PSTE-Verfahren, keine zweite Freigabe, keine Keywordregel neu erfinden).
2. `FREIGEGEBENES_REGAL` (feste Auftragskennung, Keyword/Suchabsicht/Kategorie/Artikelart eingefroren; Überwachung aller wichtigen Kategorien anhand vorhandener PSTE-Analytics).
3. `EXTERNER_TITELWORKER` (bestehender Dateiweg, nur Titel).
4. `ENTNAHME+K0_EXPORT` (X Aufträge einmalig reservieren, bis Rückgabe oder gezielte Wiederaufnahme; keine Löschung aus DB).
5. `K0` extern und unverändert (81 Qualitätsregeln).
6. `RÜCKLAUF+WP_ENTWURF` (bestehendes Importprinzip übernehmen; technische ID-/Kategorie-/Doppelimport-Sicherung erhalten; **kein** neues Inhaltsqualitätsurteil, **kein** automatisches Publish).
7. `ABBRUCH_WIEDERAUFNAHME` (nur unvollständige Aufträge gezielt fortsetzen).

**Kein separater Produktionsplan für Reihenfolge, Kapazität oder Termine notwendig**, soweit das beschriebene sequentielle Regal-Modell reicht. Eine feste Auftragskennung und Status bleiben notwendig. Im bisherigen K0-Vertrag ist `plan_slot` **Pflicht** und der vorhandene Import hat eine echte PPM-Abhängigkeit: eine kompatible Zuordnung/Importanpassung muss erst bewiesen werden. `plan_slot` nicht kommentarlos streichen oder mit beliebigem Wert füllen.

**Keine neuen zusätzlichen Such-/Bewertungsworker.** 1 bestehender Fach-Entscheider, 1 externer Titelworker, 1 K0, interne einfache Entnahme/Rückgabe. Worker führen ihre eigenen Schritte aus, keine Doppelprüfung. Qualitätsprüfung ausschließlich K0; WordPress nur technische Eingangssicherung.

## Konkrete gefahrarme Reihenfolge
A. **Keine Liveänderung.** Test-WP klonen/Backup, tatsächliche Freigabe-/Kategorie-/Export-/Importdaten read-only vergleichen. Keine 5.020 ungeprüften Keywords als fertige Artikel ins Regal übernehmen.
B. **Neues Pilotplugin auf geklonter Test-WP**, zuerst nur Lesen und Ausgabe der identischen alten Freigaben; die alten Worker parallel **nicht** schreibend starten. Bestehende nachweislich funktionierende Quellfunktionen nur unverändert übernehmen oder eindeutig delegieren; Keine Aufblähung um alle 125 PHP-Dateien.
C. Drei echte historische Problemaufträge mit nachvollziehbarer Quelle bis in die WordPress-Entwürfe durchspielen, anschließend 20er-Charge. Negative Fälle: doppelte Entnahme, paralleler Start, Abbruch 13/20, derselbe Rücklauf zweimal, falsche Kategorie, K0-Fünf-Felder-Identität. Jede Wiederholung muss dieselbe Auftrags-ID behalten.
D. **Nur nach bestandenem WordPress-Echttest**: PPM-Plan-/PSERC-Funktionen nacheinander durch isolierten Test ersetzen bzw. deaktivieren. PPM und Editorial Guard nicht vorschnell löschen: Import, Sicherheitssperren und weitere abhängige Funktionen erst nach tatsächlichem Quell-/Laufbeleg.
E. **Live optional schlanker:** Redaktion/Recherche kann auf Test-/Arbeitsinstallation bleiben, Live könnte später einen reinen gesicherten Importer verwenden; nur nach Nachweis gleicher Kategoriezuordnung, dauerhafter ID und Entwurf-/Publish-Sperren.

## Risikoabwägung / Warum die Empfehlung
- **Vorteil:** Weniger Datenkopien, Übergabe- und Versionsprobleme; Sperre und Wiederaufnahme an genau einer Auftrags-ID; redaktionelle Doppelschleifen fallen weg.
- **Nicht automatisch geheilt:** Falsche Keyword-/Kategorie-Freigaben, fehlende alte Quelldaten, fehlerhaftes K0-Paket, echte WordPress-Datenbank-Probleme. Zusammenlegen allein ist keine Ursachenreparatur.
- **Risiko Komplettneubau:** Hoch. 125 PHP-Dateien, gekoppelte Klassen/PPM-Gates, zahlreiche Altverträge und 61 unvollständige historische Freigaben. Deshalb **keine Total-Neuschreibung**.
- **Risiko begrenzter Pilot parallel zur Liveinstallation:** Beherrschbar, **wenn** keine zwei schreibenden Worker dieselbe Testdatenbank bearbeiten und Altimport/PPM nicht voreilig abgeschaltet werden.
- **Freigabebedingung:** Originale 3 Aufträge + 20er-Charge, sicherer Wiederanlauf, unverändertes K0, WordPress-Entwurf, kein Duplikat, kein Publish, tatsächlicher Datensatz-Rücklesebeweis. Offline-Mocks allein reichen nicht.

**Status:** Konzept nach Quelle geprüft, Pilot **empfohlen**, Umsetzung/WordPress-Test noch nicht erledigt. Keine Behauptung, der Zielworkflow sei bereits nachgewiesen.
