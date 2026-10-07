# AFFILIATE-ZENTRALE — ÜBERGABEWEGWEISER 07.10.2026

**Rolle:** kurzer Wegweiser. Keine zweite CURRENT-/Status-/NEXT-ACTION-Wahrheit.  
**Bei jeder Abweichung gilt ausschließlich `control/release-governance/CURRENT_RELEASE.json`.**

---

## 1. EINSTIEGSPUNKT FÜR DEN NEUEN CHAT

Für diesen Workstream gilt **keine STARTMASTER-Navigation**.

Pflichtweg:

1. `release/affiliate-zentrale/AGENTS.md`
2. `control/release-governance/CURRENT_RELEASE.json` — einzige Current-Autorität
3. Frischecheck gegen Branch `affiliate-release-current`
4. Wenn Manifest/Source seit Current unverändert: **KEINE VOLLREKONSTRUKTION. Direkt die eine NEXT ACTION aus Current ausführen.**
5. Wenn verändert: **nur das Delta** seit Current prüfen.

**Keine Bibliothek.**

---

## 2. ZIELVERTRAG

Autoritative Zielquelle:

`protocol/AFFILIATE_RELEASE_BANNER_IMPORT_BASIS_TARGET_20261007.md`

Ziel unverändert:

- Banner müssen aus echten Providerdaten belastbar einer korrekten Portal-Kategorie/Zielseite zugeordnet werden.
- Keine erfundenen Kategorien/Titel als Fachbeweis.
- Zielzuordnung erst nach technischer Bannerprüfung.
- Frontend liest gespeicherte Zielkarten; kein Provider-HTTP im Frontend.
- Tarifcheck und CHECK24 als Direktpartner.
- manueller Einzelbannerimport.
- Performance-Konzept erhalten.
- keine neue Ranking-/Target-Architektur.

---

## 3. WAS WURDE GEMACHT

### Frühere 6.72.199-Arbeit

Es wurden u. a. umgesetzt:

- vollständigerer ADCELL-Rohdatenerhalt;
- ADCELL-Kategorie-ID/-Name;
- Verify-before-Assign;
- Fail-closed bei kaputten Bildern;
- Retry eines später erneut importierten fehlgeschlagenen Bildes;
- Tarifcheck;
- CHECK24;
- manueller Bannerimport;
- CHECK24-Mehrfachziele;
- Performance-KISS: maximal 5 technische Assetprüfungen, Banner zuerst, Restplätze Produkte.

Der interne Lauf `37606358698` war für den damaligen Manifeststand PASS.

**Aber:** Der spätere Live-Screenshot des Nutzers hat bewiesen, dass dieser Candidate die eigentliche Live-Aufgabe **nicht gelöst** hat:
- Banner weiterhin ohne korrekte sichtbare/nutzbare Kategorie;
- Schabracken weiterhin falsch/nicht zugeordnet;
- Tarifcheck-Filter nicht zuverlässig.

Der alte Candidate-ZIP mit SHA
`dba7441a02821385ed723c031000f390f05c5c17e33a9a5f9e2e388281c3393b`
ist deshalb **nicht mehr der aktuelle Pluginstand und darf nicht erneut ausgegeben werden**.

### Aktueller Delta-Rootfix

Frische Delta-Analyse fand einen konkreten Sourcefehler:

`maybe_reconcile_banner_state_v672195()` ließ nur 6.72.195–6.72.198 zu, obwohl der zugehörige Runner `run_v672195_banner_reconcile()` 6.72.199 bereits unterstützte.

Folge:
Der normale Bestands-Reconcile konnte unter 6.72.199 über diesen Admin-Einstieg nicht starten. Bereits vorhandene Live-Banner konnten damit auf alten/leeren `topic_targets` stehenbleiben.

Aktueller Rootfix:

1. 6.72.199 bekommt nach abgeschlossenem ADCELL-Basislauf genau **einen** Bestands-Reconcile über den vorhandenen Runner.
2. Keine neue Reconcile-Architektur.
3. Tarifcheck/CHECK24-Filter wurde auf Partneridentität erweitert, damit auch historische Direkt-/Manuellimporte erfasst werden können.
4. Karten zeigen künftig ausdrücklich:
   - **Provider-Kategorie**
   - **gespeichertes Portalziel**
