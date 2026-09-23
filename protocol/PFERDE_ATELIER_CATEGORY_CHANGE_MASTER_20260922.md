# Pferde Atelier – CATEGORY CHANGE MASTER

Stand: 2026-09-22  
Status: **AUTHORITATIVE CATEGORY-CHANGE CONCEPT / WORKLOG / ERROR REGISTER**  
Scope: Pferde Atelier – neue Themenfamilien `Pferdesättel`, `Trensen`, `Offenstallbau`, `Paddockbau`, `Reitplatzbau`

## 0. Zweck und Hard Rule

Diese Datei ist die zentrale fachlich-technische Akte für **jede künftige Änderung an der Pferde-Atelier-Kategoriestruktur**, damit kein neuer Chat oder Worker die Abhängigkeiten erneut zusammensuchen oder erraten muss.

HARD RULE:
- NICHT RATEN.
- Vor Änderungen immer diese Akte + `control/release-governance/CURRENT_RELEASE.json` lesen.
- Bestehende funktionierende Fach-/Performance-/Designlogik nicht rückbauen.
- Keine Mikro-Patcher-Kette. Pro betroffener bestehender Komponente ein sauberer, versionierter Gesamtstand.
- Jede Änderung benötigt harte Positiv-/Negativtests in einer möglichst 1:1-WordPress/MariaDB-Simulation.
- **Ohne belegten Test-PASS keine Abnahme.**
- Live WordPress: **vor jedem schreibenden Apply zwingend DRY-RUN/PREFLIGHT**.
- Jeder Apply braucht exakten Ausgangs-Hash/Version, Readback und dokumentierten Fallback.
- PASS darf nur ein echter Prüfer/Readback behaupten, nie der Worker selbst.

## 0A. Verbindlicher Zielvertrag / Definition of Done

Die Kategorieänderung ist erst abgeschlossen, wenn **alle** folgenden Punkte gemeinsam belegt sind:

1. Die 5 neuen Produktseiten und 25 neuen Artikelkategorien sind als exakt 30 neue Knoten korrekt gebunden; bestehende Eltern/Kinder bleiben unverändert.
2. PPA-013 liefert für diese Struktur die bereits bestätigten 30 individuellen Langtexte, die fünf passenden Icons und das Exact-7-Desktop-Raster sowie zusätzlich die fünf noch fehlenden kurzen Kachelvorschauen im bestehenden Kartenmechanismus.
3. Die Affiliate-Zentrale verwendet eine aus dem exakt gebundenen aktuellen Vollbaum abgeleitete Portalstruktur und einen dazu hash-/count-konsistenten eBay-Zielkatalog. Performance-, Provider-, Ranking-, Banner- und Fachlogik bleiben außerhalb des Struktur-Deltas byte-/verhaltensgleich.
4. PSTE liest die reale WordPress-Struktur frisch ein; PSERC akzeptiert die neuen Kategorien über seinen bestehenden dynamischen Strukturpfad; keine manuell erfundenen Kategoriebindungen.
5. PPM 6.7.9 kennt die 25 neuen Produktionskategorien **und** besitzt für sie die vollständigen kanonischen Produktionsslots. Lauf-/testbezogene Hierarchie- oder Link-Snapshots werden nicht zu Vollregistern umfunktioniert.
6. Interne Linkziele werden aus den aktualisierten Autoritäten read-only neu gebunden; NEW-Linkbindung vor Texterstellung bleibt Pflicht.
7. Jede tatsächlich geänderte Komponente hat lokalen/CI-Positivtest, Negativtest, Regressionstest, Fresh-Unpack/Hashbeleg und einen dokumentierten Fallback.
8. Vor jedem schreibenden WordPress-Schritt läuft ein echter Dry-Run/Preflight mit `writes_performed=false`. Erst bei vollständigem PASS genau ein Apply, danach neuer Request + Readback.
9. Keine Produktionsfreigabe, solange ein Pflichtnachweis offen ist.

## 1. Aktuelle Strukturänderung

### 1.1 Fünf neue Produkt-/Hub-2-Seiten

| ID | Seite | Slug | Parent-ID | Parent |
|---:|---|---|---:|---|
| 972134 | Pferdesättel | `pferdesaettel` | 108 | Sattel & Zubehör |
| 972141 | Trensen | `trensen` | 109 | Trensen & Gebisse |
| 972148 | Offenstallbau | `offenstallbau` | 110 | Offenstall |
| 972155 | Paddockbau | `paddockbau` | 119 | Paddock |
| 972162 | Reitplatzbau | `reitplatzbau` | 120 | Reitplatz |

Offenstall und Reitplatz bleiben Parent-Kategorien. Bestehende Unterseiten/Artikelzweige dürfen nicht verschoben werden.

### 1.2 25 neue Artikelkategorien

Gesamtumfang der Strukturänderung: **5 neue Produktseiten + 25 neue Artikelkategorien = 30 neue Knoten**.

- Pferdesättel: FAQ · Beratung · Vergleich · Pflege · Kosten
- Trensen: FAQ · Beratung · Vergleich · Pflege · Kosten
- Offenstallbau: FAQ · Beratung · Vergleich · Installation · Kosten
- Paddockbau: FAQ · Beratung · Vergleich · Installation · Kosten
- Reitplatzbau: FAQ · Beratung · Vergleich · Installation · Kosten

Die exakten WordPress-Term-IDs dürfen **nicht aus einem Muster erfunden** werden. Bei Live-/Contract-Bindings müssen sie aus dem aktuellen WordPress-/Migrations-Readback stammen.

## 2. Verbindliche Darstellungsregeln

### 2.1 Exact-7 Raster
Nur wenn eine Hub-2-Seite **exakt 7 direkt veröffentlichte Unterseiten** hat:
- nur Desktop,
- ab `min-width: 901px`,
- Reihe 1 = 3 Kacheln,
- Reihe 2 = 4 Kacheln.

