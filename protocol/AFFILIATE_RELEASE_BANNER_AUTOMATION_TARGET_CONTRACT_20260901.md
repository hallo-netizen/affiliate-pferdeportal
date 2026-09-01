# AFFILIATE-ZENTRALE — VERBINDLICHER ZIELVERTRAG BANNERAUTOMATION V6.64.0

Stand: 2026-09-01
Repository: `hallo-netizen/affiliate-pferdeportal`
Branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`
Status: `BOUND / IMPLEMENTATION_PENDING`

## 1. Autorität und Ausführungsbindung

Dieser Zielvertrag konkretisiert den im `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md` bereits gebundenen nächsten Banner-Automationsblock. Vor jeder Umsetzung sind in dieser Reihenfolge zu lesen:

1. `control/release-governance/CURRENT_RELEASE.json`
2. `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`
4. dieser Zielvertrag
5. die aktuelle kanonische Source unter `release/affiliate-zentrale/current/affiliate-portal-router/`

Nur fortfahren, solange Governance weiterhin bestätigt:

- `workstream=AFFILIATE_ZENTRALE`
- `mode=ENFORCED`
- `active_candidate.version=6.64.0`
- `active_candidate.status=WORKING`
- `active_candidate.release_allowed=false`
- `execution_state.state=RUNNING_BOUND_RELEASE_GATES`
- `execution_state.authorized_next_action=RUN_BOUND_RELEASE_GATES`
- `branch_policy.active_work_branch=affiliate-release-current`

Bei Abweichung: `FAIL_CLOSED`. Keine neue Branch-, Plugin-, Worker-, Scheduler- oder Parallelarchitektur.

## 2. ERROR-REGISTER PRECHECK — VERBINDLICH

Für diesen Block sind zwingend relevant:

- `AFF-ERR-001` — kein PASS ohne vollständige Evidence.
- `AFF-ERR-002` — Last-Known-Good erst nach persistierter neuer Veröffentlichung ablösen.
- `AFF-ERR-003` — Lauf muss seinen persistierten Endzustand im Backend eindeutig zurücklesen.
- `AFF-ERR-004` — Tests mit realistischen Rohdaten; erwartetes Ergebnis nicht in Fixtures vorwegnehmen.
- `AFF-ERR-005` — spezifische Fachnähe vor generischen Pferdebegriffen/Tiefenheuristik.
- `AFF-ERR-006` — Root-Cause-Gesamtfix statt Mini-Fix-/Versionskaskade.
- `AFF-ERR-008` — Bulk-Synchronisation bestätigter DS24-Partner als Hauptworkflow; Einzelpflege nur Fallback.
- `AFF-ERR-009` — Bannerformat und Position niemals im Provideradapter fest verdrahten.
- `AFF-ERR-010` — kontinuierliche/re-entrante Neubewertung bei neuen/geänderten Portalzielen und Creatives.

Ein Lösungsweg, der eine dieser Regeln verletzt, darf nicht implementiert werden.

## 3. Belegter IST-Stand der kanonischen Source

Die aktuelle Source besitzt bereits wesentliche Bausteine, die weiterverwendet werden müssen:

- zentrales Output-Objektmodell mit Provider, Creative, Ziel, Slot, Status, Assetmaßen, Hash, Trackinglink und Source-Fingerprint;
- zentrale semantische Zielklassifikation;
- zentrale Format-/Slotprüfung;
- zentrale Output-Revalidierung und Health-Prüfung;
- zentrale Automationsqueue/-jobs und zentralen Zeitplan;
- DS24-spezifische Schlussprüfung und Two-Phase-/LKG-Sicherheitslogik;
- providerunabhängige many-to-many Zielkanten im Automatisierungskern.

Aktuell noch nicht ausreichend für diesen Zielvertrag:

1. `output_collect_local_targets()` sammelt Seiten sowie `category`/`hp_listing_category`, aber keine normalen veröffentlichten Beiträge/Artikel.
2. Das lokale Portalprofil lässt Banner aktuell standardmäßig nur auf `page`/`category` zu.
3. `output_campaign_target_key()` kennt aktuell kein `post`-Ziel.
4. Die aktive Slotmatrix wird derzeit im Affiliate-Output-Code mit konkreten Größen-/Kontextregeln aufgebaut. Das muss zu einem austauschbaren Design-/Slotvertrag werden; Providerlogik darf keine Größen-/Positionsarchitektur besitzen.
5. Die bestehende Revalidierung schützt vorhandene Objekte, erzeugt aber allein noch keine neue Zuordnung für später neu hinzukommende Beiträge/Kategorien/Slots.
6. DS24-Einzelpflege darf nicht das dauerhafte Betriebsmodell bleiben.

Diese Punkte sind Teil **eines** gebündelten Root-Cause-Blocks. Keine einzelnen Folgeversionen pro Symptom.

## 4. Einziger Zielzustand

Vom bestätigten Affiliate-Partner bis zur sichtbaren Bannerplatzierung muss ein zentraler, providerunabhängiger Lebenszyklus entstehen:

**bestätigter Partner → Bulk-Synchronisation → reales Banner erfassen → Asset/Tracking verifizieren → thematische Ziele bestimmen → passende aktuelle Designslots bestimmen → ein oder mehrere sichere Output-Objekte als Draft materialisieren → vollständige Provider- und Zentralprüfung → persistiert veröffentlichen → Last-Known-Good erst danach ablösen → regelmäßig neu bewerten.**

DS24 bleibt dabei strikt **Banner-only**. Produkt-/Listinglogik wird dadurch nicht erweitert.

## 5. Verbindlicher Architekturvertrag

### 5.1 Bulk-Partner-Synchronisation

- Für DS24 ist die Synchronisation mehrerer bereits bestätigter/zugelassener Partner in einem zentralen Lauf der Hauptworkflow.
- Der bestehende zentrale Automation-Dispatcher ist zu verwenden.
- Kein DS24-eigener Cron, Worker oder Scheduler.
- Automatischer DS24-Publish bleibt an den bereits gebundenen frischen `approved + active` Affiliation-Proof gekoppelt.
- Fehlende einmalige Vendor-Creative-URL darf einen einzelnen Partner auf `needs_input/review` setzen, aber den restlichen Bulk-Lauf nicht stoppen.
- Manueller Einzelimport bleibt nur Fallback.

### 5.2 Reale Banner und Assetmetadaten

Jedes reale Banner behält mindestens:

- Provider und Partneridentität,
- Creative-Identität,
- Trackinglink,
- Bildquelle bzw. lokales verifiziertes Asset,
- tatsächliche Breite,
- tatsächliche Höhe,
- Seitenverhältnis,
- Asset-/Image-Hash,
- Source-Fingerprint,
- Verifizierungszeitpunkt.

Keine erfundenen Banner, Platzhalter, generierten Pseudo-Banner oder beliebigen Consumer-Page-Scrapes.

### 5.3 Zentrale flexible Slotdefinition — HARDLOCK

Bannerquelle, Bannerformat und Ausgabeslot sind drei getrennte Verträge.

Die Affiliate-Zentrale darf Slots nur über eine **providerunabhängige Slotdefinitions-Schnittstelle** konsumieren. Die aktuelle Pferde-Atelier-Definition muss aus einem zentralen Design-/Slotvertrag bzw. dessen registrierter Schnittstelle/Filter stammen.

Ein Slot beschreibt Fähigkeiten, nicht einen Provider. Zulässige Felder sind insbesondere:

- `slot_id`
- aktiv/inaktiv und Vertragsversion
- zulässige `creative_type`-Klassen
- zulässige Zieltypen und Zielkontexte
- zulässiger Seitenverhältnisbereich bzw. Formatklassen
- erforderliche Mindestauflösung, soweit technisch nötig
- Darstellungsmodus wie `contain`/`cover`
- responsive Regeln ohne Verzerrung
- optionale Priorität/Position als Designinformation

Harte Regeln:

- Keine DS24-, Awin- oder sonstige Provider-Sondergröße.
- Keine feste Position im Provideradapter.
- Größen-/Positionsänderung im Design darf nur die Slotdefinition ändern; Provider- und Zuordnungslogik bleiben unverändert.
- Fehlt der gültige Design-/Slotvertrag, bleibt Veröffentlichung fail-closed.
- Passt ein Banner aktuell in keinen Slot, wird es nicht verzerrt oder zwangsbeschnitten. Es bleibt als valides Creative erhalten und wird bei später geänderten Slots erneut geprüft.
- Seitenverhältnis wird responsive nie verzerrt.

### 5.4 Vollständiger Zielkatalog: Seiten + Kategorien + Beiträge

Die zentrale Zielinventur muss veröffentlichte, tatsächlich bespielbare Ziele umfassen:

- Seiten,
- normale WordPress-Kategorien,
- veröffentlichte Beiträge/Artikel,
- bereits bestehende fachlich gebundene Spezialziele nur dort, wo der Ausgabetyp sie unterstützt.

Für Beiträge sind mindestens Titel, Slug, Kurz-/Inhaltstext, Kategorien/Taxonomiekontext und ein stabiler Zielschlüssel in die Klassifikation einzubeziehen.

Unveröffentlichte, gelöschte, fremde oder technisch nicht bespielbare Ziele werden nicht automatisch verwendet.

### 5.5 Semantische Zuordnung und Pferde-Fallback

Die bestehende spezifische Klassifikation bleibt Grundlage. Es gilt:

1. Spezifischer fachlicher Match gewinnt.
2. Generische Wörter wie `Pferd` oder reine Pfadtiefe dürfen keinen engen Treffer vortäuschen.
3. Bei eindeutig pferderelevantem Banner, aber ohne ausreichend spezifischen Treffer, ist ein **breiter fachlich sicherer Pferde-Fallback** zulässig.
4. Der Fallback darf niemals auf fachfremde Ziele ausweichen.
5. Widersprüchliche oder zu schwache Evidenz bleibt `review`, nicht erfundener Automatismus.

### 5.6 Mehrfachnutzung eines Banners

Ein reales Banner darf mehreren passenden Seiten/Kategorien/Beiträgen zugeordnet werden, wenn jedes einzelne Ziel den Sicherheits- und Relevanzvertrag erfüllt.

- Nicht mehr künstlich auf genau einen Gewinner reduzieren, wenn mehrere eigenständig belastbare Ziele existieren.
- Deduplizierung mindestens auf `Creative + Portal + Ziel + Slot`.
- Kein mehrfach identisches Objekt am selben Ziel/Slot.
- Begrenzungen dienen Last-/Qualitätsschutz und müssen zentral konfigurierbar, providerunabhängig und deterministisch sein.
- Eine Mehrfachzuordnung darf niemals einen schwachen Treffer nur zum Füllen erzwingen.

Die vorhandene many-to-many Edge-Architektur ist zu verwenden/erweitern; keine zweite Zuordnungstabelle oder Parallelarchitektur erfinden.

### 5.7 Re-entrante Neubewertung bei organischem Wachstum

Die Zuordnung ist kein Einmalvorgang.

Der zentrale Automationslauf muss Änderungen erkennen bzw. erneut bewerten können bei:

- neuem oder geändertem Banner,
- neuer/geänderter Seite,
- neuer/geänderter Kategorie,
- neuem/geändertem Beitrag,
- geänderter Slotdefinition,
- geänderter Partner-/Affiliation-Evidenz.

Zusätzlich findet ein periodischer zentraler Recheck statt. Kein Provider besitzt dafür einen eigenen Cron.

Ein heute unpassendes Banner darf bei einem morgen neu angelegten passenden Artikel automatisch erneut eine Platzierungschance erhalten.

### 5.8 Materialisierung, Veröffentlichung und Last-Known-Good

Für jedes neue oder neu zugeordnete Output-Objekt gilt:

1. Draft/inaktiv materialisieren.
2. Provider-spezifischen Schlussgate ausführen.
3. komplette zentrale Output-Revalidierung ausführen.
4. Asset, Tracking, Ziel, Slot, Source-Fingerprint und aktuelle Evidenz erneut prüfen.
5. neuen Zustand erfolgreich als `published` persistieren.
6. erst **danach** konfliktierendes Last-Known-Good-Objekt ablösen.

Persistenzfehler, stale Evidenz, ungültiger Slot oder geändertes Ziel = Rollback; Last-Known-Good bleibt unverändert.

### 5.9 Backend-Readback

Jeder zentrale Lauf muss auf derselben Fachseite einen gespeicherten Endzustand anzeigen. Mindestens sichtbar/auswertbar:

- Laufzeitstempel/Run-ID,
- geprüfte Partner,
- synchronisierte Partner,
- importierte/aktualisierte/unveränderte/gesperrte Creatives,
- geprüfte Ziele,
- erzeugte/aktualisierte Zielkanten,
- geplante Drafts,
- erfolgreich veröffentlichte Outputs,
- Reviews/Blockierungen mit Grund,
- Rollbacks/Persistenzfehler,
- Anzahl der durch Neubewertung neu gefundenen Zuordnungen.

Keine Erfolgsmeldung ohne persistierten Readback.

## 6. Erlaubter Implementierungsscope

Primär dürfen innerhalb der kanonischen Source nur die tatsächlich erforderlichen bestehenden Dateien geändert werden, insbesondere:

- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-automation-suite.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-creative-library.php` nur falls für generische Banner-Metadaten zwingend nötig
- `release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php` nur falls bestehende Hooks/Konstanten/Registrierung zwingend angepasst werden müssen

