# STARTMASTER0107 — System 4 Zielvertrag-Nachtrag — 2026-09-16

Status: **PROTOKOLL / WAS-WARUM-NACHWEIS, KEINE CURRENT-WAHRHEIT, KEIN ZIELVERTRAG**

Autoritative aktuelle Zustandsquelle bleibt ausschließlich:
`control/startmaster0107/CURRENT_STATE.json`

Aktueller verbindlicher System-4-Zielvertrag:
`isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_WORKER_DISPATCH_20260916.md`

Historisch abgelöst:
`isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`

## WAS

Bei der Abschluss-/Nachholprüfung wurde festgestellt, dass der bisher als aktuell bezeichnete Zielvertrag von 2026-09-14 zwei inzwischen falsche Acceptance-Aussagen enthielt:

1. Der vollständige Abnahmetest verlangte noch einen Worker-/Codex-Start. Aktuell ist für die Acceptance ausschließlich der gebundene deterministische Testworker zulässig; Codex ist dort verboten.
2. Der Zielvertrag bezeichnete `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` als finalen Handoff. Der aktuelle finale WordPress-Handoff ist `SYSTEM4_WORDPRESS_HANDOFF_V1` / `SYSTEM4_WORDPRESS_HANDOFF_V1.json`; `SYSTEM4_PARENT_CHAT_INLINE_V2` ist nur Transport/Relay.

Der Zielvertrag wurde deshalb am 2026-09-16 versioniert. Der alte Vertrag wurde ausdrücklich als historisch/abgelöst markiert und verweist auf die neue Zielquelle.

## WARUM

Eine als „aktuell“ markierte Zielquelle darf nicht gleichzeitig gegen die maschinell erzwungene Acceptance-Route und den realen finalen Handoff-Vertrag sprechen. Das hätte eine zweite Zielwahrheit und widersprüchliche Pflichtlektüre erzeugt.

Die Produktionsgrundarchitektur wurde nicht neu gestaltet: Produktion darf Codex weiterhin nur nach separater Freigabe als fachlichen Worker am bereits gebundenen Worker-Interface verwenden. Die Acceptance benutzt an exakt dieser Schnittstelle den Testworker, ohne einen zweiten Workflowpfad zu erzeugen.

## Ergebnis

- eine aktuelle System-4-Zielquelle;
- alter Zielvertrag eindeutig historisch;
- kein Codex im Acceptance-Test;
- finaler Handoff eindeutig `SYSTEM4_WORDPRESS_HANDOFF_V1.json`;
- Fresh-Article-, Textmaschinen-Detailcoverage- und Repair-Continuation-Pflichten im aktuellen Zielvertrag festgehalten.
