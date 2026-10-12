# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.626 CRITICAL-HOTFIX LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.626_HOBBY_DEPOT_CRITICAL_CLASS_BINDING_HOTFIX_LOCALPASS.zip`

SHA-256:
`74cd55b87a608287ff4f4d7d3d7f3f80aa84dd478b8f675ab136e297064a54ea`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.626_HOBBY_DEPOT_CRITICAL_CLASS_BINDING_HOTFIX_LOCALPASS.zip`

## Exakte Ursache des kritischen Fehlers in 1.50.625

Nicht geraten, im ZIP direkt gefunden:

Die beiden aktiven v150625-Templates riefen weiterhin die **entfernte Klasse**
`Hobby_Depot_Profile_V150624` auf.

Betroffen:
- `templates/hobby-depot-front-v150625.php`
- `templates/hobby-depot-content-v150625.php`

Die 1.50.625-Klasse hieß aber:
`Hobby_Depot_Profile_V150625`

Damit entstand beim Templateaufruf ein fataler Klassenfehler.

## Fix 1.50.626

- neue aktive Klasse `Hobby_Depot_Profile_V150626`;
- main plugin require → v150626;
- Router → v150626 Front-/Contenttemplate;
- beide Templates → ausschließlich `Hobby_Depot_Profile_V150626`;
- keine alten V150624/V150625-Klassenreferenzen mehr in aktivem PHP;
- Design/Bilder/Navigation/Monetarisierung von 1.50.625 unverändert übernommen.

## Fresh Hardtest

- PHP **10/10 PASS**;
- ZIP-Integrität PASS;
- deklarierte Hobby-Klasse: nur `Hobby_Depot_Profile_V150626`;
- alle aktiven Template-/Main-Referenzen auf genau diese Klasse;
- fehlende Klassenreferenzen: **0**;
- Binding-Assertions PASS.

## EXAKT EINE NEXT ACTION

**1.50.626 installieren. Erst prüfen, ob die Seite wieder ohne Critical Error lädt.**
