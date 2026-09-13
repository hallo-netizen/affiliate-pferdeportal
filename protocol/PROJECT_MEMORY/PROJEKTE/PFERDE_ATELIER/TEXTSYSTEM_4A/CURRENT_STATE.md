# TEXTSYSTEM 4A – CURRENT STATE

STAND: 2026-09-13
STATUS: AKTIV / ISOLIERTER GEGENPROTOTYP / NICHT PRODUKTIONSFREIGEGEBEN

## Gesicherte Vergleichsbasis

### System 4
- PR #238
- Branch `hobbyroom/system4-true-single-room-v1`
- frisch geprüfter Head: `623510bf7a7c968ae24fcb9003cf2f5d12c75bcc`
- weiterhin isolierter Teststand; kein Produktions-PASS aus dieser Prüfung.

### System 4A
- PR #255
- Branch `hobbyroom/system4a-capsule-v1-20260913`
- direkt auf den aktuellen System-4-Branch aufgesetzt;
- isolierter Gegenprototyp, kein Merge/Publish.

## Entscheidung 4 vs. 4A – korrigierter Stand

Die vorherige Entscheidung **`4A_STANDALONE_VORERST_VERWORFEN`** ist durch neue technische Evidenz überholt.

4A bleibt **offen**, aber nur wegen genau eines möglichen irreduziblen Unterschieds:

> **Wer besitzt den laufenden Workflow-State?**

Der aktuelle reale System-4-Auftrag lässt Codex im selben Task die Artikel-Workspaces/`state.json`-Dateien führen und die einzelnen Controller-Kommandos selbst aufrufen. `controller.py` liest diesen persistierten State bei jedem Schritt erneut. Der normale Hash schützt nur den `immutable_core` (`contract`, Snapshot, Batch, Artikel); der mutable Gesamtzustand ist kein ausschließlich von einem außerhalb des Workers liegenden Wächter authentifizierter Zustand.

Das ist ausdrücklich **kein bewiesener kompletter Release-Bypass**. Es ist eine reale äußere Einflussfläche auf den Workflow-State und damit für die Zielanforderung „eine Tür, ein Wächter“ relevant.

## 4A-Prototyp – aktueller Architekturbeweis

Der Gegenprototyp besitzt einen einzigen internen `CapsuleController`:
- echter Workflow-State bleibt innerhalb des Supervisors;
- außen existieren nur `capsule_id`, enger Arbeitsauftrag und read-only Status;
- Worker/Codex darf ausschließlich Arbeitsinhalt zurückgeben;
- Steuerfelder wie `phase`, `publish_allowed`, Route oder PASS sind keine zulässige Worker-Rückgabe;
- Prüfer geben nur PASS/FAIL + Hash/Findings zurück;
- FAIL öffnet ausschließlich Same-Article-Repair;
- Crash-/Resume-Checkpoint ist HMAC-authentifiziert;
- veränderter Checkpoint blockiert;
- `publish_allowed=false` besitzt keine externe Eingabefläche.

Lokal auf dem Prototyp ausgeführt:
- **13/13 Architekturtests PASS**;
- automatische Supervisorfolge `research → facts → draft → fullcheck`;
- Worker-Steuerfeld-Injektion BLOCK;
- Same-Article-Repair PASS;
- manipulierter Checkpoint BLOCK;
- falscher Prüfer-Hash BLOCK;
- 1.000 unabhängige Mock-Kapseln ohne Zustandsvermischung PASS.

Diese Tests beweisen **nur die Architektur**, nicht Inhalt, Design, PPM/LT oder Produktionsreife.

## Kein 4A-Entscheidungskriterium

Ausdrücklich **nicht** als Vorteil von 4A gewertet:
- frühere feste 7er-Bindung;
- frühere feste `Beratung`-Bindung;
- WordPress-Handoff.

Diese Punkte sind/werden in System 4 selbst bereinigt.

## WordPress – bereits frisch geklärt

Der reale Importer `Portal SEO Editorial Plan Compiler 0.28.23` besitzt bereits den generischen Zielvertrag `SYSTEM4_WORDPRESS_HANDOFF_V1`:
- mindestens 1 Artikel, keine feste Import-Obergrenze;
- `article_type` nicht auf `Beratung` festgelegt;
- alle Artikel vor dem ersten Write vollständig preflight-geprüft;
- Draft-only;
- Readback nach Write;
- Rollback bei Abweichung;
- `publish_allowed=false`.

Quelle/Details: `WORDPRESS_HANDOFF.md`.

4A baut **keine neue WordPress-Schnittstelle**.

## Inhalt / Design / Qualität – unverändert

4A darf ausschließlich dieselben vorhandenen Autoritäten READ-ONLY verwenden:
- bestehende Textmaschine/Fachregeln;
- `content_guard`;
- `design_guard`;
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- PSERC/PSTE/SEO-/Link-/Tabellen-/Metadatenregeln;
- vorhandene Querschnitts-/Wiederholungsprüfung;
- WordPress-Plugin 0.28.23.

Wenn 4A dafür neue Fach-/Design-/Qualitätsregeln oder Ersatzprüfer benötigt: **4A verwerfen**.

## Nächster Entscheidungsbeweis

Noch offen und jetzt ausschließlich relevant:
1. 4A direkt gegen den aktuellen System-4-Head betreiben;
2. vorhandene echte System-4-Prüfer unverändert READ-ONLY in den Supervisor einbinden;
3. Supervisor-Autorität real vom Codex/Worker trennen;
4. Research → Facts → Production Context → Draft → FULL-Check → Same-Article-Repair mit demselben Fach-/Design-/Qualitätsniveau beweisen;
5. vorhandene Querschnittsprüfung einbinden;
6. exakt `SYSTEM4_WORDPRESS_HANDOFF_V1` erzeugen;
7. danach real 1/3/25/1000 und mehrere bereits freigegebene Beitragsarten positiv/negativ prüfen.

## Abbruchschwelle

Wenn die reale Trennung Supervisor ↔ Codex nur durch neue Signer-, Token-, Room-, Receipt- oder Package-Kaskaden möglich wäre, wird 4A **sofort beendet**.

Dann wird die brauchbare Härtungsidee in Konzept 4 übernommen statt ein fünftes System zu bauen.

Kein Produktions-PASS ableiten.
