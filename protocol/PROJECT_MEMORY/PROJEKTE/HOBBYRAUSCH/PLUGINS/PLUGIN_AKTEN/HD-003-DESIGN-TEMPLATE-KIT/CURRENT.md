# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.626 CRITICAL-HOTFIX LOCAL HARD PASS / LIVE-PASS OFFEN**

Version:
**1.50.626**

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.626_HOBBY_DEPOT_CRITICAL_CLASS_BINDING_HOTFIX_LOCALPASS.zip`

SHA-256:
`74cd55b87a608287ff4f4d7d3d7f3f80aa84dd478b8f675ab136e297064a54ea`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.626_HOBBY_DEPOT_CRITICAL_CLASS_BINDING_HOTFIX_LOCALPASS.zip`

## Root Cause
1.50.625 Front-/Contenttemplates riefen irrtümlich die entfernte Klasse `Hobby_Depot_Profile_V150624` auf.

## Fix
- Main require v150626;
- Klasse V150626;
- Fronttemplate v150626 → V150626;
- Contenttemplate v150626 → V150626;
- Router v150626;
- kein Designrollback.

## Lokal
- PHP 10/10 PASS;
- ZIP PASS;
- Klassenreferenzintegrität PASS;
- Templatebinding PASS;
- stale V150624/V150625 active PHP refs = 0.

## EXAKT EINE NEXT ACTION
**1.50.626 installieren und nur prüfen: lädt die Seite wieder ohne Critical Error?**