Weitere aktuelle Source-Dateien nur mit belegter unmittelbarer Notwendigkeit für diesen Zielvertrag.

Verboten:

- eBay-Source-/Run-Logik ändern,
- idealo-Verhalten ändern,
- neue Pluginarchitektur,
- neuer Scheduler/Worker/Queue,
- `.github/workflows/**`,
- Archive oder historische Sources verändern,
- immutable Tests/Governance-Guards verändern,
- Design-CSS für diesen Block neu erfinden,
- Pluginversion nur wegen eines Folgefehlers hochzählen,
- bereits bestandene hash-identische eBay-Gates wiederholen.

## 7. Pflichtprüfungen — POSITIV

Der lokale Gesamtworkflow muss mindestens beweisen:

1. Mehrere bestätigte DS24-Partner können in einem zentralen Lauf verarbeitet werden; ein `needs_input`-Partner stoppt andere nicht.
2. Reales Banner wird mit echten Maßen/Ratio/Hash erfasst.
3. Geänderte zentrale Slotdefinition wird ohne Änderung des DS24-/Providercodes übernommen.
4. Ein Banner kann zwei oder mehr eigenständig passende Ziele erhalten, ohne Duplikat am selben Ziel/Slot.
5. Ein veröffentlichter neuer Beitrag wird beim nächsten zentralen Recheck als mögliches Ziel erkannt.
6. Ein zunächst nicht passendes Format wird nach einer später passenden Slotdefinition neu bewertet.
7. Eindeutig pferderelevantes breites Creative kann den sicheren Pferde-Fallback nutzen.
8. Spezifischer Treffer gewinnt vor generischer Tiefe/Pferdewort.
9. Veröffentlichung erfolgt in der Reihenfolge Draft → Vollprüfung → persistiert published → erst dann Supersede.
10. Backend zeigt den persistierten Endzustand des Laufs.

