## 19.11.2026 09:45 – NEUER LIVE-SICHTSTAND: RECHERCHEOBERFLÄCHE VERFÜGBAR

- Echter Screenshot der Hobbydepot-WP-Rechercheoberfläche: **keine Einrichtungs-Blockermeldung mehr sichtbar**; **379 offene Themenbereiche**, **0 recherchiert**, **0 Fehler/gesperrt**; **2.241 von 2.241 Artikelkategorien zugeordnet**, WordPress insgesamt **3.520 Kategorien**; **0 gespeicherte Originalthemen**, **0 Aufträge**. Nächstes Thema **3D-Bogenschießen**, Anzahl **5**.
- Recherche aktuell **GESTOPPT / PLUGIN_ACTIVATED_MANUAL_START_REQUIRED**, keine automatische Wiederaufnahme, kostenpflichtige DataForSEO-Checkbox **nicht aktiviert**. Kein Providerlauf/keine K0-Produktion gestartet. Alte bestätigte Credentials nicht erneut anfordern.
- **Maßgebliches Plugin unverändert 0.4.24.5** `Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip` im zentralen Pluginbüro und Fachbüro. Archivkopie aus Büro geöffnet: **506.541 Bytes**, SHA256 `42f648b59a99fda0b1684c0e174a9430f4d9d131eaa8d98548157c5d8e09e2ba`, **87/87 ZIP-CRC**, 78 PHP, 8 JSON, WP-Ordner `texterstellung-hobbydepot`, Header **0.4.24.5**. Keine neue Version/Änderung.
- Büro-eigene `Texterstellung-CURRENT.md` aktualisiert, neue Standakte `Texterstellung_Stand_20261119_0945.md` in beiden Dateibüros gespeichert. Ausführliche GitHub-Akte `SCREENSHOT_RECHERCHE_379_OFFEN_20261119_0945.md`.
- **Grenzen:** Screenshot beweist keine exakte laufende Pluginheader-Version oder komplette DB-Integritätsabnahme; K0-Artikelarten weiterhin bisher BLOCKED, keine automatisch angenommene Freigabe. Nächste mögliche Arbeit ist die kontrollierte Kategorien-Recherche nach ausdrücklicher Kostenfreigabe; keine blind gestartet.
---

## 19.11.2026 – AKTUELL UND MAẞGEBLICH: 0.4.24.5, realen Sandbox-Migrationsfehler gezielt korrigiert

- **Live-Screenshot:** `PSTE_CONTEXT_BLOCKED_PSTE_SANDBOX_RECORD_STORE_LEGACY_OPTION_MISSING`. Direkter Fehler im Original `PSTE_Sandbox_Record_Store::sourceMetaCheap()`; fehlende Altoption bei frischem Portal, obwohl Original-`PSTE_Semantic_Review_Sandbox::stored()` leeren Ausgangszustand kennt. Zusätzlich blockierte TXE-AJAX bereits `BLOCKED` vor erlaubter Original-Fortsetzung.
- **Aktuelle einzige Ersatz-ZIP** `Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip`, SHA256 `42f648b59a99fda0b1684c0e174a9430f4d9d131eaa8d98548157c5d8e09e2ba` / 506541 Bytes, Wurzelordner `texterstellung-hobbydepot`, Version `0.4.24.5`.
- Exakt **4 vorhandene Dateien verändert, 83/87 identisch** zu 0.4.24.4: signierten Original-Leerbestand nur beim tatsächlichen Fehlen einmalig anlegen, Original-Streammigration, eng erlaubte BLOCKED-Job-Fortsetzung und AJAX-Weiterleitung. **Keine neue Architektur und kein K0-/Recherche-/Datenspeicher-Schutzabbau**.
- Belege: Originalsource-Tests (9/9), echte leere Original-Sandbox-Migration bis COMPLETE, 12 echte Kontext-`processBatch`-Aufrufe mit unveränderter UUID bis COMPLETE (nachgelagerte WP-/Indexdaten simuliert), gerendertes Browser-JS → PHP-AJAX → COMPLETE, alter Nullthemen-Test 12/12, bestehender 1-Datensatz-Speicher unverändert, beschädigter Speicher gesperrt; PHP 78/78, JSON 8/8, ZIP 87/87. **KEIN Live-WP-E2E-Test**.
- Zentrales Pluginbüro `/Hobby Depot/Plugin-Büro/` und Fachbüro `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/` **erfolgreich gespeichert und unveränderte ZIP aus Library zurückgelesen**; eigene `Texterstellung-CURRENT.md` und Prüfbericht aktualisiert. Vorherige 0.4.24.4 archiviert.
- **Nächster Klick:** Sicherung prüfen, **0.4.24.5** hochladen und vorhandenes Plugin ERSETZEN, `Texterstellung → Recherche → Vorhandene Einrichtung fortsetzen` einmal; keine neue kostenpflichtige Recherche, kein neuer K0-Lauf, keine Credentials oder Diagnose erneut anfordern.
- Vollständige Beweise `LIVE_SANDBOX_LEGACY_OPTION_MISSING_FIX_0_4_24_5_20261119.md` und `/Hobby Depot/Plugin-Büro/Texterstellung_0.4.24.5_PRUEFBERICHT.md`.

---

## 19.11.2026 – AKTUELL: 0.4.24.4 gegen LIVE-MIGRATIONSFEHLER (vorgeprüft, noch nicht auf Live abgenommen)

