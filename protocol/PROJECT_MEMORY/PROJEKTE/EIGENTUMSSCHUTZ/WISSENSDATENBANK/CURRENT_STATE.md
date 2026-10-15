# HAB & BEWAHR – WISSENSDATENBANK – CURRENT STATE
<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->
STAND: 2026-10-14
STATUS: **42 QUELLENBEZOGENE GLOSSAR-KURZDEFINITIONEN IM GRUNDBESTAND / 96 RECHERCHEKANDIDATEN NACH 4 GESPERRTEN KATEGORIE-DUBLETTEN / 0 VOLLSTÄNDIG QUELLEN- UND REDAKTIONELL FREIGEGEBENE 150–200-WORT-EINZELARTIKEL / DESIGN 0.1.14 LOKAL PASS / WP-LIVE OFFEN**.

## ZIEL
Übernehme das quellengebundene Fachwörterbuch-Modell von Pferde-Atelier, aber keine Pferdethemen/-texte. Jede Glossarakte ist eigenständig, validierbar und für spätere WordPress-Entwürfe bestimmt. Benutzer-SEO erfolgt über sinnvolle Begriffe, nicht massenhaft dünne Seiten.

## GEPRÜFTE VORLAGE
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`,
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/GLOSSAR_STRUKTUR.md`,
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/TECHNIK_GLOSSAR_MANAGER_CURRENT.md` und
`PFERDE_ATELIER/DESIGN/CURRENT_STATE.md` (Pferde-Design 1.50.541 LIVE PASS). Quelle liefert 150–200-Wort-Textvertrag, Quellenmodell, Synonyme, Related, World, primary_target, REVIEW und Draft-Readback. Nicht die WordPress-Livefreigabe auf Hab & Bewahr übertragen.

## IMPLEMENTIERT – 14.10.2026 (NUR LOKAL + CAMPUS)
- Struktur des echten Pferde-Atelier-Wissensbüros inklusive `AKTENSCHRAENKE/GLOSSAR`, Strukturbürotür, Quellenstandard, Fachvertrag, Designvertrag, Register, Technikvertrag und EINE Current-Autorität übernommen und auf Sicherheit zugeschnitten. `AUTORITAETSPLAN.json` enthält jetzt Scope `EIGENTUMSSCHUTZ_WISSENSDATENBANK`.
- Separates WIP-Archiv mit **100 einzelnen Kandidatendatensätzen**: `HAB_UND_BEWAHR_GLOSSAR_100_KANDIDATEN_WIP.zip`, SHA256 `99522a0c069613960bbb2b5fc2e6f8dacadb743dbec71bead5ae258069fa07f6`; persönliche Wissensablage `/Eigentumsschutz/Wissensdatenbank/Glossar/`. 4 gegen **tatsächliches 546er R3-Readback** bestätigte exakte Kategorienamen gesperrt: Anwesenheitssimulation (WP 435), Gaswarnmelder (222), Stromausfallmelder (238), Wassermelder (210). 96 Recherchekandidaten, 0 als GEPRUEFT markiert.
- **0.1.8 WordPress-Implementierung**: Gleichidentisches vorhandenes Designplugin `hab-bewahr-design-vorschau/`, ZIP `HAB_UND_BEWAHR_DESIGN_0.1.8_GLOSSAR_MANAGER.zip`, SHA256 `c4b3f89eb1e3bebecc1c7ac3f78510f6f3c37ddae41b6adc87ad17dbbd253769`. In WordPress `hbdp_glossar_term` als eigenständiger redaktioneller CPT, A–Z-Index, Suche, Einzelansicht mit Beziehungen, Quellenprüf-/Freigabe-Metabox, Admin-Batch-Staging mit Zweitbestätigung (max 25), Draft-only, Readback, Rollback, read-only Prüfbedarf 6/12/24. Kein weiteres Plugin, keine Kategorienwrites oder Crons.
- Frontend nutzt *bestehenden zentralen* `editorial:glossar`-WP-Seitenknoten (R3-Readback: Seite 184), falls veröffentlicht; sonst robusten `/glossar/`-Fallback. Frühere direkte `/glossar/`-Route zeigt/redirectet zu EINER gültigen kanonischen Seite. Kein WP-Page-Neuanlageautomatismus, keine Veröffentlichung von 100 bloßen Kurzdefinitionen.
- Fachliche Grenze: Alte `data/glossary.json` ist **aus dem Design-ZIP entfernt** und als Einzelakten-WIP-Paket im Wissensbüro gesichert. Solange 0 freigegebene Begriffe: brauchbare Glossarseite mit Vorbereitungsvermerk plus `noindex` statt dünne SEO-Unterseiten. Bei ersten freigegebenen Posts automatisch A–Z-Index und indexierbare Detailseiten.
- Prüfungen: PHP-Lint alle PHP-Dateien; 17/17 Validator-Positiv/Negativprüfungen; 4/4 Import-Mockpfade (korrekter Draft-Import, Dublette BLOCK, Schreibfehler-Rollback, Readback-Rollback); 20/20 Chromium-Ansichten (Startseite, leeres Glossar, befülltes Glossar, Detailseite x 5 Viewports 320–1280px) inkl. Suche/Overflow/JS; ZIP-Integrität; WordPress-Live **NICHT** geprüft. 0.1.7-Nav-/Bildassets unverändert.
- Vorbild ist das Konzept und Layoutprinzip (Pferde-Designquelle 1.50.541/Glossa-Relation 1.50.528), **keine nachgewiesene pixelgenaue 1:1-Codekopie**; die originalen PPA-Plugin-ZIPs waren in dieser Sitzung nicht im Container verfügbar.

## AKTUELL – GLOSSAR-GRUNDBESTAND 0.1.14 / 15.10.2026
- **Nutzerentscheidung:** Mobiles Logo nach echtem Screenshot nun ausdrücklich „PASS“, **nicht** weiter bearbeiten. Facharbeit ab jetzt Glossar, eigenes Wissensdatenbank-/Glossarbüro.
- **42 konkret redaktionell verfasste, quellenbezogene Kurzdefinitionen** in allen sechs Schutzwelten: Einbruch 9, Vandalismus 6, Wasser 7, Feuer 7, Wetter 6, Technik 7. Jede mit Begriffsname, Welt, individueller Kurzdefinition, benannter öffentlich zugänglicher Fachquelle und verifizierbarer originaler URL (u. a. Polizeiliche Kriminalprävention, BBK, Verbraucherzentrale, VDE, BSI, Deutscher Feuerwehrverband). Status **RECHERCHEGESTUETZTER_KURZREGISTER_ENTWURF**, nicht `GEPRUEFT` im Sinne der 150–200-Wort-Pferde-Atelier-Einzelakte. Die Belegquellen müssen vor konkreter Einzelpublikationsfreigabe erneut genau pro Aussage gesichtet werden.
- **Autoritative fachliche Ablage der 42 Datensätze** im persönlichen Wissensbüro unter `/Eigentumsschutz/Wissensdatenbank/Glossar/SICHERHEITSGLOSSAR_KURZREGISTER_42_QUELLENBEZOGEN_WIP.json`, identische schreibgeschützte Auslieferungskopie in Version 0.1.14 `data/glossary-quickreference.json`. 100 bisherige Kandidatenakten bleiben eigenständig in der Wissensablage; 4 exakte WordPress-Kategoriedubletten verboten; 96 fachliche Recherchekandidaten. Nicht behaupten, alle 96 seien fertig bearbeitet.
- **Publikationsmodus:** Öffentliche `/glossar/`-A–Z-Übersicht zeigt die 42 Kurzerklärungen ohne WordPress-Schreibvorgänge. Solange keine fachlich geprüfte WordPress-Glossar-Einzelakte ausdrücklich veröffentlicht ist, bleibt das Glossar **noindex**; 42 Kurzerklärungen erhalten keine eigenen dünnen URL-Einzelseiten. Native vom Editor geprüfte/veröffentlichte `hbdp_glossar_term`-Beiträge ersetzen die gleichnamige Kurzerklärung statt Dopplung, mit sinnvollem Link. Das separate Glossar-Admin-Draft-Import-/Rollbackverfahren bleibt unverändert.
- **Installierbares ZIP:** `HAB_UND_BEWAHR_DESIGN_0.1.14_GLOSSAR_AZ_42_BEGRIFFE.zip`, SHA256 `368a9e9a4e59d52d268d7b5c0be4cef37825cc3fd043d7d86fdafcfd5f4031a2`, 1.650.841 Bytes. Identischer Plugin-Ordner `hab-bewahr-design-vorschau/`; 52 Dateien, delta gegenüber 0.1.13: vier bestehende geändert (Hauptplugin nur Version/Asset-Cache, `includes/glossary.php`, `assets/glossary.css`, README), zwei neue (`assets/glossary.js`, `data/glossary-quickreference.json`). Alle übrigen Dateien **bytegleich**, insbesondere mobile Logos/Header-CSS, Kategoriebaum, Hauptwelt-Langtexte und Breadcrumb.
- **Local Gate:** 7/7 PHP-Syntax, 42/42 JSON-Einträge mit eindeutiger Slug-ID, Quellen-URLs vorhanden, 6/6 Welten; Chromium 14/14 verschiedene Breiten/mit und ohne nativen publizierten WordPress-Term, Suche, Negativsuche, Weltfilter, Published-Begriff-Dedupe sowie kein horizontaler Overflow PASS; ZIP-CRC PASS. **Echte WP-Live-Sichtung von `/glossar/` noch offen**. Die URL wurde zuvor von außen durch Web nicht zuverlässig abgerufen; kein künstlicher Live-PASS.

## BESTAND
- Unter `/mnt/data/HAB_UND_BEWAHR_DESIGN_0.1.7_MOBIL_GLOSSAR.zip` waren **100 unvalidierte Kurzdefinitionen** (nur Begriff/1 Satz/Welt) enthalten. Sie sind **KANDIDATEN**, keine SEO-/Publish-Freigabe.
- Zentrales Portal hat den bestehenden WP-Zielknoten `editorial:glossar` für „Glossar A–Z“ (WP Page ID 184, Slug `magazin-glossar-a-z` im R3/V8-Readback vom 13.10.2026). Nicht ungeprüft zweite öffentliche Seite anlegen. Die Designversion 0.1.7 registriert zusätzlich eine eigene `/glossar/`-Rewrite; LIVE-Befund des Nutzers: leer/nicht sichtbar. Exakte WP-Ursache OFFEN.
- 7 Pferde-Glossardatensätze sind quellengebunden, **keiner** davon ist fachlich direkt auf Sicherheit übertragbar.

## ZIELVERTRAG
Einzelakten/Validator/WordPress-Draft gemäß `GLOSSAR/GLOSSAR_STRUKTUR.md`, Frontend gemäß `GLOSSAR/DESIGN_GLOSSAR.md`. Nicht ohne echten Quellenbeleg freigeben.

## ERSTER OFFENER BLOCKER
WordPress-Glossarroute, vorhandene Zielseite und Plugin-Owner nicht live kontrolliert; alle 100 Sicherheitskandidaten sind redaktionell ungeprüft. Keine Live-PASS-Behauptung.

## EXAKT EINE NEXT ACTION
**Mit dem einzigen vorhandenen WordPress-Designplugin die identitätsgleiche Version 0.1.14 in WordPress aktualisieren und LIVE `https://hab-und-bewahr.de/glossar/` auf dem Smartphone/Desktop prüfen: A–Z mit 42 Begriffen, Textsuche, sechs Weltfilter und benannten Originalquellen sichtbar.** Erst nach echtem Live-PASS beginnt quellenbasierte Einzelrecherche und kontrollierte 25er-Draftproduktion im Glossarbüro. Keine automatische SEO-Veröffentlichung, kein neuer Kategorie-Sync, kein weiteres Designplugin.
