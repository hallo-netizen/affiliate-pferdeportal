# Pferdeatelier – aktuelle Texterstellung 0.4.31 / Ursachenfix (18.11.2026)

**Aktueller freigegebener Installationskandidat: 0.4.31.** Auf Live zuletzt durch Nutzerdiagnose bestätigt: **0.4.30**. Eine Live-Installation von 0.4.31 ist **NICHT** nachgewiesen.

## Beweisführung: Screenshot, Diagnosen, Zielvertrag, Quellcode
- Screenshot `Bildschirmfoto 2026-11-18 um 13.17.09.png`: 0.4.29, Live-Recherche mit **5.016 Originalthemen**, Auftragsregal **0**. Das sind zwei getrennte Register.
- Testdiagnose 0.4.27 auf `oliver-beil.de`: **61 Aufträge** (15 EXPORTIERT, 3 FREI, 3 IMPORTIERT, 40 METADATEN_OFFEN). Live-Diagnose 0.4.30 auf `pferde-atelier.de`: **0 Aufträge**, neuer lokaler Recherche-Stand 1. ZIP-Installation überträgt keine WordPress-Optionen zwischen Domains. Ein blindes Übertragen der 61 Testaufträge ist weder erfolgt noch Teil dieses Fixes.
- Live-Diagnose `texterstellung-diagnose-20261118-124900.json`: vorhandene `CATEGORY`-Quittung um 12:46:27 UTC **erfolgreich gespeichert** (held=0); K0-Export versuchte vor weiterer `EDITORIAL`-/`TITLE`-Quittung um 12:47:15 und 12:47:46 UTC und scheiterte jeweils an `NO_K0_READY_ORDERS`.
- Ursprünglicher C-Vertrag 13.11.2026 und MINI-QA 14.11.2026: Einmalige Kategorieentscheidung, eine Redaktion (FREI/BELEGT/KLÄRUNG), ein Titel (nur für FREI), ein WordPress-Auftragsregal, unveränderter 5-Felder-K0-Vertrag, Entwürfe ohne Liveveröffentlichung, keine Zusatz-Worker oder doppelten Prüfungen. Die 0.4.30 hatte nach vollständigen Worker-Quittungen noch den zusätzlichen finalen Importpfad; die Benutzeroberfläche erlaubte K0 auch bei 0 fertigen Aufträgen.

## Umsetzung 0.4.31
- **Ein Workflow, unveränderte drei vorhandene Facharbeiter**. Nach dem letzten nötigen bereits geprüften Worker-Checkpoint wird im **selben bestehenden WordPress-Speichervorgang** automatisch der K0-fertige Auftrag gebucht. **Kein separater vierter FINAL_IMPORT**, keine zweite Entscheidung.
- Bereits vollständig vorliegende 0.4.30-Quittungen können ohne zweite Upload-Datei aus ihrem gespeicherten Bestand technisch fertiggestellt werden. Ein Fehler bei der technischen Platzbindung wird **sichtbar gemeldet**, die gültigen Worker-Quittungen bleiben erhalten und der bestehende Worker kann identisch wiederholt werden.
- WordPress-Übersicht/MINI-Export/MINI-Import zeigen den **nächsten offenen MINI-Schritt**. Bei **0 für K0 bereiten** Aufträgen erscheint keine irreführende Exporttaste; der vorhandene MINI-Auftrag wird fortgesetzt. Keine neue Recherche und keine Datenmigration.
- Magazin weiterhin Bereich, tatsächliche Magazin-Unterkategorie weiterhin Pflicht aus dem eingefrorenen bestehenden WordPress-Kategoriebestand (an der einzigen CATEGORY-Stelle).
- Original-PSTE, PSERC, K0 samt Canonical-Linkregel, DataForSEO, Draft-Import, alle alten Inhalte, andere Portale und Frontend **nicht geändert**.

## Vor Ausgabe geprüfte Nachweise
- `78 / 78` PHP-Syntaxläufe
- `16 / 16` MINI-Altfall-/Kategorien-/Menü-Regressionen
- `38 / 38` bestehende Import-/Diagnoseregressionen
- `48 / 48` echte lokale PHP-Workflow-Gegenproben mit WordPress-Nachbildung: 1 und 3 Themen über CATEGORY/EDITORIAL/TITLE in genau 1 bzw. 3 WordPress-Aufträge und genau 1 bzw. 3 5-Felder-K0-Exporte; 3 eindeutige Slots; Neuimport des gleichen Titels ohne Duplikat; gültige Alteingaben bleiben erhalten; Wiederaufnahme von alten 0.4.30-Quittungen; fehlerhafte Titel, technische Buchungskollisionen, Themen mit KLÄRUNG, falsche Stationsreihenfolge.
- ZIP-Test: **88 Dateien, CRC korrekt, 86 bytegleich zu 0.4.30; nur Hauptdatei und README geändert.**
- ZIP SHA256 `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d`.

**Bestand im bestehenden privaten Pferdeatelier-Pluginbüro** `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`:
- `Texterstellung-0.4.31-KISS-DURCHGAENGIGER-MINI-ABLAUF-PFERDEATELIER.zip`
- `PFERDEATELIER-TEXTERSTELLUNG-0431-GESAMTPRUEFUNG-20261118.md`
- `Texterstellung-0.4.31-WORKFLOW-E2E-48-TESTS.log`
- `Texterstellung-0.4.31-MINI-REGRESSION-16-TESTS.log`
- `Texterstellung-0.4.31-IMPORT-REGRESSION-38-TESTS.log`
- `Texterstellung-0.4.31-PHP-SYNTAX-78-TESTS.log`
- `Texterstellung-0430-zu-0431-NUR-AENDERUNGEN.patch`

## Installationsschritte
1. `pferde-atelier.de/wp-admin` → Plugins → Plugin hinzufügen → Plugin hochladen → ZIP 0.4.31 → Jetzt installieren → **bestehendes Plugin ersetzen, nicht löschen**.
2. Texterstellung → **Übersicht**: 0.4.31 und **Nächster Schritt** kontrollieren. Nach den letzten vorliegenden Liveprotokollen wurde CATEGORY gespeichert und EDITORIAL sollte noch offen sein. **Die aktuelle Anzeige entscheidet.**
3. Texterstellung → **MINI-Export** → bestehenden Auftrag erneut herunterladen; **im selben MINI-Chat** ausschließlich die nächste in `resume_checkpoints` ausgewiesene Entscheidung ausgeben lassen → Texterstellung → MINI-Import. Bei FREI folgt nach Redaktion nur der Titel und dessen Import; danach automatisch WordPress-Regal. Kein vierter Abschlussimport.
4. Texterstellung → K0-Export **nur wenn „Für K0 bereit“ ≥ 1** → JSON → separater K0-Chat mit `K0:start`, Canonical-C-Linkregel und fertigtem Entwurf.
5. Texterstellung → Rückimport → fertige WordPress-JSON ausschließlich als Entwurf. Keine Veröffentlichung.

**Nicht behaupten:** realer Live-Erfolg von 0.4.31, tatsächliche komplette MINI-/K0-Chat-Runde, WordPress-Draft-Import und neue C-Linkregel sind noch NICHT live nachgewiesen. Lokale Tests sind keine echte Live-Abnahme.
