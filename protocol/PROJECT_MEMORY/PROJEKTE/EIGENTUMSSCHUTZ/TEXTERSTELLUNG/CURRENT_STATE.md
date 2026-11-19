# PASS – 19.11.2026: Hab Texterstellung 0.4.31.6 gesichert

Nutzer meldet **PASS** und verlangt Protokoll/Büroablage. **Verifiziert:** unveränderte ZIP 0.4.31.6 im Hab-Büro `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04316/`, SHA256 `29769acb82fc6aef9bee68de87248ed70d2af51fe454d1218af887f5b501a7eb`; QA/Diff/Tests liegen dort. Zusätzlich `PASS_UND_ABLAGE_20261119.md` erfolgreich archiviert. GitHub-Protokoll `HAB_04316_PASS_ABLAGE_BESTAETIGT_20261119.md`. **Keine neue Version/Änderung.** Nutzer-PASS ist protokolliert; echte Serverantwortzeit bleibt nicht separat gemessen. Maßgeblicher letzter Hab-Stand 0.4.31.6. Original-K0, MINI, Universal, Pferdeatelier, Robotik, Wassertechnik unverändert.

---

# AKTUELL 19.11.2026 – Hab Texterstellung 0.4.31.6 Performance-Release erstellt

Nutzer verlangt eigenständige Prüfung ohne Chrome-Screenshots. **Installationsfähige 0.4.31.6 ZIP fertig lokal geprüft und in Library `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04316/` mit vollständigem Quellbestand, Patch, Tests und QA erfolgreich gespeichert**. Autorisierte reine Performance-Korrektur in bisheriger Originalarchitektur: Recherche-Familien + Run-Status nur einmal lesen, vorhandene Registry bei `selectedCategory` wiederverwenden statt je Kategorie neu bauen. **83/87 Dateien identisch** mit installierter 0.4.31.5, **0 neue/gelöschte**; PHP 78/78, JSON 8/8, ZIP 87/87 PASS. **7/7 Backendansichten vollständiges HTML unverändert**, **16/16 Statusmuster** und **16/16 direkte Original-vs.-Korrektur-Familien-/Kategorienhashes gleich**. 5 lokale Cold-PHP-Läufe 285/93: Median **622,25 ms → 57,69 ms**; eine redundante SQL-Leseabfrage entfällt. Keine Fachentscheidung, MINI/K0, Pferdeatelier, Universal-Blanko oder Website geändert. **Server-Minuten-Timeout noch nicht remote gemessen/als gelöst bewiesen.** Kein extra Diagnose-Plugin oder Screenshot verlangt. SHA ZIP `29769acb82fc6aef9bee68de87248ed70d2af51fe454d1218af887f5b501a7eb`. Vollprotokoll `HAB_04316_PERFORMANCE_ORIGINAL_AUSGABE_IDENTISCH_20261119.md`. Nächster Nutzerweg: nur Hab 0.4.31.5 durch 0.4.31.6 via WP Plugin-Upload ersetzen, dann Recherche öffnen.

---

# PERFORMANCE-STAND 19.11.2026 – Hab Texterstellung 0.4.31.5 UNVERÄNDERT

Nachbarprojekt Pferdeatelier nur als Inspiration (dort 2.218 option_value-Reads in 17 Seiten), **nichts übernommen**. Original-Hab-Recherche-GET mit echten 0.4.31.5 PHP-Klassen und 285/93 **synthetischem** WordPress-Datenbestand lokal simuliert. **7/7 Admin-Bereiche PASS**, Recherche 49.608 HTML-Bytes/285 offene Kategorien. **Konkret bewiesene Doppelarbeit:** `familyAnchors` zweimal + `categoryProgress`-SQL-SELECT zweimal, neben 1.140 get_term_meta + 114 get_post_meta Aufrufen für dynamische Kategoriekarte (WordPress-API-Aufrufe, nicht SQL-Zahl). Beim GET 74 Optionleseaufrufe. Fünf lokale PHP-Vergleiche: Original Median **587,5 ms**, isolierte NUR-TEST-Fassung Median **298,6 ms**, SQL-Abfragen 4→3, **HTML bytegenau identisch**, 16/16 Statusmusterparität; bisherige 16 Migration-/19 AJAX-/28 Button-Prüfungen erneut PASS. **Kein neuer Installationsdownload**, kein Funktionsabbau, keinerlei Live-Pluginänderung. Reale Hab-Server-/SQL-/Cache-Zeiten noch nicht gemessen; lokaler Gewinn allein beweist NICHT Grund minutenlangen Hängers. Kompletter Verlauf `HAB_04315_RECHERCHE_BACKEND_PERFORMANCE_LOKALTEST_20261119.md`, alle QA-Dateien tatsächlich in Library `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_PERFORMANCE_20261119/` archiviert. Original-K0, Pferdeatelier und jungfräuliche Universal-Kopien unangetastet.

