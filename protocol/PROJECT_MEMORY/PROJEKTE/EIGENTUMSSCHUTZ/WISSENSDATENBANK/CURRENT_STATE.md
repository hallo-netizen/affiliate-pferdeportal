# HAB & BEWAHR – WISSENSDATENBANK – CURRENT STATE
<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->
STAND: 2026-10-14
STATUS: **GLOSSARBÜRO EINGERICHTET / 100 VORLAGEN GESICHERT, 4 IDENTISCHE WP-KATEGORIEN AUSGESCHLOSSEN, 96 RECHERCHEKANDIDATEN / DESIGN 0.1.8 GLOSSARMANAGER LOKAL PASS / 0 GEPRÜFTE FACHARTIKEL / WORDPRESS-LIVE OFFEN**.

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

## BESTAND
- Unter `/mnt/data/HAB_UND_BEWAHR_DESIGN_0.1.7_MOBIL_GLOSSAR.zip` waren **100 unvalidierte Kurzdefinitionen** (nur Begriff/1 Satz/Welt) enthalten. Sie sind **KANDIDATEN**, keine SEO-/Publish-Freigabe.
- Zentrales Portal hat den bestehenden WP-Zielknoten `editorial:glossar` für „Glossar A–Z“ (WP Page ID 184, Slug `magazin-glossar-a-z` im R3/V8-Readback vom 13.10.2026). Nicht ungeprüft zweite öffentliche Seite anlegen. Die Designversion 0.1.7 registriert zusätzlich eine eigene `/glossar/`-Rewrite; LIVE-Befund des Nutzers: leer/nicht sichtbar. Exakte WP-Ursache OFFEN.
- 7 Pferde-Glossardatensätze sind quellengebunden, **keiner** davon ist fachlich direkt auf Sicherheit übertragbar.

## ZIELVERTRAG
Einzelakten/Validator/WordPress-Draft gemäß `GLOSSAR/GLOSSAR_STRUKTUR.md`, Frontend gemäß `GLOSSAR/DESIGN_GLOSSAR.md`. Nicht ohne echten Quellenbeleg freigeben.

## ERSTER OFFENER BLOCKER
WordPress-Glossarroute, vorhandene Zielseite und Plugin-Owner nicht live kontrolliert; alle 100 Sicherheitskandidaten sind redaktionell ungeprüft. Keine Live-PASS-Behauptung.

## EXAKT EINE NEXT ACTION
**Das bestehende Designplugin 0.1.7 in WordPress mit EINER identitätsgleichen 0.1.8-ZIP aktualisieren und LIVE die vorhandene Glossarseite bzw. `/glossar/`, die Backend-Menüs „Glossar → Geprüfte Batches/Prüfbedarf“ sowie mobile/Desktop-Seiten prüfen; keine fremden Kategorien ändern oder weitere Plugins installieren.** Danach beginnt die Fachrecherche des ersten 25er-Kandidatenpakets, nicht Auto-Publish.