5. Performance-Konzept unverändert.

Geänderte Source-Dateien:

- `includes/trait-ppar-automation-suite.php`
- `includes/trait-ppar-creative-library.php`

---

## 4. ANALYSE DER BISHERIGEN LÖSUNGSWEGE — NICHT WIEDERHOLEN

Diese Punkte gehören zum Fehlerlernen und dürfen im neuen Chat nicht wieder als neue „Lösung“ verkauft werden:

1. **Lokaler/Fixture-PASS ist kein Live-Beweis.**  
   6.72.198 und der frühere 6.72.199-Candidate waren intern grün, der Livefehler blieb.

2. **Provider-Rohdaten/Kategorien korrekt speichern reicht nicht**, wenn der vorhandene Live-Bestand danach nicht neu reconciled wird.

3. **Verify-before-Assign ist Sicherheitslogik**, aber kein Ersatz für den fehlenden Bestands-Reconcile.

4. **Banner-vor-Produkte** löst Wartezeiten/Performance, **nicht** die fehlende fachliche Kategoriezuordnung.

5. **Real-ADCELL wurde zu früh als einziger Restblocker behandelt.**  
   Der spätere Live-Screenshot hat einen davorliegenden Funktionsfehler bewiesen.

6. **Dropdown vorhanden bedeutet nicht Filter funktioniert.**  
   Tarifcheck im UI war kein Beweis für korrekte Filterung.

7. **Keine Prüforgien.**  
   Keine neuen Tests, Workflows, Architekturideen oder historischen Rundreisen, solange Current nur das Plugin-Build verlangt.

Autoritative Fehlerquelle:
`protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md#AFF-ERR-056`

---

## 5. WAS MUSS NOCH GEMACHT WERDEN

Der aktuelle Rootfix ist **nur Source**.

Noch nicht vorhanden:

- kein neues Rootfix-ZIP;
- kein neuer PASS für den Rootfix-Manifeststand;
- kein Live-Beweis, dass Schabracken nun korrekt zugeordnet werden;
- kein Live-Beweis, dass Tarifcheck nun korrekt filtert.

Deshalb darf aktuell weder „fertig“ noch „PASS“ behauptet werden.

---

## 6. EXAKTER STATUS QUO

Autoritative Current-Autorität:

`control/release-governance/CURRENT_RELEASE.json`

Aktueller Stand:

