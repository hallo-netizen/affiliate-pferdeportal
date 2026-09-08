# P3 – ECHTE PPM/PSERC-SCHNITTSTELLENPROBE

Datum: 2026-09-08
Status: GO, ECHTE PAKET-/SCHNITTSTELLENPROBE PASS, NOCH KEIN ECHTER ARTIKELLAUF

## Laborisolation

Für den Binärzugriff wurde ausschließlich ein separater wegwerfbarer GitHub-Labor-Basisbranch verwendet:
`alternative/seo-text-central-machine-lab-base-20260908`

Dieser Runner ist Testinfrastruktur, NICHT Teil der Architektur und NICHT für main vorgesehen.

Draft-PR nur gegen den Laborbranch: #162.
Kein PR/Commit nach main.

## Lauf 1 – korrekt geblockt

Der erste echte Laborlauf stoppte bereits in der P0-P2-Regression.

Ursache:
Der im Prototyp fest eingetragene SHA-256 des eingefrorenen P2-Stubs war falsch.

Folge:
`TEXTMACHINE_IDENTITY_MISMATCH`

Bewertung:
POSITIVER Sicherheitsbefund. Die Maschine akzeptierte den nicht exakt gebundenen Maschinenstand nicht.

KISS-Fix:
nur den falschen SHA korrigiert, keine Architekturänderung.

## Lauf 2 – PASS

P0-P2 Regression:
12/12 PASS.

P3 echte Pakete:
PASS.

Bewiesen:
- PPM 6.7.9 ZIP exakt SHA-256
  `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- PSERC ZIP exakt SHA-256
  `77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314`
- realer PSERC Bridge vorhanden
- reale PPM Pipeline vorhanden
- PHP-Syntax der echten Eintrittsdateien PASS
- reale Eintrittsstelle:
  `PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan`
- Ein-Byte-Paketmanipulation -> BLOCKED
- keine Änderung der Textmaschine
- kein Publish
- für diese Schnittstellenprobe kein neuer produktiver Handoff erforderlich

## Gegenprüfung

### 0,0 Freiheit
PASS für P3.
Die reale Engineidentität ist paket-/hashgebunden und nicht durch Worker-/Chatwahl ersetzt.

### Einfluss von außen
PASS für geprüfte Paketidentität.
Paketdrift wird fail-closed geblockt.

### KISS
PASS.
P3 fügt der Architektur keine Komponente hinzu.
Der GitHub-Laborrunner ist nur externe Testinfrastruktur.

### Nachhaltigkeit
PASS als Schnittstellenprinzip.
Die bestehende reale Produktionskomponente kann als unveränderliche Einheit geprüft werden, statt intern nachgebaut zu werden.

### Themenunabhängigkeit / Batch / Automatisierung
P0-P2 bleiben PASS.
P3 verändert diese Architektur nicht.

### Weniger Fehleranfälligkeit
VORLÄUFIG PASS.
Die echte PPM-Schnittstelle kann über eine einzige gebundene Eintrittsstelle identifiziert werden.

## GO/STOP

GO zu P4.

P4 darf nur:
- eine vorhandene mitgelieferte PPM-Test-Fixture identifizieren,
- danach genau einen echten No-Publish-Testlauf ausführen.

Keine künstlichen Produktionsdaten erfinden.
Keine WordPress-Schreibaktion.
Keine neue Workflow-/Handoff-Schicht.

Wenn der echte Lauf nur durch neue Sonderarchitektur möglich wäre:
STOP.