---

# NEUER LIVE-STAND 19.11.2026 09:16 – Hab 0.4.31.5 meldet EINRICHTUNG ERFOLGREICH

Echter WordPress-Screenshot: Einrichtung erfolgreich abgeschlossen. Kategorien können jetzt angezeigt werden. Ausgeliefertes JavaScript meldet dies nur bei job.status=COMPLETE plus result.ready=true, dann automatisches Neuladen. Der noch sichtbare Button Einrichtung fortsetzen ist ein Übergangstext aus finally, nicht Beleg für einen gescheiterten Job. **Keine weitere Pluginversion!** Nächster Nutzerweg: Recherche-Seite vollständig neu laden und **erst dann** die offene Kategorie-/Themenzählung prüfen. Noch nicht belegt: richtige Kategorieübersicht, DataForSEO-Echtlauf, MINI/K0-E2E. Live-Screenshot-Status in HAB_04315_LIVE_MIGRATION_COMPLETE_SCREENSHOT_20261119.md und Library PLUGIN_FREIGABEN/04315/HAB_TEXTERSTELLUNG_LIVE_ERFOLG_20261119_0916.md protokolliert. Universal, Robotik, Wassertechnik und Original-K0 unverändert.

---

# AKTUELLSTER STAND 19.11.2026 – Hab Texterstellung 0.4.31.5

**Fehler nach erfolgreichem Klick in 0.4.31.4:** `PSTE_EDITORIAL_RULESET_RAW_KEYWORD_INVARIANT_FAILED`, PSTE-Safe-Migration bei gespeichertem fortsetzbarem Job angehalten. **Konkrete Originalcodeursache reproduziert für leeren `topic_pool`:** Null-Themenphase überspringt Raw-Baseline-Scan, gespeicherte Chain leer, alte Abschlussprüfung vergleicht fälschlich mit zulässigem Seed. Minimale Korrektur in **vorhandener** Originalmethode `editorialMigrationVerifyComplete`, nur für `expected=0`, `cursor=0`, `savedChain=''` den ursprünglichen Seed verwenden. Alle strengen Prüfungen für nichtleere Daten und abweichende Tabellen unverändert. **0.4.31.5-ZIP** bereit, SHA256 `7e80f7f08f5ca628d9cf803d6d805b0848437230ae4438d131ca280976db742a`, 516790 Bytes; 84/87 Quelldateien unverändert, PHP 78/78, JSON 8/8, ZIP 87/87. Reproduktion alt PASS; 16 gezielte Fehler-/Fortsetzungsprüfungen, 19 WordPress-AJAX- und 28 Browser-Klick-Prüfungen PASS. **Bestehenden PAUSED_ERROR-Job in Test ohne Reset über CORE_VERIFY_FINAL, FINAL_TOPIC_VERIFY_BATCH und FINAL_VERIFY fortgesetzt.** Vollständige ZIP samt Diff/Build/QA/Testskripten **im Hab-Plugin-Büro `PLUGIN_FREIGABEN/04315` tatsächlich gespeichert**. Keine Live-Datenbank/Produktiv-K0-Überprüfung; reale PSTE-Themenzahl vom Nutzer bislang unbekannt. 0.4.31.4 durch 0.4.31.5 **ersetzen, nicht vorher löschen**, dann denselben Vorgang fortsetzen. Bei weiterem Fehler erst echte read-only Phasen-/Zählungsevidenz statt Blindfix. **Pferdeatelier, Universal-Blanko, Robotik/Wasser, MINI und K0 unverändert.** Volles Protokoll: `HAB_04315_LEERER_THEMENBESTAND_ORIGINAL_INVARIANT_FORTSETZUNG_20261119.md`.

