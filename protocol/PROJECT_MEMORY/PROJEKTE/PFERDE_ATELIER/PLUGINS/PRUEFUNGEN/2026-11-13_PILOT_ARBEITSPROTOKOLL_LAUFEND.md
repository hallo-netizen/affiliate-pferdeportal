# Pferdeatelier KISS – Pilot-Arbeitsprotokoll (laufend)

**Stand:** 13.11.2026. **Arbeit im getrennten Arbeitsverzeichnis**, nicht in vorhandenen WordPress-Plugins oder Live.

## Schritt 1 – Originale gesichert und Grenze bestätigt
- Originale als nur-lesbare Vorlage: PSTE QA 0.57.144.50, SHA256 `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`, 83 PHP-Dateien; PSERC QA 0.28.71, SHA256 `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`, 42 PHP-Dateien.
- Sie sind **QA-Originale**, nicht mit unbekanntem Live-Installationsstand gleichzusetzen.
- Nachgewiesen: PSTE verarbeitet SEO-Freigabe, Titel und Analytics; PSERC enthält K0-5-Felder-Grenze und Export/Import. Bestehender PSERC-Import ruft PPM679 Runtime Gate auf; nicht einfach entfernen.
- **Ziel:** separat installierbarer Pilot mit eigenem Ordner, eigenem Datenbereich, ohne Schreiben/Deaktivieren bisheriger Plugins. Sofortiges Umschalten der produktiven Worker ausdrücklich verboten.
- GitHub-Protokoll dokumentiert nur Arbeitsstand, keine offizielle neue Current-Autorität. Nach jedem relevanten Arbeitsschritt ergänzen.

**Status:** Quellenzuordnung und Pilotentwicklung laufen; keine Installation, keine WordPress-Live-Änderung, noch kein durchgängiger Echtlauf.


## Schritt 2 – Sofortartikel-Quellweg nachgewiesen und Zielvertrag ergänzt
- Tatsächlicher bestehender Einstieg in PSTE `includes/class-pste-admin.php`: `shortPathCreateExport` ab Zeile 1815; manueller Themenimport über `PSTE_Repository::importManualTopics`, ohne neuen DataForSEO-Aufruf, anschließend gezielter PSERC-Compiler nur für ausgewählte Themen. Originalcode: Kurzweg darf nicht den globalen 5.020er-Lauf starten.
- Alte Blockade: `shortPathCompileExactManualSelection` hängt im letzten Schritt ebenfalls an PSERC-/PPM-Artikelplätzen. Der bestehende Kurzweg muss beim Pilot **denselben** zentralen Themenstatus verwenden.
- Zielvertrag **Regel 19** auf GitHub ergänzt: Kurzweg erhalten, keine zweite Themenliste, sofort mit Kategorie-Abdeckung synchronisieren, Titel/K0/Rückgabeformat unverändert.
- Echte Altfreigabe-Datei hat 61 `FREI`-Fälle mit vorhandenen Titeln, aber ohne verbindliche Kategorie/Beitragsart und Planplatz. Diese Werte nicht nachträglich raten. **Sicherer Import hält unvollständige Altaufträge an**, statt sie als READY auszugeben.
- Bestehende Exportvorlage: `PSERC_TEXTMACHINE_METADATA_BATCH_V2` mit genau fünf Feldern; der aktuelle Import `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` hängt über `PPM679_Editorial_Plan_Runtime_Gate::record_readback` am PPM-Plan. Neuer Pilot darf ihn nicht stillschweigend als unverändert PPM-frei behaupten.

**Stand:** GitHub-Zielvertrag und Arbeitsprotokoll fortgeschrieben. Nächster Schritt: ausschließlich neue Pilotdateien im eigenen Ordner, keine Änderungen an alten Pluginquellen.