## 8. Pflichtprüfungen — NEGATIV

Mindestens beweisen:

1. Unbestätigter/fremder/nicht freigegebener DS24-Partner wird nicht automatisch veröffentlicht.
2. Pending/rejected/inactive/stale/missing DS24-Affiliation bleibt fail-closed.
3. Banner mit unpassendem Seitenverhältnis wird nicht verzerrt oder zwangseingepasst.
4. Fehlender/inkompatibler Slotvertrag verhindert Veröffentlichung.
5. Fachfremder Beitrag erhält kein Pferdebanner.
6. Schwache/mehrdeutige Ziele werden nicht durch Mehrfachnutzung künstlich befüllt.
7. Dasselbe Creative erzeugt am selben Ziel/Slot kein Duplikat.
8. Persistenzfehler lässt Last-Known-Good live und rollt den neuen Zustand zurück.
9. Ein früher generisch aktivierter, provider-spezifisch nicht freigegebener Kandidat ist am Request-Ende wieder inaktiv/draft.
10. Bekannte Fehlerwege aus `AFF-ERR-001..010` werden nicht reproduziert.

## 9. Gesamtworkflow-/Regressionstest

Gemeinsam zu prüfen, nicht als isolierte Einzelabnahme:

- Bulk-Partner → Bannerimport → Assetprüfung → Zielinventur → semantische Zuordnung → Mehrfachkanten → Slotmatching → Draft → Finalgate → Publish → LKG → Readback → Recheck nach Portalwachstum.
- eBay bleibt funktional und unverändert.
- idealo bleibt funktional und unverändert.
- Awin bleibt funktional und unverändert; generische Slot-/Zieländerungen dürfen bestehende sichere Bannerwege nicht zerstören.
- DS24 bleibt Banner-only.
- bestehende Kontroll-/Veto-/Emergency-Off-Regeln bleiben bindend.
- reale/realitätsnahe Rohdaten für die bekannten Klassifikationsproblemfälle verwenden.

