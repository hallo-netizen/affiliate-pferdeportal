# PFERDE-ATELIER – BÜRO PLUGINS

<!-- CAMPUS_SINGLE_TRUTH_ENTRY_V1 -->

## ERSTER SCHRITT BEI JEDEM CHATWECHSEL: ORIGINAL TATSÄCHLICH LESEN

**Nicht bei GitHub nach einer externen Binärdatei suchen:** Laut verbindlichem `SYNC_VERTRAG.md` liegt `/Campus-Plugins/PFERDE_ATELIER/PPA-005/CURRENT.zip` im **separaten persistenten Plugin-Schrank**, während GitHub nur Steuerung und Inventar enthält.

Vor Aussagen wie „Original vorhanden“, „ich kann das Plugin lesen“, „Original aktuell geprüft“ oder vor Paketbau: die **echte vollständige ZIP im physisch verbundenen Plugin-Schrank** öffnen, alle Einträge prüfen und den SHA256 der tatsächlichen Datei gegen die geltende Current-Bindung abgleichen. Ein in GitHub eingetragener Pfad, eine SHA-Zeichenfolge, ein alter QA-Bericht oder ein erfolgreiches `--metadata-only` beweisen ausdrücklich **keinen Zugriff auf die Binärdatei**.

**Zugriffsdiagnose 02.11.2026:** In der hier verbundenen Files-Library ergab das direkte Öffnen von `/Campus-Plugins/PFERDE_ATELIER/PPA-005` die Meldung `Library path not found`. Das ist eine **fehlende Verbindung zu diesem Ablageort in diesem Arbeitskontext**, **kein** Beweis für gelöschte oder nicht existierende Originaldateien. GitHub-404 ist für diesen separaten Schrank kein Gegenbeweis. Den Standort nicht neu erfinden, keine alten ZIPs als Ersatz und keine zusätzlichen Prüfer-Plugins bauen. **Nur tatsächlichen externen Schrankzugang klären; bis zum physischen Readback kein Installer.** Bei neuem Zugriff erneut prüfen; diesen zeitbezogenen Fehler niemals als dauerhafte Aussage behandeln.

## HARD RULE – EINE CURRENT-AUTORITÄT

Diese Bürotür ist **nur Navigation**.

Pflichtweg:
`START_HERE → protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json → genau eine Current-Autorität → Frischecheck → deren NEXT ACTION`.

`HOBBYRAUM.md` ist nur eine abgeleitete Ausführungsfläche und niemals Quelle für den aktuellen Status oder die NEXT ACTION.

Bei frischer unveränderter Current-Bindung: **keine Vollrekonstruktion**.
Bei belegter Änderung: **nur Delta prüfen**.



## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das zentrale Plugin-Büro des Pferde-Ateliers. Es hält den Überblick über alle im Pferde-Atelier verwendeten/entwickelten Plugins und deren isolierte aktuelle Ausgabeartefakte.

**HIER BIST DU RICHTIG, WENN …**  
du ein Pferde-Atelier-Plugin finden, den aktuellen isolierten Pluginstand entnehmen oder nach einer echten Pluginentwicklung/-aktualisierung den Ausgabestand synchronisieren willst.

**DU DARFST …**  
die autoritative Fach-/Releasequelle frisch lesen, daraus ein isoliertes Pluginartefakt ableiten, hashen, prüfen und im Ausgabeschrank aktualisieren.

**DU DARFST NICHT …**  
hier Fach-/Release-/LIVE-Wahrheit neu erfinden, aus alten Mastern raten, allgemeingültige Module zu Pferde-spezifischen Modulen umklassifizieren oder Secrets speichern.

**ALS NÄCHSTES …**  
`AUTORITAETSPLAN.json` → Current-Autorität → Frischecheck → NEXT ACTION → ggf. `HOBBYRAUM.md` → `REGISTER.md` → bei Artefaktarbeit `SYNC_VERTRAG.md`.

## Rolle

