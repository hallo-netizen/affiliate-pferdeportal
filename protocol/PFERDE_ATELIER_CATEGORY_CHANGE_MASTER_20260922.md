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

## 0A. Verbindlicher Zielvertrag / Definition of Done – KATEGORIE/STRUKTUR ONLY

**Gültig ab 2026-09-23.** Dieser Zielvertrag ersetzt den früher breiteren Scope mit Text-/Designaufgaben für die laufende Kategorieintegration.

Die Kategorieintegration ist erst abgeschlossen, wenn **alle** folgenden Punkte gemeinsam belegt sind:

1. Einzige fachliche Kategorien-Wahrheit bleibt `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`, erzeugt aus dem aktuellen WordPress-Export vom 23.09.2026. Keine Automatik, kein Kategorieplugin, keine zweite Kategorienquelle.
2. Für jedes tatsächlich installierte Plugin, das Pferdeportal-Kategorien oder Portalstruktur konsumiert, wird die **exakte aktuelle GitHub-Quelle über PLUGINS-Büro → zuständiges Fachbüro → technische Hauptquelle** gebunden. Kein Serverabruf und keine Rekonstruktion aus veralteten Ständen.
3. Erlaubt sind ausschließlich Kategorie-/Strukturänderungen: IDs, Slugs, Namen, Parent-/Portalzuordnungen, technische Kategorie-Kopien/Ableitungen, ausschließlich kategorienbedingte Count-/Hash-Bindungen und read-only Strukturrefreshes.
4. **Nicht Teil dieses Zielvertrags:** Texte, Kachelvorschauen, Designinhalte, Plugin-Konzepte, Performance-, Provider-, Ranking-, Banner- oder sonstige fachfremde Logik. PPA-013 darf nur auf eine statische Kategorien-/Portalstrukturbindung geprüft werden; Inhalte/Design bleiben unangetastet.
5. PPM 6.7.9 muss die 25 neuen Produktionskategorien und 125 neuen kanonischen Slots konsistent enthalten. Dieser Punkt ist mit signiertem Build-Integrity-PASS bereits geschlossen.
6. Affiliate-Zentrale muss im **installierten aktuellen Stand 6.72.152** ausschließlich die bereits hart getestete Portalstruktur und den bereits hart getesteten eBay-Katalog als technische Kategorienableitung erhalten; alle übrigen Dateien bleiben unverändert.
7. PSTE muss im **tatsächlich installierten aktuellen Live-Stand** seine technische Kategorieableitung auf 1149 Produktionskategorien korrekt konsumieren und die Keyword-/Themenzuordnung gegen diesen Bestand zuverlässig auflösen. Am 24.09.2026 wurde live **0.57.8** beobachtet; der lokale 0.57.9-Kandidat ist nicht installiert und nicht freigegeben. PSERC 0.28.23 nutzt den bestehenden dynamischen Strukturpfad; kein 25er-Hardcoding.
8. Portal-/Link-Verbraucher werden nur auf tatsächliche statische Kategorie-/Strukturkopien geprüft. Dynamische Leser erhalten ausschließlich den notwendigen read-only Refresh/Readback.
9. Bereits gültige, hash-identische Altbeweise werden nicht vollständig wiederholt. Nur das neue Delta wird positiv, negativ und auf unveränderten Altbestand geprüft, soweit für die konkrete Änderung erforderlich.
10. Vor jedem späteren schreibenden WordPress-Schritt: echter Dry-Run/Preflight mit `writes_performed=false`; erst danach genau ein Apply + neuer Request + Readback.
11. Keine Produktionsfreigabe, solange ein Kategorie-/Strukturverbraucher noch ungeklärt oder nicht auf die zentrale Kategorienwahrheit gebunden ist.

## 0B. Scope-Hinweis zu historischen Abschnitten

Die nachfolgenden Abschnitte zu früheren Text-/Design-/Kachelaufgaben bleiben ausschließlich **Historie/Nachweis des früher breiteren Auftrags**. Sie sind **kein aktueller Zielvertrag und keine aktuelle NEXT ACTION**. Für den laufenden Auftrag gilt ausschließlich Abschnitt 0A plus die aktuelle Status-/NEXT-ACTION-Autorität `control/release-governance/CURRENT_RELEASE.json`.

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


## 16. PPM 6.7.9 Signaturabschluss (2026-09-23)

Der in Abschnitt 15 gebaute exakte Kandidat wurde mit dem vorhandenen autorisierten PPM-Ed25519-Schlüssel `ppm679-ed25519-3614e3fc87ba2767` signiert.

- Manifest SHA256 unverändert: `7ec6966c7c1a9c921bcaa6061cbdeb91b229f508bc93ef59e20a617d7d7d6482`
- Public-Key SHA256: `3614e3fc87ba2767d669d573f388e2fa99fda3f1aa0741465adc79a341311dd7`
- signierter Kandidat SHA256: `cb64d1ee7fcf9c3bc4ff5aa9e2e8cb948763c2c2c1a7ad956b90f980da9e40fa`
- `PPM679_Build_Integrity`: **PASS**
- kein WordPress-Write.

