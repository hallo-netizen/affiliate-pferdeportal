# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – REALTEST / REPARATUR VERBOTEN**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`93ba987c56f7b08ffba009210e3012c036fec18d`

Dispatcher:
`codex-chat-launcher = 93ba987c56f7b08ffba009210e3012c036fec18d`

M01–M36:
**MASCHINELL GESAMT PASS.**

M17 / M22 / M26 / M35 / M36:
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
`b91219b9613ff8557c7ddd510d959076348242eb`

Fehlerquelle Blob:
`1d55e12d845126a3ffd359f4ee080ebaba6fbe7b`

Protokoll Blob:
`11b9f4d874e5535fcecb2dea5289d3d4b42e218d`

Änderungsregister Blob:
`28b90ca69e033609c6e482d7e3e54bee7ea11574`

Historische Matrix:
`647732791cdf764399164b471aa7fddc262d9296`

Regression-Runner:
`a6d42c7f355b9ad23ff435a78ff7e74aee4dc8be`

RECOVERY_BASE_SHA:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

## NEXT ACTION

**Realtest auf Dispatcher PR #107 starten und ohne Zwischenreparatur bis Terminal laufen lassen.**

PR #107 bleibt offen und wird niemals gemergt.