---
# NEUER AKTUELLER STAND 19.11.2026 – Hab Texterstellung 0.4.31.4 Klickkorrektur

**0.4.31.3 ist nachweislich installiert, aber der Einrichtungsknopf reagierte nicht** (Screenshot 08:36, `NOT_STARTED`). Echte Ursache reproduziert: nicht abgeschlossenes Inline-JavaScript-IIFE aus `TXE_Workshop::migrationSetupHtml`, SyntaxError `Unexpected end of input` → kein Klick-Handler/kein AJAX. **0.4.31.4** mit einziger fehlender `})();`-Zeile, Versionskopf und README gebaut. **85/87 Dateien bytegleich** zur 0.4.31.3, keine neuen Klassen/Architektur/Recherche-/MINI-/K0-Änderungen. Tatsächlich ausgegebenes PHP/JS getestet; **28 Browser-Klick-Tests + 19 echte Original-PSTE-Backend-AJAX-Prüfungen**, PHP 78/78, JSON 8/8, ZIP CRC 87/87 bestanden. ZIP SHA256 `42f9d4e11c0d5f0080428a1693bdb4e01ff81fd16005819bde76f5b6212d7e89`. **Plugin/Quellen/Testberichte mit Upload-Status succeeded in Library `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04314/` gesichert**. Vollbericht `HAB_04314_BUTTON_AJAX_JS_ROOT_CAUSE_20261119.md`. Nächster Nutzerweg: 0.4.31.4 **über** 0.4.31.3 installieren, dann Einrichtungsbutton; reale Vollmigration in WordPress noch nicht als bestanden nachgewiesen. Universal Blanko und Pferdeatelier unangetastet. **0.4.31.3 nicht mehr empfehlen.**

---

# AKTUELLER INSTALLATIONSSTAND 18.11.2026 – Hab Texterstellung 0.4.31.3

**0.4.31.3 – neue Hab-Ersatzversion lokal gebaut, getestet und im Büro archiviert.** Screenshot bestätigte installierte 0.4.31.2, aber ursprüngliche PSTE-Migration ohne Startfunktion (Aktivierungsstopp `PLUGIN_ACTIVATED_MANUAL_START_REQUIRED`). Nun in bestehendem `TXE_Workshop` einziger Einrichtungsbutton mit altem PSTE-Safe-Migration-Job (start/advance und Wiederaufnahme), einmalige bestehende PSTE-Baseline aus gebundenen Hab-Kategorien, bestehender Original-Rechercheschalter und korrekter Versionstext. **Nur Hauptdatei plus README geändert, 85/87 Dateien byteidentisch** zu 0.4.31.2; kein Architekturumbau, keine neuen Klassen, keine MINI/K0/Pferdeatelier/Universal-Änderung. ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.3_VOLLSTAENDIGE_EINRICHTUNG.zip` SHA256 `a86a9dafbaf7e6604dd1217c428098ec54387d2763165bff47ce41a606a8bafd`, 516355 Bytes; **78 PHP / 8 JSON / ZIP CRC PASS**, migrationsbezogene Original-PHP-Simulation, 285/93 synthetische Kategorienprobe und MINI-Regression bestanden. **WordPress-Live-Migration und DataForSEO-Echtdurchlauf nicht durchgeführt**. ZIP, Build, Testskripte, Protokoll und QA **gespeichert im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04313/`**. Vollständiges Protokoll: `HAB_04313_ORIGINALMIGRATION_FREIGABE_20261118.md`. Nächster Nutzerklick: bestehendes Plugin mit 0.4.31.3 ersetzen → Texterstellung → Recherche → `Einrichtung vollständig durchführen`. Keine extra Versionskontrolle, kein neues Plugin bis zu echten Fehlerbelegen.

---

