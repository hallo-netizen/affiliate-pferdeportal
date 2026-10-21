# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.50.710 FOOTER EXAKTER AKTIVER RENDERER KORRIGIERT / LIVE OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.710_FOOTER_REALFIX_EXACT_RENDER.zip`

SHA-256:
`cbb321ff0c766cbef16bd362f767dcc799cbb27b1a0cc4ee7156b7c53f4cd807`

Größe:
58,829,071 Bytes.

## Bewiesener Stand

1.50.709 hat live bereits strukturell gegriffen:
- weiße Zusatzzeile weg;
- unterer Abstand weg;
- Copyright im dunklen Footer vorhanden.

Damit ist HD-003 der aktive sichtbare Footer-Renderer.

## Fehler im aktiven Renderer

- Originallogo wurde durch `filter:brightness(0) invert(1)` weiß reduziert;
- Links 14 px / Überschriften 15 px / Claim 13.5 px;
- Negativtest bewies: Hobbyfinder konnte über importiertes Informationen-Menü wieder auftauchen.

## 1.50.710

- V150710 aktiver Runtimepfad;
- Originallogo farbig, kein Weißfilter;
- Logo 215 px;
- Claim 14.5 px;
- Überschriften 16.5 px;
- Links 16 px;
- Hobbyfinder, Anbieter und Zeit/Budget explizit aus importiertem Info-Menü ausgeschlossen;
- dunkle Farbwelt unverändert;
- Copyright bleibt;
- HD-001-Autofooter bleibt deaktiviert.

## Tests

- negativer Render mit absichtlich eingeschleustem Hobbyfinder/Anbieter/Zeit-Budget: alle 0 Treffer PASS;
- Magazin bleibt PASS;
- Footer exakt einmal PASS;
- PHP 138/138 PASS;
- Main-Router ausschließlich V150710 PASS;
- ZIP PASS.

## EXAKT EINE NEXT ACTION

**1.50.710 installieren und Footer live prüfen.**