## Schritt 3 – Installierbarer, strikt isolierter Pilot erstellt und lokal geprüft
- **Ein eigenständiges Plugin-Verzeichnis:** `portal-kiss-auftragszentrale-pilot`, Version `0.1.0-test`; bestehende WordPress-Plugins bleiben vollkommen unangetastet.
- **Nur isolierte Test-WP:** Aktivierung gesperrt, solange die Website nicht ausdrücklich `staging`, `development`, `local` oder per Testkonstante als Test ausgewiesen ist. Kein Autostart, kein Cron, keine Änderung des WordPress-Frontends, keine Anfrage an DataForSEO.
- **Ein neuer Pilot-Auftragsbereich:** `pkiss_pilot_orders_v1` ausschließlich auf der Testkopie. Freigegebene Themen importieren, Sofortartikel anlegen, externen Titel zuordnen, Charge verbindlich reservieren, gleiche Charge jederzeit erneut herunterladen, fertigen K0-Rücklauf als Entwurf zuordnen.
- **Daten-/Formatgrenze:** `PSERC_TEXTMACHINE_METADATA_BATCH_V2` mit genau fünf unveränderten Feldern und Original-Hash; `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`/alte System4-Rückgabe als Eingabeformate.
- **Altfälle:** Die 61 tatsächlich `FREI`-Freigaben ohne Kategorie-/Beitragsart-Beleg sind sicher übernommen, aber als `METADATEN_OFFEN` gehalten. Drei echte bestehende K0-Metadatenbelege ergänzen genau die drei zugehörigen Fälle, ohne neue Fachentscheidung und ohne 64 statt 61 Aufträge zu erzeugen.
- **35/35 lokale PHP-Gegenproben PASS** mit isolierten WordPress-Funktionsnachbildungen: alter 61er Bestand, ursprünglicher 3er-K0-Handoff, echter SHA-Abgleich, Sofortartikel, Titelrückgabe, doppelte Exporte, Lock bei gleichzeitigem Zugriff, Wiederholung früherer Exportchargen, fehlerhafte Rückgabe, unveränderter Importvertrag, Entwurfsstatus, doppelter Import, zweites Portal.
- **Bestandsoriginale unverändert SHA-256:** PSTE `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`, PSERC `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`.
- **Installierbare TEST-ZIP (nicht Live):** `Portal_KISS_Auftragszentrale_PILOT_0.1.0_NUR_TEST_20261113.zip`, SHA-256 `6d9fa7eb9ffb0bc7b7d1f78ee03ab33156e2ff5915bf63d13111122c80066019`, 11.259 Bytes, WP-Pluginordner mit eigener README, ZIP-Integrität PASS.
- **Getrenntes Gegenprobenpaket:** `Portal_KISS_PILOT_0.1.0_PRUEFNACHWEISE_20261113.zip`. Beide ZIPs plus `PILOT_PRUEFBERICHT_20261113.md` dauerhaft in der Files-Library unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` abgelegt und zur Wiederaufnahme referenziert.

### Verbindlich OFFEN – keine fertige Komplettablösung behaupten
1. Vorhandener PSTE-Recherche-/Freigabe-Worker und **vollständiger** kurzer Dienstweg (`PSTE_Repository::importManualTopics` mit Bestands-/Kategorieprüfung) müssen **noch** in die Einplugin-Grenze aufgenommen werden. Der Pilot ermöglicht momentan nur bereits genehmigte Freigabedateien und manuell vorentschiedene Sofort-Aufträge; keine automatische neue SEO-Freigabe.
2. Externer MINI-Titelprozess selbst bleibt unverändert; Testpilot kann den fertigen Titel zuordnen, aber hat noch keine automatische Auslese des gewohnten Titel-Rückgabeformats.
3. Das tatsächliche WordPress-/K0-Ende-zu-Ende-Ergebnis steht aus. Simulierter Entwurfsimport **ist kein echter K0- oder WordPress-Test**.
4. Der Test-Importer ersetzt die alte **PPM-Buchung** intern bisher nicht in seiner vollständigen bisherigen Schutzwirkung. Ohne native PPM-/Guard-Quell-/Laufprüfung nicht als Live-Ersatz freigeben.
5. Dateiinterne Einzelfehler dürfen langfristig nicht andere gültige Rückläufe stoppen. Der Pilot stoppt bei einem ungültigen Eintrag derzeit noch die gesamte Datei; vor einer vollen Freigabe gegen Zielvertrag anpassen.
6. Kategorie-Abdeckungsfunktion in PSTE ist als Original nachgewiesen, im Pilot derzeit noch nicht als allgemeiner Report integriert.
7. Erforderlich: realer TEST-WP-Durchlauf mit vorhandenen realen drei Aufträgen und 20er-Charge, echter Kurzweg, Titel, Rückgabe, Teilabbruch und Veröffentlichungs-/Dubletten-Sperren. **Bis dahin kein Ersatz der Altplugins.**

### Nächste Handlung
**Nicht neu beginnen:** Originale + Pilot-ZIP aus der genannten Library lesen. Dann die echten PSTE-Aufrufe für Recherche, redaktionelle Freigabe, Kurzweg und Titel-Anbindung **nur dort** aufnehmen, wo sie im aktuellen Workflow wirklich gebraucht werden. Danach mit echter Test-WordPress-Datenbank anhand ursprünglicher Quellen und des unveränderten K0-Vertrags testen. Keine Live-Änderung. Kein zusätzlicher SEO-/Qualitäts-Worker.

**Status nach Schritt 3:** Testpilot gebaut und lokal geprüft; GitHub-Dokumentation aktualisiert. WordPress-Installation weiterhin nicht vorgenommen.

## Schritt 4 – Bezeichnung und alleinstehende Installation festgelegt
- **Neuer eindeutiger Backend-Name:** `Artikelwerkstatt – KISS (Test)`.
- Neuer, isolierter Pluginordner und neuer eigener WordPress-Datenspeicher. Keine Änderung, Deaktivierung, Verschiebung oder Überschreibung der vorhandenen PSTE-, PSERC-, PPM- oder Guard-Plugins durch dieses Paket.
- **Benutzerbedingung:** Keine unvollständige Plugin-ZIP zum Herunterladen anbieten. Eine Test-ZIP erst ausgeben, wenn der Stand tatsächlich für die ausdrücklich getrennte Testinstallation installierbar ist und die vollständige im Paket behauptete Funktionsstrecke lokale Regressionen besteht.
- **Alleinarbeit in Test-WP:** Nach gesichertem Backup kann der Nutzer alte Plugins dort selbst deaktivieren. Neue Werkstatt darf keine Klassen oder Methoden dieser deaktivierten Plugins voraussetzen. Bestehende Originaldaten bleiben unangetastet und können nur lesend übernommen werden.
- Offene Integration aus Pilot 0.1.0: echte Keyword-Datenquelle, vorherige Einmalentscheidung, Vollformat Titelrunde, kurzer Dienstweg, Teilimport ohne Gesamtabbruch, Kategorien-Abdeckungsübersicht.
- **Status:** Integrierter Test-Build in eigenem Arbeitsverzeichnis in Bearbeitung, keine Installer-Freigabe zu diesem Zeitpunkt.


## Schritt 5 – Artikelwerkstatt – KISS 0.2.0 TESTINSTALLATION
**Abgeschlossen am 13.11.2026, nur isolierte TEST-WP-Freigabe, kein Live-Release.**
- **Eindeutiger Name:** `Artikelwerkstatt – KISS (Test)`, Pluginordner `artikelwerkstatt-kiss`, Version `0.2.0-test`.
- **Standalone:** Keine Klassenaufrufe aus PSTE, PSERC oder PPM nötig. Benutzer kann diese Altplugins auf der TEST-WP manuell deaktivieren. Plugin selbst deaktiviert/überschreibt nichts.
- **Vorhandene Bausteine bewusst übernommen:** PSTE-DataForSEO-Requestklasse (isoliert umbenannt, Credentials nur lesend, separater Cache), identische PSTE-Keyword-Normalisierung und Verschlüsselungsleser, Titelgovernance-Datei und `PSTE_RAW_KEYWORD_MINI_BATCH_V1`-Feldgrenze, ursprünglicher K0-5-Felder-Vertrag `PSERC_TEXTMACHINE_METADATA_BATCH_V2`, exakte plan_slot-Hashfunktion, K0-Import-Datenformate.
- **Ein zentrales Regal:** `awk_kiss_orders_v1`, Status-FREI/Metadaten-offen/Exportiert/Importiert, Sofortartikel, DataForSEO-Recherche + einmalige redaktionelle Freigabe, Export identischer Titel-/K0-Dateien, idempotenter Entwurfimport, isolierte fehlerhafte Einzelartikel, Kategorien-Abdeckungsübersicht.
- **83 einzigartige lokale Gegenproben bestanden** (35 vorhandene + 28 Integrations- + 15 Admin/20er-Charge + 5 Fehlereinzel-Isolation). Fünf PHP-Syntaxprüfungen und ZIP-CRC aller sieben Paketdateien bestanden. Aus Originalfreigaben 61 FREI mit historischen Titeln ohne erfundene Kategorien, 3 belegte Original-K0-Aufträge, 20er-Charge 13+7, wiederholte Doppelimporte, separater Hobby-Depot-Kontext. Die PHP-/WordPress-/DataForSEO-Ausführung war **lokal mit Nachbildungen**, nicht auf der echten WP-Testinstallation.
- **Test-Installer:** `Artikelwerkstatt_KISS_0.2.0_TEST_INSTALLIEREN.zip`, **25.740 Bytes**, SHA256 **`f381f622af5eca5714a2f289169ce3774ef9afdf68423b9f2be416fcb1830171`**. Vollständige ZIP gespeichert in der persistenten Library unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` sowie **verlustfrei als Base64 in GitHub**, Zweig `docs/pferdeatelier-produktionsplan-kiss-20261113`, Datei `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/PILOT_ARTIKELWERKSTATT/Artikelwerkstatt_KISS_0.2.0_TEST_INSTALLIEREN.zip.b64`. Die lokale Quell-/Testakte liegt ebenfalls in derselben Library.
- **Abnahmebericht:** `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/PRUEFUNGEN/2026-11-13_ARTIKELWERKSTATT_0.2.0_TESTABNAHME_UND_CHATUEBERGABE.md`.
- **Originale nach Prüfsumme unverändert:** PSTE SHA256 `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`; PSERC SHA256 `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`.
- **Offen, NICHT als erledigt behaupten:** automatische vollwertige alte PSTE-Semantik (im Testpilot nur einmalige **manuelle** redaktionelle Freigabe nach Recherche), echter DataForSEO-Anbieterabruf, echter externer MINI-Worker-/K0-Rücklauf, echter WordPress-Draft-Test, unbewiesene neue Auftrag-ID vs PPM-K0-Altplan. Darum nur **Testinstallation**, nicht Liveersatz.
- **Nächste Aktion:** Nutzer installiert Test-ZIP auf separater WordPress-Testinstallation, aktiviert; deaktiviert Alt-SEO-/Plan-/Produktionsplugins **nur dort selbst**; beginnt mit einem sicheren Sofortartikel und einem echten K0-Rücklauf. Ergebnisse gegen genau diese gespeicherte Abnahme prüfen. Nicht erneut Architektur umbauen.


