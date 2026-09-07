# DESIGN – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / KANDIDAT BEREIT

## AKTUELLER BEFUND

- V1.50.473: REJECTED / FAIL.
- V1.50.474: REJECTED / FAIL – Artikel fälschlich intern aufgeteilt.
- Beide Kandidaten bleiben gesperrt.

## AKTUELLER AUFTRAG

**Nur Elementtausch. Keine Artikelzerlegung.**

V1.50.475 wurde frisch aus dem exakten bestätigten V1.50.472-Vorgänger gebaut.

Zentrale Reihenfolge:
1. Unterkategorie-/Beitragsart-Verweise;
2. vollständiger bestehender Artikelblock;
3. Beitragsvorschau / meistgelesene Beiträge;
4. Partnerbanner;
5. Produkte;
6. Direktwerbeplatz.

## HARTE REGEL

Der Artikelblock selbst wird **nicht geparst, nicht geteilt, nicht neu zusammengesetzt und nicht umgestaltet**.
Er wird nur als vollständiger bestehender Block verschoben.

## KANDIDAT

Branch:
`fix/category-content-order-v150475-20260907`

Beleg:
`design-baseline/2026-09-07/v150475-category-content-order/`

Installer:
`PFERDE_ATELIER_DESIGN_V1.50.475_CONTRACT_V104_NUR_ELEMENTTAUSCH_HARD_LOCAL_INSTALLIEREN.zip`

ZIP SHA-256:
`ab6f3f820b01f1043d74200b031560695757db8395a2910c18264c40f34aa689`

PHP SHA-256:
`0151b5d66132675795c982b8a0c4ca0326ead9419f9e8ba882d751240a75b40c`

## HARD LOCAL

POSITIV:
- Basis exakt V1.50.472: PASS
- nur eine Paketdatei verändert: PASS
- V104 byte-identisch: PASS
- Kategorie-CSS byte-identisch: PASS
- Artikelblock vollständig/unverändert: PASS
- Zielreihenfolge: PASS
- PHP-Lint/ZIP-Integrität: PASS

NEGATIV:
- Artikel vor Verweise zurückverschoben: BLOCKED / PASS
- Banner vor Beitragsvorschau zurückverschoben: BLOCKED / PASS
- Artikel dupliziert: erkannt / PASS
- fremde Paketdatei verändert: erkannt / PASS

## NEXT ACTION

Nur V1.50.475 installieren und die reale Seite prüfen.
Bis dahin: kein LIVE-PASS, kein Merge, keine weitere Paralleländerung.

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
