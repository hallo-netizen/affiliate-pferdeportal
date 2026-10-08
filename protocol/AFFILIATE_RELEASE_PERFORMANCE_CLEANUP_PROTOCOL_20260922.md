# Affiliate Performance Cleanup – Problem-/Fehler- und Arbeitsprotokoll 2026-09-22

Rolle: historisches WAS/WARUM-/Fehlerprotokoll und Nachweisweg.
KEINE CURRENT-/Status-/NEXT-ACTION-Quelle. Dafür gilt ausschließlich `control/release-governance/CURRENT_RELEASE.json`.

## Problemstellung

Der eingeschobene Performanceblocker wurde zunächst durch massive Affiliate-DB-Wiederholungen sichtbar:
- ca. 13.671 Queries / ca. 10,3 s Serverzeit;
- ca. 11.297 Control-Decision-Lookups;
- ca. 1.484 eBay-BUSINESS-Lookups;
- ca. 305 Creative-Library-Lookups.

6.72.144 beseitigte identische Same-Key-Wiederholungen request-lokal.
6.72.145 ergänzte bounded Batch-Reads für viele verschiedene Keys/Hashes.

Live-Readback nach 6.72.145:
- Affiliate-Einzelquery-Explosion beseitigt;
- gemessene Seiten nur noch ungefähr 318–339 DB-Queries;
- Backendzeit blieb dennoch ca. 4,8–6,7 s;
- damit verlagerte sich der belegte Hauptengpass auf PHP-/Hook-/Template-CPU.

Diagnosebefunde:
- sehr hohe Hookzahlen, u. a. get_post_metadata/get_term/options;
- Router: quadratische eBay-Titelähnlichkeitsarbeit und wiederholte identische Rankingberechnungen;
- Designplugin: derselbe große WordPress-Menübestand wird für Desktop und Mobile separat durch den teuren Core-Setup-Pfad geschickt.

## Durchgeführte Router-Bereinigung

Aufbauend auf dem live getesteten 6.72.145-Stand:
- exact-safe Vorfilter vor `similar_text()`; die bestehende Schwelle `>= 92.0` bleibt alleinige Duplikatentscheidung;
- Titelsignaturen einmal pro Titel vorberechnet;
- request-local Memo für identische `ranked_campaigns_for_slot()`-Aufrufe im öffentlichen Frontend;
- Admin/Cron/REST/WP-CLI/AJAX vom Ranking-Memo ausgeschlossen.

Harte Nachweise:
- 53.361 alte/neue Titelpaarentscheidungen identisch;
- kompletter zweistufiger Seller-/Diversity-Output identisch;
- 792 Unique-Titel: kein False Duplicate;
- 6.72.145 Batch-DB-Vertrag erhalten;
- Bannerregression erhalten;
- GitHub CPU Run 35693134066 SUCCESS;
- Ranking Memo Run 35693058767 SUCCESS;
- Combined Run 35693264536 SUCCESS.

Kandidat:
- `AFFILIATE_ZENTRALE_V6.72.147_PERFORMANCE_CPU_RANKING_CLEANUP_HARDTEST.zip`
- SHA-256 `905f6db0941c04d0275aad3e63db8bdca80fb95f6659de2d2bb118359a9d72a5`
- Fresh-Unpack 27/27 byteidentisch;
- PHP-Lint 21/21 PASS;
- gegenüber 6.72.145 nur `includes/trait-ppar-ebay.php` plus Versionsdatei geändert.
- 6.72.142 GOLDMASTER unverändert.

## Durchgeführte Design-Bereinigung

KISS-Lösung:
- beide bestehenden `wp_nav_menu()`-Aufrufe bleiben bestehen, weil Desktop und Mobile unterschiedliche Objektfilter benötigen;
- nur der teure WordPress-`wp_setup_nav_menu_item`-Setup wird für den zweiten Render request-lokal wiederverwendet;
- Umsetzung über die offiziellen Pre-/Post-Setup-Hooks.

WordPress-7.1.1-Hardtest mit 120 Menüeinträgen:
- Baseline zweiter Render: 2.520 Metadata-Hooks;
- bereinigt zweiter Render: 360;
- Reduktion 85,7 %;
- Desktop-HTML SHA unverändert;
- Mobile-HTML SHA unverändert;
- Desktop-/Mobile-spezifische Filter unverändert;
- GitHub Run 35693870974 SUCCESS.