Das PLUGINS-Büro ist Inventar-, Update- und Ausgabepult.

Autoritative technische/Fach-/Release-/LIVE-Wahrheit bleibt immer im zuständigen Fachbüro bzw. an dessen gebundener technischer Hauptquelle.

Die physischen Plugin-ZIPs liegen persistent im zentralen Ausgabeschrank:
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/CURRENT.zip`

Dazu liegt jeweils:
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/MANIFEST.md`

Diese Dateien sind ausschließlich hashgebundene, abgeleitete Ausgabekopien des autoritativen Stands.

## Klassengrenze

Allgemeingültige Plugin-Kerne bleiben unter `ALLGEMEINGUELTIGE_BAUSTEINE/` autoritativ.
Eine Kopie im Pferde-Atelier-PLUGINS-Büro bedeutet nur: dieses Plugin wird im Pferde-Atelier verwendet. Sie ändert die Modulklasse nicht.

Pferde-spezifische Plugin-Kerne bleiben fachlich im jeweiligen Pferde-Atelier-Büro autoritativ.

## Harte Vorsperre

Vor jeder technischen Aktion:
`protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → relevante autoritative Fehlerquelle frisch lesen.
Treffer = bekannten Fehlerweg nicht wiederholen.

## Zentrale Leitungen

- Handlungsweg: `protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md`
- Fehlerwegweiser: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum/Änderungen: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Zielverträge: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`

## Abschlussregel

Wenn ein Chat tatsächlich ein Plugin entwickelt oder aktualisiert hat, muss vor Abschluss geprüft werden, ob dessen isolierte `CURRENT.zip` + `MANIFEST.md` im zentralen Ausgabeschrank auf den neuen belegten Stand synchronisiert wurden.

Kann der aktuelle Pluginstand nicht vollständig und eindeutig aus der autoritativen Quelle erzeugt/bezogen werden: nicht raten, bisherigen Stand nicht ersetzen, `Plugins: BLOCKED`.


## Neueste Teststand-Übergabe 08.11.2026 – PSTE/PSERC (maßgeblich)

**Zuerst [CURRENT_STATE.md](CURRENT_STATE.md), Abschnitt „AKTUELLER REALSTAND – 08.11.2026 16:05 BERLIN“, lesen.** Danach [EVIDENCE/ISTSTAND_20261108_1605_EXTERNE_SEO_WEG_UXDATEN.md](EVIDENCE/ISTSTAND_20261108_1605_EXTERNE_SEO_WEG_UXDATEN.md) und [INSTALLATIONS_PAKETE/TESTPAAR_20261108_ARCHIV/MANIFEST.md](INSTALLATIONS_PAKETE/TESTPAAR_20261108_ARCHIV/MANIFEST.md) lesen. Der Betreiber hat beide Testplugins installiert und zweimal echte MINI-Exportdateien geliefert; die zweite enthält 1.179 technisch vorhandene Einträge, aber noch inhaltlich defekte 9 Editorial-/144 PPM679-Titel. Kein externer SEO-Owner-Lauf und kein Rückimport. **Keine erneute Diagnose, keine erneuten Screenshots/Uploads oder Plugininstallation anfordern.** Die Test-ZIPs liegen als echte Binärdateien in der privaten Dateiablage `/pferdeatelier/PLUGINS/`, in GitHub mit Hash und Status eingetragen. Nicht mit der älteren GitHub-Installations-ZIP oder autoritativen `CURRENT.zip` verwechseln. K0 bleibt unverändert; Draft-PR #682 nicht mergen.


## NEUESTER STAND 08.11.2026 – PSTE 0.57.144.23 QA, 36 lokale PASS