- Generation: **258**
- Version: **6.72.199**
- Branch: `affiliate-release-current`
- Source: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Source-Dateien: **28**
- Manifest: `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- Manifest-SHA-256: `a51ef1236e8caa530493b65cc0c0e7c9c553f147a55745f4924f643b1b6ee844`
- aktueller Source-Status: **ROOTFIX SOURCE BOUND**
- neues Rootfix-Plugin: **NICHT GEBAUT**
- neuer Rootfix-PASS: **NICHT VORHANDEN**
- Release erlaubt: **NEIN**

Letzter alter interner Lauf:
`37606358698` — PASS **nur für den früheren Manifeststand**; nach den zwei Rootfix-Sourceänderungen stale.

Letzter Livebefund:
**FAIL** — Nutzer-Screenshot: keine korrekte Kategoriezuordnung / Schabracken weiterhin falsch / Tarifcheck-Filter nicht zuverlässig.

---

## 7. EXAKT EINE NEXT ACTION

**BUILD_ROOTFIX_PLUGIN**

Ein einziges installierbares ZIP exakt aus dem aktuellen manifestgebundenen Rootfix-Source bauen.

**Keine Tests davor. Keine neue Architektur. Keine neue Analyse.**

Danach ist der nächste operative Schritt ein enger Livecheck genau der zwei gemeldeten Fehler:
1. bestehende Banner zeigen/erhalten korrekte gespeicherte Kategorie/Portalziele;
2. Tarifcheck-Filter zeigt Tarifcheck-Banner.

---

## 8. VERBINDLICHER ARBEITSWEG — KISS

Harte Regeln für den nächsten Chat:

- Current Generation 258 übernehmen, wenn der Frischecheck keine Änderung zeigt.
- **Nicht** auf Generation 256 oder den alten Candidate zurückspringen.
- alten ZIP-SHA `dba744...` **nicht** wieder ausgeben.
- keine neue Testdatei;
- kein temporärer GitHub-Testworkflow;
- keine erneute Vollprüfung alter Gates;
- keine neue Rankinglogik;
- keine neue Targetarchitektur;
- kein Hoster-/Cache-Raten;
- kein Frontend-HTTP;
- keine größere Batchgröße;
- kein Performance-Rückbau.

Wenn der neue Rootfix später live noch scheitert:
**nur den ersten konkret sichtbaren Fehler untersuchen und genau diesen beheben.**

---

## 9. PERFORMANCE-HARDLOCK

Unverändert:

- maximal **5 technische Assetprüfungen pro Lauf**;
- Banner zuerst;
- nur freie PrüfsLOTS mit Produkten auffüllen;
- feste Bannerplätze bleiben feste Bannerplätze;
- feste Produktplätze bleiben feste Produktplätze;
- keine Monsterläufe;
- keine neue Frontend-Klassifikation;
- keine zusätzlichen Frontend-DB-/HTTP-Wege durch diesen Rootfix.

---

## 10. FEHLERPROTOKOLL

Autoritative Fehlerquelle:

`protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`

Aktuell relevant:

- **AFF-ERR-054:** historische Importbasis/Verify-before-Assign-Arbeit.
- **AFF-ERR-055:** früher fehlender Ausführungsweg; historisch geschlossen.
- **AFF-ERR-056:** **aktuell maßgeblich** — Livefehler blieb trotz vorherigem Candidate; konkreter 6.72.199-Reconcile-Einstiegsfehler gefunden; Filter/Anzeige-Rootfix Source-seitig ergänzt; Rootfix noch nicht gebaut/live bewiesen.

Keine Fehler nur im Chat belassen.

---

## 11. PLUGIN-STATUS

Plugin:

- ID/Verzeichnis: `affiliate-portal-router`
- Name: Affiliate-Zentrale
- Art: Eigenentwicklung
- Version: 6.72.199
- Fachquelle: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Branch: `affiliate-release-current`
- aktuelles Manifest: `a51ef1236e8caa530493b65cc0c0e7c9c553f147a55745f4924f643b1b6ee844`

Plugin wurde im aktuellen Delta geändert.

Im Repository wurde **kein** separates
`PLUGINS/ISOLIERTE_PLUGINS/.../CURRENT.zip`-Pult gefunden.

Die Bibliothek ist vom Nutzer ausdrücklich ausgeschlossen und wurde nicht benutzt.

Daher nach Artefaktregel:
- altes CURRENT-/Candidate-ZIP **nicht** als aktuellen Rootfix ausgeben;
- isolierte Plugin-Synchronisierung derzeit **BLOCKED**, bis das neue exakte Rootfix-ZIP gebaut und der erforderliche Livebefund vorliegt.

---

## 12. PROTOKOLLCHECK

- Fehler: **NACHGEHOLT**
- Protokoll: **NACHGEHOLT**
- Warum/Entscheidungen: **NACHGEHOLT**
- Current-Autorität: **NACHGEHOLT / PASS**
- Bürotür/Einstiegspunkt: **PASS** — für diesen Workstream AGENTS → Current, kein STARTMASTER
- Frischecheck: **DELTA GEPRÜFT**
- Hobbyraum: **NICHT BETROFFEN**
- Zielvertrag: **PASS / unverändert**
- Archiv: **NICHT BETROFFEN**
- Paul/Worker/Parallelbranch: **NICHT BETROFFEN**
- Eine Wahrheit: **PASS**
- Tests: **OFFEN** — Rootfix-Source hat noch keinen neuen PASS; bewusst keine Testschleife gestartet
- Plugins: **BLOCKED** — Rootfix-ZIP noch nicht gebaut; isoliertes CURRENT.zip ohne Bibliothek nicht verfügbar

---

## 13. NEUER CHAT — IN EINEM SATZ

**AGENTS → Current Generation 258 → Frischecheck → bei unverändertem Manifest keine Rekonstruktion → exakt BUILD_ROOTFIX_PLUGIN ausführen → danach nur die zwei gemeldeten Livefehler prüfen.**

Diese Übergabe ist keine zweite Current-Wahrheit.
