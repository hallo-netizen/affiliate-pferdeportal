# Texterstellung – aktueller installierbarer TESTSTAND

**Version: 0.4.2**, 14.11.2026. **Nur getrennte WordPress-Testseite, keine Live-Freigabe.**

- Die **vorhandene** Version 0.4.1 wurde gezielt korrigiert, nicht neu gebaut.
- Datei (im Projekt-Library-Büro): `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_0.4.2_Altfreigaben_Korrektur_NUR_TESTWORDPRESS.zip`.
- SHA-256: `788271f4ff0d2596d7fa1dabb142973caa55205261cac065c1231bce444be9b7`.
- **164 ursprüngliche PSTE-/PSERC-Dateien unverändert.** 169/172 Altdateien unverändert. Nur `texterstellung.php`, Diagnosetest und README geändert; eine kleine rein technische Abgleichklasse hinzugefügt.
- Originalfreigabe, Original-K0, Draft-Importer, Testmodus, Sperren und planfreier Ablauf bleiben erhalten.
- **Fehlerbehebung der 61 Aufträge:** Der Altimport liest vor der Übernahme einmalig die im **gleichen WordPress** gespeicherten PSTE-Themen anhand der originalen Freigabe-UUID. Er übernimmt nur bereits **abschließend genehmigte, eindeutige** Kategorie/Artikelart und verwendet genau diese ursprüngliche UUID als technische K0-Kennung. Keine neuen SEO-Entscheidungen oder Planungsplätze. Ohne nachgewiesene Originalmetadaten bleiben betroffene Altaufträge gesperrt; kein Raten.
- 117/117 PHP Syntax PASS, 94/94 lokale QA-Kontrollen PASS, darunter 61 tatsächliche Diagnose-Auftragskennungen/Titel gegen nachgebildete persistierte Fakten. **Bei vollständig fehlenden Original-Kategorie-/Artikelartdaten bleiben 61/61 gesperrt; bei 12 genehmigten Originaldatensätzen 12 bereit; bei 61 vollständig genehmigten Quellrecords 61 bereit und 61 QA-Entwürfe.** Diese Varianten sind *simuliert*, keine Behauptung über den wirklichen WP-DB-Zustand oder echte K0-Textproduktion.

**Installation auf derselben separaten Testseite:** WordPress → Plugins → Plugin hochladen → die neue ZIP → bestehendes Texterstellung-Plugin durch neue Version ersetzen, aktiv lassen, **Texterstellung → Redaktionsplan → Bestehende FREI-Freigaben übernehmen**; anschließend **Texterstellung → Diagnose** herunterladen. Keine neue kostenpflichtige Recherche starten. Der Altbestand bleibt gespeichert.

Quellnachweise: [Diff](TXE_042_EXACT_SOURCE_DIFF.patch), [Manifest](TXE_042_MANIFEST.json), [QA-Ergebnisse](TXE_042_QA_RESULTS.json), [technischer Reader](TXE_042_LEGACY_SOURCE_BRIDGE.php), [Hauptdatei](TXE_042_PLUGIN_MAIN.php).

**Noch unbewiesen:** tatsächliche Verfügbarkeit der bestätigten Originalkategorien für alle 61 in der WordPress-Testdatenbank, echter Google/PAA-Abruf, K0 81-Regel-Textlauf, echter WP-Ende-zu-Ende-Probelauf. **Keine Live-Freigabe nach Zielvertrag.**