## Schritt 6 – Nutzerpräzisierung: Diagnose für belegbasierte Fehlersuche + Name Texterstellung
**Anforderung 13.11.2026:** **Ein Plugin „Texterstellung“** statt „Artikelwerkstatt – KISS“. Die **Diagnose ist Bestandteil desselben Plugins**, kein zusätzliches Diagnose-/Prüfplugin.
- **Zweck der Diagnose:** Im Fehlerfall für den Entwickler/Assistenten nachprüfbare technische Belege, statt anhand von Screenshots Ursachen zu raten: letzte Aktionen mit Zeit und Ergebnis, genaue Fehlerkennungen, Auftrags-/Schrittzuordnung, Statusverteilung, fehlende Pflichtfelder, Import-/Export-Sperrgründe und Einstellungen/Plugin-Versionen (nur diagnostisch).
- **Einfache Bedienung:** Im WordPress-Backend eine Diagnose-Zusammenfassung und ein einzelner JSON-Download. Bericht kann vom Nutzer in Chat hochgeladen werden; **kein automatisches Versenden**.
- **Datensparsam:** Keine Passwörter, API-Tokens, Cookie-/Nonce-Werte oder vollständige Artikeltexte im Report, keine personenbezogenen Rohdaten. Technische Angaben und einzelne Keyword-/Auftragsdaten soweit zur Fehlersuche erforderlich. Nur berechtigter Administrator, Download nur mit Nonce.
- **Nur protokollieren, nicht doppelt entscheiden:** Diagnose darf keine neuen inhaltlichen Prüfungen, keine SEO-Nachentscheidung, keine weiteren Worker und kein Nachschreiben alter Pluginoptionen hinzufügen. Nur tatsächlich beobachtete Fehler melden; “kein Fehler festgestellt” ist kein Live-Abnahmebeweis.
- **Testinstallation:** Isolierte WP-Testkopie, alte Plugins unangetastet; eigene Daten; Import/K0/Titelverträge unverändert.
- **Status:** Entwicklung der Umbenennung und integrierten Diagnose begonnen. Kein neuer Installer ausgegeben; Abschluss erst nach lokalen Gegenproben und Code-/GitHub-Sicherung.


