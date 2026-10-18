# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.688 LIVE / 1.50.689 DELTA-UPDATER GEBAUT + ZIP/PHP/HARD-ASSERTIONS PASS / WORDPRESS-READBACK OFFEN**

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.687_CATEGORY_LEVEL_ROLLOUT_ICONS_DUMMY_POSTS.zip`

SHA-256:
`9a881f3b3b7cf25ab2cfdc5f9a2c62b878fa5cc7513ba8678524f98b7464235b`

## Scope

Vom abgenommenen Kettenhemdflechten-Pilot auf die komplette gleiche logische Ebene:
- 379 Page-Knoten;
- 16 direkte Category-Term-Knoten;
- 395 Detail-Hubs insgesamt;
- 2.979 letzte Kategorien unter den Page-Knoten.

Darstellung:
- kein Hero;
- Icon + H1 + 150–200-Wörter-Text;
- 45–62 Wörter sichtbar;
- 4/2/1-Kartenraster;
- Produkte nach der ersten 4er-Reihe;
- Banner nach dem restlichen Kategorienblock;
- bis zu 4 Beitragsvorschauen;
- bestehender weiterer Werbeplatz danach.

## Zentrale Icons

Semantische, portalweite Registry für die letzte Kategorieebene.
FAQ, Vergleich/Kaufberatung, Grundlagen, Ausrüstung usw. erhalten überall dieselbe Rollen-Iconbindung.
Kein Zufalls-/Hash-Icon.

## Kettenhemd-Dummybeiträge

4 veröffentlichte Testbeiträge mit:
- passender Unterkategorie;
- Featured Image;
- idempotentem Seeder;
- realer 4er-Beitragsvorschau.

## QA

- PHP 105/105 PASS;
- V150687 Front-/Contentroute PASS;
- Templates positiv PASS;
- Negativtest V150686 PASS;
- Kettenhemd-Render PASS;
- 395/395 Copy-Coverage;
- Textumfang 150–170 Wörter;
- Leads 45–62 Wörter;
- 395 unterschiedliche Texte;
- 4/4 Dummy-Posts, Kategorien und Bilder;
- Seeder idempotent PASS;
- Postpreview Limit 4 PASS;
- Delta zu 1.50.686: 1 geändert / 4 neu / 0 entfernt;
- Dirty Overlay PASS;
- ZIP PASS;
- Roundtrip 1146/1146 PASS.

## EXAKT EINE NEXT ACTION

**1.50.687 installieren und Kettenhemdflechten plus zwei weitere Seiten derselben Ebene real lesen.**


## Kandidat 1.50.688

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.688_KETTENHEMD_CARD_REFINEMENT.zip`

SHA-256:
`a57ba6a8ec158191276673d309825787cfc0ec6d0c192bed358a97e193cac843`

Scope:
- Kettenhemd-H1 sichtbar als `Kettenhemd` + `flechten`;
- Kettenhemd-Karten größer/deutlicher, aber dezent;
- Untertitel stark gekürzt;
- FAQ-Frontendtitel gekürzt;
- Detail-Level-Produkttitel neutral `Empfehlungen`;
- Detail-Level-Kachelüberschrift ohne H1-Dopplung;
- zentrale Großschreibungsregel für sichtbare Kurztexte;
- Meta-Titel unverändert.

QA:
- PHP 108/108 PASS;
- reale V150688-Route PASS;
- Templates positiv PASS;
- V150687-Negativtest PASS;
- Renderassertions PASS;
- Delta 1 geändert / 3 neu / 0 entfernt;
- ZIP PASS;
- Roundtrip 1149/1149 PASS.

## EXAKT EINE NEXT ACTION

**1.50.688 installieren und Kettenhemd-Seite visuell abnehmen.**


## Kandidat 1.50.689

`HOBBY_DEPOT_TEMPLATE_KIT_UPDATE_1.50.689.zip`

Scope nur Kettenhemd:
- H1 `Kettenhemd flechten` einzeilig;
- Banner direkt unter Intro;
- 8 Kacheln ohne Affiliate-Unterbrechung;
- Empfehlungen/Produkte unter allen Kacheln;
- passende Beiträge danach;
- Meta-Titel, Slug, URL, Hub2 und andere Detail-Hubs unverändert.

Auslieferung:
- fail-closed Delta-Updater für exakt 1.50.688;
- Backup vor Schreibzugriff;
- neue V150689-Dateien zuerst;
- Main-Umschaltung zuletzt;
- Readback im Updater;
- Updater deaktiviert sich nach erfolgreicher Anwendung.

QA:
- ZIP integrity PASS;
- PHP lint PASS;
- hard assertions PASS;
- GitHub Actions Run 39139756377 SUCCESS.

## EXAKT EINE NEXT ACTION

**1.50.689 Delta installieren/aktivieren und Kettenhemd frontendseitig abnehmen.**
