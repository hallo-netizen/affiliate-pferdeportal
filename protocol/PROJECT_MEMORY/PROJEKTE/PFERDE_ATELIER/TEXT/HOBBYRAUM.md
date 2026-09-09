# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – REALTEST / REPARATUR VERBOTEN**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`05f5d00ec924e108d6700f39d22d9ec1d47318a6`

Dispatcher:
`codex-chat-launcher = 05f5d00ec924e108d6700f39d22d9ec1d47318a6`

M01–M35:
**MASCHINELL GESAMT PASS.**

M17 / M22 / M26 / M35:
**integriert behoben.**

## JETZT AUSSCHLIESSLICH

**Echter frischer STARTMASTER0107-7/7-Realtest.**

Verbindlich:
- zuerst exakten HEAD prüfen;
- Cloud Entry;
- Production Preflight;
- Runtime Entry;
- Current Action / Single Door;
- alle 7 Artikel vollständig frisch;
- keine alten Artikel/JSONs/Proofs/Recovery-/Quarantäne-/Release-Artefakte als Produktionsquelle;
- Current Codex ist der gebundene Fachworkflow-Worker;
- kein zweiter Executor / keine Capability-Suche;
- reale aktuelle Fachworkflow-Artefakte und Pflicht-Stage-Proofs erzeugen;
- `FACHWORKFLOW_HANDOFF_REQUEST.json` exakt aus den gebundenen Current-Action-Werten erzeugen;
- ausschließlich `fachworkflow_handoff.command`;
- echter PPM 6.7.9;
- nur nach `FACHWORKFLOW_PROOF_HANDOFF_PASS` → `submission_command`;
- nächstes gebundenes Item;
- danach 107008.

## STOP-REGEL

Im Realtest:
- **keine Reparatur**;
- keine Architekturänderung;
- keine neue Route;
- kein Fix auf einen FAIL.

Terminal ausschließlich:
1. 7/7 PASS + 107008 PASS,
oder
2. erster echter technischer BLOCKED / USER_ACTION_REQUIRED.

Dann erst wieder Hobbyraum-Reparaturphase eröffnen.

## PUBLISH-GRENZE

- `publish_allowed=false`;
- kein Auto-Publish;
- keine WordPress-Schreibaktion;
- Veröffentlichung nur nach ausdrücklicher Nutzerfreigabe.

## AUTORITATIVE BELEGE

Current State Blob:
`65da28894fd3af555150dc85a1b3249f7cf45a1e`

Fehlerquelle Blob:
`b322f233f60f45d22976fea9bc3a227be29c6fbb`

Protokoll Blob:
`bfdc8baa14775bc849de942758f16d04c3067a85`

Historische Matrix:
`a3c6a468dc1cf380c3a874ef86805d978d78e582`

Regression-Runner:
`f7af847ed46fcae6527037eef06487b2f6d77786`

RECOVERY_BASE_SHA:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

## NEXT ACTION

**Realtest auf Dispatcher PR #107 starten und ohne Zwischenreparatur bis Terminal laufen lassen.**

PR #107 bleibt offen und wird niemals gemergt.