## Schritt 7 – Texterstellung 0.3.0 mit integrierter Diagnose abgeschlossen
**13.11.2026 – Nur isolierter Test-Installer; echte WordPress-Testabnahme noch offen.**
- **WordPress-Plugin heißt ab jetzt `Texterstellung`**, nicht KISS; ZIP `Texterstellung_0.3.0_TEST_INSTALLIEREN.zip`, 30.973 Bytes, SHA256 `9fe7d4a3e4f168bace01f014ff4f358db2f01b6b8b9e532734f2085bfbb91974`. Hauptdatei `texterstellung/texterstellung.php`, sechs PHP-Dateien insgesamt; PHP ab 8.1. ZIP CRC erfolgreich.
- Aus ausschließlich eigener Kopie des alten Piloten 0.2.0 abgeleitet; **alle drei alten Quellen unverändert**: Pilot 0.2.0 SHA `f381f622af5eca5714a2f289169ce3774ef9afdf68423b9f2be416fcb1830171`; PSTE 0.57.144.50 QA SHA `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`; PSERC 0.28.71 QA SHA `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`.
- **Eine integrierte Diagnose für den Assistenten/Entwickler**, keine zweite fachliche Prüfung oder zusätzliches Plugin. Im Admin unter **Werkzeuge → Texterstellung → Diagnosebericht für die Fehlersuche herunterladen (JSON)**. Nur Admin mit Nonce; kein automatisches Senden. Das maschinenlesbare JSON enthält genau beobachtete Schritte/Fehlercodes, betroffene Aufträge, Statuswerte, Herkunft der Artikelplätze, technische Liefer- und Entwurfbelege. Keine API-Credentials, keine vollständigen Artikeltexte, kein Token-/Nonce-Export; Wörter/Titel können für die Fehlersuche enthalten sein. Ereignisverlauf auf 160 begrenzt. Separates kleines Eventlog ist *nur* Diagnose; redaktionelle Wahrheit bleibt eine einzige Auftragstabelle/WordPress-Option.
- **119 lokale Prüfungen bestanden**: 35 Originalaufträge/61 echte Altfreigaben, 28 neue Funktionsprüfungen, 15 20er-Chargen/Backend, 5 Isolierung fehlerhafter Einzelartikel, 27 Diagnoseprüfungen, 9 direkte Fehler-/JSON-Download-Abnahmen. Sechs PHP-Syntaxprüfungen und ZIP-Integrität. Der Fehler `NO_APPROVED_READY_ARTICLES` wurde gezielt im Admin simuliert und im Verlauf tatsächlich wiedergefunden. Ein fehlerhafter Importartikel wurde als `RETURN_ITEM_HELD` protokolliert.
- **61 historische FREI-Fälle:** fehlende Kategorie/Artikelart in Quelle korrekt diagnostiziert. Ihre lokal erzeugten Platzkennungen werden ausdrücklich als solche gekennzeichnet, nicht als PPM-gebucht.
- Datenbereich und PHP-Klassen der Texterstellung von altem Testpilot getrennt. Keinerlei WordPress-Live-, Originalplugin-, Core- oder Frontendänderungen. Titel-/K0-5-Felder-/Rückgabeformate bleiben unverändert.
- **GitHub:** dieses Protokoll, Zielvertrag Regel 20, `2026-11-13_TEXTERSTELLUNG_0.3.0_DIAGNOSE_ABNAHME.md`, Release-Manifest und verlustfreie Base64-ZIP im Ordner `PILOT_TEXTERSTELLUNG`. Außerdem in der persistenten Files-Library `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` gespeichert. PR #768 bleibt DRAFT.
- **Nächste Arbeit:** Nutzer installiert nur die neue Texterstellung-ZIP auf separater TEST-WP. Benutzer deaktiviert dort selbst bisherige Plugins, falls notwendig. Vor und nach realem ersten Test über die eingebaute Schaltfläche Diagnose-JSON sichern. Bei Fehlern zuerst das JSON auslesen, keine Ursachen raten.
- **Noch offen:** automatischer gleichwertiger PSTE-SEO-Fachentscheid, echte DataForSEO-/K0-/WordPress-E2E-Abnahme und PPM-Slot-Kompatibilität. Deshalb Testinstallationsfreigabe, **keine Livefreigabe**. Keine Behauptung, die 61 alten Artikel seien fertig produzierbar.