Bei 6, 8 oder jeder anderen Kachelzahl: bestehendes Verhalten unverändert.  
Tablet/Mobil: durch diese Regel unverändert.

Aktueller Nutzer-Readback 2026-09-22:
- Icons: PASS
- Exact-7 3/4-Anordnung: PASS
- 30 Langtexte: PASS

### 2.2 Fünf neue Icons
Bestehende Iconfamilien wiederverwenden:
- `pferdesaettel` -> Sattel
- `trensen` -> Trensen & Gebisse
- `offenstallbau` -> Offenstall
- `paddockbau` -> Paddock
- `reitplatzbau` -> Reitplatz

Keine neue parallele Iconlogik.

### 2.3 Kategorietexte
Für **alle 30 neuen Knoten** gilt:
- 150–200 Wörter,
- natürliches Deutsch,
- konkrete Suchintention der jeweiligen Kategorie,
- Unterthemen wirklich behandeln,
- keine Generator-/Schablonensprache,
- keine Padding-Sätze,
- keine generischen Schlussformeln,
- Hauptkeyword natürlich, **kein Keyword-Stuffing**,
- keine bloße Wiederholung desselben Textmusters mit ausgetauschtem Substantiv.

Die 25 Blattkategorien müssen ihre jeweilige Intent-Kategorie sichtbar abbilden (FAQ/Beratung/Vergleich/Pflege bzw. Installation/Kosten).

### 2.4 Fünf kurze Kachel-Vorschautexte
PPA-013-Seitenkarten lesen `post_excerpt` bzw. `post_content` und trimmen die Kartenansicht auf maximal 18 Wörter. Die fünf neuen Produktseiten besitzen noch keine passende Kurzquelle.

Verbindliche Kurztexte:
- Pferdesättel: „Sättel für unterschiedliche Reitweisen, Pferderücken und Anforderungen an Passform, Druckverteilung und Komfort.“
- Trensen: „Zäumungen für feine Hilfengebung, passende Verschnallung und eine pferdegerechte Einwirkung beim Reiten.“
- Offenstallbau: „Planung und Bau von Offenställen mit passenden Laufwegen, Liegeflächen, Fressplätzen, Boden und Wetterschutz.“
- Paddockbau: „Paddocks mit tragfähigem Aufbau, sicherer Einzäunung, guter Entwässerung und alltagstauglicher Flächenplanung.“
- Reitplatzbau: „Reitplätze mit abgestimmtem Unterbau, Tretschicht, Entwässerung und Pflege für dauerhaft gute Nutzbarkeit.“

Die Kurztexte sind **nicht** Ersatz für die 150–200-Wörter-Editorialtexte.

## 3. Systeme, die die 30 neuen Knoten kennen müssen

### A. PPA-013 / Affiliate Portal Template Kit
Status:
- Icons PASS.
- Exact-7 Raster PASS.
- 30 Langtexte PASS.
- offen: fünf kurze Kachelvorschauen.

Regel:
- PPA-013 bleibt die dauerhafte Darstellungsquelle.
- temporäre Patcher dürfen nach erfolgreichem Readback entfernt werden.
- Performance-Helfer `pa-affiliate-design-performance` nicht überschreiben/mergen/entfernen.

### B. Affiliate-Zentrale / Portalstruktur
**MUSS aktualisiert werden.**

Statische Autorität:
- `affiliate-portal-router/assets/portal-structure-v279.json`

Verbraucher:
- Affiliate-Zentrale/eBay-Zielrouting.
- System4 Prewrite liest dieselbe Portalstruktur.

Erforderliches Delta:
- +5 Produktseiten,
- +25 Artikelkategorien,
- bestehende 8 Main-Hubs/übrige Struktur unverändert.

### C. Affiliate-Zentrale / eBay-Zielkatalog
**MUSS aus der aktualisierten Portalstruktur neu generiert werden.**

Datei:
- `affiliate-portal-router/assets/ebay-portal-catalog-v2.json`

Der bestehende Loader bindet den Katalog hart an den SHA der Portalstruktur und prüft feste Zielzahlen. Daher nach Strukturänderung:
- source_sha256 neu,
- Produktzielzahl +5,
- Artikelzielzahl +25,
- neue Produkt-/Artikelziele vollständig,
- bestehende Ziele byte-/semantikgleich soweit nicht vom Delta betroffen,
- Suchregeln/Providerlogik nicht ändern.

### D. Portal SEO Topic Engine (PSTE)
**Kein neues statisches Kategorien-Hardcoding belegt.**

Belegter Hierarchiepfad:
`WORDPRESS_PAGE_TREE_PLUS_FLAT_CATEGORY_READ_ONLY`

Erforderlich:
- nach Live-Strukturänderung frischen WordPress Taxonomy/Portal Snapshot erzeugen,
- Topic Map / Research-Plan neu erzeugen,
- prüfen, dass alle 30 neuen Knoten exakt einmal erscheinen,
- Positiv: neue Kategorien werden gefunden,
- Negativ: alte Kategorien/Eltern bleiben unverändert, keine Dubletten/Phantomknoten.

### E. Portal SEO Redaktionsplan Compiler (PSERC)
**MUSS nach PSTE/Strukturrefresh neu generiert werden.**

Relevant:
- `PSERC_PORTAL_STRUCTURE_REGISTRY_V1`

Regel:
- keine manuell erfundenen Kategoriebindungen,
- neue Slots nur aus aktualisierter Struktur-/SEO-Autorität,
- bestehende Slots nicht umhängen,
- Canonical-Slot-/Strukturprüfungen müssen weiter fail-closed bleiben.

### F. Portal Production Machine / PPM 6.7.9 / System4
**HARTER AUDIT 2026-09-22: differenzierte Behandlung; nicht alle drei Dateien sind Vollregister.**

