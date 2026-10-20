# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.704 HOBBYFINDER RUNTIME LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.704_HOBBYFINDER_RUNTIME_LOCALPASS.zip`

Library:
`/Hobby Depot/Plugin-Büro/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.704_HOBBYFINDER_RUNTIME_LOCALPASS.zip`

SHA-256:
`558ed2a17cd5123cdad5c7719d2554d64e413f628f29a07a1d06e6b4dca476fc`

Größe:
58,681,497 Bytes.

## Basis

- direkte Basis: 1.50.703;
- stabile Klasse bleibt `Hobby_Depot_Profile_V150699`;
- keine Template-/Klassenumbenennung;
- Footer-/Serviceseitenfix 1.50.703 bleibt unverändert;
- Kategorie-/Bild-/Affiliate-/SEO-Struktur unverändert.

## Finder-Vertrag

- Slug `hobbyfinder` = eigener HD-003-Content-Route;
- Datensätze ausschließlich über HD-007 read-only API;
- keine persistente Hobbykopie in HD-003;
- exakt 862 Datensätze erforderlich, sonst fail-closed;
- echte Zielobjekte ausschließlich über HD-004 `hd_category_registry_resolve()`;
- keine erfundenen Ziel-URLs;
- Ergebnis-Karte: Passungswert + Gründe + Was ist das? + Was macht man? + Was braucht man? + Der Reiz.

## Lokale QA

- PHP 135/135 PASS;
- Diff gegen 1.50.703: exakt 3 Dateien;
- Runtime 862/862 PASS;
- Profile 862/862 PASS;
- Route PASS;
- fehlendes HD-007 fail-closed PASS;
- gerendertes JavaScript Syntax PASS;
- ZIP PASS.

## ERSTER OFFENER BLOCKER

Echter WordPress-Readback mit aktivem HD-007.

## EXAKT EINE NEXT ACTION

**HD-007 1.0.0 aktivieren, danach HD-003 1.50.704 installieren und den Hobbyfinder real positiv/negativ prüfen.**