## Schritt 8 – Texterstellung 0.4.0: Vollständiges Backend-Hauptmenü und Redaktionsrunde
**13.11.2026, isolierte Kopie, keine Alt-/Liveänderung.**
- Die frühere 0.3.0 hatte alle Stationen unter `Werkzeuge` und nur vereinfachte redaktionelle Handfreigabe. **Anforderung korrigiert:** eigenständiger linker Menüpunkt `Texterstellung` mit 8 Untermenüs, nicht eine lange Werkzeuge-Seite.
- Zusätzlich **externe einmalige redaktionelle SEO-Entscheidungsdatei** `TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1`: recherchierte Themen, vorhandene WordPress-Beiträge, fest vorgemerkte Aufträge und Kategorieinventar; Rücknahme von FREI/BELEGT/KLAERUNG; unveränderliche Quelldaten; fehlerhafter Einzelfall isoliert, Korrektur derselben Charge möglich. Kein neuer nachgelagerter SEO-Prüfer.
- Eigene verschlüsselte DataForSEO-Zugangsdaten pro Testportal statt Abhängigkeit von alten PSTE-Optionen; nur lesender Fallback für historische gespeicherte Daten.
- **Eindeutige Zuständigkeit:** Während die externe Redaktionsdatei bearbeitet wird, blockiert eine zusätzliche manuelle Freigabe desselben Themas. Titel-, K0-, Rückgabe- und Diagnoseschnittstellen unverändert.
- **151 unterschiedliche lokale PHP-Gegenproben bestanden** über 6 Gruppen, plus gesonderte echte Fehleraktions-/JSON-Download-Prüfungen in der Simulation. Neue Simulation: 20 Keywords => 15 FREI, 3 BELEGT, 2 KLÄRUNG => 15 Titel => 15 K0-Aufträge => 10+5 WordPress-Draft-Mocks, Zweitimport 0 Duplikate.
- ZIP `Texterstellung_0.4.0_TEST_INSTALLIEREN.zip`, 34.346 Bytes, SHA256 `8a5c2faf39081e05d5610bb4757e9d4f6d8eaaa8f52ca0771007be0ab6c8c3c5`, ZIP-Test/6 PHP-Syntaxprüfungen PASS. Alte PSTE/PSERC/TXE-.3-Dateien bitidentisch (Manifest/Abnahmebericht).
- Sicherung: Vollständiger Installer und Tests/Manifeste persistent im Library-Büro `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`; Installer verlustfrei auch als Base64 auf GitHub unter `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/PILOT_TEXTERSTELLUNG/Texterstellung_0.4.0_TEST_INSTALLIEREN.zip.base64.txt`. GitHub-Leseprotokoll `2026-11-13_TEXTERSTELLUNG_0.4.0_ABNAHME_UND_CHATUEBERGABE.md`.
- **Noch offen:** echter WP-Test, echter DataForSEO-Anbieterabruf, echter externer K0-Rücklauf auf neuem Auftrag/Slot, automatische vollwertige PSTE-SEO-Entscheidung. Ein vollständiger WP-E2E-Erfolg darf nicht behauptet werden.
- **Genau nächste Handlung:** Nutzer installiert **nur 0.4.0** auf separater TEST-WP; dort selbst alte Plugins deaktivieren, nicht auf Live. Linke Navigation `Texterstellung → Diagnose` vor dem ersten echten Versuch; danach `Sofortartikel`, echte Kategorie und Rücklauf testen. Bericht als JSON bereitstellen; Fehler nur nach Datenbeweis reparieren.