# Live-Screenshot 18.11.2026 18:15 – tatsächlicher Installationsstatus noch prüfen

**Wichtig:** Screenshot `Texterstellung 0.4.31 KISS` ist KEIN Beleg für falsche Pluginversion, da dieser Text im Hab-0.4.31.2-PHP weiterhin fest steht. Pluginheader der echten ZIP meldet 0.4.31.2. Screenshot zeigt `PLUGIN_ACTIVATED_MANUAL_START_REQUIRED` (nach Originalaktivierung gewollte Recherche-Sperre), `originale PSTE-Migration ... nicht abgeschlossen`, Auftragsregal 0. Das Status-Aktualisieren ist nur Seiten-Neuladen; bis PSTE READY ist kein Live-Kategorien-Readback und keine Recherche-Freigabe gezeigt. **Nächster Nutzerklick: Plugins → Installierte Plugins → Texterstellung – Hab & Bewahr, Version 0.4.31.2 ablesen.** Erst danach Originaldiagnose der Migrationsphase, keine bezahlte Recherche. Keine neue ZIP, keine Programmänderung, keine K0-Änderung. Vollständiger Nachweis in `HAB_04312_SCREENSHOT_WP_AKTIVIERUNG_STATUS_20261118.md` und in beiden Library-Büros gespeichert.

---

# 18.11.2026 – NEUER AKTUELLER STAND: Hab-Plugin 0.4.31.2 mit Kategorienanbindung

**Autorisierte minimale KATEGORIENZUORDNUNG umgesetzt.** Original 0.4.31 und Hab 0.4.31.1 bleiben unangetastet; neue Hab-Version 0.4.31.2. Zwei alte Quelldateien an schon vorhandene APKW-WP-R3-Bindung angepasst, kein Neubau, keine neuen Klassen/Kategorien, keine MINI-/K0-Änderung. 83/87 Dateien bytegleich, 78 PHP und 8 JSON geprüft, ZIP CRC PASS. WP-Mocks: zwei bekannte Hab-Kategorien, 5 Suchabsichten auf denselben Term, 285/93 synthetischer Mengentest, inaktive/verwaiste Kategorie als Negativfälle, 7/7 Original-MINI-Prüfungen. **ZIP ist lokal WordPress-installationsfähig; echter WordPress-/DataForSEO-/K0-Lauf steht noch aus.** Voller Nachweis: HAB_04312_KATEGORIENANBINDUNG_PRUEFSTAND_20261118.md; ZIP, Build und Prüfbericht tatsächlich in Hab-Library /hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/04312 gespeichert. Pferdeatelier und Universal-Blanko unverändert.

---

# AKTUELLSTER PRÜFSTAND 18.11.2026 – Originalsemantik 30/30, kein Neubau

**Ohne Programmänderung** originale PSTE-Recherche-Semantik mit 10 Fällen auf je **Original 0.4.31, Hab 0.4.31.1, Blanko 0.4.31.1** getestet: **30/30 PASS**. Konfigurationsabkürzung `article_type = Hab-Themen-Kategoriename` wurde ausgeschlossen, weil z.B. `Fensterschloss` bei Artikeltyp `Beratung` erkannt, bei `Türen & Fenster` als Artikeltyp aber zurückgewiesen wird. Fragestellungen und Kosten ebenso an echte Artikelart gebunden. Keine neuen Funktionen, keine Fixes, keine K0/WordPress/DataForSEO-Änderung, bestehende drei ZIP-SHA und CRC unverändert. **Keine Produktionsfreigabe** für die minimalen Hab-/Blanko-Kopien, da die Original-Recherche eine fachlich andere Kategorie-Typ-Zuordnung voraussetzt. Prüfbericht/Testergebnisse/Test-PHP **in beiden Library-Büros unter `PRUEFUNG_SEMANTIK_OHNE_UMBAU_20261118` gespeichert**. Volles Protokoll `ORIGINAL_RECHERCHE_SEMANTIK_30_TESTS_OHNE_UMBAU_20261118.md`. Nur vollständig geprüfte installierbare ZIPs als Chat-Downloads.

---

# Stand 18.11.2026 – Abschlussprüfung OHNE Umbau/Neubau