- **Vom Betreiber real gemeldeter Stop:** `PSTE_EDITORIAL_RULESET_RAW_KEYWORD_INVARIANT_FAILED`. Das war trotz vorheriger „54 Tests“ NICHT mit echtem PSTE-Nullthemenbestand getestet worden. Diese vorherige Test-/Freigabeaussage war zu weitgehend.
- **Reproduzierbarer Originalbug:** 0.4.24.3 überspringt `EDITORIAL_RAW_BASELINE_BATCH` bei 0 Themen, verlangt aber genau diese Baseline später. Original PHP wirft exakt gemeldeten Fehler. **Ob die echte WP-Tabelle 0 Themen enthält, ist nicht aus dem Server bestätigt; dieser Fehlercode kann auch Daten-Drift bedeuten.**
- **Version 0.4.24.4** (ZIP `Texterstellung_Hobbydepot_0.4.24.4_MIGRATION_NULLBESTAND_FIX.zip` SHA256 `8ee94512c7b8e9dc84d82bdc65b9641aea7057825528709b1546f369eb7e8e69` / 504008 Bytes) repariert nur zwei Originalfunktionen: Baseline auch bei 0 Themen; streng begrenzte Altjob-Fortsetzung ohne Umgehen anderer Datenintegritätschecks. Dritte Datei: Versionsheader. 84/87 bytegleich, keine Architektur, kein K0-/Import-/Recherche-Umbau.
- **Tests:** 12 gezielte Original-PHP-Funktionstests PASS einschließlich bestehendem `PAUSED_ERROR` bis `COMPLETE` mit derselben UUID in WP-Datenbank-Mocks, falsche Werte weiterhin BLOCKED; 2 gerenderte JS/AJAX-Tests; PHP 78/78, JSON 8/8, ZIP 87/87. **Keine Live-DB-Verifikation, keine überzogene 100%-Behauptung.**
- **Pluginbüro erfolgreich gespeichert:** `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.4_MIGRATION_NULLBESTAND_FIX.zip` sowie Fachbüro `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`. `Texterstellung-CURRENT.md` im echten Pluginbüro aktualisiert, Bericht dort und im Fachbüro; alte 0.4.24.3 archiviert.
- **Einziger nächster Schritt:** WP-Datenbanksicherung prüfen, 0.4.24.4 über **Ersetzen** installieren und `Texterstellung → Recherche → Vorhandene Einrichtung fortsetzen` einmal ausführen. Bei Abbruch ohne Wiederholungsversuche die echte Migrationsphase und Themenzahl auslesen; keine neue Recherche starten.
- Ausführlicher Beleg: `LIVE_FEHLER_NULLTHEMEN_MIGRATION_0_4_24_4_20261119.md`.

---

## 19.11.2026 – AKTUELL: BUTTON-KLICKWEG 0.4.24.3 GEPRÜFT, KEIN NEUER BUILD

- Nutzer verlangt wegen des Hab-&-Bewahr-Fehlers am Button `Recherche-Einrichtung abschließen` eine erneute SIMULATION vor Liveeinsatz. Bei Hab war ein JavaScript-Syntaxfehler im tatsächlich ausgegebenen Seitencode nachgewiesen; **das ist kein Beleg für denselben Fehler in Hobbydepot**.
- Aktuelle Hobbydepot-ZIP `Texterstellung_Hobbydepot_0.4.24.3_RECHERCHE_EINRICHTUNG.zip` im Pluginbüro **bytegenau überprüft**, SHA256 `e5674fb897cc9ca4d4594d7c8ca2a1621d92535a8651815535040005fecb78d4`, 87 valide ZIP-Dateien. **Keine Codeänderung/keine neue Version.**
- Echter PHP-UI-Render + JS-Syntax, Klick-Event, Fetch an `admin-ajax.php`, Fortschritt/Weiterleitung, Serverfehlerdarstellung und Netzwerkfehler: alle lokalen Tests PASS. AJAX-Handler `TXE_Workshop::ajaxSafeMigration()` mit PSTE-/WordPress-Mocks inklusive Baseline/Kontext/Fehlersperren getestet, Browser ↔ AJAX Kopplung 3 Requests PASS. **Nicht** als echter WordPress-/MySQL-E2E-Nachweis ausgeben.
- Ergebnis: der konkret in Hab aufgetretene Nichtreaktionsfehler ist in der aktuellen Hobbydepot-Version **nicht reproduzierbar**. Datengesteuerte Blocker der tatsächlichen WordPress-Kategorien bleiben ungeklärt; kontrolliertes Stoppen statt willkürlicher Freigabe.
- Bericht im zentralen Pluginbüro `Texterstellung_0.4.24.3_KLICKWEG_PRUEFBERICHT_20261119.md`, Fachbüro `HOBBYDEPOT_04243_KLICKWEG_BROWSERSIMULATION_20261119.md`, GitHub `KLICK_SIMULATION_0_4_24_3_20261119.md`. **Aktuelles Plugin bleibt unverändert 0.4.24.3.**
- Nutzer-Klickpfad (falls 0.4.24.3 schon installiert): `Texterstellung → Recherche → Recherche-Einrichtung abschließen`, einmal; darunter muss `Einrichtung gestartet …` erscheinen und danach Fortschritt/Blockermeldung. Kein echter WordPress-Klick wurde hier ausgelöst.

---

## 18.11.2026 – AKTUELL: Texterstellung 0.4.24.3, Recherche-Einrichtung in EINEM Bedienvorgang

- **Neue einzige aktuelle Ersatz-ZIP** `Texterstellung_Hobbydepot_0.4.24.3_RECHERCHE_EINRICHTUNG.zip`, SHA256 `e5674fb897cc9ca4d4594d7c8ca2a1621d92535a8651815535040005fecb78d4`, 503882 Bytes. WordPress-Pfad unverändert `texterstellung-hobbydepot/texterstellung.php`; gültige höhere Version als 0.4.24.2.
- **Büroablage erfolgreich:** `/Hobby Depot/Plugin-Büro/` sowie `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`; auch `Texterstellung-CURRENT.md` und Prüfbericht im zentralen Pluginbüro neu gespeichert. Alte ZIPs Archiv.
- **Exakt 3 bestehende Dateien geändert, 84/87 byteidentisch, keine Architekturänderung.** Vorhandene sichere PSTE-Migration, vorhandener Kontextjob, vorhandener WordPress-Kategoriesnapshot werden per 1 Admin-Klick `Texterstellung → Recherche → Recherche-Einrichtung abschließen` nacheinander ausgeführt. Fortsetzen/Rechenfortschritt vorhanden, keine DataForSEO-Kosten bei Einrichtung, K0-/PSERC-/Entwurfsschutz unverändert.
- Die bisher ungebundene 0-Einträge-Pferde-Schutzkarte war nicht validierbar; jetzt nur für ausdrücklich signiertes Hobby-Nullschutz-Profil zulässig. Die Originalfunktion entscheidet weiterhin allein auf Basis der echten WordPress-Kategorien. Wenn keine eindeutigen Kategorien erkennbar: **harte Sperre vor Migration**, keine erfundenen Entscheidungen.
- **54/54 lokale Tests PASS**: 3 Boot, 25 Funktion, 5 PSERC, 13 UI, 7 Migration Negativ, 1 positiver langlebiger Migrationsstart; PHP 78/78, JSON 8/8, ZIP 87/87, JS Syntax. **Noch kein authentifizierter WordPress-E2E-PASS**.
- Credentials nach Nutzerangabe gespeichert, keine erneute Aufforderung; alte Diagnose bereits bekannt. Externe K0-Artikelarten weiterhin **BLOCKED** (separater K0-Vertrag nicht ändern/freigeben).
- Nächste konkrete Aktion: vor DB-Migration WPvivid-Backup, 0.4.24.3 mit WordPress-„Ersetzen“ installieren, dann **einen Klick „Recherche-Einrichtung abschließen“**. Webseite geöffnet lassen. Kostenpflichtige Suche nur mit bereits vorhandenem Kostenhaken später. Kein weiterer Testplugin-Zwischenstopp.
- Beleg `RECHERCHE_EINRICHTUNG_0_4_24_3_20261118.md` und `/Hobby Depot/Plugin-Büro/Texterstellung_0.4.24.3_PRUEFBERICHT.md`.

