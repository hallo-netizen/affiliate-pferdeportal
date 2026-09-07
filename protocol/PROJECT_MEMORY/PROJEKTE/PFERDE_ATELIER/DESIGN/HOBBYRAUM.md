# DESIGN – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / KANDIDAT BEREIT

## 1-KLICK-ÜBERSICHT

**AKTUELLER BEFUND**  
V1.50.473 ist nach realer Nutzerprüfung **REJECTED / FAIL** und bleibt gesperrt.

**NEUER KANDIDAT**  
V1.50.474 wurde **frisch aus dem exakten archivierten V1.50.472-Vorgänger** gebaut, nicht aus V1.50.473.

**ALS NÄCHSTES – EINZIGE AKTION**  
V1.50.474 installieren und auf „Gebisse“ prüfen. Danach mindestens eine zweite Kategorie derselben Ebene gegenprüfen.

## ZIELREIHENFOLGE

1. H1 + kurzer bestehender Lead;
2. Unterkategorie-/Beitragsart-Verweise;
3. bestehende Artikel-Fortsetzung;
4. Beitragsvorschau / meistgelesene Beiträge;
5. Partnerbanner;
6. Produkte;
7. Direktwerbeplatz.

## KANDIDAT

Branch:
`fix/category-content-order-v150474-20260907`

Beleg:
`design-baseline/2026-09-07/v150474-category-content-order/`

Installer:
`PFERDE_ATELIER_DESIGN_V1.50.474_CONTRACT_V104_KATEGORIE_REIHENFOLGE_HARD_LOCAL_INSTALLIEREN.zip`

ZIP SHA-256:
`71e0f88cd2181e55f5dde75d8e94f4ba4439cfd5ea2fc76406edf71b979f9f2e`

PHP SHA-256:
`283afddad9cf64eefe2e3a3176e0ec674ad19b6d0672abcd04a0f540e2c0b50d`

## HARD LOCAL QA

- exakter V1.50.472-Basishash: PASS
- 498/498 Paketdateien vorhanden: PASS
- außerhalb `pferde-template-kit.php` keine Datei verändert: PASS
- V104 allgemein/Pferde byte-identisch: PASS
- zentrales Kategorie-CSS byte-identisch: PASS
- PHP-Lint: PASS
- Intro-Split Positiv/Negativ: PASS
- gewünschte Blockreihenfolge: PASS
- Negativtest falsche Reihenfolge: BLOCKED / PASS
- Negativtest fremde Paketdatei verändert: BLOCKED / PASS
- ZIP-Readback 498/498 byte-identisch: PASS

## HARTE GRENZE

Bis zur Nutzerprüfung:
- **kein LIVE-PASS** für V1.50.474;
- kein main-Merge;
- V1.50.473 nicht wiederverwenden;
- keine weitere Designänderung parallel.

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum/Änderungen: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie: `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`