Hashgebundene PPM-Autorität:
- Paket: `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
- SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- GitHub-Actions-Hard-Audit Run `35783744612`: Paket-SHA PASS.

Gebundene Dateien im Paket:

1. `portal-production-machine/contracts/complete-portal-category-source-v1.json`
   - Contract: `PPM679_COMPLETE_PORTAL_CATEGORY_SOURCE_V1`
   - aktueller SHA256: `316135b57b9c6edbd620250cd88adfbe46d9060fbdaf1e38130933f985b10fbd`
   - enthält aktuell **1124** WordPress-Zielkategorien,
   - Counts binden 329 Produktseiten / 1124 Zielkategorien / 1520 Menüeinträge,
   - Mappingregel leitet die Produktseite aus dem Kategorie-Slug ab.
   - **Hier müssen die 25 neuen Produktionskategorien in den vollständigen Kategorienbestand aufgenommen werden**, sofern der vorgesehene Runtime-Refreshweg nicht bereits einen externen Ersatz erlaubt. Dieser Refreshweg wird vor Paketänderung noch hart geprüft.

2. `portal-production-machine/contracts/category-hierarchy-snapshot-v1.json`
   - Contract: `PPM679_CATEGORY_HIERARCHY_SNAPSHOT_V1`
   - aktueller SHA256: `cebfe0a6a7583d8829154c74f61d38b2b2d8f8094e1308165cef1ff122f17ad2`
   - enthält nur **6** Kategorien.
   - `known_limits` sagt ausdrücklich: **„This bundled snapshot is a controlled current test subset. A future complete user-supplied hierarchy file replaces it without source-code changes.“**
   - **Daher NICHT pauschal um 25 Kategorien erweitern.**
   - Für einen echten neuen Lauf muss der aktuelle Hierarchie-Snapshot aus der realen WordPress-/Portalstruktur neu erzeugt bzw. als aktueller user-supplied Snapshot gebunden werden.

3. `portal-production-machine/contracts/wordpress-link-target-snapshot-v1.json`
   - Contract: `WORDPRESS_LINK_TARGET_SNAPSHOT_V1`
   - aktueller SHA256: `14b79bd4de494f5b66b20686f6a271c132fa11ac2824ddf06e849dd50c240bf2`
   - enthält nur die **3 Pflichtrollen** `parent_category`, `semantic_related`, `further_information`.
   - Scope ist ausdrücklich der aktuelle **G9 FAQ candidate link target**-Satz.
   - `runtime_read_only_revalidation_required_before_any_write=true`
   - `automatic_replacement_forbidden=true`
   - **Daher NICHT pauschal fünf neue Seiten hineinschreiben.** Für einen neuen Artikel/Lauf müssen die drei echten Linkziele aus dem aktuellen Kontext neu gebunden und vor jedem Write read-only revalidiert werden.

System4 `machine_point0.py` bindet vor der Texterstellung zusätzlich die statische `affiliate-portal-router/assets/portal-structure-v279.json`. Dort müssen die 25 neuen Level-4-Ziele vorhanden sein, damit ein Artikel in einer neuen Kategorie überhaupt sauber vorgebunden werden kann.

HARD RULE:
- PPM-Paket selbst erst ändern, wenn der vorgesehene externe Refresh-/Replacement-Weg für `complete-portal-category-source-v1.json` hart geprüft ist.
- Keine plan-/laufbezogenen Snapshots zu Vollregistern umfunktionieren.
- Term IDs bleiben Runtime-Kontrollwerte, nie semantische Identitäten.

### G. Interne Links / Link Policy
**MUSS neu aus aktualisierten Autoritäten erzeugt/readback-geprüft werden.**

Verträge:
- `portal_link_registry_snapshot_v2`
- `WORDPRESS_LINK_TARGET_SNAPSHOT_V1`

Ziel:
- fünf neuen Produktseiten dürfen als echte veröffentlichte interne Ziele verwendet werden,
- Parent/Semantic/Further-Information Rollen bleiben regelkonform,
- NEW-Linkbindung vor Texterstellung bleibt Pflicht,
- keine toten, falschen oder nicht veröffentlichten Ziele.

### H. Weitere Plugins
Kein Plugin wird allein wegen seines Namens geändert.  
Für Bildzentrale, HivePress, Yoast, Kategorietext-Audit, Editorial Guard, Category Structure Guard etc. gilt:
- nur ändern, wenn Quell-/Runtime-Prüfung eine harte Kategorienliste oder veraltete Strukturbindung belegt,
- dynamische WordPress-Leser nur refresh/readback, kein unnötiges Hardcoding.

## 4. Versions-/Quellhardlocks

### PPA-013
Belegter Ausgang vor Kategorieabschluss:
- 1.50.556
- Main SHA256: `33451736b0215e4f2b60e62555f697f9a2d94c2925e894882f261dbea3929119`

Belegter erfolgreicher Source-Apply:
- 1.50.558
- Main SHA256: `840130139597c6152a385475c05b2786c96d08bd137785e127280d9aabe979f1`

Performance-Helfer geschützt:
- `pa-affiliate-design-performance`
- SHA256: `2b74db4f0e599f5200a9faaa08b08e4a7cf7c7b951ce55ec62939f96fa890b92`

### Affiliate-Zentrale – KRITISCH
Nicht vom alten Repo-Releasebaum ausgehen.

Belegt:
- alter `release/affiliate-zentrale/current/`-Pluginheader im Repo: **6.72.105**
- später belegter Performance-Kandidat/live verwendeter Stand: **6.72.145**
- 6.72.145 Paket laut Evidence:
  `AFFILIATE_ZENTRALE_V6.72.145_PERFORMANCE_BATCH_READ_ROOTFIX_HARDTEST.zip`
- dokumentierter Paket-SHA256:
  `a5d6bccb11d41005be0f0db40b2dcdb32b8e40e73a772411b44039adedc548de`

HARD RULE:
**Kein Kategorieupdate der Affiliate-Zentrale darf den alten 6.72.105-Releasebaum als Ersatz für den späteren 6.72.145-Live-/Performance-Stand installieren.**
Vor einem Affiliate-Apply muss der exakte aktuelle Live-/Kandidatenbaum vollständig hashgebunden sein.

## 5. Testvertrag für jede betroffene Komponente

Vor WordPress:
1. exakte Ausgangsversion + SHA belegen,
2. Delta nur in erlaubtem Scope,
3. PHP/JSON/Syntax/Schema,
4. lokale/hobbyroom 1:1-Simulation,
5. Positivtests,
6. Negativtests,
7. Regression der unveränderten bestehenden Kategorien,
8. Fresh-Unpack/Installer-Byteidentität,
9. Testreport + SHA,
10. Fallbackartefakt/Backup fest hinterlegen.

Pflicht-Positivfälle:
- alle 5 Produktseiten erkannt,
- alle 25 Blattkategorien erkannt,
- korrekte Parent-/Hierarchy-/Article-Type-Bindings,
- fünf neuen Produktseiten sind gültige Link-/Affiliateziele wo fachlich vorgesehen,
- bestehende Kategorien weiterhin identisch.

Pflicht-Negativfälle:
- fehlender Knoten -> fail-closed,
- falscher Parent -> fail-closed,
- falscher Artikeltyp -> fail-closed,
- doppelter Slug -> fail-closed,
- veralteter Structure SHA -> fail-closed,
- falscher Plugin-/Source-SHA -> kein Apply,
- 6/8/andere Kachelzahl -> kein Exact-7-Raster,
- Tablet/Mobil -> keine neue Exact-7-Regel,
- Affiliate-Provider-/Ranking-/Performance-Logik darf sich durch reines Strukturdelta nicht verändern.

## 6. WordPress-Livevertrag

**Zwingend DRY-RUN/PREFLIGHT vor jedem Apply.**

Dry-Run muss mindestens liefern:
- erwartete Live-Version,
- erwartete Live-SHAs,
- aktive relevante Plugins,
- 5 Produktseiten/IDs/Parents/Slugs,
- 25 Blattkategorien mit echten Term-IDs und Parentbindung,
- geplante Datei-/DB-Änderungen,
- `writes_performed=false`,
- Fallback/Backupziel,
- Ergebnis PASS/FAIL.

Nur bei vollständigem PASS:
- exakt ein Apply,
- danach neuer Request,
- kompletter Readback,
- Frontend-/SEO-/Production-/Link-Checks,
- erst danach Produktionsfreigabe.

Bei jedem FAIL:
- sofort fail-closed,
- kein weiterer Teilapply,
- Rollback auf exakt dokumentierten Ausgangsstand,
- Fehler hier im Abschnitt 8 protokollieren.

## 7. Fallback

Für jeden Plugin-/Contract-Stand:
- vorherigen vollständigen Pluginbaum oder eindeutig reproduzierbaren Goldmaster separat sichern,
- SHA256 festhalten,
- keine Rücksicherung aus einem älteren unvollständigen Repo-Stand,
- DB-/Snapshotänderungen mit Vorher-Snapshot sichern,
- Rollback danach durch Readback verifizieren.

PPA-013 vorhandene Backupnamen aus Apply 1.0.2:
- `ppa013-category-completion-manifest-20260922-194858-33451736b021.json`
- `ppa013-category-completion-main-20260922-194858-33451736b021.php.bak`

## 8. Fehler-/Änderungsprotokoll

### Fehler A – Scope zunächst fälschlich nur 5 Texte
Ursache:
- nur die fünf neuen Produktseiten betrachtet.
Korrektur:
- tatsächlicher Scope = 5 Produktseiten + 25 Blattkategorien = **30 Texte**.
Prävention:
- Strukturänderung künftig immer als kompletter Knotenbaum inventarisieren, bevor Inhalte gebaut werden.

### Fehler B – Kategorietexte zu schablonenhaft
Befund:
- Wortzahl war PASS, Inhalt/Suchintention jedoch zu gleichförmig.
Korrektur:
- Regeln auf echte Nutzerfragen/Intent je Kategorie gebunden,
- Keyword-Wiederholung begrenzt,
- keine Schablonen-/Paddingtexte.
Nutzer-Readback danach: Texte PASS.

### Fehler C – Patcher 1.0.0 Apply
Code:
`POST_APPLY_READBACK_FAILED_ROLLBACK_ATTEMPTED`
Ergebnis:
- automatischer Rollback auf PPA-013 1.50.556,
- Struktur/Performance-Helfer unverändert.
Ursache:
- unzureichend kontrollierter Schreib-/Readbackpfad.

### Fehler D – Patcher 1.0.1 Text-Meta
Code:
`TEXT_WRITE_IMMEDIATE_READBACK_FAILED_ROLLBACK_ATTEMPTED`
Befund:
- PPA-013 Source hatte Kandidaten-SHA erreicht,
- Fehler beim ersten Kategorietext-Meta-Readback.
Root cause:
- neuer Meta-Schreibweg war unnötig und wich vom historischen PPA-013-Editorialmechanismus ab.
Korrektur:
- Meta-Schreibweg verworfen,
- historische Editorial-Katalog-Logik V1.50.470–472 wiederverwendet.

### Änderung E – Patcher 1.0.2
Ergebnis:
- Source Apply PASS,
- PPA-013 1.50.556 -> 1.50.558,
- nur `pferde-template-kit.php` geändert,
- Performance-Helfer SHA unverändert,
- keine Text-Meta-Schreiberei.

### Änderung F – Textscope 1.0.3
Korrektur:
- 30 statt 5 Kategorietexte.
Nutzer-Readback:
- Texte PASS,
- Icons PASS,
- Exact-7 3/4 PASS.

### Fehler G – fünf leere Kachelvorschauen
Befund:
- nur fünf neue Produktseiten betroffen.
Root cause:
- Seitenkarten lesen `post_excerpt`/`post_content`; Langtexte im Editorial-Katalog sind nicht dieselbe Kartenquelle.
Korrektur:
- fünf kurze Vorschautexte gemäß bestehender <=18-Wörter-Kartenlogik.
Status:
- noch in Gesamtintegration einzubauen.

### Risiko H – Affiliate alter Repo-Stand
Befund:
- `release/affiliate-zentrale/current` ist 6.72.105,
- späterer belegter Performance-Stand wurde als 6.72.145 dokumentiert.
Risiko:
- Strukturupdate auf altem Baum würde Performance-/Fachänderungen rückbauen.
Hardlock:
- vor Änderung exakten aktuellen Live-Baum beschaffen/verifizieren; sonst Affiliate-Apply BLOCKED.

### Fehler I – historischer 6.72.145-Hardtest war nicht sauber an 6.72.142 gebunden
Harter Audit 2026-09-22:
- Workflow `.github/workflows/affiliate-performance-batch-hardtest.yml` kopiert als Ausgangspunkt `release/affiliate-zentrale/current/affiliate-portal-router`.
- Dieser Repo-Baum steht aktuell/prüfbar auf **6.72.105**, nicht 6.72.142.
- Die beiden Performance-Patchskripte wurden darauf angewendet; der Workflowtext bezeichnete das anschließend als 6.72.144/145.
Folge:
- der alte Workflow-SUCCESS ist **kein ausreichender Beweis für einen vollständigen echten 6.72.142→145-Quellbaum**.
- dieser Nachweis wird für die jetzige Kategorieintegration ausdrücklich **nicht** als Source-Basis akzeptiert.
Prävention:
- jeder künftige Plugin-Hardtest muss Ausgangsversion **und kompletten Ausgangsbaum-Hash** vor dem Patch hart prüfen.
- WordPress-Dry-Run muss vor Affiliate-Apply den tatsächlich aktiven Live-Baum bzw. mindestens alle betroffenen Dateien vollständig hashen.

## 9. Aktueller Ablauf für diese Änderung

1. Zentrale Akte + CURRENT binden.
2. Exakte aktuelle Quellen je betroffener Komponente verifizieren.
3. PPA-013: nur fünf Kurzvorschauen ergänzen; bereits PASS Raster/Icons/30 Langtexte nicht neu erfinden.
4. Portalstruktur um 30 Knoten erweitern.
5. Affiliate eBay-Katalog aus dieser Struktur neu erzeugen.
6. PPM-Category/Hierarchy/Link-Snapshots aus aktualisierter Autorität neu erzeugen.
7. PSTE aus echter WordPress-Struktur neu snapshotten/Topic Map neu bauen.
8. PSERC danach neu generieren.
9. Linkregistry neu generieren.
10. pro geändertem Plugin/Contract harte Positiv-/Negativ-1:1-Simulation.
11. Gesamt-E2E.
12. vollständige Dokumentation + Fallback.
13. WordPress DRY-RUN/PREFLIGHT.
14. nur bei PASS Apply.
15. neuer Request + Readback.
16. erst danach Abschluss/PASS.

## 10. Aktueller Status

- 5 neue Produktseiten: live vorhanden.
- 25 neue Artikelkategorien: live angelegt.
- PPA-013 30 Langtexte: Nutzer bestätigt PASS.
- PPA-013 Icons: Nutzer bestätigt PASS.
- PPA-013 Exact-7 Raster: Nutzer bestätigt PASS.
- offen: fünf Kachelvorschauen.
- offen: 30-Knoten-Propagation in statische Portal-/Affiliate-/PPM-Autoritäten.
- offen: PSTE/PSERC/Link-Refresh.
- offen: vollständige 1:1 Positiv-/Negativ-Evidence.
- offen: WordPress Dry-Run.
- **keine Produktionsabnahme ohne diese Nachweise.**


## 11. Harte Baseline-Evidence 2026-09-22

GitHub Actions Workflow:
- `Category Integration Hard Baseline`
- Run `35783612898`: SUCCESS
- Run `35783744612`: SUCCESS

Beide Runs führten vor dem Audit real aus:
- `release_guard.py governance-check` -> PASS
- `release_guard.py start --branch affiliate-release-current` -> PASS
- exaktes PPM-6.7.9-Paket aus `main` -> SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1` PASS
- read-only Portal-/Affiliate-/PPM-Baseline-Audit -> PASS