**Nur originalgetreue Bestandsprüfung, alle drei Plugin-ZIPs unverändert.** Original/Hab/Blanko ZIP-CRC, je 78 PHP/8 JSON und 7/7 unveränderte MINI-Funktionstests PASS. Hab/Blanko: Pferde-Magazin-Automatik korrekt deaktiviert, allgemeine Notfall-Sperre aktiv, die leere originale PSTE-Recherche-Karte korrekt blockiert. Vorhandener Hab-Readback und Magazin-Seiten geprüft; Seiten sind keine Magazin-`category`-Terme. 11 PHP-Dateien enthalten noch Pferde-Worttreffer (überwiegend Altvertrag/Kommentare/inaktive Logik; vereinzelte alte Wort-Sondermuster bleiben), daher keine Null-Treffer-Aussage. **Reines Auskommentieren ist eine gute Blankokopie, aber keine voll funktionsfähige Hab-Artikelproduktion**, weil Original-Recherche eine verbindliche nichtleere Artikeltyp-/R3-Kategoriekarte benötigt. Keine Fantasietypen, keine Programmänderungen, keine neue ZIP, keine Installationsfreigabe. Vollbeleg: `ABSCHLUSSPRUEFUNG_REINE_KOPIE_OHNE_UMBAU_20261118.md`; vollständige Prüfdateien in **beiden** Library-Büros unter `ABSCHLUSSPRUEFUNG_OHNE_UMBAU` tatsächlich abgelegt.

---

# Aktuellster Originalcode-Nachweis 18.11.2026 – KEIN neues Plugin / KEIN Download

**Weiterarbeit ohne Zwischenstopp durchgeführt.** Die erhaltenen minimalen 0.4.31.1 Hab-/Universal-Kopien und das 0.4.31 Pferdeatelier-Original sind unverändert und erneut CRC+SHA-geprüft. **6/6 unabhängige Original-PHP-Tests** beweisen: Unter echter Hab-R3-Seite führt pauschal derselbe PSTE-Kategorieartikeltyp zu Kategorieverlust (Original quarantänisiert ein Fachthema). Die Hab-Daten liefern keine feste Typenvariante, MINI darf später die K0-Schreibart separat entscheiden. Zudem `PSTE_Journal_Article_Type` in den Kopien ohne pferdespezifische Magazin-Kategoriedefinition (0 statt vormals 9). Ein funktionsfertiges Hab-Plugin lässt sich somit NICHT durch ausschließlich Auskommentieren produzieren; Portaldaten erfinden oder neue Architektur bauen ist verboten. Kein Pluginfreigabestatus vortäuschen. Vollständiges aktuelles Protokoll `MINIMAL_0431_ORIGINAL_RECHERCHE_GRENZE_20261118.md`, nachweislich in **beiden Library-Büros** unter `PRUEFUNG_ORIGINAL_RECHERCHE_20261118` abgelegt. Nur fertig freigegebene Installations-ZIPs als Downloads. Keine Original-/Live-/K0-Änderung.

---

# KORRIGIERTER AKTUELLER STAND – 18.11.2026: MINI bereits richtig, NICHT umbauen

**Neu am Originalcode mit Hab- und Blanko-Kopie 21/21 lokale Tests bestanden:** Der bestehende MINI-CATEGORY-Worker wählt bereits genau einmal Kategorie und **separat** K0-Artikelart (Beratung, FAQ, Pflege, Vergleich, Anleitung). Die bisherige pauschale Behauptung, eine feste Hab-K0-Schreibartikelart je WP-Kategorie sei zum MINI-Betrieb notwendig, ist korrigiert. **Nichts an MINI/K0 ändern.** Der verbleibende Engpass ist ausschließlich der FRÜHERE alte PSTE-Kategorien-Snapshot für SEO/Recherche: Er verlangt eine befüllte `PSTE_Portal_Category_Map` mit ihrem eigenen `article_type`-Feld; Pferdekarte wurde bei Minimal-Klon bewusst entfernt. Eine begrenzte Hab-WP-Bestandsprüfung vom 14.11. belegt echte Kategorien/R3, aber keine fixierten PSTE-Typen. **Keine neuen Kategorien, keine neue Architektur, keine Fixes, kein installierbares Release.** Vollständiger Bericht und Testskript in beiden Büroablagen: `PRUEFUNG_MINI_ORIGINAL_20261118`; GitHub-Protokoll `MINI_ORIGINAL_UNABHAENGIGE_ARTIKELARTEN_VERIFIZIERT_20261118.md`. ZIPs 0.4.31/0.4.31.1 unverändert, CRC+Hashes PASS.

