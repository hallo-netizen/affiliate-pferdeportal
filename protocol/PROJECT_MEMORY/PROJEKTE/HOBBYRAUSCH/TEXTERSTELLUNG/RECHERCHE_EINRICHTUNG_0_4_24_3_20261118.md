# 18.11.2026 – Hobbydepot Texterstellung 0.4.24.3, EIN vollständiger Einrichtungsweg

**VERBINDLICHER SCOPE:** Bestehendes Plugin, kein Architekturumbau, kein Neubau. Baseline 0.4.24.2 bleibt archiviert. In exakt 3 bestehenden Dateien korrigiert.

## Nachgewiesene Ursache
1. Nutzerdiagnose 0.4.24.1: 0 Aufträge/Recherchen, K0 `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`, alte Testbestätigung auf produktiver Domain.
2. DataForSEO-Credentials laut Nutzer danach gespeichert (nicht erneut abfragen).
3. Originalcode hatte bereits `PSTE_Safe_Migration_Job::start/advance`, `PSTE_Context_Refresh::start/processBatch` und `PSTE_Snapshot::siteBaseline`, aber keine Bedienung der Migration im Texterstellungs-Menü.
4. Originalkopie-Fachdatei `original/pste/fixtures/portal-category-map-v1.json` war `WORKCOPY_NOT_BOUND`, 0 Einträge, leeres SHA; originaler Loader blockierte 0 Einträge. Dies war ein weiterer bislang übersehener Quellfehler.

## Durchgeführt
- `texterstellung-hobbydepot/texterstellung.php`: WordPress-Version **0.4.24.3**. Ein Startbutton **Texterstellung → Recherche → „Recherche-Einrichtung abschließen“**. Admin + gültiger WordPress-Nonce + bestehende Sitefreigabe. Browser steuert *dieselben* originalen PSTE-Migration-/Kontextjobs requestbegrenzt bis COMPLETE, gespeicherte Fehler bleiben fortsetzbar. Kostengate bleibt beim späteren Recherchestart. Vor Migration wird vorhandener WordPress-Kategoriesnapshot einmalig validiert und gespeichert; unklare Kategoriezuordnung stoppt VOR dem Migrationsstart. Am Ende wird nur die vorhandene Recherche-Option `feature_enabled` aktiviert, ohne Recherche-/Provideraufruf.
- `original/pste/includes/class-pste-portal-category-map.php` und `original/pste/fixtures/portal-category-map-v1.json`: Null geschützte Pferde-Kategorien gelten nur als **explizit signierte Hobby-Dynamikvariante** (Hash `a32f5a7b62ec009350739bcd02289220574e545cf2c8985e525ad6ff4f306475`). Die fachliche Kategorieauflösung bleibt allein bei dem alten `PSTE_Snapshot`; kein Ersatz-Kategoriebaum, keine neuen Entscheidungen, unpassende Strukturen bleiben BLOCKED.

**84 von 87 Datei-Inhalten byteidentisch** zu 0.4.24.2, **keine zusätzlichen PHP-Dateien**, kein K0-/PSERC-/MINI-/Entwurfsschutz-Umbau. Bestehender Testseiten-Sicherheitsnachweis bleibt technisch aktiv, aber die zuvor unerwünschte Testmaske war bereits in 0.4.24.2 aus der UI entfernt.

## Lokale Nachweise
ZIP 87/87 CRC, PHP 78/78, JSON 8/8 PASS; 3 Boot, 25 Funktionen, 5 PSERC Rückimport, 13 UI/Gates, 7 neue Negativ-/Map-Prüfungen, 1 positiver originaler gesicherter Migrationsstart, JS Syntax => **54 lokale Einzelprüfungen PASS** (plus JS Syntax). 0 tatsächliche DataForSEO-Provideranfragen, 0 WP-Artikelwrites in Tests.

**Grenze:** Keine authentifizierte echte WordPress-Datenbank, daher weder live Kategorie-Snapshot noch vollständiger sicherer PSTE-Migrations-/Kontextlauf bewiesen. Der angelegte Ablauf ist lokal getestet, die tatsächlich unterstützte Portalstruktur wird erst vom Originalcode auf WordPress selbst geprüft. Externe K0-Typautorität noch `K0_PORTAL_ADAPTER_PENDING` / `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`, daher **KEINE vollständige K0-Textproduktionsfreigabe**. Keine künstliche Umgehung dieser Sperre.

## Aktuelles installierbares Plugin und Büro
- `Texterstellung_Hobbydepot_0.4.24.3_RECHERCHE_EINRICHTUNG.zip` SHA256 `e5674fb897cc9ca4d4594d7c8ca2a1621d92535a8651815535040005fecb78d4`, 503882 Bytes.
- Verzeichnispfad unverändert `texterstellung-hobbydepot/texterstellung.php` (WordPress „Ersetzen“ 0.4.24.2).
- Zentrales Dateienbüro `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.3_RECHERCHE_EINRICHTUNG.zip` und separater Fachordner `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/` sind **tatsächlich erfolgreich geschrieben**.
- Eigene Current-Datei `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` aktualisiert, globales CURRENT anderer Plugins nicht überschrieben. Prüfbericht `/Hobby Depot/Plugin-Büro/Texterstellung_0.4.24.3_PRUEFBERICHT.md`, Fachkopie im Texterstellungsbüro.

## Nächster Nutzerkontakt
Ein WordPress-Backup vor Migration sicherstellen; 0.4.24.3 per „Ersetzen“ installieren. **Texterstellung → Recherche → Recherche-Einrichtung abschließen** einmalig klicken und Seite offen lassen, bis fertig oder konkrete Fehlermeldung. **Keinen weiteren Diagnosebericht verlangen**, die ursprüngliche Diagnose liegt vor und wurde geprüft. Nach Abschluss kann die Recherche mit ihrem originalen Kostenhaken gestartet werden, aber **K0 bleibt gesperrt**, bis die externe Artikelarten-/Kategorienfreigabe belegt ist.
