# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – READ_ONLY CORRIDOR / FIX_FORBIDDEN**

## EINZIGE ARBEITSWAHRHEIT

Aktueller Stand:
`CURRENT_STATE.md`

Autoritative aktuelle Fehlerquelle:
`QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md`

Technischer Corridor:
- `TECHNICAL_CORRIDOR_ROOTCAUSE_20260907.md`
- `TECHNICAL_CORRIDOR_MATRIX_20260907.md`

Ziel:
`QUELLEN_AKTUELL/03_ZIELVERTRAG_AKTUELL_20260905.md`

WARUM:
`protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

## CURRENT MAIN / DISPATCHER

`main = 93ba987c56f7b08ffba009210e3012c036fec18d`

`codex-chat-launcher = 93ba987c56f7b08ffba009210e3012c036fec18d`

PR #107:
permanenter Dispatcher / offen / niemals mergen.

## AKTUELLE ARBEIT

**Kein Produktfix. Kein Realtest. Nur read-only Corridor-Arbeit.**

Current State bindet:
- B16 als aktuellen Liveblocker;
- `FIX_FORBIDDEN`;
- keinen Produktkandidaten;
- zwei offene bestehende Autoritätslücken:
  1. NEW-Link-Provenienz;
  2. `design_format`-Evidence-Semantik.

Der sichtbare LanguageTool-Stop wird nicht separat repariert.

## NEXT ACTION

**Genau eine Frage read-only schließen:**

Existiert bereits eine unveränderte autoritative Fachworkflow-Quelle außerhalb des aktuell gebundenen STARTMASTER-Pfads, die für NEW

1. die drei artikelbezogenen Linkbindungen deterministisch erzeugt und
2. die bestehende Bedeutung/Evidence von `design_format` eindeutig definiert?

Arbeitsweg:
1. nur vorhandene aktuelle/originale Quellen lesen;
2. keine historischen Produktionspläne als Produktionsquelle verwenden;
3. keine neue Linklogik;
4. keine neue Designregel;
5. keine neue Stage;
6. keinen neuen Executor/Runner/Workflow bauen.

Wenn beide vorhandenen Autoritäten gefunden werden:
- Corridor-Matrix aktualisieren;
- B16 zuerst als fortlaufende ausführbare History-Regression aufnehmen;
- danach genau einen konsolidierten KISS-Kandidaten;
- Positiv/Negativ/Invarianten;
- erst danach neuer Realtest.

Wenn eine Autorität nicht existiert:
**STATUS → BLOCKED dokumentieren. Kein Ersatzweg.**

## KEIN AKTIVER KANDIDAT

CANDIDATE_BRANCH: NONE  
CANDIDATE_HEAD_SHA: NONE  
INTEGRATION_ALLOWED: false

Der geparkte LT-Branch
`hobbyroom/languagetool-runtime-rebind-20260907`
ist nur historische Beweisquelle und kein Integrationskandidat.

## PARALLELBRANCH

Alternative:
`alternative/seo-text-central-machine-20260908`

Fresh Head:
`b3cdf639fc8bd40e7c3c044fce03f88bb3508472`

PR #195:
offen / Draft / isoliert.

Aus diesem Originalweg:
- nicht verändern;
- nicht mergen;
- keine Statuswahrheit übernehmen.

## NICHT ANFASSEN

- SEO-5-Felder-Handoff;
- Textmaschine/Fachregeln;
- Tabellen-/Link-/LanguageTool-/Designregeln;
- PPM/PSERC/PSTE-Regeln;
- Single Door;
- Publish-Grenze;
- WordPress;
- PR #107 mergen;
- PR #195 verändern;
- historische Artikel/Pläne als NEW-Produktionsquelle.

## AUTORITATIVE BLOB-BINDUNGEN

CURRENT_STATE:
`accd8010443fdb99eeab2ebd47d85a43c8b845ca`

Fehlerquelle:
`12f49603118c7448c436ec97e85be41bddf80d7f`

Protokoll:
`c5b0bef4424be6c572364b7e6eacfaaf1b816f79`

Änderungsregister:
`0cf9e1eb3744add9e79f1eab5b19fc8892945b04`

Hobbyraum-Standard:
`8c90de4920ec81e10f3952bbd52208fad5a42367`

Corridor-Matrix:
`5d19d5a0c2b56533f1a47cab349ad768ec1e6663`

Corridor-Rootcause:
`93fe9ac6df12faef654dfdba5e08f35f83362b94`

Paul:
`08fee3940a8f693ac6bb505df2e083b8515e2dd9`

Zielvertrag:
`9150da14699e319381f9119cebfcee90233c3521`

## SCHUTZ

Ruleset:
`Pferde Atelier Main Hardlock`

- active;
- required: `hardlock`, `hardlock-base`;
- bypass: leer;
- current user bypass: never.

Kein Publish.