Belegte Basis:
- Portalstruktur SHA256: `b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`
- Portal: 329 Produktseiten / 1124 Themenkategorien / 1520 Menüeinträge
- eBay-Katalog SHA256: `4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`
- eBay-Katalog: 329 Produktziele / 1124 Artikelziele / 316 Business Concepts / 59 Hub Concepts / 375 routable Concepts
- die 5 neuen Produktseiten und 25 neuen Artikelkategorien fehlen in beiden statischen Basen noch erwartungsgemäß
- für keinen der fünf neuen Titel existiert bereits ein gleichnamiger normalisierter Business-Concept; ein unbeabsichtigtes Concept-Merge ist damit nicht vorgegeben
- aktueller Repo-Releasebaum der Affiliate-Zentrale meldet 6.72.105 und ist deshalb nicht als Live-Plugin-Ersatz freigegeben.

Evidence-Artefakte:
- Run 35783612898 Artifact ID `10719280682`
- Run 35783744612 Artifact ID `10719391536`


## 12. Abschluss-/Nachholprüfung 2026-09-23 – belastbares Delta seit Generation 99

Dieser Abschnitt ist **Protokoll/Evidence-Zusammenfassung**, keine zweite CURRENT-Wahrheit. Dynamischer Status und genau eine NEXT ACTION bleiben ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