Damit war der PPM-Blocker geschlossen. **Historischer Hinweis:** der damals genannte PPA-013-Inhaltsschritt wurde später durch den verbindlichen KATEGORIE/STRUKTUR-ONLY-Scope in Abschnitt 0A abgelöst und ist keine aktuelle NEXT ACTION.


## 17. Verbleibende Kategorie-Verbraucher – historischer Zwischenstand 2026-09-23

Nach abgeschlossenem signiertem PPM-Delta wurden die übrigen Verbraucher bis zur jeweils verfügbaren aktuellen Quelle geprüft.

- **PPA-013:** aktueller Vollstand fehlt; nur fünf Kachelvorschauen offen; kein Rückgriff auf alte Vollstände.
- **Affiliate 6.72.145:** Hardtest und exakter SHA belegt, Voll-ZIP aktuell nicht verfügbar; Kategorien-Delta bleibt fertig, Integration in 6.72.105 ist verboten.
- **PSTE:** keine Kategorie-Codeänderung; frischer WordPress-Struktur-Readback erforderlich.
- **PSERC:** vorhandener Compiler-0.28.23-Snapshot bindet noch 1124 Kategorien; nach PSTE-Refresh neu erzeugen.
- WordPress weiterhin ohne Write.

Evidence:
`release/affiliate-zentrale/evidence/category_remaining_consumers_20260923.md`.


## 18. PSERC 25er-Real-ID-Delta PASS (2026-09-23)

Die 25 neuen Kategorien wurden mit ihren echten WordPress-Term-IDs 1577–1601 und den echten Produktseiten-/Elternketten aus der aktuellen WordPress-XML durch den vorhandenen `PSERC_Portal_Structure_Gate` geprüft.

Ergebnis:
- 25/25 dynamisch registriert;
- `PSERC_PORTAL_STRUCTURE_PASS`;
- `write_attempted=false`;
- keine PSERC-Codeänderung;
- keine 25er-Hardcodierung;
- Altbestand nicht erneut voll geprüft.

Der sichtbare 0.28.23-Metadaten-Snapshot bindet weiterhin 1124 Kategorien; offen ist nur der reale vollständige PSTE/PSERC-Runtime-Refresh auf 1149.

Evidence:
`release/affiliate-zentrale/evidence/pserc_current25_real_id_dynamic_20260923.md`.


## 19. HARD SCOPE – nur Kategorien/Struktur (2026-09-23)

Für die laufende Kategorieintegration gilt ab hier verbindlich:

**Erlaubt**
- zentrale Kategorienliste;
- IDs, Slugs, Namen, Parent-/Portalzuordnungen;
- technische Kategorie-Kopien/Ableitungen;
- category-only Portalstruktur/eBay-Katalog;
- Count-/Hash-Bindungen, die ausschließlich durch Kategorien geändert werden;
- read-only PSTE/PSERC-Strukturrefresh;
- aus der Kategorie-/Portalstruktur abgeleitete Linkziel-Eignung.

**Verboten**
- Texte;
- Kachelvorschauen;
- Designinhalte;
- fachliche Plugin-Konzepte;
- Performance-, Provider-, Ranking- oder Bannerlogik;
- sonstige nicht-kategoriebezogene Änderungen.

Bereits abgeschlossene Kategoriebeweise werden nicht erneut ausgeführt.

PPA-013-Inhaltsarbeit ist ausdrücklich **außerhalb dieses Kategorie-Scopes**.

Historischer damaliger Blocker: exakter Affiliate-6.72.145-Vollstand. **Abgelöst:** die reale installierte Basis wurde später als **6.72.152** festgestellt. Aktueller Blocker/NEXT ACTION steht ausschließlich in `CURRENT_RELEASE.json`.


## 20. Affiliate-Kategorieartefakt original wiedergewonnen (2026-09-23)

Keine Rekonstruktion.

Originales GitHub-Actions-Artefakt aus dem bereits abgeschlossenen Hardtest:
- Run: `35784852533`
- Artifact: `10719063406` / `category-integration-candidate-hardtest`

Darin exakt:
- `portal-structure-v279.CANDIDATE.json`
  - SHA256: `ce5a312b9017e58c8968a9f0ff132df7cd8d34c7899911a522e03c49eb1a3eed`
- `ebay-portal-catalog-v2.CANDIDATE.json`
  - SHA256: `6513ce4ea3e077ca1410ffbfa684138f688e772e07aa8aa483464a6fa8277ff2`

Belegte Kandidatenzahlen:
- Produktseiten: 334
- Artikelkategorien: 1149
- Menüeinträge: 1550

Diese beiden Dateien sind **technische Kategorieableitungen**, keine zweite Kategorienquelle. Fachliche Wahrheit bleibt ausschließlich `KATEGORIEN.tsv`.

Wichtig:
Der historische Checkout des Performance-Hardtests enthält unter `release/affiliate-zentrale/current` die Version **6.72.105**. Er darf ausdrücklich **nicht** als Ersatz für den fehlenden exakten 6.72.145-Vollstand benutzt werden.

