# 19.11.2026 – Hobbydepot Texterstellung 0.4.24.8, DataForSEO Echt-/Testbetrieb als EIN bestehender Einstellungsweg

## Tatsächliche Ursache aus Quellen und Originalcode
- Echtdiagnose `texterstellung-diagnose-20261119-114324.json`: Abschluss `3D-Bogenschießen` mit neun **vollständig sachfremden** Phone/Pizza/SEO-Keywords, alle korrekt BLOCKED, 0 verwertbar. Website-WordPress ist production, aber das sagt NICHTS über den DataForSEO-Betriebsmodus.
- **Original-PSTE** `PSTE_Plugin::defaults()['environment']='sandbox'`, `PSTE_Plugin::settings()` liest `pste_settings_v1` und überschreibt Defaults nur bei gespeichertem Wert. Der Client verwendet `sandbox.dataforseo.com`, wenn der Wert nicht ausdrücklich `production` ist; sonst `api.dataforseo.com`. Das bisherige Hobby-WordPress-Plugin hat Credentials gespeichert, aber keinen sichtbar bedienbaren Modus.
- Der Live-Diagnoseexport der alten Version dokumentiert NICHT den gespeicherten Anbieter-Modus des alten Auftrags. **Die beiden Werte werden nicht erraten.** Offizielle DataForSEO-Sandbox-Dokumentation beschreibt die beobachteten Dummy-Daten als normales Sandboxverhalten.
- Vorherige falsche Empfehlung einer „kostenlosen Recherche bei ausgeschaltetem Haken“ ist korrigiert: Das existierende Formular verlangt `cost_ack` selbst im Sandboxbetrieb. Die Korrektur berührt die Kostenbestätigung nicht.

## 0.4.24.8 – nur zwei vorhandene PHP-Dateien geändert
- Installations-ZIP `Texterstellung_Hobbydepot_0.4.24.8_DATAFORSEO_ECHTDATEN_MODUS.zip`. SHA256 **`0f7cb6e8d35653fcf46aa7d03438d646e9c9f8ea79dbd29d95287f269d44510b`**, **508854 Bytes**.
- **85/87 Dateien bytegleich** mit 0.4.24.7, genau `texterstellung-hobbydepot/texterstellung.php` und `texterstellung-hobbydepot/includes/class-txe-diagnose.php` geändert. Alle Original-PSTE-/K0-/PSERC-/MINI- und Publisher-Dateien unverändert.
- Ein zentraler lesender Modus-Owner `TXE_Workshop::providerModeStatus()`: gibt nur aus dem bestehenden `PSTE_Plugin::settings()` den Modus, Quelle (default vs stored) und den erwarteten Anbieter-Host zurück. Ungültige Einstellungen = UNKNOWN und BLOCKED.
- UI in `Texterstellung → Recherche` und `Diagnose` zeigt **tatsächlichen gespeicherten Modus**; ein Admin kann in **EINEM vorhandenen `pste_settings_v1.environment`-Feld** nach ausdrücklicher Echtdaten-/Kostenbestätigung auf `production` umstellen. Kein neuer Settings-Store, keine zweite Entscheidungsstelle. Save ist reiner WordPress-Settings-Write ohne API/Recherche/Artikel; bestehende andere Werte/alte Forschungsjobs werden unverändert gehalten. Laufende/unklare Jobs blockieren Umschalten.
- Neue Forschungsaufträge sind bei Sandbox/unbekanntem Modus am **zentralen bestehenden Handle-Eingang** gesperrt, damit keine zweite Runde irrelevanter Dummy-Keywords entsteht. Bei production gilt der **unveränderte** separate `cost_ack`-Schutz weiter.
- Diagnoseexport enthält jetzt `environment.dataforseo_provider_mode` (aktueller Site-Settings-Modus) und für jeden lesbaren ursprünglichen abgeschlossen/archivierten Run `original_candidate_reasons.original_provider_mode` aus **dessen originalen persistenten payload.environment**. So ist der 3D-Bogenschießen-Lauf selbst überprüfbar, ohne ihn neu zu starten.

## Testbelege / ehrlich begrenzter Umfang
- **23** Original-WordPress-Stubszenarien zu Default/Store/Invalid, tatsächlich gerenderter Modus-/Kosten-UI, Speichern/Bestätigung/Nonce, anderen Settings unverändert, keine Provider-/Artikelwrites, Sandbox-Neurecherche-Block und nachgelagerter Kosten-Block.
- **4** isolierte read-only historische Runner-Szenarien zum gespeicherten originären `environment`.
- **69** unveränderte Originalprovider-/Archiv-/Timeout-/Recherchetätigkeiten mit neuem Quellbaum nochmals ausgeführt (38 + 31): alle PASS. Zusammen **96 lokale Prüfungen**.
- ZIP **87/87 CRC**, PHP **78/78 Syntax**, JSON **8/8 gültig**, höhere WP-Version, unveränderte WP-Installationswurzel, nachgewiesene genau 2 geänderte Dateien.
- **Kein authentifizierter WordPress- oder DataForSEO-Liveabruf** ausgeführt. Kein E2E-Produktionserfolg behauptet. Die tatsächliche Speicherung und der alte Forschungsmodus können erst nach Installation mit neuer UI / Diagnose abgelesen werden.

## Erfolgreich archiviert
- Zentrales Büro `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.8_DATAFORSEO_ECHTDATEN_MODUS.zip` sowie eigener `Texterstellung-CURRENT.md` und `Texterstellung_0.4.24.8_PRUEFBERICHT.md`.
- Fachbüro `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/` die gleiche ZIP, `PRUEFBERICHTE/` MD/JSON/96-Prüfungsprotokoll und Current.
- 0.4.24.7 verbleibt als Vorgänger unverändert im Archiv.

## Exakt nächster Benutzerweg
1. Sicherung per WPvivid prüfen; **0.4.24.8** via WordPress „Installiertes Plugin ersetzen“ aktualisieren.
2. `Texterstellung → Recherche` zeigt **DataForSEO-Modus** und Host. Wenn **Testbetrieb**, `Echte Daten (Production)` auswählen, Häkchen zur bewusst kostenpflichtigen Produktion setzen und `DataForSEO-Modus speichern`. **Dabei werden NULL Recherchen erzeugt und keine Daten von 3D-Bogenschießen gelöscht oder neu eingestuft.**
3. Wenn Production gespeichert und in der UI sichtbar, danach separat **genau einen neuen offenen Themenbereich** mit zusätzlichem Kostenhaken ausdrücklich freigeben; keinen unbeaufsichtigten 378-Kategorien-Lauf. Wenn ungeeignet: alte Daten anhand neuer Diagnoseregel prüfen, nicht die Schutzregeln lockern.