### 12.1 Affiliate-Zentrale – exakte Quellbindung aus dem Affiliatebüro nachgeholt

Persistente Fachablage geprüft:
- `/Pferde-Atelier/Affiliate-Zentrale/SICHERUNG/AFFILIATE_ZENTRALE_V6.72.142_GOLDMASTER_ROLLBACK_DO_NOT_OVERWRITE.zip`
  - SHA256 `8c25b833bb9c6a017cf83e767ac86bf221468c790445062077991f17462b5b6d`
  - 27 Dateien
  - Rolle: unveränderlicher Rollbackanker.
- `/Pferde-Atelier/Affiliate-Zentrale/TESTKANDIDATEN/AFFILIATE_ZENTRALE_V6.72.145_PERFORMANCE_BATCH_READ_ROOTFIX_HARDTEST.zip`
  - SHA256 `a5d6bccb11d41005be0f0db40b2dcdb32b8e40e73a772411b44039adedc548de`
  - 27 Dateien
  - Rolle: live-getestete Performance-Arbeitsbasis für die Kategorieintegration; kein Goldmaster.

Harter Baumvergleich 6.72.142 -> 6.72.145:
- nur 6 Dateien unterscheiden sich: `includes/trait-ppar-control-contract.php`, `includes/trait-ppar-ebay-account-deletion.php`, `includes/trait-ppar-ebay.php`, `includes/trait-ppar-output-objects.php`, `pferdeportal-affiliate-router.php`, `readme.txt`.
- `assets/portal-structure-v279.json` ist in beiden byteidentisch, SHA256 `b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`.
- `assets/ebay-portal-catalog-v2.json` ist in beiden byteidentisch, SHA256 `4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`.