Keine Abnahme aus einem einzelnen Provider- oder UI-Test.

## 10. ERROR-REGISTER POSTCHECK

Vor jedem lokalen PASS-Bericht dokumentieren:

- neue Fehler gefunden: ja/nein,
- falls ja: vor weiterem Fix neue `AFF-ERR-...`-ID mit Root Cause und Nicht-Wiederholungsregel eintragen,
- bekannter Fehlerweg wiederholt: ja/nein,
- falls ja: Gate = FAIL,
- Evidence für alle relevanten POSITIV-/NEGATIV-/Regressionstests,
- kein `fertig`/`Release`/`PASS`, solange geforderte Evidence oder Live-Gates fehlen.

## 11. Source-/Manifest-/Governance-Bindung nach erfolgreicher Implementierung

Erst wenn die komplette lokale Pflichtprüfung bestanden ist:

1. tatsächliche geänderte kanonische Source hashen,
2. `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` exakt neu berechnen,
3. Manifest-SHA berechnen,
4. nur die daraus zwingend folgenden aktuellen Manifest-Bindungen in `control/release-governance/CURRENT_RELEASE.json` aktualisieren,
5. `active_candidate.version=6.64.0`, `status=WORKING`, `release_allowed=false` beibehalten,
6. `explicit_scope_product_deals_partner_analytics` bleibt bis zum vollständig gebundenen Gate `PENDING`,
7. historische PASS-Evidence nicht umetikettieren,
8. kein finales Installer-ZIP vor finalem Gate.

## 12. Abschlusszustand dieses Zielvertrags

Dieser Vertrag ist erst technisch erfüllt, wenn die gesamte Kette gemeinsam nachgewiesen ist. Ein lokal erfolgreicher Kandidat ist noch kein Live-/Release-PASS.

Nach lokalem Gesamt-PASS folgt der gebundene reale WordPress/MariaDB-/Provider-Live-Nachweis. Bis dahin bleibt `release_allowed=false`.
