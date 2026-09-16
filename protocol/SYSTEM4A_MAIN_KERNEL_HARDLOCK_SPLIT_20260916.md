# System 4A — Main-Kernel / Hardlock-Split

Stand: 2026-09-16
Status: KERNEL_PREQUALIFIED / PROTECTED_CLOSEOUT_BLOCKED

## Ausgangslage

Der vollständig vorqualifizierte System-4A-Stand liegt auf `531a40bedf6f4bd9c709d1ad36d4c46db966c166`. Zuvor wurde aktuelles `main` (`9cdb171343794f609b6cca36329774c2289b5cd6`) über PR #263 in den 4A-Testbranch eingebunden.

Auf genau diesem Head sind erfolgreich:

- System 4A Real LT68 PPM679 Acceptance, Run `35105842734`, alle 37 Schritte PASS;
- System 4A Repair Owner Contract, Run `35105842615`, PASS;
- System 4A Exact Head Bundle, Run `35105842657`, PASS;
- kompletter 1-Artikel-Weg;
- kompletter 3-Artikel-Weg mit isoliertem Repair;
- 1..N-Handoff-Prüfung.

Der Status bleibt ausdrücklich Branch-Vorqualifikation, nicht Gesamt-PASS.

## KISS-Trennung

Der getestete Stand wurde in zwei Verantwortungsbereiche getrennt.

### A — normaler System-4-Kern

Draft-PR #264 basiert direkt auf aktuellem `main` und übernimmt den getesteten `isolated_system4/**`-Baum. Keine STARTMASTER-, ENDSTEMPEL-, Workflow-, Release-, Plugin- oder Publish-Änderung wird dort übernommen.

Der Immutable Base Hardlock (`hardlock-base`) ist auf diesem Kandidaten PASS.

### B — geschützter Abschluss

Draft-PR #262 bleibt ausschließlich Beleg/Kandidat für die geschützte Abschlussstrecke 107008 -> PSERC -> GitHub ENDSTEMPEL -> WordPress-Importformat -> byte-identische Parent-Chat-Datei.

Er ist nicht als Merge-Weg freigegeben.

## Bewiesene Schutzblocker

1. `Pferde Atelier Immutable Base Hardlock` blockiert Änderungen an `.github/workflows/**` und `control/startmaster0107/ENDSTEMPEL_*` mit `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
2. Der Deterministic Entrance Gate blockiert den geänderten 107008-Bundle-Stand mit `NEXT_BUNDLE_HASH_MISMATCH`; ein neuer Bundle-Hash darf nicht außerhalb der vorgebundenen State-Autorität eingeführt werden.
3. Der aktive Main-Ruleset verlangt `hardlock` und `hardlock-base` und hat aktuell keinen Bypass-Akteur.
4. Der `hardlock`-Workflow wird auf Pull Requests nur für definierte Pfade ausgelöst; `isolated_system4/**` gehört nicht zu diesen Pfaden. Ein rein isolierter System-4-Kernel kann deshalb den verpflichtenden `hardlock`-Kontext nicht selbst erzeugen.

Dieser Protokolleintrag dokumentiert genau diesen realen Integrationsbefund und ist keine Ersatzprüfung oder Freigabe.

## Nächster zulässiger Weg

- PR #264: nur main-kompatiblen Kernel und diese Befunddokumentation prüfen; kein Publish. Ein Merge erfolgt nicht aus diesem Protokoll heraus.
- PR #262: nicht mergen; geschützte Abschlussänderungen bleiben BLOCKED, bis eine ausdrücklich autorisierte Governance-/Prebinding-Strecke die 1..N-ENDSTEMPEL-/107008-Änderung zulässig macht.
- Keine Abschwächung von Hardlock, Signatur, 107008 oder `publish_allowed=false`.
- Kein künstlicher PASS und kein manueller State-/Bundle-Hash-Umbau.

`publish_allowed=false`