Damit ist Risiko H für die **Ausgangsquelle der Kategorieintegration** aufgelöst: nicht 6.72.105 rekonstruieren; 6.72.145 ist die exakt gebundene Arbeitsbasis, 6.72.142 ausschließlich Fallback.

### 12.2 Portalstruktur/eBay-Katalog – Candidate-Hardtest PASS

GitHub Actions:
- Workflow: `Category Integration Candidate Hardtest`
- erster Lauf `35784782645`: FAIL, weil der Negativfall `wrong_private_bucket` noch nicht fail-closed war.
- Korrekturcommit `ad90791538fbb2a0f42b5d89edd430afdd3c8d91`: Affiliate-Bucket-Negativgate gehärtet.
- Run `35784852533`: **SUCCESS**.

Geprüfter Kandidat:
- Portalstruktur SHA256 `ce5a312b9017e58c8968a9f0ff132df7cd8d34c7899911a522e03c49eb1a3eed`
- eBay-Katalog SHA256 `6513ce4ea3e077ca1410ffbfa684138f688e772e07aa8aa483464a6fa8277ff2`
- 334 Produktseiten
- 1149 Artikel-/Themenkategorien
- 1550 Menüeinträge
- 334 Produktziele
- 1149 Artikelziele
- 321 Business Concepts
- 380 routable Concepts
- 316 supply-required Ziele

Acht Negativfälle PASS/fail-closed:
1. doppelter neuer Produktseiten-Slug,
2. falscher Parent,
3. falscher Artikeltyp,
4. falsche Ausrüstungsreihenfolge,
5. veralteter Katalog-Source-SHA,
6. fehlende Business-Concept-Abdeckung,
7. falscher Private-Bucket,
8. falscher Katalog-Count.

Für die reale Affiliate-Pluginintegration gilt weiterhin: nur diese zwei Kandidaten-JSONs in den exakt gebundenen 6.72.145-Vollbaum übernehmen; alle anderen Dateien müssen unverändert bleiben. Noch **keine** WordPress-Installation/Promotion.

### 12.3 PSERC – dynamische neue Kategorien hart bewiesen

GitHub Actions:
- Workflow: `Category Integration PSERC Audit`
- Head `7d9a11e6353ed070624e676f73817d5ddb84c4fe`
- Run `35785760506`: **SUCCESS**.

Der Run bindet exakt das PSERC-Paket SHA256 `77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314` und führt zusätzlich den dynamischen Kategorie-Positiv-/Negativtest aus. Ergebnis: neue Kategorien können über den bestehenden dynamischen Strukturpfad akzeptiert werden; falscher Parent/Ancestor/Dublette bleiben blockiert. Kein statisches manuelles 25-Kategorien-Hardcoding in PSERC erforderlich.

### 12.4 PPM 6.7.9 – exakte Paketbindung und korrigierter tatsächlicher Scope

Der Hard-Baseline-Workflow wurde nur für Evidence erweitert, damit das exakt geprüfte PPM-ZIP selbst als Workflow-Artefakt erhalten bleibt.