---

## 18.11.2026 – DataForSEO-Zugangsdaten vom Betreiber eingetragen; nächster echter Blocker PSTE-Migration

- Betreiber hat die DataForSEO-Zugangsdaten im bestehenden Plugin **nach eigenen Angaben gespeichert**. Nicht nochmals nach Login/Passwort oder Diagnose fragen. Tatsächliches Speichergebnis noch nicht durch neue Live-Diagnose bestätigt.
- Verbindliche 0.4.24.2-Quellprüfung: `txe_credentials_save` speichert nur die Schlüssel über `PSTE_Credentials::saveFromAdmin`; es startet keine kostenpflichtige Recherche. `TXE_Workshop::activate()` legt den bewusst manuell gestoppten Zustand `PLUGIN_ACTIVATED_MANUAL_START_REQUIRED` an. Der „Status einmal aktualisieren“-Link ist nur eine GET-Aktualisierung, **kein** Migrations- oder Freigabeknopf.
- Das aktuelle echte WordPress-Screenshot zeigt **„Die originale PSTE-Migration ist noch nicht abgeschlossen“**. Laut Source verhindert `PSTE_Plugin::isReady()===false` die Kategorie-Recherche, und `txe_research_next` würde bei manuellem Start `ORIGINAL_PSTE_MIGRATION_REQUIRED` zurückgeben.
- Die unveränderte Original-PSTE besitzt bereits `PSTE_Safe_Migration_Job::start()` und `::advance()`, aber die aktuelle TXE-Adminoberfläche registriert nur `txe_research*`, `credentials_save` und weitere vorhandene Aktionen – **keine Bedien-/POST-Verbindung zur bestehenden sicheren Migration**. Bloßer Seitenreload ist keine Lösung. Keine kostenpflichtige Recherche auslösen.
- Nächster sachlich notwendiger Schritt: Die vorhandene sichere PSTE-Migration über den minimalen zulässigen Originalweg ausführbar machen, nach Datensicherung und mit eindeutiger Benutzerfreigabe, ohne neue Architektur oder zweite fachliche Entscheidungsstelle. Erst bei `PSTE_Plugin::isReady()` die Research-Kategorien und Kostenkontrolle prüfen. K0-Artikelarten weiter BLOCKED.
- Maßgebliche ZIP unverändert `Texterstellung_Hobbydepot_0.4.24.2_TESTOBERFLAECHE_BEREINIGT.zip` im Hobbydepot-Pluginbüro. Diese Protokollierung hat KEIN Plugin gebaut und KEINE WordPress-/Datenbank-Migration gestartet.

---

## 18.11.2026 – SCREENSHOT RECHERCHE (18:19): NÄCHSTER KLICK KLARGESTELLT

- Betreiber ist sichtbar unter **Texterstellung → Recherche** und sieht `RECHERCHE GESTOPPT / PLUGIN_ACTIVATED_MANUAL_START_REQUIRED` sowie den vorhandenen Hinweis `PSTE-Migration noch nicht abgeschlossen`. Dies ist ein sicherer Aktualisierungsstopp, keine automatisch startende Recherche.
- **Quellcode der geprüften 0.4.24.2-ZIP:** DataForSEO Login/Passwort befinden sich **nicht auf „Recherche“**, sondern **Texterstellung → Diagnose** im Abschnitt `DataForSEO Zugangsdaten`, Button `Zugangsdaten der Originalengine speichern`. Keine Kosten durch Speichern.
- Weitere Bedienung: Login/Passwort dort eintragen, speichern, **keinen Recherchestart** auslösen; vorher PSTE-Migration/Kategoriebestand klären. K0-Sperre bleibt.
- Versionsstand und Pluginbüro bleiben **0.4.24.2** unverändert. Beleg `SCREENSHOT_RECHERCHE_CREDENTIALS_KLICKPFAD_20261118.md`.

---

## 18.11.2026 – AKTUELL UND MAßGEBLICH: Texterstellung 0.4.24.2, echte Diagnose liegt vor

