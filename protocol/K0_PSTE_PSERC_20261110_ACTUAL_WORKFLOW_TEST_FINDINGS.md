# Tatsächlicher KISS-Workflowtest 10.11.2026: PSTE + PSERC + K0

**STATUS: ALLE AUSGEFÜHRTEN PRÜFUNGEN PASS; DIE SEO-INTENT-HERKUNFTSBINDUNG IST NICHT NACHGEWIESEN, DA DER BESTEHENDE 5-FELD-EXPORT DIESE NICHT ENTHÄLT. KEINE PRODUKTIVFREIGABE.**

## Exakte Plugin-Versionen aus dem geprüften ZIP (nicht Behauptung, dass WordPress diese bereits installiert hat)
- PSTE-0.57.144.33-KISS-BEREINIGT-NUR-TEST.zip, SHA256 `cd62e7c58dce4bfe9c75026bb604e0182f45a12f5d26075d9b1a85a859472ae2`.
- PSERC-0.28.60-KISS-EXTERNER-SEO-OWNER-NUR-TEST.zip, SHA256 `c9c7e90b265e650739d2568a7cb807238db7f081ddcf7d8698fe64961b84f22a`.
- K0: ausschließlich Kopie `qa/k0-editorial-owner-only-20261110`, 81 HARDrules nach den 4 ausdrücklich genehmigten Titel-/Keyword-Entfernungen. K0 `konzept0-portal-neutral-20261002` UNVERÄNDERT mit 85 Regeln.

## Test 1 – echte PHP-Klassen aus aktuellen ZIPs, 29/29 PASS (lokal)
- In PHP 8.4 wurden direkt aus den beiden ZIPs die Klassen `PSTE_DataForSEO_Client`, `PSERC_Title_Gate`, `PSERC_Metadata_Boundary` und `PSERC_Stable_Json` ausgeführt.
- Es wurden die drei echten Provider-Schrittmethoden `keywordSuggestionsDriverStep`, `relatedKeywordsDriverStep`, `keywordIdeasDriverStep` mit **simulierten** HTTP-Providerantworten ausgeführt; Endpoint-Whitelist, Antworten, extrahierte Keywords, Caching, Fehlerfall geprüft.
- Wichtig: Mock-Providerdaten waren gezielt so gewählt, dass sie die 3 Original-Keywords aus dem Benutzer-Export enthalten; dies **beweist nicht**, dass DataForSEO diese Keywords tatsächlich aktuell recherchieren würde. Keine echte Provider-Abfrage/Kosten und keine WordPress-Datenbank.
- **Originale WordPress-TEST-Übergabedatei** `seo-redaktionsplan-produktionshandoff-42619ca7...json` im unveränderten PSERC .60: `validateBatch` PASS, `requireReadyBatchForExport` PASS, alle 3 Titel im vorhandenen PSERC-Title-Gate PASS, keiner korrigiert oder umgeschrieben.
- Manipulation Titel/Batchhash, doppelter Planplatz und ein sechstes `search_intent`-Feld im exportierten Element werden weiterhin BLOCKED. FAQ-Titel ohne erforderliches `?`, Doppelpunkt im Titel ebenfalls bei vorhandener PSERC Titelprüfung BLOCKED.
- Exakte PHP-Quellen, Mock-Test und JSON-29/29-Bericht in Projekt-Library `/pferdeatelier/PLUGINS/QA/PSTE_05714433_PSERC_02860_DATAFORSEO_MOCK_HANDOFF_20261110.json` und `..._TEST_20261110.php`.

## Test 2 – GitHub K0 QA einschließlich ECHTER LanguageTool 6.8 und WordPress-Export
- [GitHub QA Actions Run 42839831576](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42839831576): **PASS**.
- Bestand: **51/51** K10-Tests plus **7/7** neue K0-SEO-Owner-Negativtests PASS; Python-Syntax PASS; originaler Writer-, LanguageTool-, WordPress-Export- und Github-Produktionsworkflow-Dateivergleich PASS.
- Echter ursprünglicher Dreier-Hand-off: **3/3** Einzel-Intakes, automatische Portalzuordnung, originaler Titel, Suchintention im vorhandenen Autor-Kontext und NEUE 81er-Regelbindung für den Writer = PASS. Diese drei Tests bedeuten **3 K0-Schreibaufträge vorbereitet**, nicht 3 neu geschriebene fertige Artikel.
- Ein bereits fertig verifizierter echter Artikel (Horseware-Regendecken, `...-01-r2`) wurde **schreibfrei** in den **neuen Writer-Job mit aktuellem 81er-Regelpaket** übernommen und neu versiegelt. **80 Text-/Quellen-/Aufbauregeln vor LanguageTool PASS**.
- **ECHTES LanguageTool 6.8** erneut mit exakt hashgeprüfter JAR-Datei auf dem unveränderten sichtbaren Artikeltext ausgeführt: 0 Fehler / PASS. **Finale 81er-Gesamtprüfung PASS**.
- Neuer `SYSTEM4_WORDPRESS_HANDOFF_V1` für genau diesen originalen Artikel gebaut und vollständig `verify_export` geprüft: **PASS**, Titel und Body **unverändert**, ursprüngliche kanonische ID/Planplatzverknüpfung erhalten. Diese Datei wurde **NICHT** in WordPress importiert oder veröffentlicht.
- Negativtests: Titeländerung im Writer, Suchintent-Änderung nach Writer-Job und Titeländerung im WordPress-Export = BLOCKED.
- Test benutzt bewusst eine **vorher echt verifizierte WordPress-Kategorie (ID 10)** aus der früheren Produktionsdatei. Keine frische Neurecherche für den wiederverwendeten Artikel; dies ist ein **Regressionstest**, kein neuer frisch recherchierter Produktionsauftrag.
- Der unveränderte aktive K0-Workflow selbst wurde NICHT ausgelöst. Die Tests laufen auf getrenntem QA-Branch und haben nur lesende GitHub-Rechte.

