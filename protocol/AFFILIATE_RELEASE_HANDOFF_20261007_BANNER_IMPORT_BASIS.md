# AFFILIATE-ZENTRALE — ÜBERGABEWEGWEISER 07.10.2026

**Rolle:** ausschließlich kurzer Wegweiser für den nächsten Chat. Keine zweite CURRENT-/Status-/NEXT-ACTION-Wahrheit.  
**Wenn irgendeine Angabe hier von `control/release-governance/CURRENT_RELEASE.json` abweicht, gilt ausschließlich Current.**

---

## 1. EXAKTER EINSTIEG FÜR DEN NEUEN CHAT

1. `release/affiliate-zentrale/AGENTS.md` lesen.
2. `control/release-governance/CURRENT_RELEASE.json` lesen — **einzige Current-Autorität**.
3. Frischecheck: prüfen, ob Source-Manifest bzw. Plugin-Source seit dem dort gebundenen Stand verändert wurden.
4. Wenn unverändert: **KEINE VOLLERMITTLUNG, KEINE TESTWIEDERHOLUNG. Direkt die eine NEXT ACTION aus Current ausführen.**
5. Nur wenn eine relevante Änderung belegt ist: **nur das Delta** prüfen.

Für diesen Workstream **keine STARTMASTER-Navigation und keine Bibliothek**.

---

## 2. ZIELVERTRAG

Autoritative Zielquelle:

`protocol/AFFILIATE_RELEASE_BANNER_IMPORT_BASIS_TARGET_20261007.md`

Kernziel:

- echte Providerbasis vollständig und nachvollziehbar übernehmen;
- keine synthetischen Titel/Fantasiedaten als Fachbeweis;
- Zielzuordnung erst nach technischer Bannerprüfung;
- Frontend liest nur gespeicherte Zielzuordnungen;
- Tarifcheck und CHECK24 als Direktpartner nutzbar;
- einzelnes händisches Einfügen von Bannern möglich;
- Performance-Konzept erhalten;
- **keine neue Ranking-/Target-Architektur bauen**.

Zielvertrag wurde in diesem Abschluss nicht verändert.

---

## 3. WAS WURDE GEMACHT

Am 6.72.199-Source wurden die identifizierten Ursachen behoben:

- ADCELL-Providerdaten werden vollständig wert-/typgetreu in der Creative Library erhalten und gehasht.
- echte ADCELL-Kategorie-ID/-Name werden übernommen.
- fehlende/kaputte ADCELL-Rohbasis blockiert fail-closed.
- synthetisch erzeugte Ersatz-Titel zählen nicht als fachliche Evidenz.
- Providerfeld `information` wird erhalten.
- **Verify-before-Assign gilt global:** kein Banner erhält eine feste Zielkarte vor erfolgreicher technischer Assetprüfung.
- fehlgeschlagene Bilder bleiben innerhalb eines Laufs fail-closed; ein späterer echter Provider-Reimport darf nur die technische Prüfung erneut öffnen.
- Tarifcheck ist explizit auswählbar.
- CHECK24 ist als eigener Direktpartner eingebaut und nutzt den bestehenden sicheren Kosten-/Versicherungsweg.
- händischer Einzelbanner-Import ist eingebaut.
- CHECK24-Mehrfachzielkarten werden zur Laufzeit korrekt gelesen.
- KISS-Performancefix: technische Assetprüfung bleibt **maximal 5 Assets pro Lauf**; zuerst wartende Banner, nur freie PrüfsLOTS werden mit Produkten aufgefüllt.
- **Feste Bannerplätze und feste Produktplätze auf der Website wurden nicht verändert.**
- kein Frontend-HTTP hinzugefügt;
- keine neue Rankingebene;
- keine Erhöhung der Batchgröße.

### Belastbar ausgeführter interner Endlauf

Run: `37606358698`  
Evidence: `release/affiliate-zentrale/evidence/affiliate_router_v672199_internal_candidate_gate_20261007.md`

PASS:

- Governance / Source / Tree / Start;
- PHP-Syntax;
- frisches WordPress 7.1.2 + MariaDB;
- installierter Pluginbaum 28/28 byteidentisch zum Manifest;
- statischer ADCELL-Basisvertrag;
- ADCELL mocked WordPress/MariaDB E2E;
- 6.72.198 -> 6.72.199 Upgrade-E2E;
- Tarifcheck / CHECK24 / manueller Banner-E2E;
- Verify-before-Assign;
- Retry eines zuvor fehlgeschlagenen Assets;
- bestehende Bannerregression;
- Installer-Fresh-Unpack;
- Source/ZIP-Byteidentität 28/28;
- ZIP-Integrität.