- **Neue Ersatz-ZIP** `Texterstellung_Hobbydepot_0.4.24.2_TESTOBERFLAECHE_BEREINIGT.zip`; WordPress-Pfad unverändert `texterstellung-hobbydepot/texterstellung.php`. SHA256 `63812431443f8de47a04cbcf3879e3b5fb524c88fb21541562eb28c159ee9293`, **503056 Bytes**. Hauptablage `/Hobby Depot/Plugin-Büro/`, Fachablage `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`; beides hochgeladen.
- 0.4.24.2: **nur Hauptdatei geändert**, **86/87 Dateien bytegleich**; alte `0.4.20 KISS – TEST`-Überschrift, Testmaske/Checkbox/Bestätigungsbutton und störende Testmeldungen aus sichtbarem Backend entfernt. **Keine** neuen PHP-Dateien, Hooks, Architektur, K0-/Recherche-/MINI-/PSERC-/Publish-Regeländerungen. Sicherheitsgates bleiben; nicht bestätigte Installationen erhalten Sperrmeldung.
- Reale Nutzerdiagnose `texterstellung-diagnose-20261118-165236.json`, plugin=0.4.24.1, im Fachbüro archiviert: `site_host=www.hobby-depot.de`, `wp_environment=production`, **aber alte Testbestätigung=true** (kein Staging-Beweis); 0 Aufträge, 0 Recherchen, DataForSEO-Zugangsdaten fehlen, K0-Artikelarten `BLOCKED: K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`. Diagnose bereits vorhanden – **nicht erneut anfordern**.
- PHP-Lint **78/78**, JSON **8/8**, ZIP **87/87**, lokale Tests **46/46 PASS**: 3 Boot, 25 Funktion, 5 Originalimport, 13 UI/Sperren. Noch **KEIN Live-/Provider-/K0-End-to-End-PASS**. WordPress-Installation der 0.4.24.2 noch nicht bestätigt.
- Neue eigene Current-Akte `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` überschrieben, globales Pluginbüro-CURRENT anderer Plugins unangetastet. Vollbeleg: `DIAGNOSE_UND_TESTOBERFLAECHE_04242_20261118.md`.
- **Nutzer-Schritt:** 0.4.24.2 via WordPress-„Ersetzen“ einspielen und Übersicht einmal ansehen, ob Maske weg und 6 Bereiche vorhanden. Keine kostenpflichtige Recherche / K0-Produktion beginnen. Kein zusätzlicher Diagnoseexport.

---

## 18.11.2026 – AKTUELLER NUTZERSTAND: Plugin 0.4.24.1 gesichert, Test-UI für nächstes Update notiert

- **Aktuelle ZIP** `Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip` im echten Pluginbüro `/Hobby Depot/Plugin-Büro/` erneut geprüft: SHA256 `55eeeb3beabeac2c316617cdb67e3934d51ae75b6d3568e0e3fb0a1147426b36`, 503435 Bytes, 87 ZIP-Einträge, 0 CRC-Fehler, Hauptdatei `texterstellung-hobbydepot/texterstellung.php` Version 0.4.24.1. **Keine Codeänderung dieser Runde.**
- Büro-eigene Akte `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` erstellt; bestehendes globales `CURRENT.md` der Bildzentrale bewusst unverändert.
- Neuer Betreiber-Screenshot: `Texterstellung 0.4.20 KISS – TEST`, Testinstallations-Checkbox + Freischaltbutton auf normaler Domain `hobby-depot.de`. **Nicht anklicken.**
- **Nächste angeforderte Änderung:** unnötige alte Testmaske und KISS–TEST-Überschrift entfernen, **nur bestehende UI bereinigen**, keine Architektur/Eigenentwicklung. Der alte Test-Gate-Code und fachliche K0-/Recherche-/Import-/Publish-Sperren dürfen dabei nicht unbemerkt aufgehoben werden. K0-Produktionsfreigabe ist nicht nachgewiesen.
- Bildschirmbeleg und Arbeitsumfang: `PLUGINBUERO_SCREENSHOT_TESTUI_20261118.md`. Keine aktualisierte Installations-ZIP in dieser Runde, **0.4.24.1 bleibt CURRENT**.

---

## 18.11.2026 – MASSGEBLICHES ZIP-RELEASE FÜR ERSETZEN: 0.4.24.1

- Nutzer-Screenshot bestätigt: installiert `0.4.24`, zuvor hochgeladen `0.4.23-hobbydepot-bereinigung.2` → WordPress meldet niedrigere Versionsnummer. **Behoben** durch genau eine Änderung im vorhandenen ZIP: Pluginheader `Version: 0.4.24.1`. Keine Architektur-/Funktionsänderung.
- **Aktuelle Ersatz-ZIP:** `Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip`, SHA256 `55eeeb3beabeac2c316617cdb67e3934d51ae75b6d3568e0e3fb0a1147426b36`, 503435 Bytes. Root `texterstellung-hobbydepot/` weiterhin identisch zur ursprünglichen installierten 0.4.24.
- **Ablagen** erfolgreich geschrieben: `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip` UND `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip`.
- 86/87 Inhalte unverändert, 87/87 ZIP-CRC, 78/78 PHP-Lint, 8/8 JSON gültig, `version_compare` PASS. Details `VERSIONSKORREKTUR_0_4_24_1_20261118.md`.
- **Nächster Schritt** ausschließlich: Plugin 0.4.24 per WordPress-Ersetzen durch 0.4.24.1 aktualisieren, danach vorhandenen Diagnosebericht unter `Texterstellung → Diagnose` als JSON herunterladen und hier hochladen. Bis dahin KEINE bezahlte Recherche oder K0-Produktion; keine WordPress-Installation als bereits erfolgt behaupten.

---

## 18.11.2026 – AKTUELL: WORDPRESS ERSETZEN – NUR ZIP-ORDNERNAME BERICHTIGT

- Nutzer bestätigt, dass die **erste Hobbydepot-Texterstellung bereits installiert ist**. „Ersetzen“ erschien bei bisheriger ZIP nicht. Eigene vorherige Aussage „noch nicht installiert“ war falsch.
- Nachgewiesener ZIP-Unterschied: erstes Hobbydepot-Installationspaket 0.4.24 `texterstellung-hobbydepot/texterstellung.php`; bisheriges gereinigtes 0.4.23 `texterstellung/texterstellung.php`. **Jetzt Paketpfad zurück auf `texterstellung-hobbydepot/` gebracht.**
- Korrigierte ZIP `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_ERSETZEN.zip` SHA256 `a4356ec3db1263179a8aa12397418ea4efddab138f1abbe80ccfe8417f586a67`. **87/87 Dateiinhalte unverändert**, 78/78 PHP PASS, ZIP CRC PASS. Keine Code-/Workflow-/K0-Änderung.
- Installation: ZIP hochladen, WordPress sollte bei installiertem identischem `texterstellung-hobbydepot` den Ersatz anbieten. **Keine vorherige Deinstallation anweisen.** Tatsächliche Live-Verzeichnisidentität nicht unabhängig geprüft, keine unbedingte Gewissheit.
- Detailprotokoll: `ERSETZEN_ZIP_ORDNERKORREKTUR_20261118.md`.

---

## 18.11.2026 – Ersetzen-Dialog tatsächlich NICHT vorhanden (Betreiberangabe)