- Commit: `5ba4b5aa694050a0b575e35a988d277c2516b4eb`
- Workflow: `Category Integration Hard Baseline`
- Run `35824322686`: **SUCCESS**
- Artifact ID `10734567188`
- PPM-Paket SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1` PASS.

Exakter Paket-Audit:
- `complete-portal-category-source-v1.json`: 1124 vollständige WordPress-Zielkategorien.
- `three-type-complete-category-hierarchy-snapshot-v2.json`: ebenfalls 1124 vollständige semantische Kategorien; dies ist der bisher im Integrationsscope übersehene Voll-Hierarchie-Snapshot.
- `category-hierarchy-snapshot-v1.json`: nur 6 Kategorien, ausdrücklich kontrollierter Test-Subset -> **nicht** pauschal erweitern.
- `wordpress-link-target-snapshot-v1.json`: laufbezogener 3-Rollen-Linkziel-Snapshot -> **nicht** pauschal erweitern.
- `canonical-complete-editorial-plan-v1.json`: 1124 Portal-Kategorien, 5620 Portal-Slots, 5665 Gesamtslots inklusive Journal. Jede Kategorie besitzt exakt 5 kanonische Slots.

Neuer erster PPM-Blocker:
- Die 25 neuen Produktionskategorien benötigen deshalb **125 neue kanonische Portal-Slots**.
- Nur Kategorien in die Vollquelle/Hirarchie aufzunehmen würde später erneut `CANONICAL_SLOT_MISSING` erzeugen.
- Zielcounts aus der bestehenden 5-Slot-Regel sind damit 1149 Portal-Kategorien / 5745 Portal-Slots / 5790 Gesamtslots, **aber diese Counts sind noch kein PASS**; sie müssen durch einen generierten, vollständig hashgebundenen PPM-Kandidaten bewiesen werden.
- Der vorhandene Reimportvertrag erlaubt `ADD`; neue Kategorien starten als `REGISTERED_PENDING_RESEARCH_AND_OWNERSHIP_REVIEW`. Automatische stille Migration ist verboten.

### 12.5 PPA-013 – belastbare und nicht belastbare Aussagen trennen

Belastbar:
- Nutzer bestätigt 30 Langtexte PASS.
- Nutzer bestätigt fünf Icons PASS.
- Nutzer bestätigt Exact-7 3/4-Raster PASS.
- fünf kurze Kachelvorschauen fehlen weiterhin.

Nicht als neuer Hash-PASS belegt:
- Nach dem 30-Text-Lauf wurde im Chat kein vollständiger neuer PPA-013 Versions-/Main-SHA-Readback geliefert. Der letzte exakt hashgebundene Source-Apply bleibt daher 1.50.558 / `840130139597c6152a385475c05b2786c96d08bd137785e127280d9aabe979f1`; der funktionale Nutzer-PASS für die 30 Texte wird separat geführt.
- Vor dem späteren 5-Kachel-Vorschautext-Apply muss deshalb erneut die **wirklich aktuelle** PPA-013-Version/Source gebunden werden. Nicht aus 1.50.558/1.50.559 raten.

### 12.6 Aktuell noch offen

- PPM: 25 ADD-Kategorien + vollständiger Hierarchie-Snapshot + 125 kanonische Slots + abhängige Hash-/Governance-/Reconciliation-Bindungen als ein konsistenter 6.7.9-Kandidat; 1:1 Positiv/Negativ/Regression.
- PPA-013: exakten aktuellen Live-Vollstand binden und nur fünf Kachelvorschauen ergänzen; vorhandene PASS-Funktionen schützen.
- Affiliate-Zentrale: zwei geprüfte Candidate-JSONs in exakten 6.72.145-Vollbaum integrieren; übrige 25 Dateien byteidentisch; noch keine CURRENT-/Live-Promotion.
- PSTE: nach späterer Live-Strukturänderung echter frischer WordPress-Snapshot/Topic-Refresh.
- PSERC: dynamische Fähigkeit ist bewiesen; nach PSTE-Refresh echten neuen Plan-/Registry-Stand erzeugen/readbacken.
- Links: echte Linkziele pro Lauf read-only neu binden.
- Gesamt-E2E, vollständige Fallback-Dokumentation und WordPress-Dry-Run vor jedem Apply bleiben Pflicht.

### 12.7 Fehlernachtrag

**Fehler J – Affiliate Candidate Negativgate zunächst zu schwach**  
Run `35784782645` ließ den manipulierten `wrong_private_bucket`-Fall durch. Korrektur: Validator gehärtet. Run `35784852533` danach SUCCESS mit allen 8 Negativfällen.

**Fehler K – Affiliate-Quelle zunächst nur aus veraltetem Repo-Stand betrachtet**  
Die Fach-/Pluginbüro-Ablage wurde zu spät als Primärquelle geprüft. Korrektur: 6.72.145 und 6.72.142 aus der persistenten Affiliate-Ablage materialisiert und vollständig hash-/baumverglichen. Prävention: bei Pluginarbeit immer zuerst Pluginbüro + Fachbüro + CURRENT lesen.

**Fehler L – PPM-Scope zunächst unvollständig**  
Zunächst wurden nur `complete-portal-category-source-v1.json`, kleiner Hierarchie-Snapshot und Link-Snapshot betrachtet. Exakter Paket-Audit zeigt zusätzlich den vollständigen `three-type-complete-category-hierarchy-snapshot-v2.json` und den kanonischen Gesamtredaktionsplan. Korrektur: PPM-Integration muss alle wirklich gebundenen Vollautoritäten samt 125 neuen Slots berücksichtigen; kleine laufbezogene Snapshots bleiben laufbezogen.

### 12.8 Exakter nächster fachtechnischer Schritt

**PPM 6.7.9 zuerst vollständig schließen:** aus dem exakt gebundenen Paket SHA `acbda93b…` einen ADD-only-Kandidaten für die 25 neuen Kategorien erzeugen, der die Voll-Kategoriequelle, den vollständigen Hierarchie-Snapshot und exakt 125 neue kanonische Slots konsistent nachzieht; alle abhängigen Self-/Binding-Hashes und Reconciliation-Counts deterministisch aktualisieren; danach lokaler/CI-Positiv-, Negativ- und Regressionstest. Keine WordPress-Schreiboperation.

### Fehler M – CURRENT-Next-Action war nicht Guard-konform
Frischecheck 2026-09-23:
- Head `871a81dc0382c4bdad54eb3d30c493f7daa73535`
- Workflow `Category Integration Hard Baseline`, Run `35826881075`: **FAIL**
- exakter Fehler: `AFFILIATE_RELEASE_GUARD_BLOCKED:AUTHORIZED_NEXT_ACTION_INVALID`.

Ursache:
- `execution_state.authorized_next_action` enthielt den freien fachlichen Text `BUILD_AND_HARDTEST_PPM679_25_CATEGORY_ADD_125_SLOT_CANDIDATE`.
- Der unveränderte Governance-Guard erlaubt dort ausschließlich die kanonischen Tokens `COMMIT_EXACT_V6638_21_FILE_SOURCE_TO_CANONICAL_ROOT`, `RUN_BOUND_RELEASE_GATES` oder `FINALIZE_RELEASE`.

Korrektur:
- `authorized_next_action` auf das Guard-konforme Token `RUN_BOUND_RELEASE_GATES` gesetzt.
- Der **exakte fachliche nächste Schritt** bleibt ausschließlich in `execution_state.bound_user_scope_action` gebunden.
- Der Guard selbst wurde nicht verändert.

Prävention:
- Bei jeder CURRENT-Änderung zuerst die zulässige Enum des unveränderten Guards prüfen.
- Freie Fachbeschreibung nie in ein enum-gebundenes Governance-Feld schreiben.

### Fehler N – alter PPA-013-Teilzielvertrag erzeugte Zielvertrags-Drift
Frischecheck 2026-09-23:
- `protocol/AFFILIATE_RELEASE_PPA013_CATEGORY_COMPLETION_TARGET_20260922.md` enthielt noch den historischen Scope „nur fünf Kategorietexte“.
- Der inzwischen verbindliche Gesamtumfang lautet 5 Produktseiten + 25 Blattkategorien = 30 Knoten/30 Texte plus systemweite Propagation.

Korrektur:
- Die historische PPA-013-Datei ist ausdrücklich als **abgelöster Teilzielvertrag** markiert.
- Verbindliche Zielquelle für diese Änderung ist ausschließlich Abschnitt **0A** dieser Datei.
- `CURRENT_RELEASE.json.user_scope_lock.current_focus_scope_ref` zeigt auf diese zentrale Kategorieakte.

Prävention:
- Scope-Erweiterungen ändern die eine Zielautorität; alte Teilzielverträge bleiben nur Historie/Wegweiser und dürfen nicht parallel als aktueller Scope referenziert werden.

## 13. Statischer Einstieg für einen neuen Chat

Diese Sektion ist nur Routing, **keine** zweite Status- oder NEXT-ACTION-Wahrheit.

1. `protocol/PFERDE_ATELIER_CATEGORY_CHANGE_MASTER_20260922.md` lesen, insbesondere Abschnitt 0A und Fehlerprotokoll.
2. Danach ausschließlich `control/release-governance/CURRENT_RELEASE.json` als aktuelle Status-/Blocker-/NEXT-ACTION-Autorität lesen.
3. Branch `affiliate-release-current` frisch gegen seinen Head prüfen.
4. Den zu CURRENT gehörenden neuesten `Category Integration Hard Baseline`-Run prüfen.
5. Bei unveränderter Bindung keine Vollrekonstruktion; direkt `execution_state.bound_user_scope_action` innerhalb des kanonischen `authorized_next_action` ausführen.
6. Bei neuem FAIL nur das Delta untersuchen und zuerst CURRENT nachziehen.


## 14. HARD RULE – zentrale Pferdeportal-Kategorienquelle ab 2026-09-23

Diese Regel ersetzt für den **Kategorieninhalt** jede ältere Formulierung, die interne Plugin-/PPM-Dateien als eigene Kategorieautorität lesen lässt.

Verbindlich:
- **Einzige Kategorien-Wahrheit:** `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`.
- Ausgangsquelle dieser Liste: aktueller WordPress-Export `pferdeatelier.WordPress.2026-09-23.xml`.
- Bestand: **1160 WordPress-Kategorien**.
- **Keine Automatik.**
- **Kein Kategorieplugin.**
- **Keine zweite Kategorienquelle.**
- Bereits erbrachte Altbeweise werden nicht erneut vollständig durchgetestet.
- Plugin-/PPM-interne Kategorienlisten dürfen nur notwendige technische **Ableitungen/Kopien** der zentralen Liste sein; sie besitzen keine eigene fachliche Autorität.
- Bei künftiger Pluginarbeit wird nur das jeweilige Plugin gegen die zentrale Liste abgeglichen und nur dessen Delta geändert.
- Änderungen an der zentralen Liste werden ausschließlich in `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/AENDERUNGSPROTOKOLL.md` dokumentiert.

### Fehler O – Kategorieverwaltung unnötig als Plugin/Automatik aufgebaut

Der zwischenzeitliche Kandidat `PFERDEPORTAL_KATEGORIEN_V0.2.0_CANDIDATE_MIN.zip` und sein eigener Workflow waren zu komplex und widersprachen dem KISS-Ziel. Beide wurden entfernt. Verbleibend sind ausschließlich zentrale Liste + Änderungsprotokoll.


## 15. PPM 6.7.9 Kategorie-Delta – funktional fertig, Signatur offen (2026-09-23)

Der PPM-interne, aus der alleinigen `KATEGORIEN.tsv` abgeleitete Kategorie-/Planstand wurde als isolierter Kandidat gebaut.

Belegt:
- 1149 Produktionskategorien;
- 5745 Portalslots;
- 5790 Gesamtslots;
- 25 neue Kategorien / 125 neue Slots;
- alte 1124 Kategorien, 5620 Portalslots und 45 Journal-Slots value-identical;
- fokussierte Category-Source-, Editorial-Registry-, System-Inventory- und Hard-Rule-Prüfung jeweils 0 Fehler;
- Positivfall neuer Slot PASS;
- Negativfall fehlender Slot PASS;
- kein WordPress-Write.

Kandidatenarchiv: `PORTAL_PRODUCTION_MACHINE_V6.7.9_CATEGORY_25_SLOT125_UNSIGNED_CANDIDATE.zip`
SHA256: `3063c150f551d0743425b7364248113f6dfd6fc0fc1e63272da85db93d07dc35`
Build-Manifest SHA256: `7ec6966c7c1a9c921bcaa6061cbdeb91b229f508bc93ef59e20a617d7d7d6482`

**Einziger verbleibender PPM-Kandidatenblocker:** `BLOCKED_BUILD_SIGNATURE_INVALID`.
Die bestehende Signatur gehört zum alten unveränderten Build. Sie darf nicht nachgebaut, umgangen oder erfunden werden. Der nächste Schritt ist ausschließlich eine autorisierte Ed25519-Signatur des exakt gebundenen neuen Manifests; danach nur Build-Integrity-Readback.

Evidence: `release/affiliate-zentrale/evidence/ppm679_category_delta_candidate_20260923.md`.