Die beiden Kategorieableitungen selbst bleiben als geprüfte Bytes gültig und werden nicht neu gebaut. **Historischer Hinweis:** die damalige 6.72.145-Basis wurde später durch den real installierten Stand **6.72.152** als Zielbasis abgelöst. Die aktuelle Bindung steht ausschließlich in `CURRENT_RELEASE.json`.


## 21. Live installierter Plugin-Stand als Kategorie-Basis (2026-09-23)

Die reale WordPress-Pluginliste wurde als Versionsbasis gebunden. Alte Repository-Annahmen dürfen diesen Live-Stand nicht überschreiben.

Kategorie-/Strukturkandidaten:
- Affiliate-Zentrale (Portal-kompatibel) **6.72.152**
- Affiliate Portal Template Kit (Pferde-kompatibel) **1.50.559**
- Portal Production Machine **6.7.9**
- Portal SEO Redaktionsplan Compiler **0.28.23**
- Portal SEO Themenengine **0.57.6**
- Portal Category Structure Repair Guard **1.0.1**
- Portal Production Center **1.1.1**
- Portal Production Link Policy Gate **1.0.1**
- Portal Link Policy Runtime Verifier **1.0.0**
- Allgemeine Bildzentrale **2.7.6**

Vorhandene read-only Quellwege:
- PPM-Quellpaket Exporter **1.0.0** -> exakter aktiver PPM-Quellstand
- SEO-Quellpaket Exporter **1.0.0** -> exakte installierte PSTE-/PSERC-Quellen

HARD SCOPE:
nur Kategorien/Portalstruktur. Keine Texte, kein Designinhalt, keine Plugin-Konzepte, keine Performance-/Provider-/Ranking-/Bannerlogik.

Einzige Kategorienwahrheit bleibt `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`.


## 22. Abschluss-/Nachholprüfung 2026-09-23 – Kategorieintegration

Rolle: **Historie/Nachweis**, keine zweite CURRENT-/NEXT-ACTION-Wahrheit.

### Frischecheck
- zuständige technische Current-Autorität: `control/release-governance/CURRENT_RELEASE.json`
- Branch: `affiliate-release-current`
- vor dieser Nachholung geprüfter Head: `5f5d5b320327ecf4aff33fea132932f194dc53c4`
- `Category Integration Hard Baseline` Run `35855777737`: **SUCCESS** auf genau diesem Head.
- keine Vollrekonstruktion des bereits bewiesenen Altbestands.

### Routing / Büros
- PLUGINS-Büro: `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/START_HERE.md`
- dortige Regel bestätigt: Inventar/Routing im PLUGINS-Büro; Fach-/Release-/LIVE-Wahrheit im zuständigen Fachbüro bzw. technischer Originalquelle.
- allgemeingültiges `KATEGORIENMODELL` ist **nicht** die Pferdeportal-Kategorienquelle und bleibt unberührt.
- für diese Arbeit gilt: **GitHub-Büro/Fachquelle, nicht Server und nicht Bibliothek.**

### Belastbarer Kategorienstand
- einzige Kategorien-Wahrheit: `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`
- 1160 WordPress-Kategorien insgesamt; 1149 Produktionskategorien + 11 sonstige Kategorien.
- PPM 6.7.9: Kategorie-/Slot-Delta signiert, Build-Integrity PASS; abgeschlossen.
- PSERC 0.28.23: 25 neue reale Kategorien 1577–1601 über bestehenden dynamischen Gate-Pfad PASS; **kein 25er-Code-Hardcoding**.
- Affiliate-Zentrale: real installiert **6.72.152**. Die bereits hart getesteten Kategorieableitungen bleiben:
  - `portal-structure-v279.CANDIDATE.json` SHA256 `ce5a312b9017e58c8968a9f0ff132df7cd8d34c7899911a522e03c49eb1a3eed`
  - `ebay-portal-catalog-v2.CANDIDATE.json` SHA256 `6513ce4ea3e077ca1410ffbfa684138f688e772e07aa8aa483464a6fa8277ff2`
  Aktueller 6.72.152-Vollbaum ist noch exakt über das AFFILIATE-/PLUGINS-Büro zu binden; 6.72.105/6.72.145 dürfen nicht als Zielbasis angenommen werden.
- PSTE: real installiert **0.57.6**. Exakter GitHub-PASS-Nachweis:
  - Workflow `PSTE Real WordPress HTTP E2E`
  - Run `35693065234`
  - Artifact `10679790400`
  - getestete ZIP SHA256 `71bae2436fc1c3d52c06cefe551517af32a89eeb005457331e2c44136a1c888f`
  - exakte Quellprüfung zeigt statische technische Ableitung `fixtures/portal-category-map-v1.json` mit **1124** Einträgen.
  - Kategorie-Delta deshalb: ausschließlich diese Map **+25 -> 1149**; keine PSTE-Recherche-/Provider-/Workflowlogik ändern.