- ZIP-Inhalt **erneut direkt geöffnet**: Original 0.4.23 und bereinigtes 0.4.23 besitzen beide dasselbe WordPress-Hauptverzeichnis `texterstellung/` und Hauptdatei `texterstellung/texterstellung.php`. Eine Reparatur des Paketordnernamens wäre hier **nicht begründet**.
- Gesicherte WordPress-Pluginliste vom 01.11.2026 enthält keine Texterstellung; über die heutige Installation gibt es keinen direkten Live-Beleg. Betreiber meldet wiederholt ausdrücklich, dass der WordPress-Button „Ersetzen“ nicht erscheint.
- Korrektur: Nie wieder den nicht vorhandenen Button anwählen lassen. WordPress zeigt ihn nur, wenn das Zielverzeichnis tatsächlich schon existiert. Bei nicht vorhandener Installation normale Installation; bei anderer Alt-Installation deren Plugin-Eintrag zuerst per vorhandenem WordPress-Deaktivieren/Löschen behandeln, nur nach Sicherung – keine gefährliche direkte Dateisubstitution, kein Neubau oder K0-Eingriff.
- Die bereinigte Test-ZIP und alle Fachsperren bleiben unverändert. Keine Livefreigabe.

---
## 18.11.2026 – KORREKTUR WORDPRESS-ERSETZEN-ANWEISUNG

- Tatsächliche ZIP `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_TEST.zip` lokal geöffnet: oberster Pluginordner `texterstellung/`, Hauptdatei `texterstellung/texterstellung.php`, Pluginname `Texterstellung – Hobbydepot`, Version `0.4.23-hobbydepot-bereinigung.2`.
- WordPress bietet "Ersetzen" nur bei einer bereits vorhandenen Installation im **selben Pluginverzeichnis**. Die letzte vollständige Hobbydepot-Live-Pluginliste vom **01.11.2026** enthält KEIN Plugin `Texterstellung`; sie ist historisch und beweist nicht den aktuellen Bestand.
- Betreiber meldet aktuell ausdrücklich **keinen Ersetzen-Dialog**. Daraus folgt nicht automatisch, dass die ZIP defekt ist; tatsächlicher aktuell installierter Pluginordner ist weiterhin UNBEKANNT. Keinen weiteren Installer/Neubau/Architekturumbau und keinen blind gestarteten parallelen Installationsweg empfehlen.
- **Einzige erforderliche Information für exakte Korrektur:** tatsächliche derzeitige WordPress-Pluginzeile/Verzeichnis des zu ersetzenden Plugins (Screenshot der Pluginliste), dann ZIP-Verzeichnisidentität prüfen. Keine Änderungen an K0, Recherche, Kategorien.

---

## 18.11.2026 – AKTUELL: minimale Diagnosekorrektur ohne Neubau / nur Testinstallation

- Basis bleibt **reine Pferdeatelier-Bereinigung** 0.4.23; einzig `TXE_Diagnose::snapshot()` behandelt den bestehenden gesperrten K0-Zustand nun lesend als BLOCKED statt abzubrechen. Zweite Änderung nur Pluginheader-Versionsangabe `0.4.23-hobbydepot-bereinigung.2`. **Kein** neuer Workflow, keine Architektur, keine Kategorie-/K0-/Import-/Recherchemethode.
- Getrennter geprüfter **Staging-Testkandidat** im Dateienbüro: `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_TEST.zip`. SHA256 `86779493f975588520fe82148ee601568916fe69f1d0884207d5d6296781bc15`.
- 85/87 Dateien bytegleich zur Bereinigung, genau zwei geändert; PHP 78/78, JSON 8/8, ZIP 87/87, 3/3 Starts, 25/25 Bedien-/Funktionstests, 5/5 Original-Rückimporttests. Keine echten WP-/Provider-/K0-End-to-End-Läufe.
- **Sperren absichtlich erhalten:** `K0_PORTAL_ADAPTER_PENDING` im ursprünglichen Hobby-Manifest, nur `discgolf-beratung` als K0-Hobbyportalzuordnung belegt, importierte Artikel im Testmodus Draft. Nicht für Live freigegeben.
- Bericht `MINIMALE_DIAGNOSEKORREKTUR_0423_20261118.md` und MD+JSON im Dateienbüro `PRUEFBERICHTE`. Original-0.4.23 und alle späteren Umbauversuche unverändert archiviert.
- **Nächster Schritt:** eine isolierte WordPress-Testinstallation und einmaliger lesender Diagnoseexport. Keine zusätzliche Diagnose-Pluginversion.

---

## 18.11.2026 – MASSGEBLICHER LETZTER STAND (unveränderte ZIP; nur Pferdeatelier bereinigt)

- **Kein neuer Plugin-Build.** Maßgeblich bleibt `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip`, SHA256 `c50caa2ed263fb1f42f4cd485ecb2d23bbece6df072d9cf8f55774161aa6e715`. Original-PSTE/K0, HD004 und WP-Daten unangetastet.
- Direkt auf der gespeicherten ZIP wiederholt: **87/87 ZIP**, **78/78 PHP**, **8/8 JSON**, **3/3 Boots**, **24/25 Funktionschecks**, **5/5 PSERC-Importchecks**. 71 identische + 16 gereinigte Quelldateien; keine Pferde-Fachregeln, zwei technische Importnamen.
- **Belegter Blocker 1:** Die Diagnoseseite scheitert an `K0_PORTAL_ADAPTER_PENDING` (Ausgangs-Hobby-Kopie). Regulärer K0-Export nicht freigegeben.
- **Belegter Blocker 2:** Beide ursprünglichen Publish-Schutzfilter halten einen importierten Beitrag auch bei manueller Veröffentlichung oder Planung auf Entwurf. Andere WordPress-Beiträge unbeeinflusst. Test-Modus, keine Live-Freigabe.
- K0-Hobby-Kategorien nur `discgolf-beratung` autorisiert; kein echter WordPress-/DataForSEO-/MINI-/K0-Echtlauf. **Nicht auf Live installieren.**
- Unter enger Benutzeranweisung KEINE weiteren eigenmächtigen Änderungen am Plugin; konkrete Nachweise: `ABNAHME_BESTEHENDER_CODE_0423_20261118.md` und `PRUEFBERICHTE/HOBBYDEPOT_0423_ECHTE_ABNAHMEGRENZEN_20261118.{md,json}` im Hobbydepot-Büro.

