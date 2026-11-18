# Pferdeatelier Texterstellung – Original-PSTE-Keywordrecherche → einziger MINI-Auftrag (QA 14.11.2026)

**Status: nur QA, nicht installieren, kein Live-/K0-Eingriff.** Verbindlich bleibt der vorhandene [Zielvertrag](TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md), kein zusätzlicher Entscheidungs-Worker.

## Konkrete Ursache und minimaler Eingriff
Der ursprüngliche Original-PSTE-Recherchejob schreibt Suchfragen in seinen vorhandenen WordPress-Themenpool. Der neue Texterstellung-MINI-Export verwendete bisher nur die älteren MINI-JA-Listen und das eigene bereits gespeicherte Texterstellung-Regal. Damit konnten neue bereits eindeutig bewiesene Original-PSTE-Keywords fehlen.

Nur in **bestehender** `texterstellung.php`, bestehendes `seoExport()`: Original-PSTE-`PSTE_Repository::adminTopicPoolPage()` jetzt **lesend** als zusätzlicher Originaleingang für noch offene Stellen der MINI-Charge angebunden. **Keine Entscheidung**, nur Übernahme bereits verbindlich dokumentierter Relevanz:
- Gespeicherter Originalpfad `portal_relevance=PROVEN`, ursprünglicher Relevanz-Beleg `ok/PASS`, unveränderte Rohfrage und Original-Hash müssen übereinstimmen.
- Nur expliziter WordPress-Pferdeportal-Kontext oder schon gebundener früherer positiver Beleg. Bloßes Wortfamilien-Matching – insbesondere mehrdeutiges **„Pferdeanhänger“** – ist nicht belastbar und bleibt in der bestehenden KLÄRUNG-/Sandbox-Bearbeitung des Original-PSTE.
- Frühere Original-FREI und bereits freigegebene/geplante/manuell bearbeitete sowie schon im gleichen Regal gespeicherte Keywords werden übersprungen. Keine Kategorie, kein Titel oder Redaktionsbeschluss wird in WordPress nachentschieden.
- Originaler neuer MINI-Auftrag bleibt mit frischem Original-WP-Bestand und Kategoriebaum gebunden, ein laufender Auftrag mit eingefrorenem Bestand und gesicherten CATEGORY/EDITORIAL/TITLE-Checkpoints; keine neue Tabelle, kein zusätzliches Plugin, kein zweiter Workflow.
- Unvollständiger Original-Leser/Seitencursor kann **kein falsches JA** erzeugen. Betroffene interne globale Quellenfehler blockieren sichere Freigaben, unabhängige bereits gespeicherte Ergebnisse bleiben bestehen.

## Belegprüfungen
- **266/266** lokale Tests PASS = vorige 247 Originaldaten-/Wiederanlauf-Gegenproben + **19** neue explizite Brückenfälle.
- **117/117** PHP-Syntaxprüfungen PASS, **164/164** Original-PSTE-/PSERC-Dateien byteidentisch.
- Historische Daten der vorhandenen Tests: **87** ursprüngliche MINI-Entscheidungen (61 FREI/20 BELEGT/6 KLÄRUNG), **1.179** archivierte WordPress-/Plätze, **1.124** originale Kategorie-/Seitenpfade.
- Die 19 zusätzlichen Input-Übernahmeprüfungen sind bewusst **nachgebildete** Original-PSTE-Kandidaten, keine heutige echte WordPress-DB-Abfrage. Geprüft: positive Originalbindung, unklare Pferdeanhänger-/Schmuckfrage, fehlender/verdrehter Nachweis, alte FREI/gebuchte/abgelehnte Themen, Seitengrenzen, kaputte Quelle, Chargengröße, unveränderte Fragen.
- Echter GitHub-/KI-MINI-Teilworker-Checkpoint-Rückkanal, administrativ zugängliche WordPress-Testinstallation, signierter Original-PPM-6.7.9-Platz und K0→WP-Entwurf **weiterhin nicht E2E-abgenommen**. Keine installationsreife Version behaupten.

## Dauerhaftes Original-Plugin-Büro
Unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`:
- `MINI_KISS_ORIGINAL_RECHERCHE_BRUECKE_20261114.patch`, SHA256 `7fc36971262a376bf8b730da41d5eadc9817887304878d5e5e2bf5eeb2d07e85`
- `MINI_KISS_ORIGINAL_RECHERCHE_BRUECKE_QA_20261114.php`, SHA256 `c9f1781e3d3a022efd07acfb9db57a7de36c635e5e5d175a3d56ddc4362b576a`
- `MINI_KISS_ORIGINAL_RECHERCHE_BRUECKE_TEST_20261114.php`, `MINI_KISS_ORIGINAL_RECHERCHE_BRUECKE_QA_20261114.md`

Nach privatem Library-Upload wurden **Patch und komplette Codequelle byteidentisch erneut eingelesen**. Keine privaten Keywordlisten nach GitHub gespiegelt.

**Nächster echter Schritt:** Den vorhandenen MINI-Start/Rückkanal real mit WORDPRESS-Checkpoint 1/2/3 unterbrechen und wiederaufnehmen und anschließend auf bestehender isolierter Testinstallation vollständig bis K0-Entwurf durchlaufen lassen. Ohne echten Endtest: `release_allowed=false`. Kein Neubau.
