# Pferdeatelier – exakt gelesener Test-Pluginstand am 02.11.2026

**NUR TEST – keine LIVE-Freigabe, keine behauptete vollständige WordPress-K0-E2E-Freigabe.**

## Erstmals erfolgreich aus der bestehenden Benutzer-Library ausgelesene Binärquelle
- WordPress-Backend vom Betreiber gezeigt: **Test oliver-beil.de: Portal SEO Themenengine 0.57.143**; **Live pferde-atelier.de: 0.57.120**.
- Vollständige physische Original-ZIP aus **bereits vorhandener Library**:
  `/Pferdeatelier/INSTALLATIONS_PAKETE/PFERDEATELIER_PSTE_0.57.143_RUECKSTELLUNGEN_PROTOKOLL_NUR_TEST.zip`
- Original-SHA256: `328b82ff2c01eb549c2f4ff72347ba6798a6d0d990c09b9d572450e526a17d68`. **116 Archivdateien; 78 PHP-Dateien**.
- Liveoriginal ebenfalls gelesen, aber unverändert:
  `/Pferdeatelier/INSTALLATIONS_PAKETE/PFERDEATELIER_PSTE_0.57.120_KISS_TEST_INSTALLIEREN.zip`.
- **Die vorherige Behauptung, man könne überhaupt keine vollständige aktuelle Quelle auslesen, war nachweislich falsch.** Der externe Campus-Ausgabeschrank ist nicht in die Bibliothek gemountet; das genaue installierte Test-Original war aber über den *vorhandenen* `/Pferdeatelier/INSTALLATIONS_PAKETE` erreichbar.

## Isoliertes volles Test-WordPress-Paket, wirklich aus 143-Original gebaut
- Testversion **0.57.143.1**: `/Pferdeatelier/TempVerify/PFERDEATELIER_PSTE_0.57.143.1_ZENTRALE_PRUEFUNG_NUR_TEST.zip`.
- SHA256 `c3d4060e6a2a248e36ba963a0ae94e5b75e4b029e5b0c36991a81aaad9aef5e3`.
- Verglichen mit exakt gelesener Original-ZIP: **116/116 Dateien erhalten, 109 bytegleich**, 7 gezielt geändert einschließlich Hauptplugin-Versionsdatei. ZIP-Integrität PASS.
- Änderungen im BESTEHENDEN Code, keine neuen Worker/Rules: einheitliche Suchanfrage und ein zentraler Cannibalization-Owner; Sandbox-/Familien-Zweitentscheidung entfernt und finaler Gate-PASS bei Sandbox-Reentry vor Hochstufung; normaler Metadatenweg nur einmal; stabile Compilerseiten-ID.
- Nachvollziehbare vollständige Testbeschreibung unter `/Pferdeatelier/TempVerify/PFERDEATELIER_PSTE_0.57.143.1_GESAMTABLAUF_PRUEFBERICHT_20261102.md`.
- 78/78 PHP-Syntaxprüfungen PASS. Tatsächliche PHP-Klassen + simulierte WP-Daten: 5.146 Testaussagen, 5.014 Themen in Seitenreihenfolge, 12 Reentry-POS/NEG, 16 PSERC-K0-Metadatengrenzen PASS.
- **Kein** tatsächlicher Test mit verbundenem WordPress-Server oder vollständigem realen K0-Writer; Live unverändert.

## Harte offene Punkte statt erfundener Fertigmeldung
- `PSTE_Context_Evaluator` trifft weiterhin mögliche `ANSWER_EQUIVALENT_EXISTING/PLANNED`-Abdeckungsentscheidungen außerhalb des zentralen Readiness Owners; hier könnte eine weitere doppelte oder widersprüchliche Fachentscheidung auftreten. Nicht blind entfernen: der Kontext enthält auch geplante Artikel, deren Schutz die Zentralprüfung nachweisen muss.
- Optionale `PSTE_Article_Ownership_Gate` via PSERC-Compiler hat eigene upstream semantische Eigentums-Bindung und Legacy-Overlap; Fachrolle gegenüber der zentralen Planung klären.
- WordPress oliver-beil.de tatsächlich mit 143.1 installieren, kritische E2E-Routen gegen echte Themen/Planbestände prüfen, externen Titel Export/Import und PSERC→K0 mit echter Datei überprüfen. **Keine Liveinstallation**.
- Intern dokumentierte 0.57.164 war **ein historischer QA-Arbeitsstand**, nicht die Betreiber-installierte Testversion; Sperrung des rekonstruierten 0.57.165 bleibt bestehen. Keine Rekonstruktion aus 164 oder 165 für diese Testerstellung.