- noch auf Kategorieabhängigkeit gegen ihre exakten GitHub-Quellen zu klassifizieren:
  - Affiliate Portal Template Kit (Pferde-kompatibel) 1.50.559
  - Portal Category Structure Repair Guard 1.0.1
  - Portal Production Center 1.1.1
  - Portal Production Link Policy Gate 1.0.1
  - Portal Link Policy Runtime Verifier 1.0.0
  - Allgemeine Bildzentrale 2.7.6

### Fehler-/Korrektur-Nachtrag

**Fehler P – falscher Quellenweg Server/Bibliothek**
- Es wurde zwischenzeitlich angenommen, aktuelle Pluginquellen müssten vom Server bzw. aus einer Dateiablage beschafft werden.
- Korrektur: Nutzerregel bestätigt: Pluginstände liegen in GitHub-Büros/Plugin-Büro. Aktueller Arbeitsweg ist ausschließlich PLUGINS-Büro -> Fachbüro -> technische GitHub-Hauptquelle.
- Prävention: nie wieder Server/Bibliothek als ersten Quellenweg für diese Pluginarbeit verwenden.

**Fehler Q – veraltete Affiliate-Zielbasis 6.72.145**
- Zwischenzeitlich wurde 6.72.145 als aktueller Integrationsbaum behandelt.
- Nutzer-Readback belegt real installiert **6.72.152**.
- Korrektur: 6.72.145 bleibt Historie; Kategorieintegration darf nur gegen exakt gebundenen 6.72.152-Vollstand erfolgen.

**Fehler R – Scope-Drift in Inhalte/Design**
- Kategoriearbeit driftete zeitweise zu PPA-Kacheltexten/Design-/Plugininhalten.
- Korrektur: HARD SCOPE in Abschnitt 0A: ausschließlich Kategorien/Struktur. Inhalte/Design/Konzepte/Performance/Provider/Ranking/Banner sind verboten.

**Fehler S – unnötiges Wiederholen bereits bewiesener Prüfungen**
- Mehrfach wurden bereits belegte Altstände erneut untersucht.
- Korrektur: KISS-Frischecheck; bei unveränderter Bindung nur Delta prüfen und vorhandene PASS-Evidence wiederverwenden.

**Fehler T – PSTE zunächst fälschlich als rein dynamischer Kategorienleser eingestuft**
- Frühere Prüfung sagte „keine statische Kategorie-Codeänderung nötig“.
- Exakte 0.57.6-GitHub-Quelle zeigt zusätzlich `fixtures/portal-category-map-v1.json` mit 1124 Einträgen.
- Korrektur: genau diese technische Ableitung muss +25 auf 1149 nachgezogen werden; übriger PSTE-Code bleibt unberührt.

### Exakter statischer Einstieg für den nächsten Chat
1. `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/START_HERE.md` als Bürotür lesen.
2. Für den Kategorieauftrag auf `protocol/PFERDE_ATELIER_CATEGORY_CHANGE_MASTER_20260922.md` Abschnitt 0A routen.
3. Danach **ausschließlich** `control/release-governance/CURRENT_RELEASE.json` als aktuelle Status-/Blocker-/NEXT-ACTION-Autorität lesen.
4. Branch `affiliate-release-current` gegen Head und neuesten `Category Integration Hard Baseline`-Run frisch prüfen.
5. Bindung unverändert -> **keine Vollrekonstruktion**, direkt die dortige NEXT ACTION ausführen.



---

## 23. Abschluss-/Nachholprüfung 2026-09-23 – Fehlerprotokoll der letzten Kategorie-Delta-Läufe

Rolle: **Historie/Nachweis**, keine zweite CURRENT-/Status-/NEXT-ACTION-Wahrheit. Aktueller Status und genau eine NEXT ACTION bleiben ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

### Fehler U – Affiliate-Delta war korrekt, Read-only-Audit zunächst noch auf alten Basiszustand gebunden

1. Run `35889536574` FAIL:
   - `BASE_CATALOG_TARGET_COUNT_DRIFT`
   - beobachtet: `articles=1149`, `products=334`
   - Ursache: Nach dem exakten Zwei-JSON-Delta prüfte der Baseline-Audit noch Annahmen des alten Basiszustands statt sauber zwischen Basis und angewendetem Kandidaten zu unterscheiden.
2. Nach erster Korrektur Run `35889748251` weiterhin FAIL:
   - `CATEGORY_JSON_PAIR_UNBOUND`
   - Katalog war bereits Kandidat `6513ce4e...`, der Audit las die Portalstruktur aber noch aus dem falschen/alten Pfad `b86a160e...`.
3. Korrektur:
   - Commit `41f8145765fb0626d27bba8aa0f30b1cd0aa12e9`: Audit für Basis- und angewendeten Affiliate-Zustand getrennt.
   - Commit `923c8fb73a3d3cf212c1a84b25779f23190a7825`: Audit-Portalstruktur an die kanonische Affiliate-Current-Quelle gebunden.
