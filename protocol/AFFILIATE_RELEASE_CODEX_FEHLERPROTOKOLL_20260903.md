# AFFILIATE-ZENTRALE — CODEX-FEHLERPROTOKOLL

Stand: 2026-09-03
Workstream: `AFFILIATE_ZENTRALE`
Status: `BINDING_ERROR_MEMORY`

## Zweck

Dieses Protokoll hält die in der aktuellen Affiliate-/Codex-Arbeit tatsächlich aufgetretenen Fehlwege fest. Diese Wege dürfen bei demselben Arbeitsstand nicht erneut versucht werden.

---

## CDEX-AFF-001 — Falscher Workstream durch globale Cloud-Eingangstür

**Symptom:** Codex band `RUN_NEW_ARTICLE_BATCH_NO_STOP` aus der Textproduktion statt `AFFILIATE_ZENTRALE` und blockierte den Affiliate-Livekandidaten.

**Root Cause:** Die globale Cloud-/STARTMASTER-Eingangstür wurde für einen Affiliate-Auftrag verwendet, obwohl dieser Workstream eine eigene Release-Governance besitzt.

**Gescheiterter Weg:**
- `control/cloud-entry-gate/cloud_entry.py start`
- `control/output-quarantine/runtime_entry_gate.py`
- `control/single-door-boundary/codex_current_action.py`
- Navigation über STARTMASTER/Capsule/Quarantine

**Nicht wiederholen:** Affiliate-Aufträge niemals über STARTMASTER, globale Cloud-Entry-, Capsule-, Quarantine- oder Textproduktions-State-Navigation führen.

**Status:** CLOSED / permanenter Hardlock.

---

## CDEX-AFF-002 — Falscher lokaler Branch-Zwang in der Arbeitsglocke

**Symptom:** `AFFILIATE_RELEASE_WORK_BELL.py` blockierte mit `WRONG_BRANCH`, weil Codex auf seinem technischen Branch `work` läuft.

**Root Cause:** Die Glocke verlangte fälschlich, dass der lokale Codex-Checkout exakt `affiliate-release-current` heißen muss.

**Gescheiterter Weg:** lokaler Branchname als Release-Autorität.

**Nicht wiederholen:** In Codex Cloud darf der technische Arbeitsbranch `work` nicht allein als Fehler gewertet werden. Autorität sind die gebundenen Affiliate-Dateien, Manifest-/Datei-Hashes und der belegte Source-Stand.

**Status:** CLOSED / Regel dauerhaft bindend.

---

## CDEX-AFF-003 — Nicht vorhandenen lokalen Branch vorausgesetzt

**Symptom:** `git switch affiliate-release-current` scheiterte mit `fatal: invalid reference: affiliate-release-current`.

**Root Cause:** Ohne Prüfung wurde angenommen, dass der GitHub-Branch als lokaler Ref im Codex-Checkout vorhanden ist.

**Gescheiterter Weg:** `git switch affiliate-release-current` ohne vorher nachgewiesenen lokalen Ref.

**Nicht wiederholen:** Niemals einen lokalen Branch/Ref voraussetzen. Vor Branchoperationen zuerst tatsächliche lokale Refs prüfen. Für den aktuellen Affiliate-Auftrag ist ein Branchwechsel nicht erforderlich.

**Status:** CLOSED / permanenter Nicht-Wiederholungsfehler.

---

## CDEX-AFF-004 — Nicht vorhandenes `origin` vorausgesetzt

**Symptom:** `git fetch origin affiliate-release-current` scheiterte, weil der Codex-Checkout kein `origin` konfiguriert hatte. Danach war `FETCH_HEAD` ebenfalls nicht vorhanden.

**Root Cause:** Ohne Prüfung wurde ein klassischer Git-Remote-Aufbau angenommen.

**Gescheiterter Weg:**
- `git fetch origin affiliate-release-current`
- `git checkout FETCH_HEAD -- ...`

**Nicht wiederholen:** Niemals `origin`, `FETCH_HEAD` oder irgendeinen Remote voraussetzen. Vor Remote-Aktionen zuerst `git remote -v` prüfen. Im aktuellen Affiliate-Auftrag keine Fetch-/Remote-Schleife mehr beginnen.

**Status:** CLOSED / permanenter Nicht-Wiederholungsfehler.

---

## CDEX-AFF-005 — Branchprüfung umgangen, danach echter Manifestfehler sichtbar

**Symptom:** Nach dem lokalen Override der Branchprüfung stoppte `release_guard.py start --branch affiliate-release-current` mit `CURRENT_MANIFEST_FORMAT`.

**Root Cause:** Nicht der Branch war danach das Problem, sondern eine tatsächlich defekte Zeile im kanonischen Manifest. Der erwartete SHA für `class-ppar-partner-analytics.php` war nur 63 Zeichen lang.

