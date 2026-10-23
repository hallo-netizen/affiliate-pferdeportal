# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.6 FULL LAYOUT FIX LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.6_FULL_LAYOUT_FIX.zip`

SHA-256:
`5c9fdfd0589e32705f2f0eacb596831a035751c455edfb7765919c0e72711ef5`

Größe:
1,349,468 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Layout-Fix

- Register-Body nutzt jetzt dieselbe Portalbreite wie Hobby Depot:
  `width:min(calc(100% - 72px),var(--hd-content,1440px))`.
- Breadcrumb nutzt dieselbe Breite.
- Profil-Hero: redundantes kleines Label `HOBBYREGISTER` entfernt.
- Hero-Inhalt leicht nach oben gezogen.
- Startseiten-Kicker `HOBBYS VON A BIS Z` bleibt bestehen.

## Artikelstatus

- 862/862 Profile erzeugen bereits acht Fließtextabschnitte.
- Final redaktionell ausformuliert sind bisher nur die Musterprofile Buchbinden und Slacklining.
- Die übrigen Profile verwenden weiterhin den automatischen Schema-F-Textgenerator auf Basis der aktuell physisch gebundenen 54 Basistraits.
- Die vollständige 57-Trait-Laufzeitprojektion ist noch nicht im Plugin gebunden.
- Daher gelten die übrigen 860 Texte noch nicht als final redaktionell abgeschlossen.

## QA

- PHP-Lint 4/4 PASS.
- Fresh-Unpack PASS.
- Portalbreite 1440-Fallback PASS.
- alter 1180px-Registerwrapper entfernt PASS.
- Profil-Hero ohne HOBBYREGISTER-Kicker PASS.
- Startseiten-Kicker erhalten PASS.
- Hero-Titel nach oben versetzt PASS.

## EXAKT EINE NEXT ACTION

**1.1.6 als vollständigen Ordner `hd-hobbyregister-core` ersetzen und live Bodybreite + Hero prüfen. Danach vollständige 57-Trait-Laufzeitprojektion binden und die 862 Detailtexte final produzieren/prüfen.**