4. Abschlussnachweis:
   - Affiliate Category Gate / Hard Baseline auf dem korrigierten Stand: Run `35889920034` SUCCESS.
   - Späterer Current bindet Affiliate 6.72.152 als `CLOSED_CATEGORY_DELTA_PASS`.
   - Keine WordPress-Schreiboperation.

### Fehler V – PSTE-Delta-Skript zunächst an falschen zentralen TSV-Hash gebunden

1. Run `35890838624` FAIL:
   - `CENTRAL_CATEGORY_SHA_DRIFT`
   - tatsächlicher zentraler Kategorienhash: `3e5f32755e09b79c3ac266d5987716dd91866dd21f77b3a522099eae7f962d69`.
2. Ursache:
   - Der neue PSTE-Delta-Prüfweg hatte einen nicht zum tatsächlich committed `KATEGORIEN.tsv` passenden erwarteten Hash fest verdrahtet und stoppte deshalb korrekt fail-closed, bevor ein Kandidat akzeptiert wurde.
3. Korrektur:
   - Commit `4d23e7ff53229d004405576e922e6758650c66df`: PSTE-Map-Delta an die exakten committed Bytes der zentralen TSV gebunden.
4. Abschlussnachweis:
   - Run `35891142282` SUCCESS.
   - PSTE 0.57.6 danach `1124 -> 1149`, exakt eine geänderte Datei `fixtures/portal-category-map-v1.json`, 130 Dateien unverändert, kein WordPress-Write.
   - Abschluss-/Weiterbindungscommit `79e9bee186cbb531f376ea9d9b451b068e483d91`.

### Prävention aus U/V

- Nach einem gültigen Delta muss der Audit ausdrücklich den **aktuellen kanonischen Sourcepfad** lesen; kein Root-/Altpfad darf still als Basis weiterlaufen.
- Hashbindungen technischer Ableitungen müssen aus den **tatsächlich committed autoritativen Bytes** stammen; kein aus Erinnerung/älterem Stand übernommener Erwartungshash.
- Fail-closed bleibt richtig: Ein fehlgeschlagener Zwischenlauf ist kein PASS und wird erst nach nachgewiesenem korrigiertem SUCCESS geschlossen.


### Fehler W – Template Kit zunächst zu früh als ohne statischen Kategorieverbraucher eingeordnet

- Ursache: Der zuerst geprüfte 1.50.558→1.50.559-Hardtest belegt nur das Delta und enthält keinen vollständigen Pluginbaum.
- Späterer historischer Vollquell-Audit fand den realen statischen Verbraucher `assets/breadcrumb-portal-map-v150310.json` mit Vertrag `PFTK_BREADCRUMB_PORTAL_MAP_V150310` und hartem 1124er Count.
- Korrektur: Template Kit bleibt Kategorieverbraucher; der aktuelle 1.50.559-Assetstand muss exakt read-only gebunden werden. Keine Rekonstruktion.

### Fehler X – Laufzeitrolle der Breadcrumb-Map zwischenzeitlich zu eng beschrieben

- Zwischenannahme: Die Map sei ausschließlich Breadcrumb-Fallback.
- Harte Quellprüfung zeigt zusätzlich `leaf_category_hub_context_v150396()`: dieselbe Map wird für den Hub-Kontext des Leaf-Fallback-Introtexts gelesen; bei fehlendem Map-Eintrag fällt die Funktion auf den echten Taxonomie-Parent zurück.
- Korrektur: Runtime-Rolle = Breadcrumb-Fallback/Menu-Validierung **plus** Leaf-Hub-Kontext für automatischen Fallbacktext. Die 25 fest gebundenen Editorialtexte bleiben davon getrennt.

### Fehler Y – SHA `580fa6c7…` falsch als Breadcrumb-Asset-SHA bezeichnet

- Das Campus-Rekonstruktionsskript `reconstruct-design-1.50.469.sh` belegt: `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5` ist der SHA256 der vollständigen historischen `pferde-template-kit.php` 1.50.469.
- Es ist **nicht** der SHA der Breadcrumb-JSON.
- Korrektur: historischer Loader-PHP-SHA wird entsprechend bezeichnet; der exakte SHA der aktuellen 1.50.559-`assets/breadcrumb-portal-map-v150310.json` bleibt offen und ist der erste Blocker.


---

## 24. Abschluss-/Nachholprüfung 2026-09-24 – PSTE Live-Delta und neuer Kategorie-Resolver-Blocker

Rolle: **Historie/Nachweis**, keine zweite CURRENT-/NEXT-ACTION-Wahrheit. Aktueller Status und genau eine NEXT ACTION stehen ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

### Frischecheck vor dem Live-Delta

- Branch: `affiliate-release-current`
- Head: `787d747410cfde5db1e8b86740c5103264725281`
- Workflow: `Category Integration Hard Baseline`
- Run: `35970840150`
- Ergebnis: **SUCCESS**
- Run-Head identisch: `787d747410cfde5db1e8b86740c5103264725281`

Damit wurde **keine Vollrekonstruktion** durchgeführt; ausschließlich das spätere Live-PSTE-Delta wurde nachgeholt.