**Status:** Isoliertes Paket und GitHub-Abnahme fertig; reale WordPress-Testabnahme offen.


## Schritt 9 – 14.11.2026: Testaktivierung auf echter WP-Seite blockiert
- **Echter Nutzer-Screenshot 08:09:** WordPress-Aktivierung auf Nutzer-Testseite `oliver-beil.de` zeigt sofort `TEXTERSTELLUNG_TEST_ONLY` mit Anforderung `WP_ENVIRONMENT_TYPE=staging` in wp-config.php. **Plugin-Eigenfehler in der Aktivierungssperre**, kein Nachweis eines WP-Problems.
- **Quellnachweis aus 0.4.0 Original-ZIP:** `texterstellung/texterstellung.php`, `TXE_Workshop::activate()` ruft `permitted()` auf und `wp_die(...)`, wenn WordPress nicht als Staging erkannt wird. Dieser Blocker macht das Plugin auf einer legitimen Testinstallation mit Standard-WP-Umgebung unbenutzbar; lokale QA hat diese reale Variante nicht abgedeckt.
- **Korrekturziel 0.4.1:** Aktivierung ohne wp-config-Änderung zulassen; **alle produktiven Plugin-Aktionen bis zur bewussten Admin-Bestätigung im Backend sperren**. Bestätigung an genau diese WordPress-Website binden; beim Kopieren auf eine andere Site erneut bestätigen; eigene Datensätze und alte Plugins unverändert. Keine WordPress-Core-/Frontendänderungen, keine SEO-Doppelprüfung, keine externe Verbindung nötig. Einziger linker Hauptmenüpunkt bleibt `Texterstellung`.
- **Abnahme vor neuer ZIP:** Originaldateien/Altdaten byteidentisch, Aktivierung in WP-Standardumgebung, alle Aktionswege vor Bestätigung blockiert, Adminbestätigung mit Nonce, nachher voller Admin-Menü-/Workflowzugriff, Fremdsite wieder gesperrt, PHP Syntax/ZIP-Integrität, reale Testseite weiterhin offen.
- **Stand:** Nachweis geprüft, kleiner gezielter Fix in separater 0.4.1-Arbeitskopie begonnen, noch keine Installerfreigabe und keine Liveänderung.


### Schritt 9 – Lösung und Testpaket 0.4.1 vollständig gespeichert
**14.11.2026 / Nutzer-Screenshot 08:09**: Testinstallation auf `oliver-beil.de` durch eigenes `wp_die` in `TXE_Workshop::activate` abgebrochen, weil `WP_ENVIRONMENT_TYPE` standardmäßig `production` meldet. Bestätigte Ursachenkette: 0.4.0 Original-ZIP `texterstellung.php` Zeilen 23–35. Kein WordPress-Fehler.