---

## 18.11.2026 – AKTUELLER STAND: FINALE QUELL- UND FUNKTIONSPRÜFUNG OHNE CODEÄNDERUNG

- **Nur fachliche Pferdeatelier-Bereinigung** bleibt maßgeblich. ZIP: `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip`, SHA256 `c50caa2ed263fb1f42f4cd485ecb2d23bbece6df072d9cf8f55774161aa6e715`. Keine neuere Codebasis/Architektur/Pluginversion.
- Im aktuellen Lauf direkt erneut geprüft: 87 ZIP-CRC, 78 PHP-Syntax, 8 JSON, 3 Startsimulationen, 24/25 WP-Funktionssimulationen und 5/5 Original-PSERC-Importerfälle. **32/33 PASS; Diagnose FAIL: K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE**.
- Pferdeatelier-Volltextscan: nur 2 historische technische Rückimport-Vertragskennungen in PHP (plus 1 Hinweis in README). Alle anderen fachlichen Pferde-Bezüge entfernt.
- K0-Hobbyprofil ist nur für `discgolf-beratung` bekannt; produktive Registrierung anderer Hobbydepot-Kategorien nicht belegt. Staging-/Echt-K0-Test noch offen. Keine Livefreigabe.
- Neuer Bericht: `ABNAHME_READONLY_0423_20261118.md`, ausführliche MD/JSON-Nachweise im Hobbydepot-Dateienbüro `PRUEFBERICHTE`. **Ohne Änderung des Plugins.**

---

## 18.11.2026 – NACHTRAG zur 0.4.23 Funktionsprüfung (MAßGEBLICH)
- **32/33 lokale Tests PASS**, 1 Diagnose-Funktionsfehler, Original-WP-Entwurfsimport in Simulation funktionierte. Keine Pluginänderung.
- Das echte K0-Current `konzept0-portal-neutral-20261002` ist `READY_FOR_FRESH_K0_START`, inklusive 4 Typen und `Anleitung=READY` (nicht mehr pauschal „K0-Regeln unbekannt“ behaupten).
- **Belegter Portalblocker:** K0-Hobbyprofil ordnet nur `discgolf-beratung` zu; alle anderen Hobby-Kategorien sind in diesem K0-Profil nicht verzeichnet. Der bestehende K0-Router versucht dann den früheren Pferdeatelier-Kategorienbestand. **Keine flächendeckende Hobbydepot-Freigabe**, ohne Original-K0-Paket zu verändern oder eine zweite Zuordnung zu erfinden.
- **Keine neue Entwicklung:** Verbindlicher Nutzer-Scope bleibt ausschließlich Pferdeatelier-Bereinigung; der Rest ist als nachgewiesene Grenze erfasst. Bericht `ERWEITERTE_FUNKTIONSPRUEFUNG_0423_20261118.md` und Dateienbüro aktualisiert.
---
## 18.11.2026 – AKTUELL: Erweiterte Funktionsprüfung, **KEINE neue Pluginversion**

- Maßgebliche ZIP unverändert: `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip` SHA256 `c50caa2ed263fb1f42f4cd485ecb2d23bbece6df072d9cf8f55774161aa6e715`.
- **32/33 lokale PHP-WordPress-Mock-Tests erfolgreich**; 1 bestätigter Funktionsfehler: Diagnoseseite bricht bei der schon vorhandenen `K0_PORTAL_ADAPTER_PENDING`-Sperre ab. 5/6 Backendseiten darstellbar.
- Echte MINI-Auftragsregal-Prüfung: speichern, wiederholen, Konflikte und unbekannte Kategorie; unveränderter Original-PSERC-Importer erstellt im Mock den Entwurf und bindet den als exportiert simulierten TXE-Auftrag korrekt. **Keine reale K0-Textproduktion, kein vollständiger Export → K0 → Rückgabe-Durchlauf**.
- ZIP 87/87, PHP 78/78, JSON 8/8. Alte Konfliktsperren aktiv. Keine echten Provider-/WordPress-Schreibzugriffe. Keine Datei im Plugin verändert, keine neue Architekturschicht.
- **Aktueller Blocker für vollständige Nutzbarkeit:** K0-Artikelartenquelle im ursprünglichen Hobbydepot-Arbeitsstand steht auf `K0_PORTAL_ADAPTER_PENDING` und Diagnose behandelt den Zustand nicht. Nach verbindlicher Nutzerweisung sind diese Funktionsänderungen ohne gesonderten Auftrag NICHT vorzunehmen. Nicht für Live installieren.
- Vollbeleg: `ERWEITERTE_FUNKTIONSPRUEFUNG_0423_20261118.md` sowie MD/JSON im `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/`.

---

## 18.11.2026 – AKTUELLER STAND: Zusatzabnahme der REINEN 0.4.23-Bereinigung

- **Keine neue Pluginversion.** Maßgeblich bleibt `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip` in `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/`. Keine Architekturänderung, keine extra Plugins.
- Reale ZIP- und Source-Nachprüfung: 87 ZIP-Einträge, 78/78 PHP-Lint, 8/8 JSON, 71 unverändert / 16 bereinigt, 4/4 original K0-Importer-PHP byteidentisch. Library-ZIP exakt gleich.
- **3/3 lokale WordPress-Mock-Startfälle** bestanden: ohne Bestätigung, mit simuliert bestätigter Testsite, bei Konflikt mit altem PSTE. Kein PHP-Startfehler, im Test keine DB-Writes oder Netzaufrufe. KEIN echter WordPress-Test.
- Offen und unverändert: K0-Typquelle aus vorheriger Hobby-Arbeitskopie `K0_PORTAL_ADAPTER_PENDING` blockiert die produktive Typverwendung und kann Diagnosefehler auslösen. Ex-Pferde-Journal-Auto-Zielzuordnung kann keine Hobby-Kategorie auswählen. Kein Live-/DataForSEO-/MINI-/K0-Echtlauf. **Keine Produktionsfreigabe, nicht auf Live installieren.**
- Detailbeleg: `0423_QUELL_UND_STARTTEST_ZUSATZABNAHME_20261118.md` und `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_TEXTERSTELLUNG_0423_ZUSATZABNAHME_20261118.md`.
- **Verbindlicher Scope beibehalten:** Nur Pferdeatelier bereinigen; keine HD004-/K0-/Recherche-Eigenentwicklung.