### Bereits geschlossene Verbraucher

Im aktuellen Chat wurden zusätzlich zu den früher geschlossenen Affiliate-/PPM-/PSTE-Map-/PSERC-Gates live geschlossen:

- Template Kit 1.50.559: Kategorie-/Breadcrumb-Map **1149/1149**, Dry-Run PASS -> exakt ein Apply -> neuer Request -> Readback PASS.
- Portal Production Center 1.1.1: Strukturbindung **1149 / 9 / 5790**, danach Build-Manifest/Ed25519-Trust-Root sauber neu gebunden; finaler Build-Integrity-Readback PASS.
- Allgemeine Bildzentrale 2.7.6, Portal Link Policy Runtime Verifier 1.0.0, Portal Production Link Policy Gate 1.0.1 und Portal Category Structure Repair Guard 1.0.1: keine zusätzliche statische Vollkopie mit 1149er Delta nötig.

Evidence:
`release/affiliate-zentrale/evidence/category_integration_pste_live_delta_20260924.md`

### PSTE-Live-Stand

Live beobachtet:
- **Portal SEO Themenengine 0.57.8**
- `Gesamtbestand neu erfassen` endete mit **Gesamtbestand erfasst.**

Der frühere WordPress-"kritischer Fehler" trat auf diesem konkreten 0.57.8-Capture-Lauf damit nicht erneut auf.

Danach blockierte die Übersicht mit:
`PSTE_ADMIN_ANALYTICS_DATASET_TOO_LARGE_USE_FILTERED_THEMENPRUEFUNG`

Dafür existiert ein lokaler 0.57.9-Kandidat, **nicht installiert und nicht freigegeben**, weil danach ein schwererer Kategorieauflösungsfehler belegt wurde.

### Neuer erster Blocker – Keyword-Kategorieauflösung

Der direkt im aktuellen Chat bereitgestellte Keyword-Export wurde ohne Bibliothek ausgewertet:

- 500 Statuszeilen
- 496 × `BLOCKED_FOR_CATEGORY`
- 4 × `AUTO_RESOLVED`
- `pferdesaettel`: 0 Vorkommen
- `trensen`: 0 Vorkommen
- `offenstallbau`: 0 Vorkommen
- `paddockbau`: 0 Vorkommen
- `reitplatzbau`: 0 Vorkommen

Auch bekannte Altziele werden blockiert. Damit ist der Fehler **nicht auf die 25 neuen Kategorien begrenzt**.

Die technische Ursache ist noch **nicht bewiesen**. Nicht raten.

### Fehler Z – PSTE-Gesamtbestand konnte im alten Stand kritisch abbrechen

Die alte synchrone Baseline-Erfassung hatte große ungebremste Datenmengen in einem Request. Der beobachtete 0.57.8-Live-Lauf konnte `Gesamtbestand neu erfassen` erfolgreich abschließen.

### Fehler AA – 0.57.8-Schutzbremse zu grob

Nach erfolgreichem Gesamtbestand blockierte die Übersicht mit `PSTE_ADMIN_ANALYTICS_DATASET_TOO_LARGE_USE_FILTERED_THEMENPRUEFUNG`.
Ein lokaler 0.57.9-Kandidat adressiert diesen Render-/Large-Dataset-Pfad, ist aber **nicht installiert**.

### Fehler AB – PSTE-Kategorieauflösung massiv unvollständig

500-Zeilen-Export: 496 `BLOCKED_FOR_CATEGORY`, nur 4 `AUTO_RESOLVED`; die fünf neuen Familien fehlen vollständig.

**Status: OFFEN / erster aktueller Blocker.**

### Fehler AC – historischer PLUGINS-START_HERE-Pfad auf aktuellem Branch nicht vorhanden