**Gezielte Korrektur 0.4.1-test:**
- Plugin lässt sich ohne Eingriff in `wp-config.php` normal aktivieren. **Kein Autostart und keine Verarbeitung vor Freigabe.**
- Linker Hauptmenüpunkt `Texterstellung` erscheint sofort. Die eigentlichen Arbeitsschritte sind erst nach einmaliger **Administratorbestätigung „Dies ist die separate Testinstallation“** auf genau dieser Site freigegeben. Adminrechte + Nonce + Checkbox erforderlich; Domainwechsel sperrt wieder.
- Alte Aufträge und ursprüngliche 0.4.0-Quellcode-Dateien unberührt. **Nur** `texterstellung.php` (Aktivierung/UI), `class-txe-diagnose.php` (ehrliche Adminbestätigung als Quellenangabe und Versionsnummer), `README` (Installationsanleitung) im **neuen** ZIP geändert. Die fünf übrigen ZIP-Dateien bitidentisch.
- **37 lokale funktionale PASS** in WordPress-Simulation (explizit `production` ohne `wp-config.php`-Override, gesperrte Aufträge vor Zustimmung, Admin/nonadmin, fehlende Checkbox, falscher Nonce, einmalige Zustimmung, Sofortauftrag, K0-Fünf-Felder, reservierte Charge, Mehrfachexport, Wiederdownload, Domainwechsel). **6 PHP-Syntaxprüfungen PASS**, ZIP-CRC PASS. Kein echter WordPress-Serverzugriff und kein echter K0-E2E-Test behauptet.
- **Aktueller Testinstaller (ersetzt 0.4.0):** `Texterstellung_0.4.1_TEST_INSTALLIEREN.zip`, 35.228 Byte, SHA256 `f34fe278eaca382ca99c7f537463644dbd1508b9fb4198980e173df59edae280`.
- Vollständiges Paket im persistenten Library-Büro `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` und als verlustfreies ZIP-Base64 im GitHub-PR (Ordner `PILOT_TEXTERSTELLUNG`) gespeichert. Bericht `2026-11-14_TEXTERSTELLUNG_0.4.1_AKTIVIERUNGSFIX_BERICHT.md`; reproduzierbare Testdatei und Release-Manifest daneben.
- **Nächster Schritt:** Nutzer lädt ausschließlich Version 0.4.1 auf der separaten Test-WP hoch und ersetzt, falls angeboten, 0.4.0. Aktivieren; links `Texterstellung` öffnen; **Testmodus mit Checkbox** freischalten; danach den echten Diagnose-JSON-Bericht ziehen und testen. **Nie** auf Live den Testmodus freigeben. Alte Plugins bleiben unangetastet.
- **Bekannte Grenze unverändert:** alte automatische PSTE-Semantik nicht 1:1 übernommen; reale WordPress-K0-Ende-zu-Ende-Abnahme offen. Keine Livefreigabe.

### Schritt 10 – Nutzer meldet: Version 0.4.1 installiert, erste Echtdiagnose ausstehend
- **14.11.2026:** Nutzer bestätigt im Chat: „4.1. ist installiert. wie weiter?“ Nur **Installation** ist bestätigt; Aktivierung, Adminfreigabe und Testlauf sind **noch nicht** nachgewiesen.
- Konkreter bestehender Bedienweg (kein Neubau): Plugin ggf. aktivieren → links **Texterstellung** öffnen → bestehende einmalige Testinstallation-Bestätigung in 0.4.1 setzen → **Diagnose**-JSON herunterladen und bereitstellen.
- Nach dem ersten echten Diagnosebericht Ursachen anhand dieser Daten prüfen. Erst anschließend regulären Sofortartikel → Titel → K0 → Import erproben. Keine Vermutung über Erfolg, keine Plugins der produktiven Website verändern.
- Nutzer wünscht künftig **normale Aktivierung ohne unnötige zusätzliche Sperrmechanik**. Für die bereits installierte 0.4.1 den aktuell tatsächlich vorhandenen Bedienweg erklären; keine ungetestete ZIP behaupten. Für einen eventuellen nächsten Patch keine weiteren unnötigen Einrichtungsanforderungen hinzufügen.


### Schritt 11 – 14.11.2026 08:22 UTC: erster echter Texterstellung-0.4.1-Diagnoseexport
**Quelle:** Nutzereingereichte reale Datei `texterstellung-diagnose-20261114-072230.json`, `generated_utc=2026-11-14T07:22:30+00:00` (08:22:30 Berlin), `diagnosis_contract=TEXTERSTELLUNG_DIAGNOSE_V1`.
- **Echter Befund:** `plugin.version=0.4.1-test`; WordPress-Testmodus adminbestätigt (`is_test_environment=true`, `test_mode_admin_confirmed_for_this_site=true`). WordPress meldet intern `wp_environment=production` – **kein Aktivierungsfehler**, weil 0.4.1 erfolgreich aktiviert ist.
- `dataforseo_credentials_present.stored_login=true` und `stored_password=true`; **das beweist nur gespeicherte Zugangsdaten, nicht deren erfolgreiche Nutzung oder Anbieterantwort**.
- `queue.saved_state=false`, `order_count=0`, `research_count=0`, `title_batch_count=0`, `last_k0_batch=null`, `orders=[]`, `last_events=[]`, `draft_faults=[]`; noch kein tatsächlicher Produktions-/Rechercheaufruf in diesem Datenbestand nachgewiesen. Keine technische Blockade aus dem JSON ableitbar.
- Weitere aktive WP-Plugins laut Diagnose u. a. Portal Production Center und Link Policy Gate, aber PSTE, PSERC und PPM nicht in aktiver Pluginliste; **kein Beleg für eine Intervention**. Altplugins nicht ungefragt deaktivieren.
- **Kleinster nächster, echter Testschritt:** Admin öffnet links `Texterstellung → Recherche`, startet genau **eine** begrenzte echte Recherche; danach denselben Diagnose-JSON-Download erneut durchführen und vorlegen. Erst dann konkrete technische Störstelle anhand der echten Events nachweisen. Keine neue Pluginversion und keine Codeänderung wegen dieses leeren Erstberichts.
- Diagnose wurde nicht automatisch gesendet; vom Nutzer hochgeladen. **WordPress-/K0-Echt-Ende-zu-Ende-Test weiterhin offen.**

