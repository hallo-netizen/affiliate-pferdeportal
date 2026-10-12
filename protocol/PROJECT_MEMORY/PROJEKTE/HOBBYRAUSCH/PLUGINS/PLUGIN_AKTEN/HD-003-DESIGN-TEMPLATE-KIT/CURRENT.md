# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.647 LOCAL HARD PASS / LIVE-PASS OFFEN**

Version:
**1.50.647**

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.647_HOBBY_DEPOT_HUB2_RELEASE_CHAIN_FATAL_FIX_LOCALPASS.zip`

SHA-256:
`db5427357bd251f084ab9a8545dee33d760a7b38ace686a5146543ca07210833`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.647_HOBBY_DEPOT_HUB2_RELEASE_CHAIN_FATAL_FIX_LOCALPASS.zip`

## Root Cause 1.50.646
Aktives V150646-Profil zeigte noch auf v150645-Templates; diese riefen die nicht geladene V150645-Klasse auf. Runtime-Fatal.

## Fix
Komplette aktive Release-Kette auf V150647 vereinheitlicht.

## Lokal
- PHP 53/53 PASS;
- ZIP PASS;
- aktive Release-Bindung end-to-end PASS;
- aktive V150645/V150646-Klassenreferenzen 0;
- Hub2-Rollout aus 1.50.646 fachlich unverändert enthalten.

## EXAKT EINE NEXT ACTION
**1.50.647 installieren und live prüfen.**