Wichtige Grenze:
- der Designfix ist als semantischer Patch hart bewiesen;
- er ist noch KEIN installierbares Ersatzpaket;
- ein historischer Design-Vollstand darf den aktuellen Live-Stand nicht überschreiben;
- zuerst muss der exakt aktuelle Live-Vollstand von PPA-013 gebunden werden.

## Kubio-Befund

Kubio ist nicht Teil dieser Bereinigung.
Ein echter WordPress-Export enthält gespeicherte `wp:kubio/...`-Blöcke. Deshalb Kubio nicht blind deaktivieren; Migration/isolierter Test kommt erst nach Abschluss von PPA-001 und PPA-013.

## Sicherungs-/Rollbackregel

Router:
- unveränderlicher Rollbackanker: 6.72.142 GOLDMASTER;
- 6.72.147 bleibt bis Live-Abnahme separater Testkandidat;
- bei Regression keine Live-Flickserie, sondern sofortiger Rückweg auf den Goldmaster.

Design:
- keinen historischen Vollstand als Ersatz für den aktuellen Live-Stand verwenden;
- bestehendes Designplugin bleibt unverändert, bis sein aktueller Vollstand exakt gebunden, gepatcht und vollständig geprüft ist.

## Aktueller Status

Nicht hier ableiten.
Immer `control/release-governance/CURRENT_RELEASE.json` lesen und dessen Frischecheck/NEXT ACTION verwenden.

## DELTA 2026-10-08 — neuer vollständiger Optimierungsauftrag nach 6.72.210

### Nutzer-Hardlock

Der Nutzer öffnet den Performance-/Aufräumscope erneut mit genau einer harten Funktionsregel:

**Komplettes praktisch sinnvolles Optimierungspotential umsetzen, einschließlich möglicher Template-Änderungen/-Löschungen, aber keine Rücknahme irgendeiner Funktion.**

Weiter bindend:
- zusammengehörige Änderungen in großen Blöcken bündeln;
- keine Plugin-/Microfix-Serie;
- keine Architektur-Neuerfindung;
- keine Verdachtsfixes;
- vor Installation lokal POSITIV + NEGATIV + Regression simulieren;
- vorhandene Performanceverbesserungen bleiben erhalten.

### Frischer Affiliate-Release-Stand

Frisch aus der technischen Current-Autorität auf `affiliate-release-current` gelesen:
- `control/release-governance/CURRENT_RELEASE.json`: Generation 296;
- Affiliate-Zentrale **6.72.210 RELEASED**, `release_allowed=true`;
- formaler Release-Check Run `37788785260` PASS;
- exakter Installer SHA-256 `43ca6033a0f8dc929f777fc6580f2b41dfd711c6f561db99658f402cc5af88a1`;
- Source-Manifest `8b3552ff93d482525e41bd0d279a609d8dd538bf672313ba29574a07f33992bf`.
Der Release ist abgeschlossen; neue Sourceänderung nur im ausdrücklich neu geöffneten Performance-Scope.

### Reale Performance-Differenz 01.10. → 08.10.

Gleicher passiver Diagnosemodus `Performance Diagnose Safe 2.3.0 / PASSIVE_NO_FILTERS`.

Normale Seiten:
- `/ausruestung/`: 302 → **420** DB-Queries; Serverzeit 1,560219 s → 1,557568 s.
- `/stall/`: 299 → **419** DB-Queries; 1,497710 s → 1,660128 s.
- `/weide/`: 302 → **419** DB-Queries; 1,528833 s → 1,586224 s.
- `.../pferdesaettel/`: 320 → **654** DB-Queries; 4,634054 s → **2,948636 s**.

Bewertung:
- Es existiert ein realer Query-Anstieg, aber die Wall-Time ist nicht überall schlechter; Pferdesättel ist trotz deutlich mehr Queries schneller.
- Daher **nicht** aus Queryzahl allein einen Performancefix ableiten.
- Beide Reports melden `db_query_timing.available=false`; Owner-/Querygruppen sind nicht aufgezeichnet. Der Verursacher des zusätzlichen Queryvolumens ist mit diesen Exporten noch nicht belastbar zugeordnet.
- Beide Reports melden keinen persistenten Object Cache (`object_cache=null`).
- Der beobachtete aktive Pluginbestand ist in den beiden Vergleichsreports gleich; reine Pluginanzahl erklärt die Differenz nicht.