**Nach dem 1.179er echten WordPress-Export wurde PSTE 0.57.144.23 als neues isoliertes Testplugin gebaut.** Die Binärdatei ist tatsächlich in der privaten Library `/pferdeatelier/PLUGINS/PSTE-0.57.144.23-EXPORTFIX-NUR-TEST.zip`; das Paar mit unverändertem PSERC 0.28.55 ist auch gesichert. Der vollständige Quellcode-Patch, Simulation, SHA und 36 PASS stehen auf GitHub unter `QA_ONLY/PSTE_05714423_EXPORTFIX/` und [Prüfbericht](EVIDENCE/PSTE_05714423_ECHTER_EXPORT_FIX_36_LOKALE_WORKFLOW_TESTS_20261108.md). **Die neue ZIP ist NOCH NICHT auf WordPress installiert und kein vollendeter echter WP-End-to-End-Test.** Noch 9 unlesbare gespeicherte Editorial-Titel und 3 PPM-Postverweise; kein blindes FREI, keine erfundenen Titel. **Keine erneute 5.016er Gesamtdiagnose, kein Keyword-Rohimport, keine neuen Aufgaben an den Nutzer zum Wiederholen bereits erledigter Schritte!** K0 unverändert, PR #682 Draft.


## Aktuellster QA-Stand 08.11.2026 – PSTE v0.57.144.24 (nicht live installiert)

Nach realem .23-WordPress-Export vom 08.11. 16:03 UTC wurde **das globale Abbrechen bei neun unlesbaren Editorial-Plan-Titeln ursächlich im bestehenden Mini-Parkhaus-Reader korrigiert**. **Alle 1.179 realen Parkhaus-Quellenzeilen bleiben in der lokalen Simulation sichtbar**, unlesbare **9 + 3** Einträge sind weiterhin für fachliches FREI gesperrt. 46 lokale PHP-Tests bestanden, 83 Lints, CRC 121. Privat archiviertes .24-Test-ZIP: `/pferdeatelier/PLUGINS/PSTE-0.57.144.24-PARKHAUS-QUELLFIX-NUR-TEST.zip`. GitHub hat [exakten Test-/Quellbericht](EVIDENCE/PSTE_05714424_1179_ECHTE_QUELLEN_46_LOKALTESTS_20261108.md), QA-Patch und Bau-/Testquellen in `QA_ONLY/PSTE_05714424_QUELLFIX/`. **Nur aktuelle oben in CURRENT_STATE dokumentierte Version als nächstes isoliert testen.** Die .24-ZIP ist noch nicht in WordPress installiert. Kein weiterer globaler Keywordlauf, keine neue Gesamtdiagnose, kein Rückimport, kein K0-Schreibzugriff, Draft-PR #682 nicht mergen.


## AKTUELLSTER WORDPRESS-ECHTTEST 08.11.2026 16:29 UTC – PSTE .24 bestätigt

**Nicht erneut .24 installieren und keine weitere JSON anfordern!** Betreiber hat PSTE .24 auf TESTseite installiert und `pferdeatelier-mini-ergebnisse-20261108-162920.json` geliefert. **1.179/1.179** Einträge und alle sechs Originalquellen erfasst, **55 lokale PHP-Replay-Checks bestanden**, aber der Fach-Freigabe-Status bleibt `complete=false` wegen exakt **9 identischen völlig inhaltslosen „Array“-Platzhaltern** und **3 nicht lesbaren alten PPM679-Post-IDs**. Die neun vollständigen Altrecords sind byte-inhaltlich durch SHA-Rückrechnung belegt; keinerlei rekonstruierbarer Titel, Artikel-ID oder Slot. Drei PPM-Slots bleiben besetzt. Jetzt **Quelle Option/Filter** der 9 und Archiv-/ID-Zuordnung der 3 klären, nicht an Freigabechecks vorbei arbeiten. Dokument: [aktueller 55-PASS-Echtbericht](EVIDENCE/PSTE_V24_ECHTER_WP_EXPORT_162920_REPLAY_55PASS_20261108.md); Quellskript unter `QA_ONLY/PSTE_05714424_QUELLFIX/LIVE_WP_20261108_162920/`, Original-JSON privat. Keine neue Pluginversion, kein K0-/Live-Schreibzugriff, Draft-PR #682 nicht mergen.