Der temporäre GitHub-Endtest-Workflow wurde nach dem erfolgreichen Lauf wieder entfernt. Seit dem erfolgreichen Lauf wurde **keine Plugin-Source-Datei mehr geändert**.

---

## 4. WAS MUSS NOCH GEMACHT WERDEN

**Genau eine fachliche Sache ist offen:**

Der echte ADCELL-Provider-Gate muss mit realen ADCELL-Zugangsdaten und echten Programm-IDs auf einem isolierten Testhost laufen:

`release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_real_provider_v672199.php`

Im internen Endlauf fehlten:

- `PPAR_ADCELL_USERNAME`
- `PPAR_ADCELL_PASSWORD`
- `PPAR_ADCELL_PROGRAM_IDS`

Darum gibt es **noch keinen Real-ADCELL-PASS** und noch keine Releasefreigabe.

Wenn dieser Gate PASS ist und das Source-Manifest unverändert bleibt:

1. **keine internen Tests wiederholen**;
2. vorhandenen Candidate-Installer als final binden;
3. `release-check` ausführen;
4. danach Release/Freigabe nach Current.

Wenn der Real-ADCELL-Gate FAIL ist:

- nur den **ersten konkret belegten Fehler** beheben;
- keine Nebenbaustelle;
- nur die durch diesen Fix stale gewordene Evidence erneut prüfen.

---

## 5. EXAKTER STATUS QUO ZUM ZEITPUNKT DIESER ÜBERGABE

Autoritative Current-Autorität:

`control/release-governance/CURRENT_RELEASE.json`

Stand nach Abschlussnachzug:

- Generation: **256**
- Kandidat: **6.72.199**
- Source: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Source-Dateien: **28**
- Source-Manifest-SHA-256: `85554ba74ccbac2a81abe15b63243c5128d6d06c7634161e32ad52504fb72800`
- interner Candidate-Gate: **PASS**, Run `37606358698`
- Real-ADCELL-Gate: **NICHT AUSGEFÜHRT**
- Release erlaubt: **NEIN**
- Candidate-ZIP: `AFFILIATE_ZENTRALE_6.72.199.zip`
- Candidate-ZIP SHA-256: `dba7441a02821385ed723c031000f390f05c5c17e33a9a5f9e2e388281c3393b`
- Candidate-ZIP Größe: **816205 Bytes**
- GitHub Actions Artifact-ID: `11475087240`
- finale Artefaktbindung: **noch offen**, weil Real-ADCELL-Gate fehlt.

Letzter sicherer Live-Vergleich:
6.72.198 war lokal grün, aber live vom Nutzer als **kein Banner auf Schabracken** gemeldet. 6.72.198 ist daher ausdrücklich **nicht** die Lösung.

---

## 6. EXAKT EINE NEXT ACTION

**RUN_REAL_ADCELL_PROVIDER_GATE**

Nur den echten ADCELL-Test mit realen Zugangsdaten/Programm-IDs auf dem **exakt unveränderten** 6.72.199-Manifeststand ausführen.

**NICHTS ANDERES VORHER.**

---

## 7. VERBINDLICHER ARBEITSWEG — KISS / KEINE SINNLOSEN TESTS

### HARTE REGEL FÜR DEN NEUEN CHAT

**KEINE SINNLOSEN TESTS. KEINE WIEDERHOLUNG BEREITS GRÜNER TESTS. KEINE „ZUR SICHERHEIT“-PRÜFORGIEN.**

Konkret:

- Run `37606358698` ist bei unverändertem Source-Manifest wiederzuverwenden.
- Nicht noch einmal WordPress/MariaDB frisch aufsetzen, nur um denselben internen Test zu wiederholen.
- Nicht noch einmal Tarifcheck/CHECK24/manuellen Bannerimport testen, solange Source unverändert ist.
- Nicht noch einmal Installer-Byteidentität prüfen, solange derselbe Candidate und dasselbe Manifest gelten.
- Keine neuen Testdateien erfinden.
- Keine temporären GitHub-Workflows bauen, solange Current nicht ausdrücklich genau das verlangt.
- Nicht aus der großen `required_release_gates`-Matrix einzelne neue Arbeitsstränge machen. Sie ist Nachweismatrix, **nicht NEXT-ACTION-Liste**.
- Immer nur `execution_state.authorized_next_action` / `bound_user_scope_action` aus Current ausführen.
- Bei PASS-Reuse gilt: **hash-identischer Stand = vorhandenen PASS verwenden.**
- Bei FAIL: nur erster echter Fehler → kleinster Fix → nur stale gewordene Evidence nachziehen.

