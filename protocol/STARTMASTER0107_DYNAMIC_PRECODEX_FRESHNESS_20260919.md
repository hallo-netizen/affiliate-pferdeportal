# STARTMASTER0107 – dynamischer Pre-Codex-Einstieg 2026-09-19

Der Status ist absichtlich selbststabil: Ein Status-Merge verändert Main. Deshalb darf CURRENT_STATE keinen festen "aktuellen Main" als dauerhafte Startfreigabe verwenden.

Vor jedem realen Codex-Start gilt zwingend:
1. Main frisch lesen.
2. Permanenten Dispatcher PR #342 frisch lesen.
3. Head von PR #342 muss exakt dem dann aktuellen Main entsprechen.
4. hardlock-base muss frisch auf genau dieser Relation PASS sein.
5. Erst danach darf Codex starten.

Letzte verifizierte Vorprüfung vor diesem Status:
- Dispatcher PR #342
- Head `93956f83ca2f8ddea5f07cb82c1b77ef393f248f`
- hardlock-base Run `35427945011` PASS
- codex-freie System4A-Acceptance `35398621624` PASS

PR #107 ist superseded. Er wurde bei Basiswartung automatisch geschlossen; Main wurde dadurch nicht verändert.

Aktueller Nutzerstop: **kein Codex, keine reale neue Artikelproduktion, kein Publish**.