---

# Stand 18.11.2026: KEIN neuer Kategorienbestand erforderlich

**Nutzer bestätigt: Keine weiteren Kategorien hinzugekommen.** Bestehenden Hab-Kategorienbestand ohne neue Abfragen nutzen. Erneut anhand des Originalcodes und der gespeicherten Daten überprüft: 285 historisch eindeutig gebundene WP-Kategorien und 93 R3-Seiten; keine nachgewiesene feste `article_type` pro Sachkategorie. C25/C26-Versicherungskategorien sind gespeicherte Konzepte, nicht ohne WordPress-Readback als importiert behaupten. **Das ist ein Unterschied der bestehenden Abläufe** (Original-PSTE erzwingt Typ pro Kategorie vor Recherche; Hab sieht spätere einmalige MINI-Artikelart vor), kein fehlender Kategorieexport. Keine Neuentwicklung / Fixes erlaubt, daher keine erfundene Zuordnung und keine Freigabe. Bestehende Original-/Hab-/Blanko-ZIPs 0.4.31/0.4.31.1 SHA und CRC erneut unverändert bestätigt. Volles Prüfprotokoll: `KATEGORIENBESTAND_UNVERAENDERT_WIRKLICHE_GRENZE_20261118.md`. Bericht in beiden Library-Büros gespeichert.

---

# Fortsetzung 18.11.2026: unveränderte Original-Karte erfolgreich getestet

**Keine Code-/Plugin-Änderung.** 0.4.31 ORIGINAL sowie Hab-/Blanko-Minimal-ZIPs 0.4.31.1 unverändert. Historischer Hab-Readback vom 13.10.: 285 Kategorien unter 93 R3-Seiten, aber 0 Artikelart-Zuordnungen. Original-PSTE-Map mit synthetischem Hab-Kategorien-Testfall: **5/5 positive Original-PHP-Tests (Beratung/FAQ/Pflege/Vergleich/Anleitung) und 1/1 Negativprobe ohne Typ PASS**. Ergebnis: bestehendes Map-Format KANN Hab-Kategorien aufnehmen, **aber es existiert in den geprüften Quellen noch keine autoritative reale Kategorie->feste Artikelart-Zuordnung**; die erdachte Testart darf nicht produktiv übernommen werden. Aktueller WP-Livebestand/K0-Registrierung nicht nachgewiesen. Daher **kein Installationsrelease**. Vollständiger Beleg: `MINIMAL_0431_ORIGINAL_MAP_HAB_GEPRUEFT_20261118.md`, Originaltests und Berichte dauerhaft in beiden Library-Büros unter `PRUEFUNG_ORIGINAL_MAP_20261118`. Nutzerregel: keine Neuentwicklung, keine Fixes, nur minimaler Original-Klon.

---

# Neuester verbindlicher Stand – Minimal-Klone aus Original 0.4.31 (18.11.2026)

**Kein 0.5.x-Universal-Neubau.** Aus der ORIGINAL-0.4.31 wurden ausschließlich die Portalbezüge für Hab & Bewahr und eine leere Kopie deaktiviert/entfernt. Beide Quellpakete mit identischem altem Workflow gebaut, keine neue Klasse/Funktion/Architektur; jeweils 78 PHP/8 JSON geprüft, 68 Quelldateien unverändert, 20 Änderungen/Löschung der Original-Signatur, 87 ZIP-Einträge. Beide Entwicklungs-ZIPs samt vollständigen Berichten und Bauskript **tatsächlich in den beiden Library-Büros unter MINIMAL_ORIGINAL_0431 archiviert**. Original-Kategorie-Map lehnt den leeren Bestand korrekt ab; Hab-Kategorien und K0-Registrierung noch nicht funktionsfertig, **nicht installieren oder downloaden**. Vollständiges Protokoll: `MINIMAL_0431_QUELLKOPIEN_PRUEFSTAND_20261118.md`. Die zuvor dokumentierten 0.5.x-Kandidaten sind als Quelle/Entwicklungsrichtung abgelöst.

