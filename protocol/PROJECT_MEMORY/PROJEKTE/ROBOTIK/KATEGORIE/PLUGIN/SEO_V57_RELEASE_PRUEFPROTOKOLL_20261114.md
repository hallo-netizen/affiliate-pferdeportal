# Robotik V57 – Kategorie-Plugin 0.4.4: gebündelte SEO-Gesamtrecherche (TEST, noch nicht WordPress-live-abgenommen)

**14.11.2026 · Einzige Pluginidentität:** `robotik-kategorie-workflow`, Update aus der tatsächlich vorhandenen Library-ZIP 0.4.3. **Kein neues Zusatzplugin, kein WordPress-Import, keine externen API-Aufrufe in der Erstellung.**

## Bewiesene Abdeckung
- **437** bekannte Suchbegriffe aus dem geprüften V52-Plan, davon 141 Robotertypen und 296 zugehörige Rubrikbegriffe. 16 fachliche HOLD-IDs werden mit Quelle mitgeführt.
- **8** Keyword-Ideas-Abfragen, jeweils eine für Haushalt (18 Typbegriffe), Garten (14), Freizeit (14), Sport (17), Bildung (10), Pflege (15), Humanoide (12), Gewerbe (41), jeweils maximal **300 Anbieter-Ideen**. Neue Ideen erhalten KEINE automatisch zugewiesene WordPress-Kategorie. Bei Erreichen des Limits ausdrücklich „möglicherweise abgeschnitten“; kein Vollständigkeitsversprechen.
- **29** eindeutige Google-Top-10-Abfragen für **16** vordefinierte, fachlich begründete SERP-Paare. Gleiche URLs pro Paar werden verglichen; dieser Befund ersetzt nicht den fachlichen Entscheid und ist kein Beweis für Indexierungserfolg. Die gebündelte Recherche umfasst **38 interne Anbieteranfragen** unter **einem manuellen Nutzer-Kostenfreigabeklick** und erzeugt **einen einzigen exportierbaren JSON-Gesamtbericht**.
- Benutzer gibt vorher ein USD-Maximalbudget an; bei derzeitigen Prüfdaten liegt die vorläufige Sicherheitsreservierung bei **0,765 USD**. Das UI schlägt 1 USD vor, **kein geschätzter tatsächlicher Rechnungsbetrag**. Für jede neue Anfrage wird ein konservativer Betrag reserviert; wird er durch Anbieteränderungen überschritten, wird die Verarbeitung gestoppt. Bereits gestartete Aufrufe können unabhängig vom Plugin Kosten verursachen. Bei ungewissem API-Timeout wird ausdrücklich nicht wiederholt.

## Unverändert gegenüber 0.4.3 – byteweise verglichen
- `includes/class-robotik-inventory.php` (lesender WordPress-Bestandsbericht)
- `includes/class-robotik-first-import.php` und `assets/robotik-first-import-plan.json` (**altes** 104-Seiten-/89-Kategorien-Importprofil weiterhin geschützt; KEINE Importfreigabe für 141er-Fachentwurf)
- `includes/class-robotik-publish.php` (bisherige Sammelveröffentlichung)
- `assets/robotik-v52-seo-candidates.json` (437er-Quellmanifest, keine neue Masterliste)
- Bestehende Zugangsdaten und zuvor gespeicherte Einzelberichte bleiben bestehen. Historische DataForSEO-Einzelaufrufe bleiben zugänglich, sind aber hinter einer eingeklappten Altsektion, um Fehlbedienung zu vermeiden.
- An Dateien geändert: Pluginheader/Version, `includes/class-robotik-dataforseo.php`, lesender README. **Keine anderen WordPress-Dateien, keine eigene DB-Tabelle, kein Cron.**

## Reale lokale Tests – ohne kostenpflichtige Daten
- PHP-Lint **5/5** Dateien PASS; ZIP hat **8** Originalpaket-Dateien, gleiche Pluginordneridentität und CRC-PASS.
- V52-Plankontrolle **437/437** Keywords, **16/16** HOLDs, **141/141** Typen als weltzugeordnete Recherche-Seedbegriffe, **8/8** Welten vorhanden, **29** eindeutige SERP-Suchtexte, **38** einzelne Anbieter-Aufgaben.
- WordPress-API-Mock mit **38** *simulierten* Antworten: gesamter Auftragsstart, alle acht Ideengruppen, 16 Überlappungsberichte, ein Fortschrittsstatus **COMPLETE**, Kosten je Antwort summiert, 437 Keywords im Bericht. Der in dieser Simulation angezeigte Betrag ist ein **Testwert**, keine echte Anbieterrechnung.
- Negativtests: zu kleines Budget → 0 Anbieter-Aufrufe; simulierter HTTP-Fehler nach begonnenem API-Aufruf → `BLOCKED_UNCERTAIN`; weiterer Klick → **kein zweiter Anbieter-Aufruf**. Simulierter zusätzlicher AJAX-Aufruf nach `COMPLETE` → **kein neuer Bezahlaufruf**.
- **Nicht als PASS behauptet:** echtes WordPress-Hosting (PHP-Zeitlimits, Sitzungen, Admin-JavaScript), echte DataForSEO-Zugangsdaten, echte API-Ergebnisse/Kosten, Live-Google-Resultate, vollständige Google-Intententscheidung, aktiver WP-Ist-Bestand 14.11.2026, neues V52-Import-Delta.

## Nächste Nutzeraktion, gebündelt
1. Nur **dasselbe vorhandene Kategorie-Plugin** mit der 0.4.4-Test-ZIP aktualisieren, zuvor WordPress-Backup. Keine zweite Pluginlinie installieren.
2. WordPress → **Robotik Kategorie → DataForSEO → SEO-Gesamtrecherche EINMAL starten**. USD-Budget bewusst bestätigen (die UI zeigt Reservierungsrahmen und Eingabefeld, Vorgabe 1,00 USD). **Nicht die historischen Einzelabfragen** benutzen. Browser-Tab während des einen Ablaufs geöffnet lassen. Bei Fehler nicht erneut kostenpflichtig starten.
3. Danach **EINEN SEO-Gesamtbericht (JSON)** herunterladen und im Chat bereitstellen. Danach bündelt der Chat den gesamten fachlichen Entscheid und die sichere WordPress-Delta-Vorschau. Erst der spätere **ausdrücklich freigegebene** Import dürfte WordPress verändern.

**Kostenquelle (Stand 14.11.2026):** https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api (Live Labs Google: 0,012 USD + 0,00012 USD je Item), https://dataforseo.com/help-center/serp-api-pricing-depth-update-faq (Live Google SERP bis 10 Treffer: 0,002 USD je Abfrage), https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_ideas-live/ (max 200 Seeds, max 1000 Ergebnisse). Diese Preise können sich ändern; es wurden keine realen Kosten erzeugt.

**Library ZIP:** `/robotik/Konzeptbüro/ROBOTIK_KATEGORIE_WORKFLOW_0.4.4_SEO_GESAMTPRUEFUNG_NUR_TEST.zip` · **SHA256:** `d7fcee60a1c3adc831b0226a6cf2413e84daaaea5732fd240fd5b3ea5f9dea10` · **ZIP-Größe:** 54.117 Bytes.