## Test 3 – aktuelles öffentliches WordPress LIVE (nur GET, KEIN Schreiben)
- [GitHub QA Read-only Run 42840365652](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42840365652): **PASS**.
- Echt aktuelle WordPress REST-Kategorie `pferdedecken-regendecken-beratung`, **ID 10** gefunden.
- `engine.k0_full_rules.verify_live_link_targets` gegen `https://pferde-atelier.de`: **3/3** vorhandene Verlinkungsziele verifiziert.
- Keine WordPress-Dateien/Plugins installiert, nichts importiert oder veröffentlicht.

## Wichtiger, nachgewiesener offener Vertragsmangel – vor Freigabe beheben
- `PSTE_Intent_Profile` bindet die Suchintention ausdrücklich aus SEO-Daten/Klassifikatoreinigung und gibt u.a. `search_intent` plus `profile_sha256` aus.
- `PSERC_Compiler::finalizeAllocationRow()` enthält diese `intent_profile` im ausführlichen Produktionsplan-/Manifest-Eintrag. `PSERC_Plan_Snapshot_Store` hält die Manifestdetails serverseitig bereit.
- **Aber `PSERC_Admin::exportLivePreview()` exportiert ausdrücklich NUR `PSERC_Plan_Snapshot_Store::materializeReadyBatch(...)`, und der geschützte Metadatenvertrag besitzt EXAKT fünf Felder (`article_type,category,plan_slot,target_keyword,title`) – ohne Search Intent.**
- Bei K0 liegt Suchintention erst im späteren `AUTHORING_CONTEXT.content_profile.search_intent` vor. Die Writer-Verifikation sichert die Unverändertheit **ab diesem Punkt**, hat aber aus dem fünfteiligen Ursprungs-Hand-off **keinen Beweis**, dass der Intent 1:1 von der PSTE-/PSERC-Freigabe stammt. Der frühere Konflikt kann daher beim Erstellen des Autor-Kontexts weiterhin entstehen, auch wenn K0 selbst nicht mehr neu entscheidet.
- **KISS-Lösung noch nicht implementiert:** Die **bereits vorhandene** freigegebene Intent-Entscheidung zusammen mit Artikel-/Planplatzbindung automatisch aus dem bestehenden PSERC-Manifest dem K0-Autor-Kontext zuordnen. Den **5-Feld-Handoff selbst NICHT erweitern**, keine neue redaktionelle Zweitentscheidung, keine Keyword-Wortzwangregel. Für den Übergang ist ein minimaler, nachvollziehbarer Eigentümernachweis/Transport erforderlich. Erst wenn der Nachweis an derselben `plan_slot`-Identität gelingt, kann K0 eine wirklich garantiert unveränderte SEO-Entscheidung übernehmen.
- Ein echter Live-DataForSEO-Lauf setzt echte im WordPress-TEST eingerichtete Provider-Credentials/Providerstatus voraus und wurde NICHT simuliert als „echter Live-Abruf“ ausgegeben.
- Ein kompletter NEUER Dreierlauf mit frisch recherchierten vollständigen Texten sowie tatsächlich installiertem aktuellem Plugin auf WordPress-TEST ist **noch nicht durchgeführt** und darf nicht als PASS bezeichnet werden.

## Sicherheitsstand
- **Kein K0-Produktionsbranch geändert; keine WordPress-Installation verändert; kein Provider gebührenpflichtig aufgerufen.**
- Beide ursprünglichen K0-Qualitätsphasen und Reparaturschleifen, 81 verbleibende Schreib-/Faktenschutzregeln, H2 Anti-Stakkato, Wort-/Absatz-/Fazit-/Tabellen-/Links-/Integritäts-Gates vollständig unverändert.
- **Aktueller Status:** QA_IMPLEMENTED, QA_PASS_FOR_TESTED_SURFACES, SOURCE_INTENT_BINDING_MISSING, FULL_FRESH_LIVE_PRODUCTION_E2E_NOT_RUN, PRODUCTION_RELEASE_BLOCKED.
