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

## CDEX-AFF-005 — Branchprüfung umgangen, aber stale Checkout weiter als aktuelle Autorität behandelt

**Symptom:** Nach dem lokalen Override der Branchprüfung stoppte `release_guard.py start --branch affiliate-release-current` mit `CURRENT_MANIFEST_FORMAT`.

**Root Cause:** Der Codex-`work`-Checkout enthält einen vom aktuellen GitHub-Affiliate-Stand abweichenden/stalen Manifestzustand. Der echte aktuelle Affiliate-Branch enthält dagegen ein korrektes Manifest mit exakt 26 normalen SHA-256-Zeilen.

**Gescheiterter Weg:** Nur den Branchnamen-Check ausschalten und danach blind den lokalen Release-Guard/Manifestzustand als aktuell behandeln.

**Nicht wiederholen:** Bei nachgewiesen stale lokalem Manifest keine weiteren Branch-/Fetch-/Guard-Varianten ausprobieren. Erst die tatsächliche Datei-/Hash-Autorität bestimmen. Der aktuelle kanonische GitHub-Stand ist `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` mit 26 Dateien und gebundenem Manifest-SHA-256 `109879a3c355dff075db4d0ccfe81e7396ed571e5c180019f85d907d56d55f77`.

**Status:** OPEN als Umgebungsabweichung; kein Affiliate-Fachfehler.

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

# Verbindlicher Precheck für weitere Codex-Schritte

Vor jedem neuen Codex-Befehl im Affiliate-Workstream muss gegen CDEX-AFF-001 bis CDEX-AFF-006 geprüft werden.

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