### Neuer belegter Affiliate-Fehler

Der 08.10.-Report meldet auf mehreren Seiten:
`Undefined variable $required_creative_type` in `pferdeportal-affiliate-router.php:2538`.

Die aktuelle 6.72.210-Source bestätigt: `render_affiliate_slot_for_context()` verwendet die Variable im normalen Rendererzweig ohne lokale Initialisierung.

Autoritativer Fehlerbeleg: `AFF-ERR-064`.
Kein separater Mikroinstaller; Reparatur nur gebündelt im Performanceblock.

### Header-/AJAX-Suche

Realer Nutzerbefund: Hauptsuche/AJAX reagiert deutlich langsamer als früher.

Geprüft:
- Relevanssi Live Ajax Search war aktiv.
- Das Hauptplugin Relevanssi fehlte zunächst.
- Nutzer installierte/aktivierte Relevanssi wieder und testete erneut: **keine erkennbare Verbesserung**.
- Damit ist „fehlendes Relevanssi“ **nicht** als Hauptursache belegt.
- Historischer Repository-Sourceextract zeigt, dass der eigene Header-AJAX-Weg bereits wesentlich früher existierte; die aktuelle Verlangsamung darf nicht als Folge einer angeblich neuen Suchentwicklung behauptet werden.
- Der 08.10.-Diagnoseexport enthält AJAX-Requests, aber keine owner-genaue SQL-Zeitaufschlüsselung. Ursache offen.

### Template-Kit-Grenze

Letzter expliziter WordPress-/Pluginreadback im PLUGINS-Büro: Affiliate Portal Template Kit **1.50.578 aktiv**.

Im aktuell autoritativen GitHub-Weg ist für diesen Abschluss **kein exakt gebundener vollständiger 1.50.578-Sourcebaum** als technische Current-Quelle nachgewiesen. Historische Sourceextracts reichen für eine Änderung nicht.

Folge: **Keine Template-Datei ändern oder löschen, bevor exakt 1.50.578 gebunden ist.** Das ist Sicherheitsbindung, keine neue Architektur.

### Große Optimierungsgruppen

1. **Runtime / Query Ownership**
   - zusätzlichen Queryanstieg reproduzieren und einem Owner/Callpath zuordnen;
   - unnötige globale Hooks/Queries requestlokal reduzieren;
   - keine Funktionsänderung.

2. **Header-Suche / AJAX**
   - alle bestehenden Ergebniswelten und Fallbacks 1:1 inventarisieren;
   - redundante Suche/DB-Arbeit nur dann entfernen, wenn Positiv- und Gegenfälle identische funktionale Ergebnisse liefern;
   - Relevanssi nicht als Ursache/Fix voraussetzen.

3. **Template / Frontend / DOM**
   - tote Altpfade, doppelte Renderer, global unnötige Hooks/Assets und DOM-Ballast prüfen;
   - Löschung nur mit nachgewiesener vollständiger Funktionsdeckung an anderer Stelle;
   - Design/Funktion/Navigation unverändert.

4. **Affiliate-Zentrale**
   - AFF-ERR-064 im selben Block beheben;
   - aktuelle 6.72.210-Ranking-/Provider-/Slot-/Veto-/Performancepfade schützen;
   - kein Rückgriff auf ältere Quellen.

5. **Plugin-/Asset-/Storage-Konsolidierung**
   - erst nach Abhängigkeitsbeweis inaktive/redundante Plugins oder Assets entfernen;
   - DB-/Storage-Closeout mit gleicher Messung vor/nachher;
   - kein neues Hilfsplugin.

### Erster sicherer Schritt

Vor jedem Sourcewrite:
**exakten aktuellen Template-Kit-1.50.578-Vollstand binden und danach einen gemeinsamen lokalen Baseline-Harness für 6.72.210 + 1.50.578 aufbauen, der normale Seiten und Header-AJAX reproduziert und POSITIV/NEGATIV/Funktionsgleichheit misst.**

Bis dahin keine Template-/Affiliate-Sourceänderung.