---

## 18.11.2026 – ERLEDIGT: REINE PFERDEATELIER-BEREINIGUNG (verbindlicher Scope)

- **Aktuelles, maßgebliches Bereinigungsartefakt:** `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip` im Hobbydepot-Dateienbüro `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/`. Original 0.4.23 bleibt unangetastet.
- Ausdrücklich **KEIN** Aufbau auf Zusatzfassungen 0.4.25–0.4.28, keine HD004-Anbindung, keine neue Architektur/Entscheidung/Funktion.
- 87 Dateien; 71 byteidentisch; 16 ausschließlich bereinigt; 78/78 PHP-Lint, 8/8 JSON, ZIP-CRC PASS; vier Original-PSERC/K0 PHP-Dateien unverändert.
- Nur zwei historische technische Pferde-Importkennungen im ausführbaren Code; keine fachlichen Pferdebegriffe. WordPress-Testseiten-Schutz weiterhin aktiv.
- **KEINE LIVE-FREIGABE, NICHT INSTALLIEREN.** Kein echter WordPress-/MINI-/DataForSEO-/K0-Abnahmelauf und keine bestätigte aktuelle Hobbydepot-Kategorietauglichkeit; K0-Artikelarten-Status bleibt pending.
- Belege: `REINE_PFERDEATELIER_BEREINIGUNG_0423_20261118.md` und `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/BEREINIGUNG_NUR_PFERDEATELIER_0.4.23_PRUEFBERICHT.md`.
---

## VERBINDLICHE AUFTRAGSKORREKTUR 18.11.2026 – GILT VOR ALLEN ÄLTEREN EINTRÄGEN

**NUR BESTEHENDE TEXTERSTELLUNG VOM PFERDEATELIER SÄUBERN. KEIN UMBAU, KEINE EIGENENTWICKLUNG, KEINE NEUE ARCHITEKTUR.**
- **0.4.26–0.4.28 nicht weiterentwickeln und nicht installieren:** dort zusätzlich eingebaute HD004-Bindungs- und Diagnosefunktionen überschreiten diesen Auftrag. Sie bleiben nur historische Zwischenstände.
- Funktionsgrundlage Original-Texterstellung **0.4.23** und ihre bestehende Hobbydepot-Quell-Arbeitskopie 0.4.23; keine neue Recherche-/Kategoriesystematik und keine erdachte Artikelart.
- Ausschließlich Pferdeatelier-spezifische Fachdaten, Texte, Beispielbegriffe und Sonderregeln neutralisieren; K0-Original, vorhandene Schnittstellen, Entscheidungspunkte und Workflow erhalten.
- Die Historie enthält noch **keine** vollständig geprüfte, verbindlich installierbare Hobbydepot-Reinigungsfassung. **Nutzer: jetzt nichts installieren.**
- Einzelbeleg und maßgebliche Abgrenzung: `AUFTRAGSKORREKTUR_NUR_PFERDEATELIER_BEREINIGEN_20261118.md`.

---

# Hobbydepot – Texterstellung: aktueller Stand

**Status:** ARBEITSKOPIE 0.4.23 ERHALTEN; INSTALLATIONSKANDIDAT 0.4.24 GEPRÜFT, ABER NICHT FÜR LIVE FREIGEGEBEN. Stand: 16.11.2026.

- Source: Texterstellung 0.4.23; eigene ZIP: `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/Texterstellung_HOBBYDEPOT_ARBEITSKOPIE_0.4.23.zip`.
- Identität der ZIP (SHA-256): `03ffe443d6879ca4170cc8660aceb8b567cbc7a85d8673e9b00bea90971420dc`.
- WordPress-Live-Abnahme: **NEIN**.
- Portaleigene Fachregeln vollständig: **NEIN** (74 von 78 PHP-Dateien mit Pferde-/PSTE-Suchtreffern; Anzahl der tatsächlich fachlich zu ändernden Stellen noch nicht bewertet).
- Alte Pferde-Kategoriekarte und Familien-Overrides: **entfernt, nicht durch Schätzwerte ersetzt**.
- K0-Änderungen: **0**.
- Redaktionsplan zurückgesetzt: **NEIN**, gesonderter aktueller Export steht aus.
- Nächste Aufgabe: Portalanpassung im jeweiligen eigenen Chat, danach eigenständige Installationsfreigabe.

## Portierung 0.4.24 – separater Prüfstand (16.11.2026)

- Neue ZIP im Hobbydepot-Dateienbüro: `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24_INSTALLATIONSKANDIDAT.zip`.
- Eigener WordPress-Pluginordner; 79 PHP-Dateien syntaktisch geprüft, ZIP-CRC bestanden. K0-Importer unverändert.
- Pferde-Kategorie- und Seed-Daten sind entfernt; die alten Pferde-Journal-/Tarif-Sonderrouten für Hobbydepot stillgelegt. Nur auf hobbydepot.de administrativ aktivierbar.
- **Noch keine Produktionsfreigabe:** Kategorieabgleich HD-004 → Recherche-/MINI-Vertrag nicht fertig; kein WordPress-DataForSEO-K0-Endtest. Automatischer fachlicher Start bleibt gesperrt.
- Vollständiger Einzelbeleg: `PORTIERUNG_0.4.24_INSTALLATIONSKANDIDAT_20261116.md` im gleichen Büro.

## 18.11.2026 – vollständiger Quellaudit 0.4.25

