# System 4A — Main-Kernel / Hardlock-Split

Stand: 2026-09-16
Status: KERNEL_PREQUALIFIED / POSTRELEASE_TRANSPORT_PREQUALIFIED / ADMIN_ENDSTEMPEL_BLOCKED / 107008_REBIND_NOT_AUTHORIZED_HERE

## Autoritative technische Basis

- aktuelles `main`: `9cdb171343794f609b6cca36329774c2289b5cd6`
- vollständig vorqualifizierter System-4A-Head nach Main-Rebind: `531a40bedf6f4bd9c709d1ad36d4c46db966c166`
- Main-Rebind in den 4A-Testbranch erfolgte über PR #263; PR #263 ist geschlossen/merged, ohne System 4A nach `main` zu veröffentlichen.

Auf `531a40bedf6f4bd9c709d1ad36d4c46db966c166` sind bewiesen:

- System 4A Real LT68 PPM679 Acceptance, Run `35105842734`: PASS, alle 37 Schritte;
- System 4A Repair Owner Contract, Run `35105842615`: PASS;
- System 4A Exact Head Bundle, Run `35105842657`: PASS;
- kompletter 1-Artikel-Weg PASS;
- kompletter 3-Artikel-Weg mit isoliertem Repair PASS;
- 1..N-Handoff PASS.

Der Marker bleibt ausdrücklich:
`SYSTEM4_BRANCH_PREQUALIFICATION_PASS_PENDING_CANONICAL_107008_ENDSTEMPEL_CHAT`

Das ist kein Gesamt-PASS und keine Produktionsfreigabe.

## KISS-Trennung — aktuelle aktive Kandidaten

### PR #264 — System-4A-Kern

Branch: `hobbyroom/system4a-main-kernel-20260916`

Inhalt:
- `isolated_system4/**` aus dem vollständig vorqualifizierten 4A-Head;
- diese Status-/Befunddatei.

Explizit nicht enthalten:
- `.github/workflows/**`;
- STARTMASTER-State oder Step-Bundles;
- `ENDSTEMPEL_*`;
- Produktions-Release-/Publish-Aktion.

Auf dem vorherigen dokumentierten Head `b841d91ee1573f0e1bb4c220675f92239daa6e36` waren beide Main-Hardlocks PASS:
- Deterministic Entrance Gate / `hardlock`, Run `35109630883`;
- Immutable Base Hardlock / `hardlock-base`, Run `35109627594`.

Nach jeder Änderung dieser Protokolldatei müssen beide Checks auf dem neuen exakten PR-Head erneut PASS sein.

### PR #266 — zustandslose 1..N-Nachstrecke

Branch: `hobbyroom/system4a-postrelease-1n-transport-20260916`
Head: `5329f1a0b1216527481db3173bb0c2076ebd9805`

Exakt zwei Dateien:
- `control/startmaster0107/chat_delivery_payload.py`
- `control/startmaster0107/GITHUB_FINAL_RELEASE.py`

Beide Dateien stammen byte-identisch aus dem vorqualifizierten 4A-Head. Sie entfernen die feste 7er-Kardinalität hinter 107008 und verlangen stattdessen den tatsächlich gebundenen Artikelcount `>=1`, ohne Artikelbytes, Signaturmodell oder Publish-Sperre zu lockern.

Auf exakt `5329f1a0b1216527481db3173bb0c2076ebd9805`:
- `hardlock` Run `35111115856`: PASS;
- `hardlock-base` Run `35111115922`: PASS.

PR #266 aktiviert 1..N nicht selbst. Er ändert weder 107008 noch State.

### PR #265 — einzige geschützte Admin-Änderung

Branch: `admin/system4a-endstempel-1n-workflow-20260916`
Head: `36f4deff41dcd054c8f46ce93d04eeb07e6ac0d1`

Exakt eine Datei:
- `.github/workflows/pferde-atelier-endstempel.yml`

Änderung:
- feste `article_count == 7`-Prüfungen werden durch integer `article_count >= 1` ersetzt;
- unabhängige Verifikation verlangt weiterhin exakt `len(articles) == article_count`;
- Ed25519-Signatur, Schlüsselidentität, Hash-/Byteprüfung, Replay-Sperre und `publish_allowed=false` bleiben unverändert.

Auf exakt `36f4deff41dcd054c8f46ce93d04eeb07e6ac0d1`:
- `hardlock` Run `35110876007`: PASS;
- `hardlock-base` Run `35110875848`: FAIL erwartungsgemäß ausschließlich am Immutable-Path-Guard, weil `.github/workflows/**` absichtlich geschützt ist.

Aktiver Ruleset `Pferde Atelier Main Hardlock` verlangt `hardlock` und `hardlock-base`; aktuell existiert kein Bypass-Akteur. Die verbundene GitHub-Schnittstelle besitzt keinen Ruleset-/Admin-Schreibweg. PR #265 ist deshalb ein echter externer Repository-Admin-Blocker. Der Hardlock darf nicht abgeschwächt werden, um den Kandidaten künstlich grün zu machen.

## 107008 / State-Bindung

Der aktuelle 107007-Bundle bindet 107008 bereits als zulässigen nächsten Schritt. Der heutige 107008-Bundle ist jedoch noch 7-Artikel-spezifisch. Eine 1..N-Änderung verändert dessen Hash.

Das Repository besitzt mit `STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py::refresh()` bereits die etablierte Hashkaskade:
107008 -> 107007 `next_binding.bundle_sha256` -> 107007-Bundlehash im `CURRENT_STATE` -> `CURRENT_STATE`-Hash im `PFERDE_ATELIER_START_HERE` -> Entry-Hash im Root-Pointer.

Diese Kaskade darf hier trotzdem nicht eigenständig ausgeführt oder manuell nachgebaut werden: `AGENTS.md` bindet State-Schreibautorität an `ENTRANCE_GATE_ONLY` und verbietet eigenständige State-/Workflowänderungen. Daher bleibt die 107008-Rebinding-Stufe offen, bis die autorisierte Eingangstür genau diesen Übergang bindet.

## Historischer Kandidat

PR #262 wurde als aktiver Merge-Weg geschlossen und bleibt nur Historienbeleg. Er wurde nicht gemergt und nicht veröffentlicht.

## Aktuell einziger zulässiger Fortgang

1. PR #264 auf seinem jeweils aktuellen exakten Head erneut über `hardlock` und `hardlock-base` beweisen; nicht automatisch mergen.
2. PR #266 bleibt separat mit beiden Hardlocks PASS; nicht automatisch mergen.
3. PR #265 bleibt Admin-only und BLOCKED, bis die geschützte Workflow-Änderung ausdrücklich repository-administrativ autorisiert werden kann.
4. Danach darf die 107008-Änderung ausschließlich über die autorisierte Entrance-/Prebinding-Strecke neu gebunden werden; keine manuelle State-/Hash-Manipulation.
5. Erst auf kanonischem, main-gebundenem Stand darf der echte Abschluss 107008 -> PSERC -> GitHub ENDSTEMPEL -> WordPress-Importformatprüfung -> byte-identische Parent-Chat-Datei laufen.

Keine Veröffentlichung, keine Artikelmutation, keine Hardlock-Abschwächung.

`publish_allowed=false`