### PERFORMANCE-HARDLOCK

Nicht zurückbauen:

- maximal **5 technische Assetprüfungen pro Lauf**;
- Banner zuerst;
- nur freie PrüfsLOTS mit Produkten auffüllen;
- keine Änderung der festen Banner-/Produktplätze;
- kein Frontend-HTTP;
- keine neue Frontend-Klassifikation;
- keine neue Ranking-/Target-Schicht;
- keine größere Batchgröße;
- keine Monsterläufe.

---

## 8. NICHT ANFASSEN

Ohne neuen konkreten Real-ADCELL-Fehler nicht verändern:

- Banner-Ranking;
- Target-/Zuordnungsarchitektur;
- feste Banner-/Produktplätze;
- Performance-Hotpaths;
- Produktlogik;
- bestehende 5er-Batchgrenze;
- Tarifcheck-/CHECK24-Konzept;
- manuelle FIXED-Zuordnung als „Systemlösung“;
- Hoster-/OPcache-/Servertheorien ohne Beleg;
- historische Root-`affiliate-portal-router/`-Quelle;
- STARTMASTER für diesen Workstream.

Keine Bibliotheksarbeit für diese Übergabe.

---

## 9. FEHLERPROTOKOLL

Autoritative Fehlerquelle:

`protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`

Relevante aktuelle Historie:

- **AFF-ERR-054:** ursprüngliche Banner-Importbasis/Verify-before-Assign-Probleme. Source-Fixes intern belegt. Aktuell bleibt davon nur der echte ADCELL-Provider-Nachweis offen.
- **AFF-ERR-055:** fehlender versionsneutraler WordPress/MariaDB-Ausführungsweg. **Geschlossen**; Run `37606358698` hat den internen Candidate-Gate erfolgreich ausgeführt.
- 6.72.198: lokal PASS, live Nutzerbefund „kein Banner Schabracken“ — nicht als Lösung verwenden.
- falsche Hypothesen wie „zweite Affiliate-Zentrale“ bzw. Hoster/OPcache nicht wieder aufwärmen, solange kein neuer Beleg vorliegt.
- frühere unnötige Workflow-/Testumwege nicht wiederholen.

Im Fehlerregister wurde der aktuelle Abschlussstand nachgezogen.

---

## 10. PLUGIN-STATUS

Plugin betroffen: **Affiliate-Zentrale / affiliate-portal-router**, Eigenentwicklung.

Aktueller Candidate: **6.72.199**.

Ein Candidate-ZIP ist gebaut und intern geprüft, aber wegen offenem Real-ADCELL-Gate noch **kein final freigegebenes Releaseartefakt**.

Im Repository wurde kein separates `PLUGINS/ISOLIERTE_PLUGINS/.../CURRENT.zip`-Pult gefunden. Die vom Nutzer ausdrücklich ausgeschlossene Bibliothek wurde nicht benutzt.

Daher:
- kein externes/isoliertes `CURRENT.zip` voreilig ersetzen;
- erst nach Real-ADCELL-PASS und finaler Releasebindung synchronisieren.

---

## 11. PROTOKOLLCHECK

- Fehler: **NACHGEHOLT**
- Protokoll/Evidence: **NACHGEHOLT**
- Warum/Entscheidungen: **PASS**
- Current-Autorität: **NACHGEHOLT / PASS**
- Einstiegspunkt: **PASS**
- Frischecheck: **DELTA GEPRÜFT**
- Hobbyraum: **NICHT BETROFFEN**
- Zielvertrag: **PASS / unverändert**
- Archiv: **NICHT BETROFFEN**
- Eine Wahrheit: **PASS**
- Tests: **OFFEN — ausschließlich Real-ADCELL-Provider-Gate**
- Plugins: **BLOCKED bis Real-ADCELL-PASS für finale Artefaktsynchronisierung**

---

## 12. NEUER CHAT — IN EINEM SATZ

**AGENTS → Current Generation 256 → Frischecheck → bei unverändertem Manifest keine Rekonstruktion und keine Testwiederholung → ausschließlich Real-ADCELL-Provider-Gate ausführen.**

Die Übergabe ist keine zweite Wahrheit. Bei jeder Abweichung gilt ausschließlich `control/release-governance/CURRENT_RELEASE.json`.
