# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-09-11
STATUS: BLOCKED / M37 HISTORY→PRODUCT TWO-PHASE ACTIVE

## EINE AKTUELLE WAHRHEIT

Current technical main:
`a2f2f1b4b7af1e905c6a0cb69c5389664b7c4ad6`

Letzter belastbarer Live-/Recovery-Baseline-Stand:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Aktuelle autoritative Fehlerquelle:
`QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md`

Vorgänger `QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md` ist nur historische Langfassung und keine CURRENT-Wahrheit mehr.

## AKTUELLER REALBLOCKER

Der letzte frische Lauf recherchierte und erzeugte den ersten Artikel und erreichte den echten PPM-6.7.9-/PSERC-Handoff.
Sichtbarer äußerer Stop:

`PPM679_REAL_EXECUTION_BLOCKED`

Der konkrete bereits vorhandene innere Bridge-Grund wurde vom äußeren Handoff nicht sichtbar erhalten. Der ursprüngliche Codex-Task ist nicht mehr verfügbar.

**Produktions-Rootcause bleibt UNKNOWN.**
Nicht raten und keinen PPM-/PSERC-Fehler erfinden.

## AKTIVE REGRESSION

M01–M36: integrierte bekannte Regression.

M37:
`Non-repairable PPM/PSERC inner reason visibility`

Der vorhandene `hardlock-base` erzwingt dafür den bestehenden Zwei-Phasen-Weg:
1. `HISTORY_AUTHORITY_MAINTENANCE`: nur Matrix + bestehender Runner; unverändertes Main muss bei M37 reproduzierbar FAIL sein.
2. `PRODUCT_FIX`: erst nach integrierter M37-History; Handoff-Fix separat; current main M37 FAIL → Kandidat kompletter M01–M37 PASS.

## AKTUELLE KANDIDATEN

History-Autorität:
- Branch: `hobbyroom/m37-history-authority-20260911`
- Head: `245b596f9d6dd67c759527a0f211dbe957f4e34f`
- Scope: ausschließlich bestehende Matrix + bestehender Runner.
- Sollbeweis: Kandidat reproduziert M37 als ersten FAIL; kein Produktfix in diesem Kandidaten.

Produktfix-Vorarbeit:
- PR247 / Branch `hobbyroom/ppm-inner-reason-visibility-20260911`
- Head vor Trennung: `d4e6d77afdb68bbb3b6759b21d159293a9e49273`
- Dort ist M37 lokal Positiv/Negativ PASS und hardlock/hardlock-base technisch PASS, aber der PR mischt History-Autorität + Produktfix und darf deshalb in dieser Form nicht integriert werden.
- Produktfix wird erst nach integrierter M37-History sauber neu auf aktuelles Main gebunden.

## HARTE GRENZEN

- kein neuer Runner;
- kein neuer Gate/Controller/Sidecar;
- keine PPM-/PSERC-/PSTE-/Textmaschinen-/Recherche-/SEO-/Link-/Tabellen-/Designregel ändern;
- kein Fake-Rootcause;
- keine Reparatur während des Produktionslaufs;
- kein WordPress-Write;
- Kein Publish.

## NÄCHSTE AKTION

History-Phase M37 maschinengebunden über bestehenden `hardlock-base` beweisen und integrieren.
Danach separaten M37-Produktfix auf das neue Main binden und M01–M37 vollständig beweisen.
Erst danach genau einen frischen ersten Artikel bis zum echten PPM/PSERC-Handoff laufen lassen, um den realen inneren Rootcause sichtbar zu erhalten.