---

# VERBINDLICHE KURSKORREKTUR 18.11.2026: KEINE NEUENTWICKLUNG

Original-Pferdeatelier-Texterstellung als technische Vorlage **unverändert in der Funktionsweise** übernehmen. Nur zwei separate Kopien (jungfräulich/universal und Hab & Bewahr); ausschließlich Pferde-Portalbezüge und Portaldaten entfernen/auskommentieren. **Keine neue Architektur, keine Fixes, keine neuen Adapter/Klassen/Prüfstationen.** Die zuvor entwickelten 0.5.x-Universal-Erweiterungen sind als Entwicklungsweg ausdrücklich verworfen, nicht als nächstes Release verwenden. Nur fertige installierbare Plugins zum Download; Protokolle ausschließlich im Büro. Einzelheiten in `KURSKORREKTUR_NUR_MINIMALE_PORTALKOPIEN_20261118.md`.

---

# Aktueller Stand 18.11.2026 – Gemeinsame Texterstellung 0.5.2-dev.1 (intern)

**Hab 62/62 und Universal 51/51 lokale Funktionstests bestanden**, je 82/82 PHP und 9/9 JSON; zwei ZIPs aus identischer Codebasis. Reale WordPress-Kategorien liefern jetzt portalfreie Recherche-Ausgangspunkte ohne voreilige Artikelart- oder SEO-Entscheidung. Original-K0-Fünffeldprüfer: korrektes Paket angenommen, verbotene Erweiterungen abgewiesen. Historisches GitHub-K0-Register ohne Hab/Robotik/Wasser; echter K0/DataForSEO/WordPress-Lauf ausstehend. Daher KEIN Installationsdownload und Produktionssperre bleibt aktiv. Alle Artefakte im jeweiligen Library-Büro `V052` gespeichert; genaue Nachweise in `UNIVERSAL_CORE_V052_QA_STAND_20261118.md`.

---

# Geprüfter 0.5.1-Quellstand (fortgeschrieben 18.11.2026)

**Nicht installierbares internes Entwicklungsarchiv, kein Plugin-Download.** Hab 39/39 und Universal 28/28 lokale Funktionstests, je 80/80 PHP und 9/9 JSON, deterministische ZIPs. Hab mit bestätigtem aktiven WP-Kategorie-Snapshot; Portalwechsel und alte Pferdeatelier-Auftragsdaten sicher isoliert. Beide vollständigen ZIPs, Tests und gemeinsamer Quellcode in den Library-Büros unter `V051`. Recherche- und K0-Echtfreigabe weiter OFFEN. Details: `UNIVERSAL_CORE_V051_QA_STAND_20261118.md`.

---

# Fortsetzung 18.11.2026 – v0.5.1-dev.1 nur im Büro

**Gemeinsame Quelle weiterentwickelt und zwei intern gespeicherte ZIP-Kandidaten gebaut; noch KEIN Installationsdownload.** Hab-Kategoriebindung mit aktivem WordPress-Snapshot geprüft, ungebundene Kategorien ausgeschlossen; Pferdeatelier-Auftrags-/Diagnoseoptionen getrennt, leeres neues Universal-Regal. PHP-Syntax 80/80 und JSON 9/9 je Version, Hab 36 und Universal 25 lokale Funktionschecks bestanden. Alte Recherche-/K0-Verträge bleiben noch offen; Produktionssperre bleibt. Einzelheiten: `UNIVERSAL_CORE_V051_QA_STAND_20261118.md`. Alle Unterlagen dauerhaft in den beiden Library-Büros unter `V051`.

---

# Verbindliche Ausgaberegel: nur freigegebene Plugin-ZIPs im Chat