**Gescheiterter Weg:** Den `CURRENT_MANIFEST_FORMAT`-Fehler vorschnell als bloß stale Codex-Checkout erklären, ohne die kanonische Manifestzeile selbst bytegenau zu prüfen.

**Nicht wiederholen:** Bei `*_MANIFEST_FORMAT` zuerst die betroffene Manifestzeile selbst prüfen: 64 Hexzeichen, Dateipfad, tatsächlicher Datei-SHA und historische belegte Bindung. Keine Branch-/Remote-Interpretation ohne diesen Beweis.

**Status:** CLOSED durch CDEX-AFF-007.

---

## CDEX-AFF-006 — Meta-Schleife statt eigentlichem Livekandidaten

**Symptom:** Statt `26 Dateien prüfen -> ZIP bauen -> WordPress live testen` entstanden nacheinander Branch-, Ref-, Remote-, FETCH_HEAD- und Guard-Schleifen.

**Root Cause:** Infrastrukturannahmen wurden jeweils einzeln repariert, obwohl sie nicht Teil des fachlichen Zielvertrags sind.

**Nicht wiederholen:** Der Affiliate-Livekandidat darf nicht durch neue Meta-Infrastruktur blockiert werden. Für diesen Stand gilt die kürzeste zulässige Kette:

1. kanonischen 26-Dateien-Stand bestimmen,
2. 26/26 Datei-Hashes prüfen,
3. Live-ZIP bauen,
4. ZIP frisch entpacken und 26/26 erneut prüfen,
5. WordPress installieren,
6. vorhandene DS24-CSV importieren,
7. 18 Partnerschaften / 10 Vendorquellen live readbacken,
8. danach finalisieren.

Keine zusätzliche Branch-, Remote-, STARTMASTER-, Discovery-, Rekonstruktions- oder Plugin-Schleife.

**Status:** ACTIVE PROCESS HARDLOCK.

---

## CDEX-AFF-007 — Kanonisches Manifest enthielt 63-stelligen SHA-256-Wert

**Symptom:** `class-ppar-partner-analytics.php` stand im aktuellen Manifest mit dem ungültigen 63-stelligen Wert `65e1979b6df19a4f415c018e1862e51c1d7fbe0baea9e433cf5202466563ad0`.

**Belegter tatsächlicher/korrekter SHA-256:** `65e1979b6df19a4c5c4eee0f19a1f4f468f7be75c5cf964f427a3dcb08b8daa4`.

**Beweis:** Derselbe 64-stellige Hash war bereits im früheren kanonischen Manifest gebunden; die Datei selbst wurde seit ihrem Commit `6007cfc18e28780d356edac858e161e36bc543be` nicht mehr verändert.

**Root Cause:** Beim späteren Neubinden des 26-Dateien-Manifests wurde genau diese Manifestzeile beschädigt. Sourcecode selbst war nicht betroffen.

**Fix:**
- `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` korrigiert,
- neuer Manifest-SHA-256: `67573f105941ed2a48476f11d138a581f9b1549de9e9dab07e03c4bcbbbf10f9`,
- `control/release-governance/CURRENT_RELEASE.json` auf den neuen Manifest-SHA gebunden,
- `protocol/AFFILIATE_RELEASE_WORK_BELL.py` auf denselben Manifest-SHA gebunden.

**Nicht wiederholen:** Vor jeder neuen Manifestbindung zwingend alle Manifestzeilen auf `^[0-9a-f]{64}$` prüfen und anschließend alle 26 tatsächlichen Datei-SHAs gegen die Liste laufen lassen. Erst danach den Manifest-SHA in Governance/Glocke übernehmen.

**Status:** FIXED / permanenter Precheck.

---

# Verbindlicher Precheck für weitere Codex-Schritte

Vor jedem neuen Codex-Befehl im Affiliate-Workstream muss gegen CDEX-AFF-001 bis CDEX-AFF-007 geprüft werden.

Wenn ein vorgeschlagener Schritt einen bereits gescheiterten Weg wiederholt: **NICHT AUSFÜHREN**.

Insbesondere aktuell verboten:
- STARTMASTER/Cloud-Entry/Capsule/Quarantine,
- `git switch affiliate-release-current`,
- `git fetch origin ...`,
- `FETCH_HEAD`-Wege,
- weitere Versuche, den lokalen Branchnamen `work` zu reparieren,
- weitere DS24-Discovery-Schleifen,
- erneute Wiederholung bereits bestandener Affiliate-Fachtests ohne Sourceänderung.

Ziel bleibt ausschließlich: **brauchbare byteidentisch geprüfte Live-ZIP -> WordPress -> vorhandene DS24-CSV -> Live-Readback -> Finalisierung**.
