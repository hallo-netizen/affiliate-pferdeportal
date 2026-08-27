# V6.61.10 FAIL – Codex-Handoff

Stand: 27.08.2026

## Live-Status
V6.61.10 ist **FAIL**. Der Live-Screenshot `Reithelme` zeigt eine massive neue Leerfläche zwischen Produktbereich-Header/Disclosure und den drei Produktkarten. Die Korrektur darf nicht als LIVE PASS bezeichnet werden.

## Nachgewiesene Änderung V6.61.8 -> V6.61.10
Die Layoutänderung betrifft `assets/frontend.css` und Inline-Geometrie in `pferdeportal-affiliate-router.php` (zzgl. Versionsnummer). V6.61.10 ersetzt die frühere feste Geometrie durch breite `grid-auto-rows:1fr`-/`height:100%`-/`minmax(0,1fr)`-Regeln über mehrere Produktgrids und Wrapper. Diese Änderung ist Hauptverdacht für die neue vertikale Aufblähung und muss in Codex mit realer Cascade/Computed Geometry bewiesen werden.

## Codex-Paket
Lokales Handoff-Paket: `CODEX_AFFILIATE_EQUAL_CARD_ROOTCAUSE_V6610_20260827.zip`

SHA-256: `684e3eab3d67946ec11ee455155904ed9941e57afe5715d914cf14ed2cd0341a`

Enthalten:
- kompletter CURRENT-V6.61.10-Quellcode,
- kompletter V6.61.8-Baseline-Quellcode,
- Full-Diff V6.61.8 -> V6.61.10,
- Live-FAIL-Screenshot V6.61.10,
- Baseline-Screenshot V6.61.8,
- bisherige lokale V6.61.10-Testreports,
- Read-only Design/CSS-Kontext,
- fertiger `CODEX_TASK_PROMPT.txt`.

## Verbindliche Abnahme
Ein weiterer Installer darf erst empfohlen werden, wenn Codex bzw. die lokale Nachprüfung beide Seiten des Gates belegt:
1. NEGATIV: aktueller V6.61.10-Fehler reproduziert und ursächlich erklärt.
2. POSITIV: drei providerneutrale Karten gleich hoch, 150x150 Bilder, Buttons gleiche Baseline **und** keine zusätzliche vertikale Leerfläche gegenüber der normalen Baseline.

Provider-, Feed-, Ranking-, eBay-/idealo-Runtime und Designplugin bleiben unverändert, sofern nicht ein zwingender Gegenbeweis vorliegt.