- **Neue getrennte Arbeitskopie 0.4.25 im Hobbydepot-Dateienbüro; NICHT INSTALLIEREN.** SHA-256 `d16f0950de6792313a1e9894740a51f15e92b20644d7584d04a06d75b8e2cde7`.
- Pferde-Spezialfälle im redaktionellen Programmcode entfernt. Der historische K0-Rückimportname bleibt genau zweimal als notwendige externe technische Kennung bestehen. Original-PSERC-Importer unverändert.
- Fehlerhafte Sperre gegen nachträgliches manuelles Veröffentlichen entfernt; Diagnose bereinigt. Stale-Research-Bootstrap und sämtliche manuellen Forschungs-/MINI-/K0-Produktionsaktionen technisch gesperrt, solange HD004→PSTE nicht **echt** verifiziert ist.
- **79/79 PHP-Lint; 16/16 lokale Vertragstests; 4/4 Bootstrap-Tests; 88/88 ZIP-Dateien PASS.** Das sind keine realen WordPress-/DataForSEO-/K0-Echtläufe.
- **Genau eine offene fachliche Arbeit:** HD004 read-only Kategorieabbildung aus dem echten WordPress nachweisen, dann einmaliger vollständiger Durchlauf. Keine Produktionsfreigabe und keine Benutzerinstallation bis dahin.
- Beleg im gleichen Büro: `QUELLENAUDIT_KISS_0425_20261118.md`. Ausführlicher Bericht und ZIP in `/hobbydepot/TEXTERSTELLUNG/`.

## 18.11.2026 – HD004-Originalcode und 0.4.26-Arbeitsstand

- Letzter überprüfter Source: `HOBBYDEPOT_TEXTERSTELLUNG_0.4.26_QUELLE_NICHT_INSTALLIEREN.zip` im Hobbydepot-Dateienbüro; vorherige 0.4.25 unverändert archiviert.
- Original-HD004 1.0.0 aus GitHub-ZIP **tatsächlich geöffnet und geprüft**; vorhandene Runtime-API belegt, aktuelle Live-Werte noch nicht geprüft.
- Die vorhandene Texterstellungs-Diagnose liest künftig eine reine HD004-Kategorieübersicht: keine neue Kategorieentscheidung und kein weiteres Diagnose-Plugin.
- Tests: 80/80 PHP-Lint, 89/89 ZIP, 16/16 Bestand, 4/4 Start, 10/10 neue HD004-Simulationen. Original-PSERC-K0 unverändert.
- Keine Livefreigabe, keine WordPress-/DataForSEO-/K0-Echtprüfung. Keine Benutzerinstallation. Fachliche Kategorie-/Artikelart-Anbindung bleibt die EINZIGE offene Entwicklungsaufgabe.
- Einzelbeleg: `HD004_BINDUNG_ARBEITSSTAND_0426_20261118.md` in diesem Büro; Dateienbericht `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_TEXTERSTELLUNG_0.4.26_ZWISCHENSTAND.md`.

## 18.11.2026 – K0-Artikelarten: Schutzsperre nachgewiesen

- Hobbydepot-Kopie nennt `authority=K0_PORTAL_ADAPTER_PENDING`; `TXE_K0_Article_Types::all()` verlangt aber zurecht `K0_RULE_VALUES_JSON` und meldet im lokalen Realcode-Aufruf `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`. **Nicht freigeben und nicht durch bloßes Umbenennen reparieren.**
- Im vorhandenen historischen Repo `hallo-netizen/k0-multiportal/quarantine/k0_sources/RULE_VALUES.json.source` stehen nur vier Arten mit Regeldefinitionen: Beratung, FAQ, Pflege, Vergleich. Die Hobbydepot-Vorliste mit zusätzlich Anleitung ist **nicht** als heutige produktive Regelquelle bestätigt. Die aktuelle K0-Typquelle muss vor Freigabe geprüft werden.
- Die offen gebliebene Integration umfasst nun ausdrücklich sowohl (a) HD004→PSTE-Livekategorie-/Artikelartenbindung als auch (b) Abgleich mit der aktuellen K0-Regelautorität, beides innerhalb eines Sammelreleases; keine zusätzliche nachgelagerte Fachentscheidung.

## 18.11.2026 – NEUER STAND 0.4.27 (Arbeitskopie, NICHT INSTALLIEREN)

- Quelle 0.4.26; genau eine bisher zu schwache WordPress-Kategorieprüfung durch HD004-lesende Kategorie-/Hobbyseitenbindung ersetzt, keine zweite Entscheidung.
- 20/20 synthetische Funktionstests; 81/81 PHP-Syntax; 90/90 ZIP; vier PSERC/K0-Importerdateien unverändert.
- Arbeits-ZIP `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/HOBBYDEPOT_TEXTERSTELLUNG_0.4.27_QUELLE_NICHT_INSTALLIEREN.zip`, SHA256 `e4183bbc4da2e3516644b42923110380131b3c328295b8419c4467bc1ef9280a`.
- **Restauftrag gebündelt:** gesamter PSTE-Recherchepfad muss die HD004-Struktur als alleinige Quelle benutzen; aktive WordPress-Zuordnung fehlt als Echtnachweis. K0-Multiportal-Repo ist Quarantäne, KEINE Typen- oder Portal-Freigabe. Nicht installieren.
- Einzelprotokoll: `HD004_KATEGORIEBINDUNG_0427_20261118.md`; Prüfbericht in Hobbydepot-Dateienbüro.

## 18.11.2026 – 0.4.28 (geprüfte Arbeitskopie, NICHT INSTALLIEREN)
- Bestehende Diagnose repariert: fehlende produktive K0-Typenregel wird als BLOCKED beobachtet statt Fatal; K0-Produktionssperre bleibt erhalten.
- Bestehende HD004-Diagnose erkennt zusätzlich doppelte Kategoriemappings, Parent-Schleifen und fehlende Seitenvorfahren. Keine zweite Autorität.
- 81/81 PHP-Lint, 90/90 ZIP-CRC, 16/16 PHP-Funktionstests bestanden; Original-PSTE und vier Original-PSERC-Importer bytegleich zu 0.4.27.
- **Nicht übersehener Kern-Blocker:** PSTE_Snapshot::dynamicResolution() enthält weiterhin `count($path)!==3`; die alte Pferde-3-Seiten-Annahme muss in der einzigen Kategorie-Quelle durch HD004 ersetzt werden. Aktueller Live-HD004-Snapshot und bestätigte aktuelle K0-Typautorität fehlen.
- Arbeitskopie: `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/HOBBYDEPOT_TEXTERSTELLUNG_0.4.28_QUELLE_NICHT_INSTALLIEREN.zip` SHA256 `74a0c7e9db498ca9c21f0709e7c43e05b253e89341c154ebfdae0f8b94d63cdd`; kompletter Nachweis `PSTE_HD004_K0_PRUEFUNG_0428_20261118.md` und im Dateienbüro `PRUEFBERICHTE`.