### Schritt 12 – 14.11.2026: Testkeyword nur als Vorschlag, nicht als garantiert neues Keyword
- Nutzer wünscht **ein konkret noch nicht recherchiertes** Keyword zum Test. Stichprobe aus originalem PSTE-Diagnoseexport `pste-gesamtdiagnose-2026-11-13.json` geprüft: Er zählt 5.020 Themen, listet aber nur 14 Beispiel-Einträge statt aller Keywords. Ein garantiert neuer Begriff ist daraus **nicht beweisbar**. Keine Behauptung einer vollständigen Gegenprüfung.
- **Konkreter Recherchetest-Vorschlag:** `Fliegendecke Pferd scheuert an der Schulter`. Volltextsuche im verfügbaren Diagnoseexport negativ, jedoch ohne vollständigen Keywordpool kein Ausschluss früherer Recherche.
- Wichtige offene Produktergänzung: Texterstellung muss den bestehenden Keyword-Pool samt Recherchestatus vor neuer Recherche verlässlich anzeigen/abgleichen, ohne Datenverlust oder doppelte fachliche SEO-Freigabe. Plugin/Live unverändert.


### Schritt 13 – 14.11.2026: Automatisierung der Recherche und Google-Fragen fehlt
**Nutzer-Test und Quellnachweis (0.4.1, kein Raten):**
- Nutzer sieht auf Seite `Texterstellung → Recherche` **manuelle Kategorie-, Beitragsart-, Suchintention-Felder** und fragt ausdrücklich, warum das nicht automatisch entschieden wird. Diese Felder sind **derzeit ein Hauptweg, keine bloße optionale Korrektur**.
- Quellcode `texterstellung/texterstellung.php`: `runResearch()` ab Zeile 341 ruft **nur** `TXE_DataForSEO_Client::keywordSuggestionsDriverStep(seed, Germany, German, limit)` auf und speichert Vorschläge als `RECHERCHIERT`. **Keine Google-PAA-Abfrage** über `peopleAlsoAsk()`. Die Definition der Methoden `peopleAlsoAsk`, `postPeopleAlsoAskTask`, `getPeopleAlsoAskTask` und `extractPeopleAlsoAskQuestions` ist in `includes/class-txe-dataforseo-client.php` Zeilen ~292–380 vorhanden, wird aber im regulären `runResearch()` nirgends aufgerufen.
- `texterstellung.php` etwa Zeilen 815–827 zeigt je Keyword **Kategorie-Dropdown, Artikelart-Eingabe, Suchintention-Eingabe, Button „Einmal freigeben“**. Zeilen ~831–837 alternativ externer `seo_export` und `seo_import` für manuelle externe Fachentscheidung. Startübersicht sagt ausdrücklich, alte PSTE-Automatik sei noch nicht gleichwertig übernommen.
- **Abweichung vom verbindlichen Zielvertrag**: Alt-PSTE-Fachautomatik für Pferdebezug, Suchintention, Überschneidung, Kategorie/Art und Abdeckungssteuerung sollte unverändert funktionsfähig übernommen werden; manuelle Eingriffe nur zusätzlich bei echten Klärfällen. Der Pilot darf nicht als funktionsgleich bezeichnet werden.
- **Weitere Abweichung:** Google-„Nutzer fragen auch“ (People Also Ask) wird aktuell nicht mitgesammelt, obwohl die ursprüngliche Clientfunktion kopiert wurde.
- **Verbindliche Reparaturrichtung:** Die **bestehende, geprüfte** Automatik aus PSTE-Original gezielt in die isolierte Texterstellung überführen. PAA im normalen Rechercheablauf mit den vorhandenen Clientmethoden integrieren, deduplizieren, Ursprungs-/Statuskennzeichnung erhalten, begrenzte API-Kosten/Fehler-Isolation. SEO-Eigentümer bleibt einmalig; manuelle Optionen nur für echte `KLÄRUNG` oder bewusst gewünschten Sofortweg. Gleiche alte Titel/K0/Import-Verträge. **Keine weiteren Plugins, kein Live-Code-Eingriff, keine neue Doppelprüfung.**
- **Stand:** Ursache eindeutig in der installierten Quellfassung 0.4.1 nachgewiesen. Noch **keine** korrigierte installierbare Fassung. Der Nutzer muss nicht manuell 20 Keyword-Felder durchgehen; dieser Umweg ist kein Ersatz für die vereinbarte Automatik.
