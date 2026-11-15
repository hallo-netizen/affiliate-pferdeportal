# Texterstellung 0.4.9: echter Benutzerfehler, verletzter Zielvertrag – NICHT BEHOBEN
Stand: 15.11.2026; Daten von oliver-beil.de aus echten Uploads; noch KEIN freigegebener neuer Release.

## Echte Daten, nicht simuliert
- Diagnose 10:50:41 UTC: `0.4.9-kiss-hard-prune-qa.1`, 61 vorhandene Aufträge, 1 `FREI` und 60 `METADATEN_OFFEN`; 40 Rechercheeinträge, 0 K0-Chargen.
- MINI-Gesamtauftrag `mini-20261115102911-353bdc69d800`: 20 originale `LEGACY_CATEGORY_ONLY` mit 20 eingefrorenen FREI-Entscheidungen und Titeln; 1.024 reale WordPress-Bestandszeilen + 61 reale WordPress-Regal-Einträge, 1.176 Kategorien. Originaldaten vom Nutzer liegen als JSON vor.
- Kategorie-Checkpoint JSON: echte 20 Zuordnungen: 6 Journal, 5 Beratung (FACH), 2 Vergleich, 1 Kosten, 4 Anleitung, 2 weitere MAGAZIN Beratung; 20 individuelle Kategorie-Slugs.
- ECHTER `txe_seo_import` 10:44:39 bis 10:44:44 UTC: 12.591-Byte-Checkpoint, 20 `CATEGORY` ohne Fehler gespeichert. Diagnose meldet `MINI_WORKER_CHECKPOINT_SAVED`, aber alle 61 Aufträge bleiben in 1 FREI / 60 METADATEN_OFFEN.
- ECHTER `txe_export` 10:50:00 UTC: `ACTION_FAILED NO_ORIGINAL_PPM679_BOOKED_ARTICLES`; 0 K0-Batches. Der tatsächliche hochgeladene Diagnosebericht enthält **keine erfolgreiche MINI-FINAL-Importaktion**. Vorherige Annahme, 20 wären endgültig K0-frei, war FALSCH.

## Nachgewiesene Zielvertragsbrüche im Originalcode der installierten Version
1. `miniWorkerCheckpoint()` speichert LEGACY-Kategorie als gesonderten Zwischenstand, fordert `FINAL_IMPORT` in `miniResumeReceipt()` an. Es erzeugt nicht automatisch den Auftrag. `seoImport()` hat dafür einen zweiten, technisch getrennten manuellen Rückgabepfad. Bei 20 vorher definitiv entschiedenen ALT-FREI-Themen unzulässiger zweiter Nutzerimport.
2. `export()` erzeugt keine Aufträge aus gespeichertem Kategorie-Checkpoint, obwohl es nur die eine gültige fertige Kategorieentscheidung gibt, und meldet dann pauschal `NO_ORIGINAL_PPM679_BOOKED_ARTICLES`.
3. `bookOriginalMiniSlot()` und `requireOriginalPpmCapacity()` verlangen `PSERC_Production_Reader::snapshot()`, das zwingend das alte Dateiverzeichnis `portal-production-machine/` mit Versionsnummer 6.7.9 und zahlreichen alten Plankontrakten lädt. **Diese Planabhängigkeit ist nicht KISS-konform.** Aktive Plugins in echter Diagnose enthalten `portal-production-center`, aber KEIN `portal-production-machine`; ob das alte Verzeichnis deaktiviert auf Platte existiert, lässt die Diagnose nicht erkennen.
4. Die 105/105 0.4.9-Vortests haben den K0-Erfolg nur mit **synthetischen** PPM-Plätzen auf **einer** einheitlichen Kategorie/Artikelart simuliert; dies beweist KEINE Eignung für die 20 realen Kategorien und KEIN Vorhandensein eines originalen PPM 6.7.9.
5. Der wirkliche K0-Eingang `PSERC_TEXTMACHINE_METADATA_BATCH_V2` erwartet nur `title,target_keyword,category,article_type,plan_slot`, wobei `plan_slot` 64 Hexzeichen und chargenweit eindeutig ist (`isolated_system4/batch_gate.py` im Repository). Der externe K0-Eingang verlangt dort KEIN historisches signiertes PPM-Slot-Inventar. Die unnötige PPM-Abhängigkeit liegt also in der WP-Plugin-Vorstufe, nicht im nachgewiesenen 5-Felder-K0-Eingang.

## KISS-Implementierungsziel – BEVOR neue ZIP
- Historisches `CATEGORY`-Checkpoint muss den alten endgültig FREI entschiedenen Auftrag unmittelbar im EINEN Regal technisch übernehmen. Kein zweiter Import, keine wiederholte Kategorie/Titel/SEO-Entscheidung. Ein alter einmal gespeicherter Checkpoint muss ohne erneuten Upload automatisch nachgezogen werden.
- `plan_slot` technisch in genau EINER zentralen WordPress-Auftragsstelle stabil vergeben und gegen sämtliche gespeicherten Slot-/Artikel-Identitäten absichern, keine externe abgeschaffte PPM-Planlese-Prüfung. Original-K0-5-Felder unverändert; originaler WordPress-Draft-Importer nach Möglichkeit als reine Schreibfunktion weiterverwenden, ohne alte Pläne als zweite Freigabe.
- Echte 61/20 Eingabedaten für jede positive/negative Simulation einsetzen; nur WordPress-Laufzeit und importierte Artikel-Bodies dürfen mangels tatsächlicher Provider-Daten nachgebildet sein und müssen als solche ausgewiesen werden. Unterbrechung nach jedem Item, erneut gleicher Import, einzelne defekte Zeile, kein Doppelauftrag, keine erneute paid Recherche, keine Live-Version.

**Aktuell:** Zielvertrag NICHT bewiesen; keine Installationsfreigabe. Dieses Audit ist ehrlicher Zwischenstand.