Ab 18.11.2026 nur **installationsfähige, abgenommene** Plugin-ZIP-Dateien zum Download ausgeben. Alle QA-ZIPs, Entwicklungsarchive, Test-JSON und Protokolle **ausschließlich im Büro ablegen**, nicht im Chat verlinken. Kleine Arbeitsschritte bündeln, fortlaufend Quelle, Fehler, Korrektur, Tests und Freigabestatus protokollieren. Der aktuelle 0.5.0-qa.1-Stand ist NICHT installierbar; K0 und Recherche noch offen. Näheres: `AUSGABEREGEL_NUR_INSTALLIERBARE_PLUGINS_20261118.md`.

---

# Aktueller Entwicklungsstand 18.11.2026: Texterstellung Universal 0.5.0-QA

**Zwei QA-ZIP-Kandidaten aus derselben Quelle erzeugt und im Hab-/Universal-Dateibüro dauerhaft gespeichert.** 80 PHP und 9 JSON pro Paket geprueft; Hab 28/28 und Blanko 22/22 lokale Funktionstests bestanden. Kategorien aus WP gelesen, Artikelart getrennt, Produktionen gesperrt. **Nicht installieren, keine echte WordPress/K0-Freigabe.** Einzelheiten und genaue Library-Ablagen in `UNIVERSAL_CORE_V050_QA_STAND_20261118.md`.

---

# Beschlossene Ergänzung: universelles Plugin

**Ein Quellcode, zwei Pakete:** Hab & Bewahr konfiguriert + universelle Blanko-Version für künftig Robotik, Wassertechnik und weitere Portale. Kein mehrfacher Umbau des Originalplugins; Kategorien aus dem aktuellen Portal lesen, Artikelart getrennt entscheiden, bestehendes K0 unverändert anbinden und vor Freigabe portalecht testen. Verbindliche Einzelheiten in `ZIELVERTRAG_UNIVERSELLE_TEXTERSTELLUNG_20261118.md`. **Dies ist ein Entwicklungsauftrag, noch kein fertig gebautes Plugin.**

---

# Standprüfung 18.11.2026 (verbindlicher neuer QA-Status)

**Die Hab-Texterstellung 0.4.24 ist NICHT für WordPress freigegeben.** Nachgewiesen: Historische Hab-Kategorien passen nicht zur alten Pferde-Kategorieerkennung (0/285), aktueller WP-Bestand und K0-Bindung ungeklärt. Drei nachweisliche Fehler in einer getrennten Quell-QA korrigiert; **kein installierbares Release**. Kompletter Nachweis: PRUEFUNG_20261118_NICHT_INSTALLIEREN.md und Hab-Dateibüro /hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_20261118/. Keine Veränderung am Original-K0, Pferdeatelier oder Live-WordPress. PR #819 bleibt offen als Entwurf.

---

# Hab & Bewahr – Texterstellung: aktueller Stand

**Status:** ARBEITSKOPIE ERSTELLT, NICHT INSTALLIEREN. Stand: 16.11.2026.

- Source: Texterstellung 0.4.23; eigene ZIP: `/hab-und-bewahr/TEXTERSTELLUNG/ARBEITSKOPIEN/Texterstellung_HAB_UND_BEWAHR_ARBEITSKOPIE_0.4.23.zip`.
- Identität der ZIP (SHA-256): `9081d5bf5546d3d8d2035e7d0e2b773adb4cacaa330c3f61036b96306d5bcc70`.
- WordPress-Live-Abnahme: **NEIN**.
- Portaleigene Fachregeln vollständig: **NEIN** (74 von 78 PHP-Dateien mit Pferde-/PSTE-Suchtreffern; Anzahl der tatsächlich fachlich zu ändernden Stellen noch nicht bewertet).
- Alte Pferde-Kategoriekarte und Familien-Overrides: **entfernt, nicht durch Schätzwerte ersetzt**.
- K0-Änderungen: **0**.
- Redaktionsplan zurückgesetzt: **NEIN**, gesonderter aktueller Export steht aus.
- Nächste Aufgabe: Portalanpassung im jeweiligen eigenen Chat, danach eigenständige Installationsfreigabe.