Der in älteren Protokollabschnitten genannte Pfad
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/START_HERE.md`
liefert auf `affiliate-release-current` aktuell 404 und darf deshalb nicht als aktuelle Bürotür behauptet werden.

Für diesen Kategorieauftrag existiert eine stärkere technische Current-Autorität. Der statische Einstieg ist deshalb:
1. `protocol/PFERDE_ATELIER_CATEGORY_CHANGE_MASTER_20260922.md` Abschnitt 0A lesen.
2. Danach ausschließlich `control/release-governance/CURRENT_RELEASE.json`.
3. Branch `affiliate-release-current` und den zu Current gehörenden `Category Integration Hard Baseline` frisch prüfen.
4. Bei unveränderter Bindung direkt die dortige NEXT ACTION ausführen.

### Exakter nächster Schritt

Nur lokal/read-only gegen den beobachteten 0.57.8-Stand und den 500-Zeilen-Export:

1. Exakten Codepfad bestimmen, der `BLOCKED_FOR_CATEGORY` erzeugt.
2. Mindestens einen blockierten Altfall und alle fünf neuen Familien gegen die 1149er Kategorieableitung/Live-Baseline verfolgen.
3. Positiv: alter gültiger Fall löst korrekt auf.
4. Positiv: alle fünf neuen Familien lösen korrekt auf.
5. Negativ: wirklich unbekannte/fremde Kategorie bleibt fail-closed.
6. Erst danach **einen konsolidierten PSTE-Kandidaten** bauen, der den noch nicht live installierten 0.57.9-Large-Dataset-Fix und den belegten Kategorie-Resolver-Fix gemeinsam enthält.
7. Vor Live-Installation vollständiger lokaler Regressionstest und sicherer Rollback auf den original E2E-geprüften 0.57.6-Stand SHA256 `71bae2436fc1c3d52c06cefe551517af32a89eeb005457331e2c44136a1c888f`.

Bis dahin:
- **0.57.9 nicht installieren**
- kein PSERC-Finalrefresh
- kein Linkregistry-Finalrefresh
- kein Gesamt-Kategorie-E2E
- keine Produktionsfreigabe


---

## 25. PSTE Resolver-Reklassifikation 2026-09-24

Rolle: **Nachtrag/Korrektur der technischen Einordnung aus Abschnitt 24.** CURRENT-/NEXT-ACTION-Wahrheit bleibt ausschließlich `control/release-governance/CURRENT_RELEASE.json`.

### Harte neue Prüfung

Die autorisierte 1149-PSTE-Kategorieableitung wurde gegen die reale `PSTE_Article_Type_Registry::build()`-/`resolve()`-Logik geprüft.

Ergebnis:
- 1149 Kategorien
- 1149 eindeutige Familie+Artikeltyp-Ziele
- 0 Dubletten
- 28/28 positive Resolverfälle PASS:
  - `gebisse-beratung`
  - `hafer-beratung`
  - `pferdedecken-winterdecken-beratung`
  - alle 25 Kategorien der fünf neuen Familien `pferdesaettel`, `trensen`, `offenstallbau`, `paddockbau`, `reitplatzbau`
- unbekannte Fremdfamilie: fail-closed PASS mit `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING`

Evidence:
`release/affiliate-zentrale/evidence/category_integration_pste_resolver_reclassification_20260924.md`

### Korrektur der Interpretation aus Abschnitt 24

`BLOCKED_FOR_CATEGORY` bedeutet im PSTE-Code **nicht ausschließlich**, dass eine Zielkategorie nicht aufgelöst werden konnte.

Der Status wird ebenfalls für Planning-Readiness- und Duplicate-/Cannibalization-Blockaden verwendet. Die Admin-Oberfläche bezeichnet ihn selbst als **„Bereits abgedeckt oder blockiert“**.

Damit sind:
- 496/500 `BLOCKED_FOR_CATEGORY`
- bekannte Altziele mit diesem Status
- 0 Vorkommen der fünf neuen Familien im bestehenden Keyword-/Topic-Pool

**kein hinreichender Beweis für einen defekten Kategorie-Resolver.**

Zusätzlich gilt:
`Gesamtbestand neu erfassen` aktualisiert Baseline/Struktur/Context, startet aber keine neue Keywordrecherche und erzeugt keine neuen Topic-Pool-Zeilen. Deshalb müssen die fünf neuen Familien nach diesem Schritt nicht automatisch im bestehenden Keywordbestand vorkommen.

### Korrigierter erster Blocker

Nicht mehr:
`PSTE_0578_EXACT_LIVE_SOURCE_BIND_AND_KEYWORD_CATEGORY_RESOLUTION_496_OF_500_BLOCKED`

Sondern:
`PSTE_0578_BLOCKED_STATUS_REASON_CLASSIFICATION_RESOLVER_DEFECT_NOT_PROVEN`

### Exakter nächster Schritt

Nur read-only:
die tatsächlich vorhandenen blockierten PSTE-Zeilen nach ihren bereits gespeicherten `reason_codes`, Planning-Readiness- und Duplicate-/Cannibalization-Gründen klassifizieren. Der bestehende PSTE-Bereich **„Konflikte“** zeigt diese Gründe bereits an.

Nur wenn bei einem bekannten gültigen Ziel tatsächlich `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING` oder ein gleichwertiger Current-Baseline-Miss belegt wird, wird ein Resolver-Fix wieder eröffnet.

Bis dahin:
- **kein Resolver-Fix erfinden**
- **0.57.9 nicht installieren**
- kein PSERC-Finalrefresh
- kein Linkrefresh
- kein Gesamt-Kategorie-E2E
- kein Live-Apply


---

## 26. Kategoriekonzeption FINAL / FROZEN – 2026-09-24

**Status: FACHLICH FERTIG / KEINE WEITERE KATEGORIEENTSCHEIDUNG OFFEN.**

Dieser Abschnitt friert die Kategoriekonzeption für die laufende Änderung ein. Technische Propagation/Readbacks können noch offen sein; die fachliche Struktur selbst wird nicht mehr verändert.

### 26.1 Finaler Strukturumfang

Exakt **5 neue Produkt-/Hub-2-Seiten**:

| Parent | Neue Produktseite | Slug |
|---|---|---|
| Sattel & Zubehör | Pferdesättel | `pferdesaettel` |
| Trensen & Gebisse | Trensen | `trensen` |
| Offenstall | Offenstallbau | `offenstallbau` |
| Paddock | Paddockbau | `paddockbau` |
| Reitplatz | Reitplatzbau | `reitplatzbau` |

Exakt **25 neue Artikelkategorien**, fünf je Produktseite:

- Pferdesättel: **FAQ · Beratung · Vergleich · Pflege · Kosten**
- Trensen: **FAQ · Beratung · Vergleich · Pflege · Kosten**
- Offenstallbau: **FAQ · Beratung · Vergleich · Installation · Kosten**
- Paddockbau: **FAQ · Beratung · Vergleich · Installation · Kosten**
- Reitplatzbau: **FAQ · Beratung · Vergleich · Installation · Kosten**

Damit bleibt der Gesamtumfang unveränderlich:
**5 Produktseiten + 25 Artikelkategorien = 30 neue Knoten.**

### 26.2 Verbindliche Intent-Abgrenzung

Damit allgemeine und bestehende spezielle Themen nicht gegeneinander kannibalisieren:

- **FAQ** = allgemeine Fragen, Grundlagen, Definitionen, typische Wissensfragen.
- **Beratung** = Auswahl-, Entscheidungs-, Planungs- und Handlungshilfe.
- **Vergleich** = Alternativen, Unterschiede, Vor-/Nachteile, Gegenüberstellungen.
- **Pflege** = Reinigung, Pflege, Erhalt und Wartung bei Pferdesätteln und Trensen.
- **Installation** = Bau, Aufbau, Ausführung und Umsetzung bei Offenstallbau, Paddockbau und Reitplatzbau.
- **Kosten** = Preise, Budget, laufende/Einmal-Kosten und Kostentreiber.

Ein Artikel wird nach seiner **dominanten Suchintention** genau einer dieser fünf Kategorien der passenden Familie zugeordnet.

### 26.3 Abgrenzung zu bestehenden Kategorien

Die fünf neuen Familien sind **breite Oberthemen**, keine Ersatzkategorien für bestehende spezifische Themen.

Beispiele:
- `trensen-*` = allgemeine Trensen-Themen; `englische-trensen-*` bleibt spezifisch bestehen.
- `offenstallbau-*` = gesamter Bau/Planung eines Offenstalls; bestehende Einzelthemen wie Bodenbefestigung, Tore, Raufen, Liegeflächen usw. bleiben eigenständig.
- `paddockbau-*` = gesamter Paddockbau; `paddockzaeune-*` bleibt das spezifische Zaun-Thema.
- `reitplatzbau-*` = gesamter Reitplatzbau; bestehende Einzelthemen wie Reitplatzboden, Drainage, Bewässerung, Beleuchtung usw. bleiben eigenständig.
- `pferdesaettel-*` = allgemeine Pferdesattel-Themen; bestehende spezifische Sattel-/Zubehörthemen bleiben eigenständig.

**Keine bestehende Kategorie wird verschoben, umbenannt, zusammengelegt oder ersetzt.**

### 26.4 WordPress-Taxonomie vs. Portalhierarchie

Harter Befund aus der einzigen Kategorien-Wahrheit `KATEGORIEN.tsv`:

- 1160/1160 WordPress-Kategorien haben `parent_slug` leer.
- Die WordPress-Kategorietaxonomie ist damit im aktuellen System **bewusst flach**.
- Auch die 25 neuen Kategorien bleiben flach.
- Die fachliche Hierarchie **Parent → Produktseite → Artikelkategorie** wird über die bestehende Portalstruktur/Ableitung gebunden, **nicht** durch WordPress-Term-Parents.

HARD RULE:
**Kein Worker darf die 25 neuen Artikelkategorien nachträglich als WordPress-Unterkategorien unter die fünf Produktseiten hängen.**

### 26.5 Harte Strukturprüfung

Aktueller Prüfstand:
- `KATEGORIEN.tsv`: **1160 Zeilen**
- globale doppelte Term-IDs: **0**
- globale doppelte Slugs: **0**
- neue echte Term-IDs: **1577–1601 = 25/25**
- jede der fünf neuen Familien: **exakt 5/5 vorgesehene Intents**
- fünf Produktseiten: **5 eindeutige IDs / 5 eindeutige Slugs**
- bestehende Struktur bleibt additiv und unverändert.

### 26.6 Freeze-Regel

Für die laufende Kategorieintegration gilt ab jetzt:

**KATEGORIEKONZEPT = FINAL / FROZEN.**

Nicht mehr offen:
- Anzahl der neuen Produktseiten,
- deren Eltern,
- Namen/Slugs,
- Anzahl und Art der 25 Artikelkategorien,
- Intent-System,
- Abgrenzung zu bestehenden Kategorien,
- WordPress-Parent-Modell.

Offen bleiben ausschließlich technische Umsetzung/Propagation/Readback-Punkte aus Abschnitt 0A. Eine Änderung dieser Konzeption benötigt einen neuen ausdrücklichen Nutzerentscheid.
